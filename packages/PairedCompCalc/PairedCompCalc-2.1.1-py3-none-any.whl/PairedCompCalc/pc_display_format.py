"""This module includes functions to format output displays of
PairedCompResultSet model results,
in either graphic or textual form.

*** Version History:
* Version 2.1.1:
2023-06-12, interaction_sep, condition_sep -> FMT
            (old hard-coded interaction_sep='*' not allowed in file names)

* Version 2.1:
2022-09-04, allow mpl_style and mpl_params argument for plot parameters
2022-09-01, attribute table as pandas.DataFrame; function tab_lr_test deleted!
2022-07-05, set figure save format in FigureRef.save method, to allow several save calls
2022-07-04, make tables as subclass of pandas.DataFrame to allow more save formats

* Version 2.0:
2021-09-03, generalized function tab_percentiles for arbitrary dimensionality
2021-09-11, generalized function fig_percentiles with input similar to tab_percentiles
2021-09-11, modified function fig_indiv_boxplot input

* Version 1.0:
2018-02-06, simplified table generation, generate only one selected table type
2018-02-18, use module variable FMT['table_format'] where needed
2018-04-19, minor changes to include population quality params
2018-08-11, minor cleanup

2018-08-29, fix percent sign switch by table_format
2018-10-02, use general FMT dict, fix table file suffix
2018-10-08, allow cat_limits in fig_percentiles and fig_indiv_boxplot
2018-11-24, changed 'x_label' to 'tested_objects' in FMT params
2019-03-27, include marginal credibility values in percentile tables
"""
import numpy as np
from itertools import cycle, product
import matplotlib.pyplot as plt
import pandas as pd
import logging

from PairedCompCalc.pc_file import Table

plt.rcParams.update({'figure.max_open_warning': 0,
                     'figure.autolayout': True})
# changes from matplotlib default settings
# other settings may be defined by user parameter mpl_params

logger = logging.getLogger(__name__)


# --------------------------- Default format parameters:
FMT = {'colors': 'rbgk',    # to separate results in plots, cyclic
       'markers': 'oxs*_',  # corresponding markers, cyclic use
       'show_intervals': True,  # include median response thresholds in plots
       'probability': 'Probability',  # heading in tables
       'attribute': 'Attribute',  # heading in tables
       'group': 'Group',  # heading in tables
       'correlation': 'Correlation',  # heading in tables
       'scale_unit': '',  # scale unit for attribute plot axis
       'interaction_sep': '\u00D7',  # mult.sign. separating condition labels in result file names
       'condition_sep': '_',    # separating attribute and its test condition(s) in file names
       }
# = module-global dict with default settings for display details
# that may be changed by user


def set_format_param(mpl_style=None, mpl_params=None, **kwargs):
    """Set / modify format parameters.
    Called before any displays are generated.
    :param mpl_style: (optional) matplotlib style sheet, or list of style sheets
    :param mpl_params: (optional) dict with matplotlib (k, v) rcParam settings
    :param kwargs: dict with any formatting variables
    :return: None
    """
    if mpl_style is not None:
        plt.style.use(mpl_style)
    if mpl_params is not None:
        plt.rcParams.update(mpl_params)
    other_fmt = dict()
    for (k, v) in kwargs.items():
        k = k.lower()
        if k in FMT:
            FMT[k] = v
        else:
            other_fmt[k] = v
    if len(other_fmt) > 0:
        logger.warning(f'Parameters {other_fmt} unknown, not used.')


# ---------------------------- Main Result Classes
class FigureRef:
    """Reference to a single graph instance
    """
    def __init__(self, ax, path=None, name=None):
        """
        :param ax: Axes instance containing the graph
        :param path: Path to directory where figure has been saved
        :param name: (optional) updated name of figure file
        """
        self.ax = ax
        self.path = path  # **** skip! defined by save method
        self.name = name

    def __repr__(self):
        return (f'FigureRef(ax= {repr(self.ax)}, ' +
                f'path= {repr(self.path)}, name= {repr(self.name)})')

    @property
    def fig(self):
        return self.ax.figure

    def save(self, path,
             figure_format,
             **kwargs):  # *** copied from EmaCalc ***
        """Save figure to given path
        :param path: Path to directory where figure has been saved
        :param figure_format: figure-format string code -> file-name suffix
        :param kwargs (optional) any additional kwargs, *** NOT USED ***
        :return: None
        """
        path.mkdir(parents=True, exist_ok=True)
        f = (path / self.name).with_suffix('.' + figure_format)
        self.fig.savefig(str(f))


