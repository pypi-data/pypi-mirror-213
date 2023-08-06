"""Script to simulate paired-comparison experiments,
collecting the results in a pc_data.PairedCompDataSet object,
just as if the dataset had been gathered from data files from a real experiment.

A simulated experiment may include
one or more Groups of subjects, each randomly drawn from a specified Population,
tested for one or more perceptual Attributes,
in one or more Test Conditions.

Paired-comparison responses are simulated using either
(1): the Thurstone Case V model, pc_simulator.SubjectThurstone, OR
(2): the Bradley-Terry-Luce model, pc_simulator.SubjectBradley.


*** Usage:
Copy and edit this script and run it for any desired simulation.


*** Version history:
* Version 2.1:
2022-07-01, adapted to store data as pandas.DataFrame objects in pc_data.PairedCompDataSet

* Version 2.0:
2021-09-15, no change, tested with new pc_display version
2021-09-23, save simulated PairedCompDataSet in xlsx format by default

* Version 1.0:
2017-11-20, tested by comparison to MatLab analysis package
2018-07-30, tested with new simulator signature
2019-04-07, tested with new generalized pc_simulation version
"""
import numpy as np
from pathlib import Path
import logging

from PairedCompCalc.pc_simulation import PairedCompSimPopulation, PairedCompSimExperiment
from PairedCompCalc.pc_simulation import SubjectThurstone, SubjectBradley

from PairedCompCalc.pc_data import PairedCompFrame
from PairedCompCalc import pc_logging, __version__

import PairedCompCalc.pc_model as pcm
from PairedCompCalc.pc_display import PairedCompDisplaySet


# ------------------------------- Set up result logging:

work_path = Path.home() / 'Documents' / 'PairedComp_sim'  # or whatever...
data_path = work_path / 'data_sim'  # or whatever, for saved data files
result_path = work_path / 'result_sim'  # or whatever, for all analysis results

pc_logging.setup(result_path=work_path,
                 log_file='run_sim_log.txt')  # to save the log file
logging.info(f'*** Running PairedCompCalc version {__version__}')

# OR
# pc_logging.setup()  # to get only console output

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# ------------------------------- Define Population(s) and Objects to be simulated:

n_objects = 3
pop_objects = [f'HA{i}' for i in range(n_objects)]
# = object labels

pop0_test_factors = ['SNR', 'Stim']

# Define a population, with mean quality for each Attribute,
# and for all combinations of conditions in each Test Factor:
pop0_quality = {'SimQ': {'Low': {'speech': [0,  1., 0.],    # SNR= 'Low', Stim= 'speech'
                                 'music':  [0., -1., 0.]},  # SNR= 'Low', Stim= 'music'
                         'High': {'speech': [0., 0.,  1.],   # SNR= 'High', Stim= 'speech'
                                  'music':  [0., 0., -1.]},  # SNR= 'High', Stim= 'music'
                         'Quiet': {'speech': [0., 0., 2.],    # SNR= 'Quiet', Stim= 'speech'
                                   'music':  [0., 0., -2.]}  # SNR= 'Quiet', Stim= 'music'
                         }
                # , 'OtherAttr': {.... } may be added here, with the same Test-Condition sub-structure
                }
# e.g., mean of attribute 'SimQ' is -2 for object 'HA2' in Test Condition (SNR= 'Quiet', Stim= 'music')
# NOTE: The quality for first object arbitrarily = 0.,
# because only the difference between object quality values determines responses.
# Results will be the same, if a constant value is added to all quality means.

pc_pop_0 = PairedCompSimPopulation(objects=pop_objects,
                                   test_factors=pop0_test_factors,
                                   quality_mean=pop0_quality,
                                   quality_std=0.3,  # inter-individual standard deviation of attribute
                                   log_response_width_std=0.,  # inter-individual resp.-threshold variations
                                   lapse_prob_range=(0., 0.2),  # uniform distr. of lapse probability
                                   subject_class=SubjectThurstone,
                                   id='pop0')
# See pc_simulation.PairedCompSimPopulation for all property definitions

logger.info(f'pc_pop_0={pc_pop_0}')

# Optionally, define other populations here,
# pc_pop_1 = PairedCompSimPopulation(... etc)
# with SAME Objects, Attributes, and Test Conditions, but different mean quality values, and id

