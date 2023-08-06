"""This module defines classes to hold paired-comparison experimental data,
and methods and functions to read and write such data.

*** Class Overview:

PairedCompFrame: defines layout of a paired-comparison experiment.
    Some properties of a PairedCompFrame instance can define selection criteria
    for a subset of data to be included for analysis.

PairedCompDataSet: all data for selected group(s), subjects, attributes, and test conditions,
    to be used as input for statistical analysis.
    Each subject should be tested in all (or most) test conditions,
    but not necessarily for all perceptual attributes.

*** Input File Formats:
Data may be imported from (and exported to) various Table-style file formats
that package Pandas can handle, e.g., Excel (xlsx), Comma-separated values (csv),
as defined in module pc_file.

Data elements may be stored in specified table columns, or other locations,
as defined by keyword parameters to methods PairedCompDataSet.load and .include.
See script run_sim and run_pc for an example.

Users may also provide their own special reader function for any other file format.

For backward compatibility,
data can also be accessed from files stored in an older text format,
defined and used by Dahlquist and Leijon (2003).
Files in this format are saved with suffix '.res'.
These files can be read using the special function pc_file_res.read_dahlquist_res.
This format is somewhat restricted and should NOT be used for new studies.


*** Input Data Files:

All input files from an experiment must be stored in one directory tree.

If results are to be analyzed for more than one group of test subjects,
the data for each group must be stored in separate sub-directory trees
on the first level just below the top directory.
All subdirectories in the tree are searched recursively for data files.

Each input file may contain paired-comparison records
for one or more test subjects judging one or more perceptual attributes,
in one or more test conditions.
File names are arbitrary, although they may be associated with
the encoded name of the participant, to facilitate data organisation.

Files for different test conditions and/or attributes may be stored in separate subdirectories.
The directory name can then be used to indicate a test-factor category or an attribute label,
if not specified within the data file itself.
For this purpose the complete file-path is searched for a sub-string
matching the desired attribute or test-condition label.

Several files may include data for the same subject,
e.g., results obtained in different test conditions,
or simply for replicated test sessions with the same subject.


*** Example Directory Tree:

Assume we have data files in the following directory structure:
~/pc_data / NH / Low,   containing files Subject0.xlsx, ..., Subject20.xlsx
~/pc_data / NH / High,  containing files Subject0.xlsx, ..., Subject20.xlsx
~/pc_data / HI / Low,  containing files test0.xlsx, ..., test10.xlsx
~/pc_data / HI / High, containing files test0.xlsx, ..., test10.xlsx

Directories 'NH' and 'HI' may contain data for different groups of test participants,
e.g, individuals with normal hearing (NH) or with impaired hearing (HI).

The sub-directories named 'Low' and 'High' may include data files collected
in two different noise conditions, with 'Low' or 'High' signal-to-noise ratio.
If so, the noise condition may or may not also be specified in a column in the file itself.

Data files for the SAME subject should then be found in BOTH sub-directories 'Low' and 'High'.
because each subject would normally be tested in both test conditions.

If tests have been done for different perceptual Attributes,
each subject should ideally be tested with all Attributes,
to allow the most accurate estimation of correlations between Attributes.
However, this is not required.

Subjects in different groups are considered separate, even if their subject ID is the same.


*** Accessing Input Data för Analysis:

*1: Create a PairedCompFrame object defining the experimental layout, e.g., as:
pcf = PairedCompFrame(objects = ['testA', 'testB', 'testC'],  # three sound processors
        attributes = ['Preference'],  # only a single perceptual attribute in this case
        test_factors = {'Sound': ['speech', 'music'],  # test factor 'Sound' with two categories
                        'SNR': ['Low', 'High']}  #  test factor 'SNR' with two categories
        )
NOTE: attribute labels must be strings that can be used as directory names.
NOTE: Letter CASE is distinctive, i.e., 'Low' and 'low' are different categories.

*2: Load all test results into a PairedCompDataSet object:

ds = PairedCompDataSet.load(pcf, path='~/pc_data', groups=['NH', 'HI'], fmt='csv')

The loaded data structure ds can then be used as input for analysis.

If fmt='xxx' is specified, the load method reads only files with the 'xxx' extension.

If the fmt argument is left unspecified, or if fmt=None,
PairedCompDataSet.load will attempt to read ALL files in the designated directory tree,
and use all files that contain paired-comparison data.

The parameter 'groups' is an optional list of subdirectory names,
one for each participant group.

The parameter pcf is a PairedCompFrame object that defines the experimental layout.
Some properties of this object can define selection criteria
for a subset of data to be included for analysis.

All test-factor categories are, ideally, defined in file columns.
If so, the sub-directory names 'Low' and 'High' are not significant,
and need not agree with any test-condition labels in the PairedCompFrame object.

However, if a desired test factor, or a desired Attribute, is NOT defined in the data file contents,
the file-reading methods will attempt to find the desired category
as a sub-string of the full path string.

Therefore, in this case the category label MUST be UNIQUE in the file paths.
For example, test_factors = {'SNR': ['Low', 'High', 'Higher']}
can NOT be used if the categories are defined by the path string.
Test-condition labels can not be sub-strings of a group name,
because the group directory name is also included in the path-string.

Similarly, result files for separate perceptual Attributes
may also be collected in different subdirectories,
and the Attribute may then be specified as a sub-string of the path
in the same way as test conditions.

Obviously, the safest policy is to include all needed data in the input file contents.

Files in the older 'res' format can not define separate test conditions or attributes.
For these files ALL test factors and perceptual attributes MUST be derived from the path-string.


*** Selecting Subsets of Data for Analysis:

It is possible to define a data set including only a subset of experimental data.
For example, assume we want to analyze only group 'HI':

ds_HI = PairedCompDataSet.load(pcf, path='~/pc_data', groups=['HI'])

Or perhaps we want to look at results for only one test condition,
and only two of the three sound objects that have been tested.
Then we must define a new PairedCompFrame object before loading the data:

small_pcf = PairedCompFrame(objects = ['testA', 'testB'],  # only two of the sound processors
        attributes = ['Preference'],  # same single perceptual attribute
        test_factors = {'SNR': ['High']}  # test factor SNR, now with only ONE category
        )
ds_AB_HI_High = PairedCompDataSet.load(small_pcf, path='~/pc_data', groups =  ['HI'])

This will include all data with SNR='High', regardless of other test-factors,
but only for the 'HI' group of subjects.

If there are data for other perceptual attributes in addition to 'Preference',
the analysis is restricted to the specified subset of attributes.

Any paired-comparisons for OTHER OBJECTS, not explicitly named in small_pcf, will be DISREGARDED.
Any results for OTHER ATTRIBUTES, not explicitly specified in small_pcf, will be DISREGARDED.
Any results having a desired test-factor category will be INCLUDED,
regardless of the category within any other test factor.

*** Version History:
* Version 2.1:
2022-09-02, PairedCompFrame.objects required as explicit input; NOT derived from data files
2022-07-02, PairedCompFrame.objects_alias changed to mapping: file label -> display label
2022-07-01, using Pandas for data input and Pandas DataFrame storage in PairedCompDataSet

* Version 2.0.1:
2022-03-08, minor fix PairedCompDataSet.load clearer error output
2022-03-09, PairedCompFrame objects_alias warning if incorrect length.

* Version 2.0:
2021-09-17, allow PairedCompDataSet.save() in xlsx format
2021-09-22, test and minor fix in PairedCompDataSet.save() method

* Version 1.0.0:
2018-03-30, changed nesting structure to PairedCompDataSet.pcd[group][attribute][subject]
    because we learn one separate PairedCompGroupModel for each group and attribute.
    Allow missing subjects for some attributes;
    identical subjects needed only for attribute correlations.
2018-04-12, Allow objects_alias labels in PairedCompFrame
2018-08-10, renamed classes PairedCompRecord and new class StimRespItem
2018-08-10, include test condition in each StimRespItem, to facilitate EMA data input
2018-08-12, simplified PairedCompRecord structure: no redundant data,
    all general experimental info given only in PairedCompFrame
2018-08-13, simplified PairedCompDataSet structure
2018-11-25, changed PairedCompFrame.systems -> objects, and similar derived names
2018-11-26, changed PairedCompFrame.response_labels -> difference_grades, and similar derived names
2018-12-07, PairedCompDataSet.save() to a set of json files

Changes in version 0.9.0:
2018-09-21, changed property name PairedCompFrame.test_factors, and some method names
2018-09-24, generalized class structure, to allow flexible new file formats
2018-09-25, using new PairedCompFile class, containing PairedCompItem instances
2018-09-30, changed signature of PairedCompFile
"""
import numpy as np
from pathlib import Path
from itertools import product
import json  # ***** backward compatibility, not needed ? use pickle?
import pandas as pd
import logging

