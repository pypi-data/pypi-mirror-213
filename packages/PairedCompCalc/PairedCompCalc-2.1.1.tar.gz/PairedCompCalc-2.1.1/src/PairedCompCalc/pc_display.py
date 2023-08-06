"""This module defines classes and functions to display analysis results
given a PairedCompResultSet instance,
learned from a set of data from a paired-comparison experiment.

Results are shown as figures and tables stored as pandas.DataFrame objects.
Figures can be saved in any file format that matplotlib can write.
Tables can be saved in any file format that pandas can write.
Thus, both figures and tables can be easily imported into a LaTeX or word-processing document.
Tables saved in .csv or .xlsx format can be imported to other data-processing programs.

*** Main Class

PairedCompDisplaySet = a structured container for all display results

Each display element can be accessed and modified by the user, before saving.

The display set can include data for three types of predictive distributions:
*: a random individual in the Population from which a group of test subjects were recruited,
    (most relevant for an experiment aiming to determine the success of a new product,
    among individual potential customers in a population)
*: the mean (=median) in the Population from which a group of test subjects were recruited
    (with interpretation most similar to a conventional significance test)
*: a random individual in a Group of test subjects, for whom paired-comp data are available

In addition, the display set can also include detailed individual results for all test subjects.

*** Usage Example:
    pc_ds = PairedCompDisplaySet.show(pc_result)
        gives a default display without detailed individual results

    pc_ds = PairedCompDisplaySet.show(pc_result,
                                    population_individual=True,
                                    population_mean=False,  # excluded
                                    subject_group=True,
                                    subject_individual=True  # including results for each participant
                                    ...  # optional other format specifications
                    )
    pc_ds.save(result_path)  # save all results as files in a directory tree.

    The display elements are accessible as, e.g.,
    pc_ds.groups['NormalHearing']['population_mean']['Intelligibility'].range.percentile_plot.ax
        = the Axes object where percentiles are plotted for this group, pooled across all test conditions
    pc_ds.groups['NormalHearing'].attr_corr is a table of credible correlations between attributes,
        in the results for the selected group, if any are credible

Figures and tables are automatically assigned descriptive names,
and stored in subdirectories with names constructed from
string labels of Groups and Attributes and test conditions,
as defined in the PairedCompFrame object of the input PairedCompResultSet instance.

If there is more than one Group,
    one subdirectory is created for each group, and one extra for all groups pooled,
    and one sub-sub-directory for each requested population / subject predictive result,
    and one sub-sub-sub-directory for each attribute, with results within the group.
    If there is more than one attribute,
    the group sub-directory may also include tables with correlations between attributes.

Thus, after saving, the display files are stored in a directory structure as, e.g.,
result_path / group / 'population_individual' / attribute / ....
result_path / group / 'subject_group' / attribute / group_total and individual lists and plots
result_path / group / 'subject_group' / attribute / 'subject_individual' / individual tables and plots
result_path / 'group_effects' / 'population_mean' / attribute / ---  (if more than one group)

*** Version History:
* Version 2.1:
2022-09-07, main function display removed; use explicit PairedCompDisplaySet.show()
2022-09-01, likelihood_ratio_test removed

* Version 2.0:
2021-08-27, changed display user interface, simplified display structure
2021-08-27, modified class AttributeDisplaySet
2021-08-27, new class AttributeDisplay, for predictive population result
2021-09-01, new class SubjectDisplay, for participant group and individuals
2021-09-04, allow 1, 2, 3, or more percentile values
2021-09-08, tabulate individual subject results
2021-09-12, cleanup doc text; FMT['show_intervals'] moved to pc_display_format

* Version 1.0:
2018-01-08, first functional version
2018-04-02, separate analyses of range displays and attribute-correlation displays
            with range displays allowing missing subjects for some attributes, but
            correlations calculated only within identical subjects across attributes.
            Renamed some classes to reflect changed structure.
2018-04-12, use objects_alias labels in all displays
2018-04-24, display estimated group-mean credible intervals
2018-05-21, PairedCompDisplaySet.display called with selected predictive model(s) as input
2018-10-02, unified handling of formatting parameters, in FMT, set_format_param
2018-10-08, display response-interval limits in percentile plots
2018-11-24, changed 'system' label to 'object' in result displays
2018-12-06, include likelihood-ratio test results in PairedCompDisplaySet
2019-03-27, include marginal credibility values in percentile tables
2020-05-15, minor bug fix for diff table generation in GroupEffectSet.display
"""
# *** allow user to select displays (attr, (test_factor_1, ...)), plot by several test factors ? ***
# *** like EmaCalc ? ***
# *** local superclass for pretty-printed repr() ?

import numpy as np
from pathlib import Path
import logging
from itertools import product
import string

from . import pc_display_format as fmt
# from .pc_lr_test import likelihood_ratio_test

from samppy.credibility import cred_diff, cred_group_diff, cred_corr

logger = logging.getLogger(__name__)


# ---------------------------- Default display parameters
FMT = {'percentiles': [5., 50., 95.],  # allowing 1, 2, 3, or more percentiles
       'credibility_limit': 0.6,  # min probability of jointly credible differences
       'group': 'Group',  # label for table heads and plots
       'subject': 'Subject',  # label for table heads
       'object': 'Object',  # label for table heads and figures
       'credibility': 'Credibility',  # heading in tables
       'probability': 'Probability',  # heading in tables
       'population_individual': True,  # show result for random individual in population
       'population_mean': True,  # show result for population mean
       'subject_group': True,  # show overview for all participants in each group
       'subject_individual': False,  # show results separately for each individual participant
       }
# = dict with default parameters that may be changed by user
# Other format parameters are handled in module pc_display_format

DEFAULT_FIGURE_FORMAT = 'pdf'
DEFAULT_TABLE_FORMAT = 'txt'