class TableRef(Table):  # copied from EmaCalc
    """A pd.DataFrame table sub-class, having its own name and special save method
    """
    def __init__(self, df, name):
        """
        :param df: a Table(pd.DataFrame) instance
        :param name: file name for saving the table
        """
        super().__init__(df)
        self.name = name

    def save(self, path,
             table_format='txt',
             figure_format=None,  # *** not used
             **kwargs):
        """Save table to file.
        :param path: Path to directory for saving self.
            suffix is determined by FMT['table_format'] anyway
        :param table_format: table-format string code -> file-name suffix
        :param figure_format: NOT USED
        :param kwargs: (optional) any additional arguments to pandas writer function
        :return: None
        """
        path.mkdir(parents=True, exist_ok=True)   # just in case
        f = (path / self.name).with_suffix('.' + table_format)
        super().save(f, **kwargs)


class DiffTableRef(TableRef):
    """Special subclass suppressing index in save method
    """
    def save(self, path,
             **kwargs):
        """Save table to file.
        :param path: Path to directory for saving self.
        :param kwargs: (optional) any additional arguments (incl. table_format)
        :return: None
        """
        if 'index' not in kwargs:
            kwargs['index'] = False  # override Pandas default = True
        super().save(path, **kwargs)


# ---------------------------------------- Formatting functions:

def fig_percentiles_df(df,
                       case_labels,
                       y_label='',
                       file_label='',
                       cat_limits=None,
                       x_space=0.3,
                       colors='rbgk',
                       markers='oxs*_',
                       y_min=None,
                       y_max=None,
                       **kwargs):  # ************** copied from EmaCalc
    """create a figure with percentile results
    as defined in a given pd.DataFrame instance
    :param df: pd.DataFrame instance with primary percentile data, saved with
        one row for each case category, as defined in df.index elements
        one column for each percentile value.
    :param case_labels: dict with elements (case_factor_i, case_labels_i),
        that were used to construct table df, with
        case_factor_i = key string for i-th case dimension,
            = name of i-th level of df.index
        case_labels_i = list of labels for i-th case dimension
            = categories in df.index.levels[i]
        df.n_rows == prod_i len(case_labels_i)
    :param y_label: (optional) string for y-axis label
    :param cat_limits: 1D array with response-interval limits (medians)
    :param file_label: (optional) string as first part of file name
    :param x_space: (optional) min space outside min and max x_tick values
    :param colors: (optional) sequence of color codes to separate results in plots
    :param markers: (optional) sequence of marker codes to separate results in plots
        len(colors) != len(markers) -> many different combinations
    :param y_min: (optional) enforced lower limit of vertical axis
    :param y_max: (optional) enforced upper limit of vertical axis
    :param kwargs: (optional) dict with any additional keyword arguments for plot commands,
    :return: FigureRef instance with plot axis with all results

    NOTE: plot will use df.index.level[0] categories as x-axis labels,
    aad index.level[1:] as plot labels in the legend
    """
    def plot_one_case(case_i, x, y_i, c, m):
        """
        :param case_i: case label
        :param x: 1D array with x values
        :param y_i: 2D array with y values
            y_i[p, i] = p-th percentile value for x[i]
            len(x) == y_i.shape[-1]
        :param c: color code
        :param m: marker code
        :return: None
        """
        n_perc = y_i.shape[0]
        if n_perc == 1:
            line = ax.plot(x, y_i[0],
                           linestyle='', color=c,
                           marker=m, markeredgecolor=c, markerfacecolor='w',
                           **kwargs)
        elif n_perc == 2:
            line = ax.plot(np.tile(x, (2, 1)),
                           y_i,
                           linestyle='solid', color=c,
                           marker=m, markeredgecolor=c, markerfacecolor='w',
                           **kwargs)
        else:
            ax.plot(np.tile(x, (2, 1)),
                    [y_i[0], y_i[-1]],
                    linestyle='solid', color=c,
                    **kwargs)
            line = ax.plot(np.tile(x, (y_i.shape[0] - 2, 1)),
                           y_i[1:-1],
                           linestyle='solid', color=c,
                           marker=m, markeredgecolor=c, markerfacecolor='w',
                           **kwargs)
        line[0].set_label(str(case_head) + '=' + str(case_i))
    # ----------------------------------------------------------

    case_keys = [*case_labels.keys()]
    case_cats = [*case_labels.values()]
    # *** df.index.levels are NOT used because they are sorted alphabetically, NOT in tabulated order
    assert df.shape[0] == np.prod([len(cc_i) for cc_i in case_cats]), 'case_labels must match df size'
    x_label = case_keys[0]
    x_tick_labels = list(case_cats[0])
    if len(case_keys) == 1:
        (case_head, case_list) = ('', [''])  # make ONE empty sub-case to facilitate indexing
    elif len(case_keys) == 2:
        (case_head, case_list) = (case_keys[1], case_cats[1])
    else:
        (case_head, case_list) = (case_keys[1:], [*product(*case_cats[1:])])
    n_cases = len(case_list)
    # ------------------------------------------------------------------
    fig, ax = plt.subplots()
    dx = (1. - x_space) / n_cases
    x = np.arange(len(x_tick_labels)) - (n_cases - 1) * dx / 2
    # = x position for first case
    if df.index.nlevels == 1:
        plot_one_case('', x, df.loc[x_tick_labels].values.T,
                      colors[0], markers[0])
    else:
        for (case_i, c, m) in zip(case_list,
                                  cycle(colors),
                                  cycle(markers)):
            y_i = df.xs(case_i, level=case_head)
            y_i = y_i.loc[x_tick_labels].values.T
            plot_one_case(case_i, x, y_i, c, m)
            x += dx
    (x_min, x_max) = ax.get_xlim()
    x_min = min(x_min, -x_space)
    x_max = max(x_max, len(x_tick_labels) - 1 + x_space)
    ax.set_xlim(x_min, x_max)
    if cat_limits is not None:
        _plot_response_intervals(ax, cat_limits)
    ax.set_xticks(np.arange(len(x_tick_labels)))
    xticks = [str(c) for c in x_tick_labels]
    ax.set_xticklabels(xticks,
                       **_x_tick_style(xticks))
    (y0, y1) = ax.get_ylim()
    if y_min is not None:
        y0 = y_min
    if y_max is not None:
        y1 = y_max
    ax.set_ylim(y0, y1)
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    if len(case_list) > 1:
        ax.legend(loc='best')
    if len(file_label) > 0:
        file_label += FMT['condition_sep']
    f_name = file_label + FMT['interaction_sep'].join(df.index.names)
    # fig.set_tight_layout(tight=True)
    return FigureRef(ax, name=f_name)