from PairedCompCalc import pc_file

logger = logging.getLogger(__name__)

_PAIR_COLUMN = pc_file.PAIR_COLUMN  # single column with tuples (stim1, stim2)
_DIFF_COLUMN = pc_file.DIFF_COLUMN  # column with integer-coded grade difference in (-M,..., +M)
# = module-internal fixed column names for PC data stored as pandas.DataFrame objects

SAVE_PAIR_COLUMNS = ('Pair_0', 'Pair_1')
SAVE_SUBJECT_COLUMN = 'Subject'
SAVE_ATTRIBUTE_COLUMN = 'Attribute'
SAVE_CHOICE_COLUMN = 'Choice'
SAVE_GRADE_COLUMN = 'Grade'
# = default column names in PC data files, for PairedCompDataSet.save(...)


# ------------------------------------------------------------------
class PairedCompFrame:
    """Defines structure of one Paired-Comparison analysis calculation.
    Data about test participants are NOT included.
    """
    # *** store objects, difference_grades, test_factors as pd.CategoricalDtype objects ?
    def __init__(self,
                 attributes,
                 difference_grades,
                 forced_choice=False,
                 objects=None,
                 objects_alias=None,
                 test_factors=None
                 ):
        """
        :param objects: sequence with unique string labels of objects being evaluated
            in order as desired for result output
        :param attributes: sequence of string labels for selected perceptual attributes
            Attribute labels MUST be strings that can be used as directory names.
        :param difference_grades: sequence with ordinal difference-magnitude rating labels
            Note: SAME ordinal grades for all attributes!
        :param forced_choice: (optional) boolean indicator that response NO Difference is not allowed.
        :param objects_alias: (optional) dict mapping of objects -> labels used for displays
        :param test_factors: (optional) iterable with elements (test_factor, category_list),
            where
            test_factor is a string,
            category_list is a list of labels for allowed categories within test_factor.
            A category label is normally just a single string,
                but may be a tuple of strings.
            May be left empty, if only one test condition is used.

        NOTE: objects, attributes, and test_factors may define a subset of
            data present in input data files.
        """
        # store object_alias as dict mapping object.key -> alias_key
        if objects is None:
            raise RuntimeError('Version >= 2.1 needs objects named, NOT extracted from data files')
            # *** no warning in future versions!
        else:
            assert len(set(objects)) == len(objects), 'Object labels must be unique'
        self.objects = objects
        if objects_alias is None:
            objects_alias = dict()
        self.objects_alias = dict(objects_alias)
        assert len(attributes) > 0 and len(attributes[0]) > 0, 'Must have at least one named attribute'
        assert len(set(attributes)) == len(attributes), 'Attribute labels must be unique'

        self.attributes = attributes
        self.difference_grades = difference_grades
        self.forced_choice = forced_choice
        if test_factors is None:
            self.test_factors = dict()
        else:
            self.test_factors = dict(test_factors)  # == OrderedDict in python >= 3.7

    def __repr__(self):
        return (self.__class__.__name__ + f'(\n\t' +
                ',\n\t'.join(f'{key}={repr(v)}'
                             for (key, v) in vars(self).items()) +
                '\n\t)')

    @property
    def n_objects(self):
        return len(self.objects)

    @property
    def objects_disp(self):  # *** generator function ? ***
        """Systems labels for display
        """
        return [obj if obj not in self.objects_alias.keys() else self.objects_alias[obj]
                for obj in self.objects]

    @property
    def n_attributes(self):
        return len(self.attributes)

    @property
    def n_difference_grades(self):
        """number of ranked magnitudes of perceived pair-difference,
        including the "equal" category if forced_choice == False,
        but not including negative differences
        """
        return len(self.difference_grades)

    @property
    def n_test_factors(self):
        return len(self.test_factors)

    @property
    def n_test_factor_categories(self):  # *** -> test_condition_shape ?
        """1D list with number of test-condition alternatives in each test factor"""
        return [len(v) for v in self.test_factors.values()]

    @property
    def n_test_conditions(self):
        return np.prod(self.n_test_factor_categories, dtype=int)

    @property
    def n_quality_params(self):
        """Number of quality parameters to be learned for each Group and each Attribute.
        """
        return (self.n_objects - 1) * self.n_test_conditions

    def test_conditions(self):  # ********* needed ?
        """generator of all combinations of (tf, tf_category) pairs from each test factor
        i.e., test_factor label included in all pairs
        len(result) == prod(len(v) for v in self.test_factors.values() )
        Generated pairs are sorted like self.test_factors.
        """
        return product(*(product([tf], tf_cats)
                         for (tf, tf_cats) in self.test_factors.items())
                       )

    def test_condition_categories(self):
        """generator of test-factor categories,
        as combinations of one category from each test-factor dimension
        :return: iterator of tuples (tc_0,..., tc_T) for all test-factor dimensions
        """
        return product(*self.test_factors.values())

    @classmethod
    def load(cls, p):  # *** needed ? use pickle instead?
        """Try to create instance from file saved earlier
        :param p: string file-path or Path instance, identifying a pre-saved json file
        :return: one new PairedCompFrame instance, if successful
        """
        try:
            with open(p, 'rt') as f:
                d = json.load(f)
            return cls(**d['PairedCompFrame'])
        except KeyError:
            raise pc_file.FileReadError(p + 'is not a saved PairedCompFrame object')

    def save(self, path, file_name='pcf.json'):  # ***************
        """dump self to a json serialized file path / file_name
        """
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)
        p = (path / file_name).with_suffix('.json')
        with p.open('wt') as f:
            json.dump({'PairedCompFrame': self.__dict__}, f,
                      indent=1, ensure_ascii=False)

    def filter(self, df):
        """Check that all given PC data agree with self properties,
        :param df: one DataFrame instance with PC data
            for ONE subject and ONE attribute
        :return: df with unacceptable rows deleted
        """
        def check_pairs(row):
            return all(obj in self.objects
                       for obj in row[_PAIR_COLUMN])

        def check_diff(row):
            r = row[_DIFF_COLUMN]
            if self.forced_choice:
                return 0 < abs(r) <= self.n_difference_grades
            else:
                return abs(r) < self.n_difference_grades
        # --------------------------------------------------
        pairs_ok = df.apply(check_pairs, axis=1).to_numpy()
        diff_ok = df.apply(check_diff, axis=1).to_numpy()
        return df.loc[np.logical_and(pairs_ok, diff_ok)]