def set_format_param(**kwargs):
    """Set / modify format parameters for this module, and module pc_display_format
    Called before any displays are generated.
    :param kwargs: dict with any formatting variables
    :return: None
    """
    other_fmt = dict()
    for (k, v) in kwargs.items():
        k = k.lower()
        if k in FMT:
            FMT[k] = v
        else:
            other_fmt[k] = v
    FMT['percentiles'].sort()  # ensure increasing values
    fmt.set_format_param(**other_fmt)  # all remaining user-defined parameters


# -------------------------------- Main Module Function Interface
# def display(pc_result, **kwargs):  # *** not needed ? ***
#     """Main function to display default set of paired-comparison results.
#     :param: pc_result: a single PairedCompResultSet object
#     :param: kwargs: (optional) any user-defined display format parameters
#     :return: single QualityDisplaySet instance with display results
#     """
#     return PairedCompDisplaySet.show(pc_result, **kwargs)


# ---------------------------------------------------------- Main Display Class:

class PairedCompDisplaySet:
    """Root container for all displays
    of selected predictive quality and attribute-correlation results
    from one pc_model.PairedCompResultSet object.
    All display elements can be saved as files within a selected directory three.
    The complete instance can also be serialized and dumped to a single pickle file,
    then re-loaded, edited, and saved, if user needs to modify some display object.
    """
    def __init__(self, groups, group_effects=None):  # , lr_test=None):
        """
        :param groups: dict with (group: GroupDisplaySet) elements
            sub-divided among Attributes
        :param group_effects: (optional) single GroupEffectSet instance,
            showing jointly credible differences between groups,
            if there is more than one group
        """
        self.groups = groups
        self.group_effects = group_effects
        # self.lr_test = lr_test

    def __repr__(self):
        return (self.__class__.__name__ + '(' +
                '\n\t'.join(f'{k}= {repr(v)},'
                            for (k, v) in self.__dict__) +
                '\n\t)')

    def save(self, dir_top, **kwargs):
        """Save all displays in a directory tree
        :param dir_top: Path or string with top directory for all displays
        :return: None
        """
        dir_top = Path(dir_top)  # just in case
        for (g, g_display) in self.groups.items():
            g = _dir_name(g)
            if len(g) == 0 or all(s in string.whitespace for s in g):
                g_display.save(dir_top, **kwargs)
            else:
                g_display.save(dir_top / g, **kwargs)
        if self.group_effects is not None:
            self.group_effects.save(dir_top / 'group_effects', **kwargs)
        # if self.lr_test is not None:
        #     self.lr_test.save(dir_top, **kwargs)

    @classmethod
    def show(cls, pcr, **kwargs):
        """Create displays for all results from a paired-comparison experiment,
        and store all display elements in a single structured object.
        :param pcr: single pc_model.PairedCompResultSet instance, with
            pcr.models[group][a_label] = pc_model.PairedCompGroupModel instance
        :param: kwargs: (optional) dict with any display formatting parameters
        :return: a single new cls instance
        """
        # get default scale_unit from pcr, if not in kwargs
        if 'scale_unit' not in kwargs:
            kwargs['scale_unit'] = pcr.rv_class.unit_label
        set_format_param(**kwargs)
        # display separate results for each group
        groups = {g: GroupDisplaySet.display(pcm_g)
                  for (g, pcm_g) in pcr.models.items()}

        if len(groups) > 1:  # prepare for group differences
            group_effects = GroupEffectSet.display(pcr)
        else:
            group_effects = None
        logger.info(fig_comments(FMT['percentiles']))
        logger.info(table_comments(pcr.pcf))
        return cls(groups, group_effects)

    # def likelihood_ratio_test(self, pcr_null, pcr):
    #     """Create table with all likelihood-ratio test results
    #     :param pcr_null: learned PairedCompResultSet instance with NULL model
    #     :param pcr: same PairedCompResultSet instance as for all other result displays
    #     Result: self.lr_test = TableRef instance with significance results
    #     """
    #     lr_result = likelihood_ratio_test(pcr_null, pcr)
    #     self.lr_test = fmt.tab_lr_test(lr_result)


# ---------------------------------------------------------- Secondary Display Classes:

class GroupDisplaySet:
    """Container for all quality displays related to ONE experimental group:
    Predictive results for the population from which the subjects were recruited,
    and descriptive data for the subject group,
    and descriptive data for each individual subject.
    as requested by user.
    """
    def __init__(self,
                 population_mean=None,
                 population_individual=None,
                 subjects=None,
                 attr_corr=None):
        """
        :param population_mean: dict with (a_label: AttributeDisplay object), for population mean,
        :param population_individual: dict with (a_label: AttributeDisplay object), for random individual,
        :param subjects: dict with (a_label: SubjectDisplay object) for participants in one group
            with response data for the given attribute.
            (Not necessarily same set of subjects for separate attributes)
        :param attr_corr: TableRef instance with correlations between attributes in this group
        """
        self.population_mean = population_mean
        self.population_individual = population_individual
        self.subjects = subjects
        self.attr_corr = attr_corr

    def __repr__(self):
        return (self.__class__.__name__ + '(' +
                '\n\t'.join(f'{k}= {repr(v)},'
                            for (k, v) in self.__dict__) +
                '\n\t)')

    def save(self, path, **kwargs):
        """Save all stored display objects in their corresponding sub-trees
        """
        if self.population_mean is not None:
            for (a, a_disp) in self.population_mean.items():
                a_disp.save(path / 'population_mean' / a, **kwargs)
        if self.population_individual is not None:
            for (a, a_disp) in self.population_individual.items():
                a_disp.save(path / 'population_individual' / a, **kwargs)
        if self.subjects is not None:
            for (a, a_disp) in self.subjects.items():
                a_disp.save(path / 'subject_group' / a, **kwargs)
        if self.attr_corr is not None:
            self.attr_corr.save(path, **kwargs)

    @classmethod
    def display(cls, pcm_g):
        """Generate all displays for ONE group
        :param pcm_g: dict with elements (a_label: pc_result.PairedCompGroupModel object)
        :return: cls instance with all displays for this group
        """
        pop_ind = None
        pop_mean = None
        subjects = None
        if FMT['population_individual']:  # ****** -> random_individual ?
            pop_ind = {a: AttributeDisplay.from_predictive(a,
                                                           pcm_ga.pred_population_ind())
                       for (a, pcm_ga) in pcm_g.items()}
        if FMT['population_mean']:
            pop_mean = {a: AttributeDisplay.from_predictive(a,
                                                            pcm_ga.pred_population_mean())
                        for (a, pcm_ga) in pcm_g.items()}
        if FMT['subject_group']:
            subjects = {a: SubjectDisplay.display(a, a_model)
                        for (a, a_model) in pcm_g.items()}
        attr_corr = None
        if len(pcm_g) > 1:  # more than one Attribute
            attr_corr = display_attribute_correlation(pcm_g)
            # might still be None if none found
        return cls(population_mean=pop_mean,
                   population_individual=pop_ind,
                   subjects=subjects,
                   attr_corr=attr_corr)


