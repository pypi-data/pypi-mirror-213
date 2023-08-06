"""This module defines functions that read / write Paired-Comparison data and analysis result tables,
from/to a table file of any kind that package pandas can handle.

A single data file for READING may include PC records from ONE or SEVERAL respondents.
The subject id may be stored in a designated column of the table,
otherwise the file name can be used as subject id,
or (in Excel-type files) the subject may be identified by the sheet name.

Regardless of the file storage format, even if an input file represents only ONE subject,
the PC data are always delivered by a generator function
pc_gen, yielding tuples (subject_id, attribute, df), where
subject_id = a string or any other object that can be used as dict key,
attribute = a single attribute key
df = a pandas.DataFrame instance with (Stim, Response, TestCond) data

Some pandas file readers can also do some
data conversions and/or type checking.
Column names may be modified before the data are delivered to caller.

For writing PC data or any other table to a file,
cast the DataFrame instance to subclass Table,
and use Table(df).save(...) method,
always creating ONE separate file for each table.


*** Version History:
* Version 2.1:
2022-09-03, allow OLD .res format for input, but only by explicit input parameters
2022-06-24, first version using Pandas DataFrame storage
"""
import warnings  # ***** only to suppress some Pandas FutureWarning

import pandas as pd
import logging

logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)

PAIR_COLUMN = '_S'  # name of stimulus-pair column in delivered DataFrame-s
DIFF_COLUMN = '_R'  # name of response-difference column in delivered DataFrame-s
# other columns contain test-factor categories, one column for each test factor.


# ------------------------------------------------ File exceptions
class FileReadError(RuntimeError):
    """Any type of exception while attempting to read PC data from a file
    """


class MissingColumnError(RuntimeError):
    """Missing some required column in PC DataFrame instance obtained from a file
    """


class ArgumentError(RuntimeError):
    """Error in calling arguments. No file can be read."""


class FileWriteError(RuntimeError):
    """Any type of exception while attempting to write a pd.DataFrame table to a file
    """