# ------------------------------------------------------------
class PairedCompDataSet:
    """All result data for one complete paired-comparison analysis.
    Includes two properties:
    pcf = a PairedCompFrame instance, defining the experimental layout,
    pcd = a nested dict containing result data for all participants
    """
    def __init__(self, pcf, pcd):
        """
        :param pcf: a single PairedCompFrame instance,
        :param pcd: nested dict {g: {a: {s: s_pc}}}, where
            g = a group-name string, empty or equal to a directory name,
            a = one of the attribute keys specified in pcf,
            s = subject ID (e.g., string or integer), and
            s_pc = a pd.DataFrame instance with one row for each PC record

        Thus, a single result DataFrame may be extracted from the pcd by nested dict indexing, e.g.,
        df = self.pcd[group][attr][subject]
        """
        self.pcf = pcf
        self.pcd = pcd

    def __repr__(self):
        return self.__class__.__name__ + '(pcf=pcf, pcd=pcd)'

    def __str__(self):
        n_subjects = {g: {a: sum(len(r) > 0 for (s, r) in a_subjects.items())
                          for (a, a_subjects) in g_attr.items()}
                      for (g, g_attr) in self.pcd.items()}
        # = subjects with non-empty pc result lists
        n_g = len(self.pcd)
        return (self.__class__.__name__ + ' with ' + f'{n_g} '
                + ('groups' if n_g > 1 else 'group')
                + ' with data from \n'
                + '\n'.join([f' {n_s} subjects for attribute {repr(a)}'
                             + (f' in group {repr(g)}' if n_g > 1 else '')
                             for (g, g_attributes) in n_subjects.items()
                             for (a, n_s) in g_attributes.items()
                             ])
                + '\n')

    @classmethod
    def initialize(cls, pcf, groups=None):
        """Create an EMPTY container for paired-comp data
        :param pcf: PairedCompFrame instance
        :param groups: (optional) list of group names,
            each element MUST be a name of one immediate sub-directory of path
        :return: a cls instance
        """
        if groups is None:
            groups = ['']  # *** must have at least one group
        pcd_df = {g: {a: dict()
                      for a in pcf.attributes}
                  for g in groups}
        return cls(pcf, pcd_df)

    @classmethod
    def load(cls, pcf, path, fmt=None, groups=None,
             # subject='file',
             # attribute=None,
             # pair=None,
             # choice=None,
             # grade=None,
             # difference=None,
             **kwargs):
        """Create a cls instance from PC data in designated table-style file(s),
        readable by Pandas.
        :param pcf: a PairedCompFrame instance defining experimental structure
        :param path: string or Path defining top of directory tree with all data files
        :param fmt: (optional) string with file suffix for data files.
            If undefined, all files are tried, so mixed file formats can be used as input.
        :param groups: (optional) list of group names, where
            each element MUST be name of one immediate sub-directory of path
        :param kwargs: dict with all necessary arguments for file reader, including:
            :param subject: (optional) string 'file' or column header in file, or 'sheet',
                defining subject id
            :param attribute: (optional) 'file' or 'path' or 'sheet' or column name,
                defining the rated attribute in the same table row or file
            :param pair: tuple of column names containing objects compared as a pair,
                OR single name of a column containing object pairs
            :param choice: the selected object in one pair
            :param grade: the selected ordinal magnitude of the difference between presented objects
            :param difference: (optional) name of column with responses
                encoded as integer in (-M,..., 0, ..., M),
                where M is the highest possible ordinal difference magnitude.
                Positive value means that 'pair_1' was selected in a pair (pair_0, pair_1)
                If difference is specified: choice and grade are not used.
            AND (optionally) any additional arguments for file reader method, e.g.,
            :param rename_cols: a dict with (file_column, use_name) pairs,
            and/or any other keyword argument to Pandas reader function, e.g.,
            :param converters: a dict with (file_column, converter_function) elements,
            :param header: integer row number containing column names.
            See Pandas.read_excel for example other input options.
        :return: a cls instance
        """
        self = cls.initialize(pcf, groups)
        self.include(path, fmt, **kwargs)
        return self

    def include(self, path, fmt=None,
                groups=None,  # allow new groups defined here
                # subject='file',  # include all in kwargs
                # attribute=None,
                # pair=None,
                # choice=None,
                # grade=None,
                # difference=None,
                **kwargs):
        """Read input data into self DataFrame objects.
        :param path: string or Path defining top of directory tree with all data file
        :param fmt: (optional) string with file suffix for accepted data files.
            If None, all files are tried, so mixed file formats can be used as input.
        :param groups: (optional) list of additional group names
        :param kwargs: additional keyword arguments as defined by method load
        :return: None
        Result: self updated with input PC data
        """
        def gen_pc_blocks(path, group):
            """generator of PairedCompBlocks to be included,
            from one or several files in selected directory.
            :param path: top directory containing PairedCompFile-readable files.
            :param group: sub-directory name in path, OR None
            :return: iterator of PairedCompItem instances,
                yielding only items accepted by pcf
            """
            for p in _gen_file_paths(path, group, fmt):
                try:
                    logger.info(f'Reading {p}')
                    for (s, a, df) in pc_file.pc_gen(p, self.pcf, **kwargs):
                        yield s, a, df
                except pc_file.MissingColumnError as e:
                    logger.warning(f'Cannot use data in {p}: {e}')
                except pc_file.FileReadError as e:
                    logger.warning(f'Can not read {p}: {e}')
                    # just skip this file, try next file
        # ----------------------------------------------------------
        if groups is None:
            groups = []
        for g in groups:
            if g not in self.pcd.keys():
                self.pcd[g] = dict()
        path = Path(path)
        for g in self.pcd.keys():
            for (s, a, df) in gen_pc_blocks(path, g):
                df = self.pcf.filter(df)
                # ***** check for missing-data cells ? ******************
                logger.info(f'Found subject {repr(s)}, attribute {a}: {df.shape[0]} PC records. '
                            + ('Some missing data. Valid data count =\n'
                               + _table_valid(df) if np.any(df.isna()) else ''))
                logger.debug(f'Subject {repr(s)}:\n' + df.to_string())
                if not df.empty:
                    if a not in self.pcd[g]:
                        self.pcd[g][a] = dict()
                    if s not in self.pcd[g][a]:
                        self.pcd[g][a][s] = df
                    else:
                        self.pcd[g][a][s] = pd.concat([self.pcd[g][a][s],
                                                       df], axis=0)

    def save(self, path, allow_over_write=False, fmt='csv',
             subject=SAVE_SUBJECT_COLUMN,
             attribute=SAVE_ATTRIBUTE_COLUMN,
             pair=SAVE_PAIR_COLUMNS,
             difference=None,
             choice=SAVE_CHOICE_COLUMN,
             grade=SAVE_GRADE_COLUMN,
             **file_args):
        """Save self.pcd in a directory tree with sub-trees for groups and attributes,
        with one file for each attribute and each subject.
        :param path: Path or string defining the top directory where files are saved
        :param allow_over_write: boolean switch, over-write files if True
        :param fmt: string label specifying file format
        :param subject: column for subject ID (ID also used as file name)
        :param attribute: column for Attribute label(s)
        :param pair: sequence (stim1, stim2) with TWO column names
            for converting single-column pair -> two separate columns in saved file
        :param difference: (optional) column for integer-coded difference
            not necessary, because choice and grade are always saved
        :param choice: column for response choice (re-coded from integer-coded difference)
        :param grade: column for response grade (re-coded from integer-coded difference)
        :param file_args: (optional) dict with arguments to specific file object
        :return: None
        """
        # ****** allow user to set column names, like load(...) **************************
        # MUST save stimulus pair labels in two separate columns for safe re-loading
        path = Path(path)
        fmt = fmt.lstrip('.')  # just in case
        for (g, group_data) in self.pcd.items():
            if len(g) == 0:
                g_path = path
            else:
                g_path = path / g
            for (a, a_subjects) in group_data.items():
                a_path = g_path / a
                a_path.mkdir(parents=True, exist_ok=True)
                for (s_id, s_df) in a_subjects.items():
                    try:
                        p = (a_path / s_id).with_suffix('.' + fmt)
                        s_df[subject] = s_id
                        s_df[attribute] = a
                        s_df[list(pair)] = s_df.apply(_encode_pair, axis=1, result_type='expand')
                        # -> two new columns with separated (stim1, stim2) labels
                        s_df[choice] = s_df.apply(_encode_choice, axis=1)
                        s_df[grade] = s_df.apply(_encode_grade, axis=1,
                                                 args=(self.pcf,))
                        if difference is not None:
                            s_df[difference] = s_df[_DIFF_COLUMN]
                        s_df = s_df.drop(columns=[_PAIR_COLUMN, _DIFF_COLUMN],
                                         inplace=False, errors='ignore')
                        pc_file.Table(s_df).save(p, allow_over_write, **file_args)
                    except pc_file.FileWriteError as e:
                        raise RuntimeError(f'Could not save {self.__class__.__name__} in {repr(fmt)} format. '
                                           + f'Error: {e}')

    def ensure_complete(self):
        """Check that every subject has data for at least SOME test_condition_categories.
        NOTE: This condition is relaxed with current hierarchical population prior.
        Analysis results are calculated even if there are NO data for some test conditions.
        Quality estimates for missing data are then determined only by the population prior.
        Non-matching subject sets are allowed for different attributes.
        :return: None

        Result:
        self.pcd may be reduced: subjects with no results are deleted.
        logger warnings for missing data.
        2022-07-01, adapted to use pd.DataFrame storage of PC results
        """
        for (g, g_attributes) in self.pcd.items():
            for (a, ga_subjects) in g_attributes.items():
                incomplete_subjects = set(s for (s, item_list) in ga_subjects.items()
                                          if len(item_list) == 0)
                for s in incomplete_subjects:
                    del self.pcd[g][a][s]
                    logger.warning(f'Subject {s} in group {repr(g)} excluded for attribute {repr(a)}; no data')
            # *** set consecutive index for each subject DataFrame ***
            # check if all attributes include the same subjects
            all_subjects = set.union(*(set(ss)
                                       for ss in g_attributes.values()))
            for (a, ga_subjects) in g_attributes.items():
                # check if attribute has NO subjects:
                if len(ga_subjects) == 0:
                    raise RuntimeError(f'No subjects in group {repr(g)} for attribute {repr(a)}')
                missing_subjects = all_subjects - set(ga_subjects)
                if len(missing_subjects) > 0:
                    logger.warning(f'No data for {missing_subjects} '
                                   + f'for attribute {repr(a)} in group {repr(g)}')
                if self.pcf.n_test_factors == 0:
                    break
                # *** else: Check if missing subjects in some test conditions:
                missing_tc_subjects = {tc: list()
                                       for tc in self.pcf.test_condition_categories()}
                for (s, df_s) in ga_subjects.items():
                    count_s = df_s.value_counts(subset=[*self.pcf.test_factors.keys()])
                    for tc in missing_tc_subjects.keys():
                        if tc not in count_s.index:
                            missing_tc_subjects[tc].append(s)
                for (tc, missing_s) in missing_tc_subjects.items():
                    if len(missing_s) > 0:
                        msg = (f'No data for {missing_s} '
                               + f'in group {repr(g)} for attribute {repr(a)} '
                               + f'in {tuple(self.pcf.test_factors)}= {tc}')
                        logger.warning(msg)