class AttributeDisplay:
    """Container for all displays for ONE attribute
    in ONE population or ONE subject group representing a population
    """
    def __init__(self,
                 range,
                 diff=None,
                 test_cond_effects=None):
        """
        :param range: RangeDisplay object with results aggregated across test_factors
        :param diff: (optional) TableRef with credible differences between objects
        :param test_cond_effects: (optional) TestCondEffectSet instance
            showing differences between objects and test_conditions
        """
        self.range = range
        self.diff = diff
        self.test_cond_effects = test_cond_effects

    def __repr__(self):
        return (self.__class__.__name__ + '(' +
                '\n\t'.join(f'{k}= {repr(v)},'
                            for (k, v) in self.__dict__) +
                '\n\t)')

    def save(self, path, **kwargs):
        """Save all stored display objects in specified (sub-)tree
        """
        self.range.save(path, **kwargs)
        if self.diff is not None:
            self.diff.save(path, **kwargs)
        if self.test_cond_effects is not None:
            self.test_cond_effects.save(path / 'test-cond-effects', **kwargs)

    @classmethod
    def from_predictive(cls, a_label, a_model):
        """Create all displays for a single attribute
        :param a_label: string identifying the attribute
        :param a_model: pc_result.PopulationPredictiveModel instance
        :return: single cls instance with all displays
        """
        pcf = a_model.pcf
        q_samples = a_model.quality_samples
        thr = a_model.cat_limit_samples
        cat_limits = _median_cat_limits(thr,
                                        pcf.forced_choice)
        # use cat_limits also for TestCondEffects ???
        if pcf.n_test_conditions > 1:
            tc_effects = TestCondEffectSet.display(a_label,
                                                   pcf, q_samples, thr)
        else:
            tc_effects = None
        q_samples = a_model.quality_samples.reshape((-1, pcf.n_objects))
        # = 2D array, now merged as if only a single test_condition_tuple

        range = RangeDisplay.create(a_label, q_samples,
                                    thr=cat_limits,
                                    object_labels=pcf.objects_disp)

        d = cred_diff(q_samples, diff_axis=1, sample_axis=0,
                      p_lim=FMT['credibility_limit'])
        diff = fmt.tab_credible_diff(d,
                                     y_label=a_label,
                                     file_label=a_label,
                                     diff_head=(FMT['object'],),
                                     diff_labels=[(obj,)
                                                  for obj in pcf.objects_disp],
                                     cred_head=FMT['probability'])
        return cls(range, diff, tc_effects)

    @classmethod
    def from_subject_group(cls, a_label, a_model):
        """Create all displays for a single attribute
        :param a_label: string identifying the attribute
        :param a_model: pc_result.PairedCompGroupModel instance, with
            a_model.subjects[s] = pc_result.PairedCompIndModel instance
        :return: single cls instance with all displays
        """
        # *** avoid duplicating code: use common sub-function with sampled input ? ***
        pcf = a_model.pcf
        q_samples = np.concatenate([s_model.quality_samples
                                    for s_model in a_model.subjects.values()],
                                   axis=0)
        # q_samples[sn, t, :] = ns-th sample vector across ALL subjects in t-th test condition
        thr = np.concatenate([s_model.cat_limit_samples
                              for s_model in a_model.subjects.values()],
                             axis=0)
        # thr[sn, :] = sn-th sample vector across ALL subjects
        cat_limits = _median_cat_limits(thr, pcf.forced_choice)
        q_map = np.concatenate([s_model.quality_map
                                for s_model in a_model.subjects.values()],
                               axis=0)
        # q_map[s, t, :] = MAP quality vector for s-th subject in t-th test condition

        # do test conditions first, with samples separated by tc
        if pcf.n_test_conditions > 1:
            tc_effects = TestCondEffectSet.display(a_label,
                                                   pcf, q_samples, thr, q_map)
        else:
            tc_effects = None

        q_samples = q_samples.reshape((-1, pcf.n_objects))
        q_map = q_map.reshape((-1, pcf.n_objects))
        # for boxplot across all test conditions and all subjects
        range = RangeDisplay.create(a_label, q_samples,
                                    thr=cat_limits,
                                    object_labels=pcf.objects_disp,
                                    q_map=q_map)

        d = cred_diff(q_samples, diff_axis=1, sample_axis=0,
                      p_lim=FMT['credibility_limit'])
        diff = fmt.tab_credible_diff(d,
                                     y_label=a_label,
                                     file_label=a_label,
                                     diff_head=(FMT['object'],),
                                     diff_labels=[(obj,)
                                                  for obj in pcf.objects_disp],
                                     cred_head=FMT['probability'])
        return cls(range, diff, tc_effects)


