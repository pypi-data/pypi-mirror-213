"""This package implements Bayesian probabilistic models
for the analysis of Paired-Comparison data,
for example, evaluating the Sound Quality of different hearing aid processing variants.

A probabilistic model is adapted to the observed data for each participant,
assuming that the responses were determined by a perceptual choice model,
either the Thurstone-Case-V model (Thurstone, 1927)
or the BTL model (Bradley and Terry, 1952; Luce, 1959).

As a result, the model can present predictive probability distributions
of the perceived quality of each presented class of stimulus "object" for
- a random individual in the population from which participants were recruited,
- the mean quality parameters in that population,
- a random individual in the group of test participants,
- each individual in the group of test participants.

Mathematical model details and learning methods are presented in (Leijon et al., 2019).

NOTE: All individual model parameters are estimated using sampling.
Therefore, the numerical results may deviate slightly between runs,
even if exactly the same input data are used.

*** Main Script Template:

run_pc: Bayesian analysis of paired-comparison data,
    using either the Thurstone-case-V or the BTL model.

*** Other Useful Script Templates:

run_sim: Generate and analyze simulated paired-comparison data,
    to be used for planning a future experiment,
    and to illustrate the package functions,
    and to exemplify the data file format and result displays

run_plan: Calculate approximate power of a planned future experiment,
    indicating the required number of test participants
    to reach a desired statistical reliability of the test results.

*** Usage: Copy and rename a template script,
    and edit the script as needed for your experiment,
    with guidance from comments in the script.

    The organisation and available formats of input data files
    are described in the doc-comment of module pc_data.

*** Main Package Modules:

pc_data: classes and load/save functions for raw input data
pc_file: functions to read and write raw paired-comparison data
pc_model: classes and functions for Bayesian probabilistic model definition and learning
pc_display: classes and functions producing figures and tables from analysis results
pc_display_format: classes and functions for figure and table formatting
pc_lr_test: functions for Likelihood Ratio significance test
    (to be used with caution, because the result is approximate)

All modules are distributed as python source files.
Users can rather easily modify input and output modules if needed.
However, for the central mathematical module pc_model,
it is recommended to discuss any changes with the package author.

*** Main Classes:

pc_data.PairedCompFrame: defines layout of a paired-comparison experiment
pc_data.PairedCompDataSet: container for all input data to be analysed

pc_display.PairedCompDisplaySet: container for all user-readable analysis results

pc_model.PairedCompResultSet: container for posterior Bayesian models learned from
    all observed subject data in one PairedCompDataSet instance.

pc_model.Thurstone: choice model according to Thurstone Case V
pc_model.Bradley: Bradley-Terry-Luce (BTL) choice model

pc_model.PairedCompIndModel: central model for the multivariate distribution
    of all quality parameters of ONE participant for ONE perceptual attribute,
    represented by Hamiltonian sampling of the posterior distribution of model parameters
    in all Test Conditions of the experiment.

*** References:

A. Leijon, M. Dahlquist, and K. Smeds (2019).
Bayesian analysis of paired-comparison sound quality ratings.
*J Acoust Soc Amer, 146(5), 3174-3183. DOI: 10.1121/1.5131024.

K. Smeds, F. Wolters, J. Larsson, P. Herrlin, and M. Dahlquist (2018).
Ecological momentary assessments for evaluation of hearing-aid preference.
*J Acoust Soc Amer* 143(3):1742–1742.

M. Dahlquist and A. Leijon (2003).
Paired-comparison rating of sound quality using MAP parameter estimation for data analysis.
In *1st ISCA Tutorial and Research Workshop on Auditory Quality of Systems*,
Mont-Cenis, Germany.

L. L. Thurstone (1927). A law of comparative judgment.
*Psychological Review* 34(4), 273–286, doi: 10.1037/h0070288.

R. A. Bradley and M. E. Terry (1952).
Rank analysis of incomplete block designs. I. The method of paired comparisons.
*Biometrika* 39, 324–345, doi: 10.2307/2334029.


*** Version history:
** Version 2.1.1:
2023-06-14, new module pc_latent with numerically safer versions of
            Bradley, Thurstone, for distributions of latent variables.
            (copied from EmaCalc)

** Version 2.1:
2022-09-01, likelihood ratio test deprecated, as suggested by JASA paper reviewer.
2022-07-04, using Pandas for data input and result tables

** Version 2.0.1:
2022-03-09, minor fix pc_model, pc_data, pc_file_xlsx for clearer logging/error displays

** Version 2.0, 2021-09-24:
pc_display can show estimated individual results for each participant.
Changed interface to function pc_display.display(...)
    to allow users to select any combination of result variants.
pc_data.PairedCondDataSet saves data in xlsx format by default.
Changed some pc_display.FMT and pc_display_format.FMT parameters.

** New in version 1.0.0, 2019-04-08:

* Major new features:
Likelihood-Ratio test for significant differences in population mean.
pc_data.PairedCompDataSet.save() method writes json subject files.
New generalized module pc_simulation, with flexibility like real experiments.
New script run_plan, and module pc_planning, to predict performance and estimate needed number of subjects

* Backward-incompatible changes:
Changed property name in pc_data.PairedCompFrame: systems -> objects
Changed property name in pc_data.PairedCompFrame: n_systems -> n_objects
Changed property name in pc_data.PairedCompFrame: systems_alias -> object_alias
Changed property name in pc_data.PairedCompFrame: systems_disp -> object_disp
Changed property name in pc_data.PairedCompFrame: response_labels -> difference_grades
Changed some pc_display_format.FMT key names.

* Other Minor changes:
Checking for missing response data from any subject in any test condition.
Included marginal probabilities for quality<=0 and >0 in percentile tables.
Minor clarifications of logging output text.


** New in version 0.9.0, 2018-10-08:

Allow xlsx input, new basic file-item structure, common for all file formats.
Result displays show response-interval limits, if display parameter show_intervals=True.
Several minor fixes in display formatting.
Changed convention for display file names.


** Version 0.8.3:
2018-02-18, First functional version
2018-03-28, Modified internal structure of pc_model.PairedCompResultSet
2018-04-03, Use all available subject data for quality estimates, even if some data are missing,
    except that attribute correlations are calculated only within each subject,
    i.e., using only subjects with complete results for all attributes.
2018-04-27, first hierarchical analysis model tested
    Use PairedCompFrame.objects_alias labels for all displays.
2018-05-21, allow choice among three types of predictive distributions
2018-08-05, using prior gauss_gamma module for population distribution, tested pc_power
2018-08-14, simplified internal structure of PairedCompDataSet
2018-08-15, First public version 0.8.3
"""

__name__ = 'PairedCompCalc'
__version__ = '2.1.1'
__all__ = ['__version__', 'run_pc', 'run_plan', 'run_sim']