def fig_indiv_boxplot(q,
                      y_label,
                      object_tuple,
                      cat_limits=None,
                      case_tuple=None,
                      x_space=0.5,
                      **kwargs):
    """create a figure with boxplot of individual results
    :param q: 2D array or sequence of 2D arrays,
        with point-estimated quality values, stored as
        q[c][n, i] = n-th individual result for s_labels[i], in c-th case variant, OR
        q[n, i] if no case variants
    :param y_label: string for y-axis label
    :param object_tuple: tuple (object_key, object_labels)
        object_key = string to become x_label in plot
        object_labels = list of strings with labels for x_ticks, one for each value in rows q[..., :]
        len(object_labels) == q.shape[-1]
    :param cat_limits: (optional) 1D array with response-interval limits (medians)
    :param case_tuple: (optional) tuple (case_order, case_list) for case variants
        len(case_list) == q_perc.shape[-2] if q_perc.ndim == 3 else case_list not used
    :param x_space: (optional) min space outside min and max x_tick values
    :param kwargs: (optional) dict with any additional keyword arguments for boxplot command.

    :return: FigureRef object with single plot axis with all results

    2018-10-08, new cat_limits parameter
    2021-09-11, input object_tuple = (x_label, object_labels)
    """
    # *** make signature same as fig_percentile ? ****************
    # *** use plt.rcParams for boxplot properties  ? ********
    if len(q) <= 1:
        return None  # boxplot does not work
    (x_label, object_labels) = object_tuple
    fig, ax = plt.subplots()
    if case_tuple is None:
        assert q.ndim == 2, 'Input must be 2D if no case variants'
        case_tuple = ('', [''])
        q = [q]
        # make it a list with ONE 2D array
    (case_head, case_labels) = case_tuple
    x_offset = min(0.2, 0.8 / len(case_labels))
    if len(case_labels) > 1:
        box_width = 0.8 * x_offset
    else:
        box_width = 0.5
    x_pos = np.arange(len(object_labels)) - x_offset * (len(case_labels) - 1) / 2
    for (y, c_label, c, m) in zip(q, case_labels, cycle(FMT['colors']), cycle(FMT['markers'])):
        boxprops = dict(linestyle='-', color=c)
        label = case_head + '=' + c_label
        # flierprops = dict(marker=m, markeredgecolor=c, markerfacecolor='w', # *** markersize=12,
        #                   linestyle='none')
        whiskerprops = dict(marker='', linestyle='-', color=c)
        capprops = dict(marker='', linestyle='-', color=c)
        medianprops = dict(linestyle='-', color=c)
        ax.boxplot(y, positions=x_pos,
                   widths=box_width,
                   sym='',  # ******** no fliers
                   boxprops=boxprops,
                   medianprops=medianprops,
                   whiskerprops=whiskerprops,
                   capprops=capprops,
                   **kwargs)
        median = np.median(y, axis=0)
        ax.plot(x_pos, median, linestyle='',
                marker=m, markeredgecolor=c, markerfacecolor='w',
                label=label)
        x_pos += x_offset

    (x_min, x_max) = ax.get_xlim()
    x_min = min(x_min, -x_space)
    x_max = max(x_max, len(object_labels) - 1 + x_space)
    ax.set_xlim(x_min, x_max)
    if cat_limits is not None and FMT['show_intervals']:
        _plot_response_intervals(ax, cat_limits)
    ax.set_xticks(np.arange(len(object_labels)))
    ax.set_xticklabels(object_labels)
    y_unit = FMT['scale_unit']
    if len(y_unit) > 0:
        ax.set_ylabel(y_label + ' (' + y_unit + ')')
    else:
        ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    if np.any([len(cl) > 0 for cl in case_labels]):
        ax.legend(loc='best')
    f_name = (y_label + '-box'
              + FMT['condition_sep'] + x_label
              + (FMT['interaction_sep'] + case_head if len(case_head) > 0 else ''))
    return FigureRef(ax, name=f_name)


def _plot_response_intervals(ax, c_lim):
    """plot horizontal lines to indicate response-category intervals
    :param ax: axis object
    :param c_lim: 1D array with scalar interval limits
    :return: None
    """
    (x_min, x_max) = ax.get_xlim()
    y = list(c_lim) + list(-c_lim)
    return ax.hlines(y, x_min, x_max,
                     linestyle='solid',
                     colors='k',
                     linewidth=0.2)


# ----------------------------------------- table displays:

def tab_percentiles(q_perc,
                    # cdf,  # ***************** prob < 0
                    perc,
                    case_labels,
                    case_order=None,
                    file_label=''
                    ):
    """Create pd.DataFrame with all percentile results.
    This function is general and can handle any dimensionality of the data.
    :param q_perc: 2D or mD array with quality percentiles, stored as
        q_perc[p, c0,...] = p-th percentile in (c0,...)-th case condition
        q_perc.shape[0] == len(perc)
    :param perc: list of percentage values in range 0-100
        len(perc) == q_perc.shape[0]
    :param cdf: min 1D array with cumulative distribution values at zero,
        cdf[c0,...,ci,...] = probability that quality <= 0 in (c0,...)-th case
        OR any other array indexing with same size and same element order
        cdf.size == number of rows as defined by case_list
    :param case_labels: (sequence OR ???) dict with elements (case_factor_i, case_labels_i), where
        case_factor_i is key string for i-th case dimension,
        case_labels_i is list of labels for i-th case dimension
        in the same order as the index order of q_perc, i.e.,
        len(case_labels_i) == q_perc.shape[i+1].
        Thus, q_perc[p, ...,c_i,...] = p-th percentile for case_labels_i[c_i], i = 0,...,
    :param case_order: (optional) sequence of case_label keys, one for each case column
        len(case_order) == len(case_list)
        Table columns are ordered as defined by case_order, if specified,
        otherwise columns are ordered as case_list.keys()
    :param file_label: (optional) string as first part of file name
    :return: a TableRef(pd.DataFrame) instance,
        with one column for each percentile,
        and one row for each combination product of case labels.
        Number of table rows == prod q_perc.shape[1:] == prod_i len(case_labels_i)
    """
    case_labels = dict(case_labels)  # if not already dict, *** require dict ? ******
    if case_order is None:
        case_order = [*case_labels.keys()]
    assert len(case_order) == len(case_labels), 'Incompatible len(case_order) != len(case_list)'
    assert all(c in case_labels for c in case_order), 'Some case_order not in case_list'
    case_shape = tuple(len(c_labels) for c_labels in case_labels.values())
    n_rows = np.prod(case_shape, dtype=int)
    # = number of table rows as defined by case_labels
    n_perc = len(perc)
    assert n_perc == q_perc.shape[0], 'Incompatible q_perc.shape[0] != n of percentiles'
    assert n_rows == np.prod(q_perc.shape[1:], dtype=int), 'Incompatible size of case_list and q_perc'
    assert case_shape == q_perc.shape[1:], 'Incompatible shape of q_perc and case_labels'
    # -------------------------------------------------------------------
    # transpose q_perc, cdf, case_labels to case_order key order:
    q_perc = np.moveaxis(q_perc, 0, -1)
    q_perc = q_perc.reshape((*case_shape, len(perc)))
    # cdf = cdf.reshape(case_shape)
    # q_perc[c_0, ..., c_i, ..., p] = p-th percentile in (c0,...,ci,...)-th case
    # cdf[c_0, ..., c_i, ...] = prob(quality <=0) in (c0,...,ci,...)-th case
    case_keys = [*case_labels.keys()]
    case_axes = tuple(case_keys.index(c) for c in case_order)
    q_perc = q_perc.transpose((*case_axes, -1))
    # cdf = cdf.transpose(case_axes)
    q_perc = q_perc.reshape((n_rows, len(perc)))
    # cdf = cdf.reshape((-1,))
    case_labels = {c: case_labels[c] for c in case_order}
    # --------------------------------------------------------------------
    df = pd.DataFrame({f'{p_i:.1f}%': q_i
                       for (p_i, q_i) in zip(perc,
                                             q_perc.T)},  # .reshape((n_perc, -1)))},
                      index=pd.MultiIndex.from_product([*case_labels.values()],
                                                       names=[*case_labels.keys()]))
    if len(file_label) > 0:
        file_label += FMT['condition_sep']  #_'
    f_name = file_label + FMT['interaction_sep'].join(case_labels.keys())
    return TableRef(df, name=f_name)


