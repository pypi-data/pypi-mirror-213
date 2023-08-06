import os
import csv
import pathlib
import shutil
import typing as t

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from pycomex.util import Skippable
from pycomex.experiment import SubExperiment

from visual_graph_datasets.config import Config
from visual_graph_datasets.web import get_file_share

# == SOURCE PARAMETERS ==
# This section contains the parameters which define the source CSV files which are to be used as the basis
# for the final dataset. At the bare minimum, these CSV files have to contain one column with the SMILES
# representation of the molecule and one column with the corresponding target value to be predicted.
# It is also possible to use multiple target value from a single CSV file.
# The CSV files can either be supplied as local files or them can first be downloaded from a remote VGD
# file share provider.

# The keys of this dictionary should be unique keys which identify the theme of each CSV file to be used in
# the subsequent merge. The values should be paths to the CSV files. If local files are to be used,
# the absolute(!) paths have to be supplied. Alternatively, if the paths cannot be found on the local system,
# they will be interpreted as path relative to the remote file share provider and it is attempted to
# download those files from there.
CSV_FILE_NAME_MAP: t.Dict[str, str] = {
    'water': 'source/water_solubility.csv',
    'benzene': 'source/benzene_solubility.csv',
    'acetone': 'source/acetone_solubility.csv',
    'ethanol': 'source/ethanol_solubility.csv',
}
# The keys should be the same keys as defined above for each of the CSV files and the values should be the
# string names of the columns of each file, which contain the SMILES string.
SMILES_COLUMN_NAME_MAP: t.Dict[str, str] = {
    'water': 'Smiles',
    'benzene': 'SMILES',
    'acetone': 'SMILES',
    'ethanol': 'SMILES',
}
# THe keys should be the same as defined above for each of the CSV files and the values should be lists
# containing all the string column names which contain the target values of the corresponding dataset.
TARGET_COLUMN_NAME_MAP: t.Dict[str, t.List[str]] = {
    'water': ['LogS'],
    'benzene': ['LogS'],
    'acetone': ['LogS'],
    'ethanol': ['LogS'],
}
SOURCE_KEYS = list(CSV_FILE_NAME_MAP.keys())  # do not modify

# This value will determine what the value will be in the target value vector for target values which are
# not known.
UNKNOWN_AS: t.Optional[float] = None

DATASET_NAME = 'organic_solvents'

# == EXPERIMENT PARAMETERS ==
PATH = pathlib.Path(__file__).parent.absolute()
EXPERIMENT_PATH = os.path.join(PATH, 'generate_molecule_dataset_from_csv.py')
BASE_PATH = PATH
NAMESPACE = 'results/generate_molecule_dataset_from_csv_multitask'
with Skippable(), (se := SubExperiment(EXPERIMENT_PATH, BASE_PATH, NAMESPACE, globals())):

    @se.hook('load_data')
    def load_data(e, config: Config):
        num_sources = len(e.p['CSV_FILE_NAME_MAP'])

        # Here we create a helper data structure. This will be a nested dict structure where the
        # first-level key is the string identifier of the source and the second-level key is the string
        # identifier of the target column.
        # The corresponding values will be the integer
        # index of where that specific target value will later be placed in the overall vector of all
        # target values
        target_name_index_map = {}
        index = 0
        for key, names in e.p['TARGET_COLUMN_NAME_MAP'].items():
            target_name_index_map[key] = {}
            for name in names:
                target_name_index_map[key][name] = index
                index += 1

        num_targets = index
        e['target_name_index_map'] = target_name_index_map
        e['num_targets'] = num_targets

        e.info(f'loading source data for multitask molecule dataset from {num_sources} source files...')

        # ~ collecting source files
        # First we are going to collect all the source files from the various places where they are defined.
        # This may simple include copying on the local file, but it also may mean downloading the file
        # from the remote file share into the local archive folder.
        e.info('collecting source files...')
        file_share = get_file_share(config, e.parameters['FILE_SHARE_PROVIDER'])
        file_path_map: t.Dict[str, str] = {}
        for key, file_name in e.parameters['CSV_FILE_NAME_MAP'].items():
            if os.path.exists(file_name):
                e.info(f' * copying {file_name}...')
                local_file_path = os.path.join(e.path, os.path.basename(file_name))
                shutil.copy(file_name, e.path)
            else:
                e.info(f' * downloading {file_name}...')
                local_file_path = file_share.download_file(file_name, e.path)

            file_path_map[key] = local_file_path

        # ~ reading and merging source files

        # We realize this as a dictionary so that we can easily check for SMILES duplicates!
        smiles_data_map: t.Dict[str, dict] = {}
        for i, (key, file_path) in enumerate(file_path_map.items()):

            with open(file_path, mode='r') as file:
                dict_reader = csv.DictReader(file)
                for row in dict_reader:
                    smiles_key = e.p['SMILES_COLUMN_NAME_MAP'][key]
                    smiles = row[smiles_key]

                    if smiles not in smiles_data_map:
                        target_vector = [e.p['UNKNOWN_AS'] for _ in range(e['num_targets'])]

                        d = {
                            'smiles': smiles,
                            'target': target_vector,
                            'data': row
                        }

                        smiles_data_map[smiles] = d

                    # "target_name_index_map" is a dictionary, whose keys are tuples of file name and
                    # target name and the corresponding values are the int indices in the target vector
                    # associated with that target value.
                    for target_key in e.p['TARGET_COLUMN_NAME_MAP'][key]:
                        index = target_name_index_map[key][target_key]
                        value = row[target_key]
                        target_vector[index] = float(value)

        return list(smiles_data_map.values())


    @se.hook('dataset_info')
    def dataset_info(e, index_data_map: dict):
        pdf_path = os.path.join(e.path, 'dataset_info.pdf')
        with PdfPages(pdf_path) as pdf:
            e.info(f'target value distribution...')

            # This helper data structure was previously created in "load_data" implementation
            target_name_index_map = e['target_name_index_map']
            n_cols = e['num_targets']
            n_rows = 1
            fig, rows = plt.subplots(ncols=n_cols, nrows=n_rows, figsize=(10 * n_cols, 10), squeeze=False)
            fig.suptitle('Target Value Distributions')
            for source_name, target_dict in target_name_index_map.items():
                for target_name, target_index in target_dict.items():
                    title = f'{target_index}: {source_name} - {target_name}'
                    e.info(title)

                    ax = rows[0][target_index]
                    ax.set_title(title)
                    targets = [value for i, d in index_data_map.items()
                               if (value := d['metadata']['target'][target_index]) != e.p['UNKNOWN_AS']]

                    e.info(f' * min: {np.min(targets):.2f}'
                           f' - mean: {np.mean(targets)}'
                           f' - max: {np.max(targets):.2f}')
                    n, bins, edges = ax.hist(
                        targets,
                        bins=e.p['NUM_BINS'],
                        color=e.p['PLOT_COLOR'],
                    )
                    ax.set_xticks(bins)
                    ax.set_xticklabels([round(v, 2) for v in bins])
                    e.info(' * done')

            pdf.savefig(fig)