class SubjectDisplay:
    """Container for all displays related to ONE perceptual attribute
    for ALL subjects in ONE experimental group
    """
    def __init__(self, group=None, tab_ind=None, ind=None):
        """
        :param group: AttributeDisplay instance with overall results for the group
        :param tab_ind: TableRef with percentiles by test conditions for all individual subjects
        :param ind: dict with elements (subject_id: AttributeDisplay object)
        """
        self.group = group
        self.tab_ind = tab_ind
        self.ind = ind

    def __repr__(self):
        return (self.__class__.__name__ + '(' +
                '\n\t'.join(f'{k}= {repr(v)},'
                            for (k, v) in self.__dict__) +
                '\n\t)')

    def save(self, path, **kwargs):
        """
        :param path: path for all displays
        :return: None
        """
        if self.group is not None:
            self.group.save(path, **kwargs)  # / 'subject_group')
        if self.tab_ind is not None:
            self.tab_ind.save(path, **kwargs)  # / 'subject_group')
        if self.ind is not None:
            for (s_id, s_disp) in self.ind.items():
                s_disp.save(path / 'subject_individual' / s_id, **kwargs)

    @classmethod
    def display(cls, a_label, a_model):
        """Create all displays for ONE attribute of ONE subject group
        :param a_label: string with attribute label
        :param a_model: pc_result.PairedCompGroupModel instance, with
            pcm_ga[s] = pc_result.PairedCompIndModel instance
        :return: a cls instance
        """
        group = None
        tab_ind = None
        ind = None
        if FMT['subject_group']:
            group = AttributeDisplay.from_subject_group(a_label, a_model)
            tab_ind = _make_subject_table(a_label, a_model)
        if FMT['subject_individual']:
            ind = {s: AttributeDisplay.from_predictive(a_label, pcm_gas)
                   for (s, pcm_gas) in a_model.subjects.items()}
        return cls(group, tab_ind, ind)


# ---------------------------------------- Third-level displays
class TestCondEffectSet:
    """Container for all displays of differences between objects and test_cond_tuples
    for ONE Attribute in ONE group.
    """
    def __init__(self, test_factors,
                 range_by_test_cond=None,
                 diff_within=None,
                 diff_between=None):
        """
        :param test_factors: dict with (test-factor: RangeDisplay) elements
        :param range_by_test_cond: single TableRef object with all percentiles,
            sub-specified for each test_cond_tuple
        :param diff_within: single TableRef object with credible differences between objects,
            within a test_condition_tuple
        :param diff_between: single TableRef object with credible differences between test_conditions,
            within each object
        """
        self.test_factors = test_factors
        self.range_by_test_cond = range_by_test_cond
        self.diff_within = diff_within
        self.diff_between = diff_between

    def __repr__(self):
        return (self.__class__.__name__ + '(' +
                '\n\t'.join(f'{k}= {repr(v)},'
                            for (k, v) in self.__dict__) +
                '\n\t)')

    def save(self, path,
             figure_format=None,
             **kwargs):
        for (tf, tf_range) in self.test_factors.items():
            tf_range.save(path, figure_format=figure_format, **kwargs)
            # name starts with test-factor label
        if self.range_by_test_cond is not None:
            self.range_by_test_cond.save(path, **kwargs)
        if self.diff_within is not None:
            self.diff_within.save(path, **kwargs)
        if self.diff_between is not None:
            self.diff_between.save(path, **kwargs)

    @classmethod
    def display(cls, a, pcf, q, thr, q_map=None):
        """Generate quality results for given attribute,
        sub-divided across test conditions within each Test Factor,
        separated for each test-condition combination in other Test Factors
        :param a: string with current attribute label
        :param pcf: pc_data.PairedCompFrame instance
        :param q: 3D array with quality samples, with
            q[n, t, :] = n-th sample quality vector in t-th test condition
        :param thr: 3D array with UPPER category threshold samples, with
            thr[n, t, :] = n-th sample vector in t-th test condition,
        :param q_map: (optional) 3D array with quality MAP estimates, with
            q_map[s, t, :] = quality MAP vector for s-th subject in t-th test condition
            boxplots generated if q_map is specified
        :return: single cls instance
        """
        q_samples = q.transpose((1, 0, 2))
        # = stored as q[test_cond, sample, object]
        cat_limits = _median_cat_limits(thr, pcf.forced_choice)
        # = 1D vector with category thresholds, same in all test conditions

        # --------------------- percentile table by test_condition_tuple
        # Table with all test-condition combinations separate, without plot
        # only if more than one test-factor dimension
        # because main effect of single factor is handled later, anyway
        if len(pcf.test_factors) > 1:
            perc_tc = np.percentile(q_samples, FMT['percentiles'], axis=1)
            # perc_tc[p, t, i] = p-th percentile of i-th object in t-th test condition
            cdf_tc = _sample_cdf_0(q_samples, axis=1)
            # cdf_tc[t, i] = cdf for i-th object at t-th test condition
            perc_tc = perc_tc.reshape((perc_tc.shape[0],
                                       *pcf.n_test_factor_categories,
                                       perc_tc.shape[-1]))
            # perc_tc[p, t0,..., tT, i] = p-th percentile for i-th object in (t0,.., tT)-th test cond.
            perc_tc = np.moveaxis(perc_tc, -1, 1)
            # perc_tc[p, i, t0,..., tT] = p-th percentile for i-th object in (t0,.., tT)-th test cond
            # with indexing to match case_labels in tab_percentiles:
            perc_by_test_cond = fmt.tab_percentiles(perc_tc,  # skip first ref object ?
                                                    # cdf=cdf_tc,
                                                    perc=FMT['percentiles'],
                                                    file_label=a,
                                                    case_labels=[(FMT['object'], pcf.objects_disp),
                                                                 *pcf.test_factors.items(),
                                                                 ]
                                                    )
        else:
            perc_by_test_cond = None
        # --------------------------------------------------------
        n_tc = pcf.n_test_factor_categories
        q_samples = q_samples.reshape((*n_tc, -1, pcf.n_objects))
        # stored as q_samples_0[tc_0, ..., tc_i,..., sample, object], i.e.,
        # one array dimension for each test factor = each key in pcf.test_factors
        if q_map is not None:
            q_map = q_map.transpose((1, 0, 2))
            q_map = q_map.reshape((*n_tc, -1, pcf.n_objects))
            # stored as q_map[tc_0, ..., tc_i,..., subject, object]
        test_factors = dict()
        for (tf, tf_conditions) in pcf.test_factors.items():
            # plot quantiles by tf, main effect for this tf dimension
            assert len(tf_conditions) == q_samples.shape[0], '*** error in axis permutation'  # *** TEST
            q_tf_0 = q_samples.reshape((len(tf_conditions), -1, pcf.n_objects))
            # q_tf_0[tc, sample, object] with samples merged for all OTHER test test_factors

            q_samples = np.moveaxis(q_samples, 0, len(n_tc) - 1)
            # moved processed test-condition axis to last among test_factors, for next tf

            if q_map is None:
                q_map_tf = None
            else:
                # include q_map boxplots:
                assert len(tf_conditions) == q_map.shape[0], '*** error in axis permutation'
                q_map_tf = q_map.reshape((len(tf_conditions), -1, pcf.n_objects))
                # stored as q_map_tf[test_cond, subject-repeated, object]
                # i.e., q_map for SAME subject may appears several times,
                # one for each of the merged test-factor conditions
                q_map = np.moveaxis(q_map, 0, len(n_tc) - 1)
                q_map_tf = q_map_tf.transpose((1, 0, 2))
                # stored as q_map_tf[sample, test_cond, object] as needed for RangeDisplay

            test_factors[tf] = RangeDisplay.create(a, q_tf_0.transpose((1, 0, 2)),
                                                   q_map=q_map_tf,
                                                   thr=cat_limits,
                                                   object_labels=pcf.objects_disp,
                                                   case_tuple=(tf, tf_conditions))

        # ------ make credible-diff between objects for each test_condition_tuple
        q_samples = q_samples.reshape((pcf.n_test_conditions, -1, pcf.n_objects))
        # system_dicts = [{FMT['object']: s}
        #                 for s in pcf.objects_disp]
        #
        # tc_dicts = [dict(tct) for tct in pcf.test_conditions()]
        # = product of test-cond in all test-factor dimensions, as needed by tab_cred_diff
        d = cred_diff(q_samples, diff_axis=2, case_axis=0, sample_axis=1,
                      p_lim=FMT['credibility_limit'])
        object_tuples = [(obj,) for obj in pcf.objects_disp]
        tc_tuples = [*pcf.test_condition_categories()]
        diff_within = fmt.tab_credible_diff(d,
                                            y_label=a,
                                            file_label=a,
                                            diff_head=(FMT['object'],),
                                            diff_labels=object_tuples,
                                            case_head=pcf.test_factors.keys(),
                                            case_labels=tc_tuples,
                                            cred_head=FMT['probability'])

        # make credible-diff between test_condition_tuple(s) for each system
        d = cred_diff(q_samples, diff_axis=0, case_axis=2, sample_axis=1,
                      p_lim=FMT['credibility_limit'])
        diff_between = fmt.tab_credible_diff(d,
                                             y_label=a,
                                             file_label=a,
                                             diff_head=pcf.test_factors.keys(),
                                             diff_labels=tc_tuples,
                                             case_head=(FMT['object'],),
                                             case_labels=object_tuples,
                                             cred_head=FMT['probability'])
        return cls(test_factors,
                   perc_by_test_cond,
                   diff_within,
                   diff_between)