# ------------------------------- Define Experimental Framework:

pcf = PairedCompFrame(attributes=['SimQ'],
                      objects=pop_objects,
                      forced_choice=False,
                      difference_grades=['Equal', 'Slightly Better', 'Better', 'Much Better'],
                      test_factors={'Stim': ['speech', 'music'], 'SNR': ['Quiet', 'High']}
                      )
# NOTE: pcf.attributes may be a subset of those defined in pc_pop_0.quality_mean.
# pcf.objects may be subset of pc_pop_0.objects, and/or listed in arbitrary order.
# pcf.test_factors may be a subset of pc_pop_0.test_factors, and in arbitrary order.
# Categories within each of pcf.test_factors may be a subset, and in arbitrary order.

# ------------------------------- Generate One Group of Subjects from each Population:

pc_group_0 = pc_pop_0.gen_subject_group(pcf, n_subjects=10)
# = a dict with elements (attr, subject_list)

# If another Population was defined above:
# pc_group_1 = pc_pop_1.gen_subject_group(pcf, n_subjects=15)

logger.info('One Simulated subject group:')
for (a, a_subjects) in pc_group_0.items():
    logger.info(f'Attribute {a}:')
    for (s_id, s) in a_subjects.items():
        for (t, tc) in enumerate(pcf.test_conditions()):
            logger.info(f' {s_id}.quality[{tc}] =\t'
                        + np.array2string(s.quality[t], precision=3,
                                          sign=' ',
                                          suppress_small=True))
        logger.info(f' {s_id}.response_thresholds =\t'
                    + np.array2string(s.response_thresholds, precision=2,
                                      sign=' ',
                                      suppress_small=True))
        logger.info(f' {s_id}.lapse_prob = {s.lapse_prob:.3f}')


# ------------------------------- Define a complete Experimental Procedure

pc_exp = PairedCompSimExperiment(pcf,
                                 n_replications=3,  # for each pair, each test condition, each attribute
                                 pair_different=True  # exclude pairs like (A, A)
                                 )
# NOTE: n_replications for pair (A, B), plus same number for pair (B, A)
logger.info(f'pc_exp= {pc_exp}')

# ------------------------------- Simulate Paired-Comparison Tests with All Groups:

# Gather all groups in one dict, with distinctive group names
test_groups = {'Group0': pc_group_0}
# OR
# test_groups = {'Group0': pc_group_0, 'Group1: pc_group_1, ...}

ds = pc_exp.gen_dataset(groups=test_groups)
# = a complete PairedCompDataSet instance with all simulated paired comparisons

# Optionally, save all data in a set of data files, one for each subject
file_format = 'csv'
ds.save(data_path, allow_over_write=True, fmt=file_format,
        # subject='Respondent',     # default, set new column names, if desired
        # attribute='Attribute',    # default, set new column names, if desired
        pair=('Pair_1', 'Pair_2'),  # always saved
        difference='Diff',  # optional
        choice='Choice',    # always saved
        grade='Grade',      # always saved
        )
logging.info(ds.__class__.__name__ + ' saved in ' + str(data_path) + f' as {file_format} files')

# Optionally, save as 'xlsx' files, too:
# file_format = 'xlsx'
# ds.save(data_path, allow_over_write=True, fmt=file_format)
# logging.info(ds.__class__.__name__ + ' saved in ' + str(data_path) + f' as {file_format} files')

# ------------------------------- Learn Analysis Model from simulated data set:

model_class = pcm.Thurstone  # or = pcm.Bradley

logging.info(f'Learning Analysis Results with {model_class}')
pc_result = pcm.PairedCompResultSet.learn(ds, rv_class=model_class)

# ------------------------------- generate all result displays:

pc_display_set = PairedCompDisplaySet.show(pc_result)
# = default display combination, showing estimated results for
# (1) random individual in the population from which participants were recruited,
# (2) the population mean,
# (3) overview of the group of participants
# *** See pc_display.FMT and pc_display_format.FMT for all available format parameters
#   and their default settings.

# ------------------------------- save all result displays in directory tree
pc_display_set.save(result_path)

logging.info(f'All results saved in {result_path} and sub-dirs.')
logging.shutdown()