def tab_credible_diff(diff,
                      diff_labels,
                      diff_head,
                      cred_head,
                      case_labels=(),
                      case_head=(),
                      y_label='',
                      file_label='',
                      # high_low=('Higher', 'Lower'),
                      and_label='and',  # label in And column
                      and_head=('', '')
                      ):
    """Create table with credible differences among results
    :param diff: list of tuples ((i,j), p) OR ((i,j,c), p),
        defining jointly credible differences, indicating that
        prob{ quality of diff_labels[i] > quality of diff_labels[j]}, OR
        prob{ quality of diff_labels[i] > quality of diff_labels[j] | case_labels[c] }
        AND all previous pairs } == p
    :param diff_labels: list of tuples with labels of compared random-vector elements
        diff_labels[i] = (label_0,...)
        diff[...] == ((i,j, c), p) <=> diff_labels[i] > diff_labels[j] with prob p,
            at case_labels[c], if case_labels are defined.
        len(diff_labels) == max possible diff category index (i, j)
    :param diff_head: tuple of keys for heading of diff_labels column in table
        len(diff_head) == len(diff_labels[i]) for all i
    :param cred_head: string for header of Credibility column
    :param case_labels: (optional) list of tuples
        case_labels[c] == (case_label1, case_label2, ...), such that
        diff[...] == ((i,j, c), p) <=> diff[...] is valid given case_labels[c]
        len(case_labels) == max possible case index c in diff
    :param case_head: (optional) tuple of case keys, one for each case-dimension table column
        len(case_head) == len(case_labels[c]) for any c
    :param y_label: (optional) string with label of tabulated attribute
    :param file_label: (optional) string for first part of file name
    :param and_label: (optional) joining AND label in first column
    :param and_head: (optional) tuple with two strings for head first column
    :return: DiffTableRef object with header lines + one line for each credible difference
    """
    if len(diff) == 0:
        return None
    y_head_i = y_label + ' >'
    y_head_j = y_label
    # --------------------- table columns as dicts:
    col = {and_head:  [' '] + [and_label] * (len(diff) - 1)}  # first column with only AND flags
    # --------- column(s) for higher results
    diff_i = [diff_labels[d[0][0]]
              for d in diff]
    col |= {(y_head_i, d_head_k): [d_val[k] for d_val in diff_i]
            for (k, d_head_k) in enumerate(diff_head)}
    # --------- column(s) for lower results
    diff_j = [diff_labels[d[0][1]]
              for d in diff]
    col |= {(y_head_j, d_head_k): [d_val[k] for d_val in diff_j]
            for (k, d_head_k) in enumerate(diff_head)}  # cols for lesser results
    # --------- column(s) for optional case labels
    if len(case_head) > 0:
        diff_c = [case_labels[d[0][2]]
                  for d in diff]
        col |= {('', c_head_k): [c_val[k] for c_val in diff_c]
                for (k, c_head_k) in enumerate(case_head)}
    col |= {('', cred_head): [d[1] for d in diff]}
    df = pd.DataFrame(col)
    df = df.reindex(columns=pd.MultiIndex.from_tuples(df.columns))
    if len(file_label) > 0:
        file_label += FMT['condition_sep']
    f_name = file_label + FMT['interaction_sep'].join(diff_head) + '-diff'
    if len(case_head) > 0:
        f_name += FMT['condition_sep'] + FMT['interaction_sep'].join(case_head)
    return DiffTableRef(df, name=f_name)


def tab_credible_corr(c, a_labels,
                      file_label='Correlation',
                      and_head='',
                      and_label='and'):
    """create table of credible correlations
    :param c: list of tuple((i, j), p, md_corr), where
        (i, j) are indices into a_labels,
        p is joint credibility,
        md_corr = median conditional correlation value, given all previous
    :param a_labels: list with string labels for correlated attributes
    :param file_label: (optional) string for first part of file name
    :param and_head: (optional) string for head of first column
    :param and_label: (optional) joining AND label in first column
    :return: DiffTableRef object with header + one row for each credible correlation
    """
    if len(c) == 0:
        return None
    col = {and_head:  [' '] + [and_label] * (len(c) - 1)}  # first column with only AND flags
    col |= {FMT['attribute']: [a_labels[i] + ' * ' + a_labels[j]
                               for ((i, j), _, _) in c]}  # correlated Attributes
    col |= {FMT['correlation']: [mdc for (_, _, mdc) in c]}  # correlation values
    col |= {FMT['probability']: [p for (_, p, _) in c]}  # joint probability values
    df = pd.DataFrame(col)
    return DiffTableRef(df, name=file_label)


# -------------------------------------- private help functions
def _x_tick_style(labels):
    """Select xtick properties to avoid tick-label clutter
    :param labels: list of tick label strings
    :return: dict with keyword arguments for set_xticklabels
    """
    maxL = max(len(l) for l in labels)
    rotate_x_label = maxL * len(labels) > 75  # ad hoc criterion
    if rotate_x_label:
         style = dict(rotation=25, horizontalalignment='right')
    else:
        style = dict(rotation='horizontal', horizontalalignment='center')
    return style