# --------------------------------- classes for differences between groups

class GroupEffectSet:
    """Container for displays of differences between populations,
    as represented by subjects in separate groups
    """
    def __init__(self, pop_mean=None, pop_ind=None):  # , subjects=None):  # *** skip subjects here?
        """
        :param pop_mean: dict with elements (a_label, AttributeGroupEffects instance)
        :param pop_ind: dict with elements (a_label, AttributeGroupEffects instance)
            both with results separated by groups
        """
        self.pop_mean = pop_mean
        self.pop_ind = pop_ind
        # self.subjects = subjects  # *** needed here ??? **************

    def save(self, path, **kwargs):
        """Save all stored display objects in their corresponding sub-trees
        """
        if self.pop_mean is not None:
            for (a, a_disp) in self.pop_mean.items():
                a_disp.save(path / 'population_mean' / a, **kwargs)
        if self.pop_ind is not None:
            for (a, a_disp) in self.pop_ind.items():
                a_disp.save(path / 'population_individual' / a, **kwargs)
        # if self.subjects is not None:
        #     for (a, a_disp) in self.subjects.items():
        #         a_disp.save(path / 'subjects' / a, **kwargs)

    @classmethod
    def display(cls, pcr):
        """Create instance with all displays
        :param pcr: single pc_result.PairedCompResultSet instance
        :return: cls instance
        """
        # re-organize model dict
        pcm = {a: {g: g_models[a]
                   for (g, g_models) in pcr.models.items()
                   if type(g) is not tuple}  # skip merged group, if any
               for a in pcr.pcf.attributes}
        # pcm[a_label][group] = pc_result.PairedCompGroupModel instance
        pop_mean = None
        pop_ind = None
        if FMT['population_individual']:
            pop_ind = {a: AttributeGroupEffects.display(a, pcr.pcf,
                                                        {g: pcm_ag.pred_population_ind()
                                                         for (g, pcm_ag) in pcm_a.items()})
                       for (a, pcm_a) in pcm.items()}
        if FMT['population_mean']:
            pop_mean = {a: AttributeGroupEffects.display(a, pcr.pcf,
                                                         {g: pcm_ag.pred_population_mean()
                                                          for (g, pcm_ag) in pcm_a.items()})
                        for (a, pcm_a) in pcm.items()}
        # if FMT['subject_group']:
        #     subjects = make quality boxplots by group and table ???
        return cls(pop_mean, pop_ind)