# ----------------------------------------- Main reading function:
def pc_gen(file_path, pcf,
           subject=None,
           attribute=None,
           pair=None,
           difference=None,
           choice=None,
           grade=None,
           rename_cols=None,
           read_fcn=None,
           **file_kwargs
           ):
    """Generator yielding data chunks, one for each attribute and subject,
    from data stored in a table-style file that can be read by Pandas.
    Each table row must include fields for one paired-comparison Stim-Response result,
    but may also include other data fields.
    :param file_path: Path to existing file for reading
    :param pcf: a pc_data.PairedCompFrame instance defining data structure
    :param attribute: (optional) 'path' or 'file' or 'sheet'
        or name of column specifying the evaluated Attribute in each table row
    :param subject: (optional) 'file' or 'sheet' or column name for subject ID label
        None -> 'sheet', if Excel-type file, otherwise -> 'file'
    :param pair: name of column with object pairs,
        OR tuple of two names of columns with labels of paired objects.
        None allowed only if pcf.objects defines exactly TWO objects
    :param difference: (optional) name of column with stored integer-coded response
        None -> difference calculated from (choice, grade) combination
    :param choice: name of column with chosen object in each stimulus pair
    :param grade: name of column with ordinal difference magnitude category
        Both choice and grade are required if difference is None
    :param rename_cols: (optional) dict with elements (old_name: new_name)
    :param read_fcn: (optional) basic read function, e.g., pd.read_excel,
        or any user-supplied function with similar signature.
        If None, a default pandas function is determined by file_path.suffix.
    :param file_kwargs: any additional arguments for the
        read function for the specific file format
    :return: generator object yielding tuples (subject_id, attribute, df),
        cleaned to include only required columns-
    """
    def gen_blocks(df, s, a, pair):
        """Process input data from one file, (or one sheet, if Excel type)
        yielding PairedCompBlock instances
        :param df:
        :param s: 'file' or name of subject column
        :param a: 'path' or 'file' or name of attribute column
        :param pair: tuple with name of attribute columns, or name of existing pair column
        :return: generator object
        """
        if rename_cols is not None:
            df.rename(columns=rename_cols, inplace=True)
        if s == 'file':
            s = '_file_subject_'
            df[s] = file_path.stem
        elif a == 'file':
            a = '_file_attr_'
            df[a] = file_path.stem
        if a == 'path':
            a = '_path_attr_'
            df[a] = _find_in_path(file_path, pcf.attributes)
        elif a is None and pcf.n_attributes == 1:
            a = '_one_attribute_'
            df[a] = pcf.attributes[0]
        elif a not in df.columns:
            raise MissingColumnError(f'No attribute found in {file_path}')
        if s not in df.columns:
            raise MissingColumnError(f'No subject ID found in {file_path}')
        if pair in df.columns:  # with tuple elements
            df.rename(columns={pair: PAIR_COLUMN})
        elif isinstance(pair, tuple):  # calculate column with tuple elements
            df[PAIR_COLUMN] = df.apply(_join_pair, args=(pair,), axis=1)
        elif len(pcf.objects) == 2:  # only ONE pair possible
            df[PAIR_COLUMN] = [tuple(pcf.objects)] * len(df)
        else:
            raise ArgumentError('Pair column(s) must be specified.')
        if difference in df.columns:
            df.rename(columns={difference: DIFF_COLUMN}, inplace=True)
        else:  # calculate it if possible
            df[DIFF_COLUMN] = df.apply(_calc_diff, axis=1,
                                       args=(PAIR_COLUMN, choice, grade, pcf))
        for (tf, tf_cat) in pcf.test_factors.items():
            if tf not in df.columns:
                df[tf] = _find_in_path(file_path, tf_cat)
        for (sa, df_sa) in df.groupby([s, a]):
            # ********* OR keep all columns, in case user wants to modify / save it again ? *******
            yield *sa, df_sa[[PAIR_COLUMN, DIFF_COLUMN, *pcf.test_factors.keys()]]
    # ----------------------------------------- Check arguments:
    if read_fcn is None:
        read_fcn = _default_reader(file_path)
    if subject is None:
        raise ArgumentError('subject (file / path / sheet / column) must be defined.')
    if difference is None and (choice is None or grade is None):
        raise ArgumentError('Both choice and grade must be defined.')
    if subject == 'file' and attribute == 'file':
        raise ArgumentError('subject and attribute cannot both be defined by file name')
    if subject == 'sheet' and attribute == 'sheet':
        subject = 'file'  # Acceptable, with warning
        logger.warning('Using file name for subject id; sheet name for attribute')
    # -------------------------------------------------------
    logger.debug(f'Reading from {file_path} with {read_fcn}')
    if read_fcn is pd.read_excel:
        if 'sheet_name' not in file_kwargs.keys():
            file_kwargs['sheet_name'] = None  # -> read ALL sheets
            # because read_excel uses sheet_name=0 by default
    elif subject == 'sheet' or attribute == 'sheet':
        raise FileReadError(f'File type {file_path.suffix} has no "sheet"s.')
    try:
        df = read_fcn(file_path,
                      **file_kwargs)
    except Exception as e:
        raise FileReadError(f'{file_path} error: {e}')
    if type(df) is pd.DataFrame:
        yield from gen_blocks(df, subject, attribute, pair)
        # *** No sheets: subject and attribute must be either 'file' or column name
    else:  # we have a dict of sheet DataFrames
        for (sh, df) in df.items():
            # may use sheet name as either subject or attribute
            if subject == 'sheet':
                s = '_sheet_subject'
                df[s] = sh
                yield from gen_blocks(df, s, attribute, pair)
            elif attribute == 'sheet':
                a = '_sheet_attr'
                df[a] = sh
                yield from gen_blocks(df, subject, a, pair)


# ---------------------------------------------------------------------
class Table(pd.DataFrame):
    """Subclass adding a general save method,
    automatically switching to desired file format.
    """
    def save(self, file_path,
             allow_over_write=True,
             write_fcn=None,
             **file_kwargs):
        """Save a pd.DataFrame to a table-style file.
        :param file_path: Path instance defining file location and full name
        :param allow_over_write: (optional) boolean, if False, find new unused path stem.
        :param write_fcn: (optional) user-supplied function with signature
            write_fcn(table, path, **kwargs).
            If None, default pd.DataFrame method is used, determined by file_path.suffix
        :param file_kwargs: (optional) any additional arguments for the
            write function for the specific file format.
        :return: None
        """
        # NOTE: CANNOT write to OLD .res format
        if not allow_over_write:
            file_path = safe_file_path(file_path)
        suffix = file_path.suffix
        try:
            if write_fcn is None:
                if suffix in ['.xlsx', '.xls', '.odf', '.ods', '.odt']:
                    self.to_excel(file_path, sheet_name=file_path.stem, **file_kwargs)
                elif suffix in ['.csv']:
                    self.to_csv(file_path, **file_kwargs)
                elif suffix in ['.txt']:
                    self.to_string(file_path, **file_kwargs)
                elif suffix in ['.tex']:
                    with warnings.catch_warnings():
                        # suppress Pandas FutureWarning about to_latex method
                        warnings.simplefilter('ignore')
                        self.to_latex(file_path, **file_kwargs)
                else:
                    raise FileWriteError(f'No write method for file type {suffix}')
            else:
                write_fcn(self, file_path, **file_kwargs)
        except Exception as e:
            raise FileWriteError(f'Could not write to {file_path}. Error: {e}')