# ------------------------------------------------ local help functions:
def _gen_file_paths(p, sub_dir=None, suffix=None):
    """generator of all file Paths in directory tree p, recursively, with desired name pattern
    :param p: Path instance defining top directory to be searched
    :param sub_dir: (optional) sub-directory name
    :param suffix: (optional) file suffix of desired files
    :return: iterator of Path objects, each defining one existing data file
    """
    if p.is_file():
        return [p]  # allow a single file
    if sub_dir is not None and len(sub_dir) > 0:
        p = p / sub_dir  # search only in sub_dir
    if suffix is not None and len(suffix) > 0 and p.with_suffix('.'+suffix).is_file():
        return [p]  # allow a single file for this group
    if suffix is None or suffix == '':
        glob_pattern = '*.*'  # read any file types
    else:
        glob_pattern = '*.' + suffix  # require suffix
    return (f for f in p.rglob(glob_pattern)
            if f.is_file() and f.name[0] != '.')


def _encode_pair(row):  # , i):
    """Extract two object labels from single pair tuple in DataFrame row
    :param row: ONE row from a PC DataFrame
    :param i: index (0 / 1) for tuple in stim column
    :return: list of TWO object labels
    """
    # return list(row[_PAIR_COLUMN[i]])
    return list(row[_PAIR_COLUMN])