class AttributeGroupEffects:
    """Container for all displays for ONE Attribute,
    illustrating differences between populations, as represented by subject groups,
    Plots CANNOT show category limits, because they may be different across groups.
    """
    # ***** can use generalized RangeDisplay class ?? *************
    # *** include boxplots if q_map is available ???

    def __init__(self, range, group_diff=None):
        """
        :param range: RangeDisplay instance with displays by group
        :param group_diff: TableRef with credible group differences
            for all objects in all test conditions
        """
        self.range = range
        self.group_diff = group_diff

    def __repr__(self):
        return (self.__class__.__name__ + '(' +
                '\n\t'.join(f'{k}= {repr(v)},'
                            for (k, v) in self.__dict__) +
                '\n\t)')

    def save(self, path, **kwargs):
        """
        :param path: Path instance to directory where results are saved
        :return: None
        """
        if self.range is not None:
            self.range.save(path, **kwargs)
        if self.group_diff is not None:
            self.group_diff.save(path, **kwargs)

    @classmethod
    def display(cls, attr, pcf, ag_models):
        """Create displays to show differences between groups
        :param attr: string label of current attribute
        :param pcf: pc_data.PairedCompFrame instance
        :param ag_models: dict with elements (g, g_model), where
            g_model = pc_result.PopulationPredictiveModel instance
                that can generate samples

        :return: a single cls instance
        """
        q_samples = [m.quality_samples for m in ag_models.values()]
        # q_samples[group][n, t0,..., tT, i] = n-th sample for i-th object in (t0, ...)-th test cond
        # might have different n_samples in different groups
        q_perc = np.array([np.percentile(q.reshape(-1, pcf.n_objects),
                                         FMT['percentiles'], axis=0)
                           for q in q_samples])
        # q_perc[g, p, i] = p-th percentile for i-th object in g-th group
        q_perc = q_perc.transpose((1, 0, 2))
        # q_perc[p, g, i] = p-th percentile for i-th object in g-th group
        # as needed by fig_percentiles
        q_cdf = np.array([_sample_cdf_0(q.reshape(-1, pcf.n_objects), axis=0)
                          for q in q_samples])
        # q_cdf[g, i] = cdf for i-th object in g-th group

        group_names = [*ag_models.keys()]
        # *** can not display response-category thresholds,
        # *** because the groups have different intervals
        # *** transpose -> objects by groups  *******************
        # ********* check case order ****************************
        q_perc = q_perc.transpose((0, 2, 1))
        # q_perc[p, i, g] = p-th percentile for i-th object in g-th group
        q_cdf = q_cdf.transpose((1, 0))
        case_labels = {FMT['object']: pcf.objects_disp,
                       FMT['group']: group_names}
        perc_by_group_tab = fmt.tab_percentiles(q_perc,  # [1:, ...],  # skip object[0] ???
                                                # cdf=q_cdf,  # [1:, ...],
                                                perc=FMT['percentiles'],
                                                file_label=attr,
                                                case_labels=case_labels,
                                                )
        perc_by_group_fig = fmt.fig_percentiles_df(perc_by_group_tab,
                                                   y_label=attr,
                                                   file_label=attr,
                                                   case_labels=case_labels
                                                   )
        range = RangeDisplay(percentile_plot=perc_by_group_fig,
                             percentile_tab=perc_by_group_tab)

        # *** Replace by ???
        # range = RangeDisplay.create(attr, q_samples, object_tuple=..., case_tuple=...)

        # credible group differences, for all objects, by test conditions
        obj_tc_heads = (FMT['object'], *pcf.test_factors.keys())
        obj_tc_labels = [(s, *tct)
                         for (tct, s) in product(pcf.test_condition_categories(),
                                                 pcf.objects_disp[1:])  # skip first object
                         # ordered linearly by (test-cond, objects), like q_samples[group]
                         # but listed as (object, test-cond)
                         ]
        # ********************* check linear index in q_samples, obj_tc_labels ***************
        q_samples = [group_q[..., 1:].reshape(-1, len(obj_tc_labels))
                     for group_q in q_samples]
        # q_samples[group][n, t_s] = n-th sample for case t_s = linear index in tc_s_labels
        d = cred_group_diff(q_samples, sample_axis=0, case_axis=1,
                            p_lim=FMT['credibility_limit'])
        group_diff = fmt.tab_credible_diff(d,
                                           y_label=attr,
                                           file_label=attr,
                                           diff_head=(FMT['group'],),
                                           diff_labels=[(g,) for g in group_names],
                                           case_head=obj_tc_heads,
                                           case_labels=obj_tc_labels,
                                           cred_head=FMT['probability'])
        return cls(range, group_diff)