# ------------------------------------------ help functions:
def safe_file_path(p):
    """Ensure non-existing file path, to avoid over-writing,
    by adding a sequence number to the path stem
    :param p: file path
    :return: p_safe = similar file path with modified name
    """
    f_stem = p.stem
    f_suffix = p.suffix
    i = 0
    while p.exists():
        i += 1
        p = p.with_name(f_stem + f'-{i}' + f_suffix)
    return p


def _default_reader(file_path):
    """Find a function that can read the given file path
    :param file_path: a Path instance
    :return: a pandas reader function, e.g., pd.read_excel
    """
    suffix = file_path.suffix
    if suffix in ['.xlsx', '.xls', '.odf', '.ods', '.odt']:
        return pd.read_excel
    elif suffix in ['.csv', '.txt']:
        return pd.read_csv
    elif suffix in ['.sav', '.zsav']:
        return pd.read_spss
    elif suffix in ['.dta']:
        return pd.read_stata
    # elif suffix in ['.res']:  # OLD file format, must be called explicitly
    #     return pc_file_res.read_dahlquist_res
    else:
        raise FileReadError(f'Cannot (yet) read file format {suffix}')


def _find_in_path(path, cat_list):
    """Find ONE attribute value in path string
    :param path: path to current file
    :param cat_list: sequence of strings that might be found as path substring
    :return: string = found substring of path
    """
    for cat in cat_list:
        if cat in str(path):
            return cat
    return None


def _join_pair(row, pair):
    """Make data for a new column with object pairs
    :param row: ONE row from pd.DataFrame instance with PC data
    :param pair: None or tuple with exactly two column names in df
    :return: list with joined tuples
    """
    # if pair is None and len(pcf.objects) == 2:  # tested by caller
    #     return tuple(pcf.objects)  # only one possible pair
    try:
        return row[pair[0]], row[pair[1]]
    except Exception as e:
        raise MissingColumnError(f'Some missing pair column: {pair}: {e}')


def _calc_diff(row, pair, choice, grade, pcf):
    """Calculate integer-encoded difference response,
    row-wise by pd.DataFrame.apply method.
    :param row: pd.Series instance indexed by attr, pair, choice, grade
    :param pair: name of column with object pairs
    :param choice: name of column with preferred object among the
    :param grade: name of column with magnitude grade of difference
    :param pcf: PairedCompFrame instance
    :return: a list with integer-encoded response values
    """
    try:
        diff = pcf.difference_grades.index(row[grade]) + pcf.forced_choice
        if row[choice] == row[pair][0]:
            return -diff
        elif row[choice] == row[pair][1]:
            return diff
        elif diff == 0 and not pcf.forced_choice:
            return diff
        else:
            return None
    except Exception as e:
        raise MissingColumnError(f'Cannot calculate response difference: {e}')


# ------------------------------------------------------------ TEST:
if __name__ == '__main__':
    from pathlib import Path
    from PairedCompCalc.pc_data import PairedCompFrame
    from PairedCompCalc import pc_logging

    work_path = Path.home() / 'Documents' / 'PairedComp_sim'  # or whatever...
    data_path = work_path / 'data' / 'Group0' / 'SimQ'  # to use simulation data generated by run_sim.py

    pc_logging.setup()  # to save the log file
    pcf = PairedCompFrame(attributes=['SimQ'],
                          objects=['HA0', 'HA1', 'HA2'],
                          forced_choice=False,
                          difference_grades=['Equal', 'Slightly Better', 'Better', 'Much Better'],
                          test_factors={'Stim': ['speech', 'music'], 'SNR': ['Quiet', 'High']}
                          )

    pc_file = pc_gen(data_path / 'pop0_Subj0.xlsx', pcf,
                     subject='sheet',
                     attribute='attribute',  # 'path',
                     pair=('pair_0', 'pair_1'),
                     # difference='difference',
                     choice='choice',
                     grade='grade',
                     )
    for (s, a, df) in pc_file:
        print(f'Subject {repr(s)}. Attribute {a}')
        print(df.head(10))