def _encode_choice(row):
    """Calculate choice variable from given DataFrame row
    :param row: ONE row from a PC DataFrame
    :return: selected object label
    """
    if row[_DIFF_COLUMN] < 0:
        return row[_PAIR_COLUMN][0]
    elif row[_DIFF_COLUMN] == 0:
        return ''
    else:
        return row[_PAIR_COLUMN][1]


def _encode_grade(row, pcf):
    """Calculate grade label from given DataFrame row
    :param row: ONE row from a PC DataFrame
    :param pcf: a PairedCompFrame instance
    :return: grade label in pcf.difference_grades
    """
    if pcf.forced_choice:  # diff_grade == 0 not allowed
        return pcf.difference_grades[abs(row[_DIFF_COLUMN]) - 1]
        # pcf.difference_grades[0] <-> difference magnitude == 1
    else:
        return pcf.difference_grades[abs(row[_DIFF_COLUMN])]
        # pcf.difference_grades[0] <-> NO difference <-> difference magnitude == 0


def _table_valid(df: pd.DataFrame):
    """Count valid data elements for all columns
    :param df: Pandas.DataFrame instance with input PC data
    :return: table string for logger output
    """
    return pd.DataFrame([df.count()]).to_string(index=False)


# ----------------------------------------- TEST:
if __name__ == '__main__':
    # from pathlib import Path
    from PairedCompCalc import pc_logging
    # from PairedCompCalc.pc_file import pc_gen

    work_path = Path.home() / 'Documents' / 'PairedComp_sim'  # or whatever...

    pc_logging.setup()  # to save the log file
    pcf = PairedCompFrame(attributes=['SimQ'],
                          objects=['HA0', 'HA1', 'HA2'],
                          forced_choice=False,
                          difference_grades=['Equal', 'Slightly Better', 'Better', 'Much Better'],
                          test_factors={'Stim': ['speech', 'music'], 'SNR': ['Quiet', 'High']}
                          )

    # ----------------------------- test PairedCompDataSet.load_df

    data_path = work_path / 'data'

    # ds = PairedCompDataSet.initialize(pcf, groups=['Group0'])
    ds = PairedCompDataSet.load(pcf, data_path, fmt='xlsx',
                                # groups=['Group0'],
                                subject='sheet',
                                attribute='attribute',
                                pair=('pair_0', 'pair_1'),
                                # difference='difference',
                                choice='choice',
                                grade='grade'
                                )
    print('Loaded ds= ', ds)
    # include same data again, just for test:
    ds.include(data_path, fmt='xlsx',
               subject='sheet',
               attribute='attribute',
               pair=('pair_0', 'pair_1'),
               # difference='difference',
               choice='choice',
               grade='grade'
               )
    print('Total included ds= ', ds)

    # ------------------------------- test save:

    save_path = work_path / 'test_write'
    ds.save(save_path, fmt='csv', allow_over_write=True)