# ------------------------------------------------ Basic Display Class:
class RangeDisplay:
    """Container for object result displays for a given attribute,
    optionally subdivided along secondary factor (test-condition or group)
    """
    # *** subclass RangeDisplayWithBox ?
    def __init__(self, percentile_plot,
                 boxplot=None,  # ********* delete here -> subclass ? ************
                 percentile_tab=None):
        """
        :param percentile_plot: FigureRef with percentile plot showing
            predictive individual and population properties
        :param boxplot: (optional) FigureRef with boxplots of individual MAP estimated results
        :param percentile_tab: (optional) TableRef with percentile_plot results tabulated.
        """
        self.percentile_plot = percentile_plot
        self.boxplot = boxplot
        self.percentile_tab = percentile_tab

    def __repr__(self):
        return (self.__class__.__name__ + '(' +
                '\n\t'.join(f'{k}= {repr(v)},'
                            for (k, v) in self.__dict__) +
                '\n\t)')

    def save(self, dir_path,
             figure_format=None,
             table_format=None,
             **kwargs):
        """
        :param dir_path: path to directory for saving files
        :param figure_format: extension string for saved figures
            might be None if only tables are to be saved in new format
        :param table_format: extension string for saved tables
            might be None if only figures are to be saved in new format
        :param kwargs: any additional settings for Table writer function
        :return: None
        """
        if figure_format is None and table_format is None:
            figure_format = DEFAULT_FIGURE_FORMAT
            table_format = DEFAULT_TABLE_FORMAT
        if self.percentile_plot is not None:
            if figure_format is not None:
                self.percentile_plot.save(dir_path, figure_format=figure_format)
        if self.boxplot is not None:
            if figure_format is not None:
                self.boxplot.save(dir_path, figure_format=figure_format)
        if self.percentile_tab is not None:
            self.percentile_tab.save(dir_path, table_format=table_format, **kwargs)

    @classmethod
    def create(cls, a_label, q_samples, object_labels,
               case_tuple=None,
               thr=None, q_map=None):
        """Make a cls instance containing displays of quality estimates,
        either as 2D, or 3D with case sub-division.
        Boxplot included only if q_map given.
        :param a_label: string label for current quality attribute
        :param q_samples: 2D or 3D array with quality samples,
            q_samples[n, i] = n-th quality sample of i-th object, OR
            q_samples[n, c, i] = n-th sample of i-th object in c-th test-condition case
        :param thr: (optional) 1D array with category thresholds for percentile plot
        :param q_map: (optional) 2D or 3D array with quality MAP estimates *** ??**********
            q_map[n, i] = n-th subject quality point estimate for i-th object, OR
            q_map[n, c, i] = n-th subject quality point estimate for i-th object in c-th case
        :param object_labels: sequence of string labels for tested objects
            len(object_labels) == q_samples.shape[-1]
        :param case_tuple: tuple (case_head, c_labels) with strings, if 3D display
            case_head = single string with case factor label
            c_labels = sequence of
            len(c_labels) == q_samples.shape[1] if q_samples.ndim == 3
        :return: a cls instance
        """
        # ****** new plot and table fcns need order objects, cases *********
        if q_samples.ndim == 3:
            assert len(case_tuple[1]) == q_samples.shape[1], 'Mismatch q_samples.shape vs case_tuple'

        q_perc = np.percentile(q_samples, FMT['percentiles'], axis=0)
        # q_perc[p, ..., i] = p-th percentile for i-th object in ...-th test cond.
        q_cdf = _sample_cdf_0(q_samples, axis=0)
        # = P[ U <= 0 ] for all objects
        # q_cdf[..., i] = cdf for i-th object in ...-th test condition
        # if case_tuple is None:
        #     case_labels = [(FMT['object'], object_labels)]
        # else:
        #     case_labels = [case_tuple,
        #                    (FMT['object'], object_labels)]
        # range_perc_old = fmt.fig_percentiles(q_perc,
        #                                  cat_limits=thr,
        #                                  y_label=a_label,
        #                                  case_labels=case_labels
        #                                  )  # ************ replace by fig_percentile_df
        if q_perc.ndim == 3:
            # q_perc[p, c, i] = p-th percentile for i-th object in c-th case
            # q_cdf[c, i] = P[ U <= 0 ] for i-th object in c-th case
            q_perc = q_perc.transpose((0, 2, 1))
            # q_perc[p, i, c] = p-th percentile for i-th object in c-th case
            q_cdf = q_cdf.transpose((1, 0))
            # q_cdf[i, c] = prob for i-th object in c-th case
            case_labels = dict([(FMT['object'], object_labels),
                                case_tuple])
        else:
            # q_perc[p, i] = p-th percentile for i-th object
            # q_cdf[i] = P[ U <= 0 ] for i-th object
            case_labels = {FMT['object']: object_labels}
        table = fmt.tab_percentiles(q_perc,
                                    # cdf=q_cdf,
                                    perc=FMT['percentiles'],
                                    file_label=a_label,
                                    case_labels=case_labels
                                    )
        range_perc = fmt.fig_percentiles_df(table,
                                            cat_limits=thr,
                                            y_label=a_label,
                                            file_label=a_label,
                                            case_labels=case_labels
                                            )
        if q_map is not None:  # *** -> separate classmethod create_with_box
            if q_map.ndim == 3:
                q_map = q_map.transpose((1, 0, 2))
                # q_map[c, n, i] = n-th subject value for i-th object in c-th case,
                # as needed by fig_indiv_boxplot
            # else:
                # q_map[n, i] = n-th value for i-th object
            f_box = fmt.fig_indiv_boxplot(q_map,
                                          cat_limits=thr,
                                          y_label=a_label,
                                          object_tuple=(FMT['object'], object_labels),
                                          case_tuple=case_tuple)
        else:
            f_box = None
        return cls(percentile_plot=range_perc,
                   boxplot=f_box,
                   percentile_tab=table)


# ---------------------------------- Help functions:
def _make_subject_table(a_label, a_model):
    """Tabulate all quality estimates for all subjects in ONE group, for ONE attribute
    :param a_label: attribute string label
    :param a_model: pc_result.PairedCompGroupModel instance
    :return: a TableRef instance with results for all subjects
    """
    pcf = a_model.pcf
    q = [s_model.quality_samples[..., 1:]
         for s_model in a_model.subjects.values()]
    # q[s][n, t, :] = n-th sample vector for s-th subject in t-th test condition
    # skipping first reference object
    q_perc = np.array([np.percentile(q_s,
                                     FMT['percentiles'],
                                     axis=0)
                       for q_s in q])
    # q_perc[s, p, t, i] = p-th percentile of i-th object for s-th subject in t-th test condition
    cdf = np.array([_sample_cdf_0(q_s) for q_s in q])
    # cdf[s, t, i] = P[q<= 0] for s-th subject for i-th object in t-th test condition
    # *** sort subjects by labels alphabetically
    s_list = [*a_model.subjects.keys()]
    s_index = np.argsort(s_list)
    q_perc = q_perc[s_index, ...]
    cdf = cdf[s_index, ...]
    s_list.sort()

    # q_perc = q_perc.transpose((1, 0, 2, 3))  # **** for current tab_percentiles
    # q_perc[p, s, t, i] = n-th sample of i-th object for s-th subject in t-th test condition
    # return fmt.tab_percentiles(q_perc,
    #                            cdf=cdf,
    #                            perc=FMT['percentiles'],
    #                            y_label=a_label,
    #                            case_labels=[(FMT['subject'], s_list),
    #                                         *pcf.test_factors.items(),
    #                                         (FMT['object'], pcf.objects_disp[1:])],
    #                            case_order=[FMT['subject'],
    #                                        FMT['object'],
    #                                        *pcf.test_factors.keys()]
    #                            )
    q_perc = q_perc.transpose((1, 0, 3, 2))
    # q_perc[p, s, i, t] = n-th sample of i-th object for s-th subject in t-th test condition
    q_shape = (*q_perc.shape[:3], *pcf.n_test_factor_categories)
    q_perc = q_perc.reshape(q_shape)
    # cdf = cdf.transpose() ****** reshape
    return fmt.tab_percentiles(q_perc,
                               # cdf=cdf,  # *************
                               perc=FMT['percentiles'],
                               file_label=a_label,
                               case_labels=[(FMT['subject'], s_list),
                                            (FMT['object'], pcf.objects_disp[1:]),
                                            *pcf.test_factors.items()]
                               )


def _median_cat_limits(thr_samples, fc):
    """get median response-interval limits from model samples
    :param thr_samples: 2D array with samples of UPPER interval thresholds
    :param fc: flag = True if forced-choice data
    :return: 1D array of response-interval limits
    """
    c = np.median(thr_samples, axis=0)[:-1]  # excluding +Inf
    # c[:] = UPPER limits on positive side
    if fc:
        c = np.insert(c, 0, 0., axis=0)
    return c


def _dir_name(g):
    """make sure group name is a possible directory name
    :param g: string or tuple of strings
    :return: string to be used as directory
    """
    if type(g) is tuple:  # several strings
        g = '+'.join(s for s in g)
    return g


def _sample_cdf_0(u, axis=0):
    """
    Probability that U <= 0 calculated from set of samples.
    :param u: array of samples drawn from U
    :param axis: (optional) axis with independent samples
        e.g., mean of U == np.mean(u, axis=axisk)
    :return: array p with
        p[...] = P(U[...] <= 0)
        p.shape == u.shape with axis removed
    """
    n = u.shape[axis]
    return (np.sum(u <= 0, axis=axis) + 0.5) / (n + 1)


def display_attribute_correlation(a_models):
    """Show jointly most credible correlations
    in subsets of all pairs of perceptual attributes
    for subjects in ONE group with learned models for all attributes
    :param a_models: dict with (a_label: m_a) elements,
        where m_a = PairedCompGroupModel instance with
        m_a.subjects[s] = a PairedCompIndModel instance that can generate quality samples
    :return: TableRef instance with correlation table, or None if no correlations found

    2018-05-20, check that number of samples are matching, i.e., RELATED across attribute
    2021-08-29, include only subjects with models learned for all attributes
        calculate correlation within each subject,
        return average across subjects
    """
    # **** show correlations separately by test conditions ??? ****
    a_labels = list(a_models.keys())
    # check if subjects are the same across attributes:
    common_subjects = set.intersection(*(set(ga.subjects.keys())
                                         for ga in a_models.values()))
    all_subjects = set.union(*(set(ga.subjects.keys())
                               for ga in a_models.values()))
    # if len(common_subjects) == 0:
    if not common_subjects:
        logger.warning('Cannot calculate correlation; no subjects with results for all attributes')
        return None
    if common_subjects < all_subjects:
        logger.warning(f'Correlations calculated only for {len(common_subjects)} ' +
                       f'of {len(all_subjects)} subjects ' +
                       'with results for all attributes')
    q_samples = [[m_a.subjects[s].quality_samples for s in common_subjects]
                 for m_a in a_models.values()]
    q_samples = np.array(q_samples)
    # stored as q_samples[a_label, subject, sample, test_cond_tuple, system]
    (n_attr, n_subjects, n_samples, n_tc, n_objects) = q_samples.shape
    q_samples = q_samples.reshape((n_attr, n_subjects * n_samples, -1))
    # join all test_conditions
    c = cred_corr(q_samples, corr_axis=0, sample_axis=1, vector_axis=2)
    # = list of tuple( ((i,j), p, median_corr_coeff )
    # indicating pairs (a_label[i], a_label[j]) with correlation != 0, with joint probability p
    if len(c) > 0:
        return fmt.tab_credible_corr(c, a_labels=a_labels)
    else:
        logger.info('No credible correlations between attributes.')
        return None


def fig_comments(perc):
    """Generate figure explanations.
    :param perc: vector with percentile values
    :return: comment string
    """
    p_min = np.amin(perc)
    p_max = np.amax(perc)
    c = f"""Figure Explanations:
    
Figure files with names like
someAttribute_xxx.pdf or xxx.jpg, or similar,
display user-requested percentiles (markers) and credible intervals (vertical bars) 
The vertical bars show the range between {p_min:.1f}- and {p_max:.1f}- percentiles.

Median response thresholds are indicated by thin lines
extending horizontally across the graph.

The credible ranges include all uncertainty
caused both by real inter-individual perceptual differences
and by the limited number of judgments by each listener.

Figure files with names like someAttribute-box_xxx.pdf
show boxplots of the distribution of point-estimated individual results 
in the group of test participants.
"""
    return c


def table_comments(pcf):
    c = """Table Explanations:

*** Tables of Percentiles:
Files with names like someAttribute_xxx.tex or *.txt
show numerical versions of the information in percentile plots-
Medians, credible ranges, and marginal probabilities for negative and positive values are shown.

*** Tables of Credible Differences:
Files with names like someAttribute-diff_xxx.tex or *.txt 
show a list of Object or Test-condition pairs
which are ALL JOINTLY credibly different
with the tabulated credibility.
The credibility value in each row is the JOINT probability
for the pairs in the same row and all rows above it.
"""
    if pcf.n_attributes > 1:
        c += """
*** Tables of Attribute Correlations
show cosine-similarity between perceptual Attribute results
across all Objects and Test Conditions.

The rows of the correlation table show
a sequence of Attribute Pairs, for which
the Correlations are JOINTLY credibly non-zero.

The probability value on each row shows the JOINT probability 
that all pairs on the same and previous rows have non-zero correlation.
The correlation value in the last column shows the
estimated conditional median cosine-similarity for the indicated pair, 
given that all the previous correlations are also truly non-zero,
"""
    return c
