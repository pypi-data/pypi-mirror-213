"""Functions for approximate Sample Size Determination (SSD)
and crude preliminary estimation of the chance of achieving desired results
in a planned paired-comparison experiment.

The calculation uses many simulations of the planned experiment.
In this way, the effects of experimental methodological variants can be predicted.


*** Methods:

Assume that a paired-comparison experiment aims at evaluating a new "object" B
compared to a state-of-the-art "gold standard" reference A.
We would then consider the experimental outcome as a success,
if the result indicates that the mean (and median) quality of B in the population
is better than that of the reference object A.

As measures of the possible results of an experiment, we estimate
the probability of a "True Positive" vs a "False Positive" result.


* True Positive Result:

This measure of experimental success is estimated as

p_true_pos =(approx) E{ P( posterior mean_quality_of_B > 0 | true positive difference) },

conditional on the assumption that the true population quality means are
(m_A, m_B) = (0., m_diff), with m_diff > 0,
and
q_std = anticipated true inter-individual standard deviations
for independent individual quality values (q_A, q_B) for objects A and B,
in Thurstone d-prime scale units.
Thus, std(q_B - q_A) ==  q_std * sqrt(2) in the population.

The calculation is done for a particular experimental procedure
with a given number of replicated presentations of each pair,
and a given range of ordinal grades in subjects' responses,
with or without judgment ties, i.e., responses indicating "No Difference".

It should be noted that the "p_true_pos" is NOT precisely equivalent to a
conventional power estimate.

The conventional "Conditional Power" is the probability that a conventional
significance test will reject the Null hypothesis, given that the true population
parameter under study has a given desired, hypothetical, value.

A corresponding "Bayesian conditional power" measure was defined by Sambucini (2017), Eq. E7.
It would be possible to estimate this measure by simulating 100 or more
complete paired-comparison experiments, but this might take too long time.

Our estimated "p_true_pos" corresponds to the performance measure
proposed by Wang et al (2002), Section 3, Point 4, Eq (5).
Because of the computational effort, only a rather crude estimate is calculated.
The accuracy is limited by the number of simulated group experiments.


* False Positive Result:

It can happen that a paired-comparison experiment indicates a positive result for B
even if the true mean qualities for A and B are exactly equal in the population.
Under this Null hypothesis, the expected probability is, of course,
exactly 50% that the posterior estimate will show up as greater for B than for A.

Therefore, this module calculates

p_false_pos =(approx) E{ P{ posterior mean_quality_of_B > m_diff | NULL Hypothesis) }

This result should be small.

Thus, the performance measures (p_true_pos, p_false_pos) are symmetrically defined.
IFF the estimated posterior distributions of quality parameters
would be exactly equal, except for their different locations,
for both the NULL and ALTERNATE populations models,
we would get p_true_pos = 1. - p_false_pos.


* Sample Size Determination (SSD):

Main module functions for SSD:
ideal_n_subjects    --- assuming that subjective quality can be exactly measured,
estimate_n_subjects --- simulating a paired-comparison study to estimate subjective quality.

These functions estimate the number of test subjects needed
to obtain a desired experimental result, e.g.,
p_true_pos > 0.9 AND p_false_pos < 0.05,
conditional on anticipated values of the true mean difference m_diff = m_B - m_A
in the population, and a hypothetical inter-individual standard deviation
of all quality values.

The results can be helpful for the planning a paired-comparison experiment,
but they cannot give any guarantee that the desired result will actually be achieved.

It is recommended to also run a few complete simulations, using the script pc_sim.py,
to see some examples of the final analysis results that might be achieved
when based on data from the real experiment.


* Predicted Individual vs. Mean Results:

The main purpose of a planned paired-comparison experiment may be
to estimate predicted results not only for the population Mean (Median)
but also for a Random Individual in the population from which test participants are recruited.

Results for a Random Individual may be relevant, for example, to predict
the proportion of potential future customers in the population
that is likely to prefer the new product 'B'.

Therefore, the performance measures (p_true_pos, p_false_pos)
can also be calculated for a Random Individual in the population,
and not only for the population Mean (Median)
which is usually considered in conventional significance tests.

However, the estimated performance measures for a Random Individual
depend mainly on m_diff, q_std, and the number of pair replications,
and improve very little with increasing number of test participants.

It may be IMPOSSIBLE to reach a high value of p_true_pos for a Random Individual in the population,
even if the quality parameters could be measured exactly for each test participant.

If the inter-individual variations are large within the population,
the distribution of predicted results for an unseen random individual
are mainly determined by the inter-individual variance,
which remains the same, regardless of the number of test participants,
and regardless of the measurement accuracy of individual results.

In contrast, the performance results for the population Mean (and Median)
always improve with increasing number of test subjects.

Therefore, the functions ideal_n_subjects, estimate_n_subjects(...) in this module
estimate the required sample size only with regard to the population Mean.

Instead, the script run_sim.py may be used to predict the outcome of the planned experiment
for a Random Individual in the population.


* Crude Approximation:

It should be remembered that the calculated performance estimates are quite crude.
Better accuracy can be achieved only by increasing the parameter n_sim
in function calls, at a cost of longer computation time.

In any case, it is recommended to run the SSD calculation twice,
to indicate the spread of estimated results.


*** References:

F. Wang and A. E. Gelfand. A simulation-based approach to Bayesian sample size determination
for performance under a given model and for separating models.
Statistical Science, 17(2):193–208, 2002. doi: 10.1214/ss/1030550861

V. Sambucini. Bayesian vs frequentist power functions to determine the optimal sample size:
Testing one sample binomial proportion using exact methods.
In J. P. Tejedor, editor, Bayesian Inference. IntechOpen, 2017. doi: 10.5772/intechopen.70168


*** Usage Example: See script run_plan.py

*** Version History

* Version 2.0:
2021-09-15, functions adapted to revised version of pc_model, no essential change

* Version 1.0:
2018-08-08, first working version
2019-04-04, adapted to use new simulation module, simplified p_false_pos measure
2019-04-06, include SSD assuming ideal exact quality measurements
"""
import numpy as np
import logging

from scipy.stats import norm
from scipy.stats import t as student_t

from .pc_simulation import gen_dataset
from .pc_model import PairedCompResultSet

logger = logging.getLogger(__name__)


# ------------------------------------------------- main module functions:
def ideal_n_subjects(m_diff, q_std,
                     n_min=3,
                     n_max=50,
                     p_true_pos=0.9,
                     p_false_pos=0.05,
                     n_sim=1000):
    """Estimate required number of test participants,
    to achieve a desired probability of correct detection of a difference (hit),
    AND a desired maximal probability of false positive detection,
    assuming that individual quality values could be measured EXACTLY,
    i.e., without a subjective paired-comparison procedure.
    :param m_diff: scalar assumed mean quality difference in a population
    :param q_std: scalar assumed inter-individual standard deviations for both (q_A, q_B)
    :param n_min: (optional) minimal feasible number of test participants
    :param n_max: (optional) maximal feasible number of test participants
    :param p_true_pos: (optional) scalar desired performance of the experiment,
        i.e., min probability of correct detection of the true positive difference.
    :param p_false_pos: (optional) scalar max probability of false positive detection,
        given zero true difference.
    :param n_sim: (optional) number of averaged simulation results for each estimate.
    :return: scalar integer n = required number of test participants.

    Method:
    Given the anticipated true difference m_diff and inter-individual q_std,
    a large number of participant groups are drawn from the simulated population.
    For each simulated group, the posterior distribution of population mean is
    a Student-t distribution with parameters determined by
    the sample mean and variance for the group.
    The estimated (p_true_pos, p_false_pos) is calculated for each group result.

    These simulations are run with different simulated group sizes = n,
    using simple bisection method, until the desired performance is achieved.
    """
    # ---------------------------------------
    def p_fcn(n):
        """Calling interface to ideal criterion function
        :param n: tentative number of subjects
        :return: tuple (p1, p0) = (true positive, false positive), where
            p1 = a 1D array of n_sim relative frequencies of positive results, and
            p0 = a similar array of results for the NULL hypothesis.
        """
        (t_1, t_0) = _ideal_posterior_means(m_diff, q_std, n, n_sim)
        # = frozen Student-t distributions for population mean = mu,
        # given (Different, Null) hypotheses,
        # each with n_sim location and scale values
        p1 = np.mean(t_1.sf(0.))  # = p(mu > 0 | true difference = m_diff)
        p0 = np.mean(t_0.sf(m_diff))  # = p(mu > m_diff | true difference = 0)
        return p1, p0
    # ---------------------------------------
    return _solve_n_subjects(p_fcn, n_min, n_max, p_true_pos, p_false_pos)


def estimate_n_subjects(pcf, m_diff, q_std, n_pres,
                        n_min=3,
                        n_max=50,
                        p_true_pos=0.9,
                        p_false_pos=0.05,
                        n_sim=3):
    """Estimate required number of test participants,
    to achieve a desired probability of correct detection of a difference (hit),
    AND a desired maximal probability of false positive detection,
    using simulated paired-comparison experiments with given layout.
    :param pcf: single PairedCompFrame instance defining experimental layout
    :param m_diff: scalar assumed mean quality difference in a population
    :param q_std: scalar assumed inter-individual standard deviations for both (q_A, q_B)
    :param n_pres: number of paired-comparison presentations for each subject
    :param n_min: (optional) minimal feasible number of test participants
        NOTE: cannot be less than 3 for predictive population models
    :param n_max: (optional) maximal feasible number of test participants
    :param p_true_pos: (optional) scalar desired performance of the experiment,
        i.e., min probability of correct detection of the true positive difference.
    :param p_false_pos: (optional) scalar max probability of false positive detection,
        given zero true difference.
    :param n_sim: (optional) number of averaged simulation results for each estimate.
    :return: scalar integer n = required number of test participants.

    Method:
    Given the anticipated true difference m_diff and inter-individual q_std,
    a large number of participant groups are drawn from the simulated population,
    and a paired-comparison experiment is simulated for each group.
    For each simulated group experiment, the posterior distribution of population mean is
    estimated from the experiment results.
    The estimated (p_true_pos, p_false_pos) is then calculated for each group result.

    These simulations are run with different simulated group sizes = n,
    using simple bisection method, until the desired performance is achieved.

    The estimation may take a few minutes for each simulated experiment.
    """
    # ---------------------------------------
    def p_fcn(n):
        """Calling interface to criterion function
        :param n: tentative number of subjects
        :return: tuple (p1, p0) = (true positive, false positive)
        """
        (p1, p0) = np.mean([_cred_ab_mean(pcf, m_diff, q_std, n, n_pres, i, n_sim)
                            for i in range(n_sim)], axis=0)
        logger.info(f'Estimated p_true_pos = {p1:.1%}, p_false_pos = {p0:.1%} with {n} subjects')
        return p1, p0
    # ---------------------------------------
    return _solve_n_subjects(p_fcn, n_min, n_max, p_true_pos, p_false_pos)


def _solve_n_subjects(p_fcn, n_min, n_max, p_true_pos, p_false_pos):
    """Solve for minimal n that satisfies two criteria:
    p_fcn(n)[0) > p_true_pos AND p_fcn(n)[1] < p_false_pos
    :param p_fcn: criterion function, possibly with crude approximations
    :param n_min: (optional) minimal feasible number of test participants
        NOTE: cannot be less than 3 for predictive population models
    :param n_max: (optional) maximal feasible number of test participants
    :param p_true_pos: (optional) scalar desired performance of the experiment,
        i.e., min probability of correct detection of the true positive difference.
    :param p_false_pos: (optional) scalar max probability of false positive detection,
        given zero true difference.
    :return: scalar integer n_subj = smallest integer satisfying the two criteria

    Method: Simple bisection
    """
    (p1_max, p0_max) = p_fcn(n_max)
    # p_min = p_fcn(n_min)
    while p_true_pos < p1_max and p0_max < p_false_pos and n_max - n_min > 1:
        n_mid = (n_min + n_max) // 2  # bisection
        (p1_mid, p0_mid) = p_fcn(n_mid)
        if p1_mid < p_true_pos or p0_mid > p_false_pos:
            # keep upper interval limit
            n_min = n_mid
        else:
            # keep lower interval limit
            n_max = n_mid
            (p1_max, p0_max) = (p1_mid, p0_mid)
    return n_max


def power_ab_individual(pcf, m_diff, q_std, n_subjects, n_pres,
                        n_sim=10):
    """
    Calculate (prob_hit, prob_false_alarm) for given test conditions
    for an individual subject in the simulated population
    :param pcf: single PairedCompFrame instance to define experimental layout.
    :param m_diff: scalar assumed mean quality difference between two objects in a population
    :param q_std: scalar assumed inter-individual standard deviations for both (q_A, q_B)
    :param n_subjects: number of test participants
    :param n_pres: number of pair presentations for each participant
    :param cred_fcn: (optional) function variant to calculate power
    :param n_sim: (optional) number of simulations for each calculated credibility value

    :return: array [p_true_pos, p_false_alarm], where
        p_true_pos = probability of correct detection of the difference.
        p_false_alarm = probability of incorrect indication of a difference, when objects are equal
    """
    return np.mean([_cred_ab_individual(pcf, m_diff, q_std, n_subjects, n_pres,
                                        i, n_sim)
                    for i in range(n_sim)], axis=0)


def power_ab_mean(pcf, m_diff, q_std, n_subjects, n_pres,
                  n_sim=10):
    """
    Calculate (prob_hit, prob_false_alarm) for given test conditions
    for the mean quality difference in the simulated population
    :param pcf: single PairedCompFrame instance to define experimental layout.
    :param m_diff: scalar assumed mean quality difference between two objects in a population
    :param q_std: scalar assumed inter-individual standard deviations for both (q_A, q_B)
    :param n_subjects: number of test participants
    :param n_pres: number of pair presentations for each participant
    :param cred_fcn: (optional) function variant to calculate power
    :param n_sim: (optional) number of simulations for each calculated credibility value

    :return: array [p_true_pos, p_false_alarm], where
        p_true_pos = probability of correct detection of the difference.
        p_false_alarm = probability of incorrect indication of a difference, when objects are equal
    """
    return np.mean([_cred_ab_mean(pcf, m_diff, q_std, n_subjects, n_pres,
                                  i, n_sim)
                    for i in range(n_sim)], axis=0)


# --------------------------------------- Module help functions:

def _ideal_posterior_means(m_diff, q_std, n, n_sim=1000):
    """Posterior distributions of quality mean for object B,
    given Different hypothesis with E[quality (q_A, q_B] = [0., m_diff], and
    corresponding quality means = [0., 0.] for Null hypothesis.
    :param m_diff: difference in true quality means Different hypothesis
    :param q_std: true st.dev of q_A and q_B are q_std in both hypotheses
    :param n: number of subjects for estimation
    :param n_sim: number of simulated experiments
    :return: (t_diff, t_null) = frozen Student-t distribution objects
        t_diff for Different-object hypothesis, t_null for Null hypothesis

    Method:
    Assume values X = (x_1,..., x_n) are exactly measured for n subjects,
    and each x_i is drawn from i.i.d Gaussian-gamma with unknown mean mu and precision tau.
    The posterior estimate of the mean mu, with tau integrated out,
    then has a Student-t distribution with
    location = x_mean = sum(X) / n
    scale = sqrt( mean( (X - x_mean)**2) ) / n
    This is now done for n_sim randomly drawn groups, each with n subjects,
    for each of the two hypotheses.
    """
    # generate n_sim group samples of X with known mean and std, for both hypotheses:
    def sample_stat(m, s, n_sim, n):
        """Generate sufficient statistics for posterior mean
        :param m: true location for random Gaussian data
        :param s: true scale for random Gaussian data
        :param n_sim: number of sampled groups
        :param n: number of simulated subjects in each group
        :return: (loc, scale) of posterior Student distribution of the mean parameter
        """
        x = norm.rvs(loc=m, scale=s, size=(n_sim, n))
        x_mean = np.mean(x, axis=1, keepdims=True)
        x_var = np.mean((x - x_mean)**2, axis=1, keepdims=True)
        return x_mean, np.sqrt(x_var / n)
    # -------------------------------------------------------

    st_dev = q_std * np.sqrt(2)
    (m1, s1) = sample_stat(m_diff, st_dev, n_sim, n)
    (m0, s0) = sample_stat(0., st_dev, n_sim, n)
    t1 = student_t(loc=m1, scale=s1, df=n)
    t0 = student_t(loc=m0, scale=s0, df=n)
    return t1, t0  # frozen Student-t distributions, each with n_sim elements


def _cred_ab_individual(pcf, m_diff, q_std, n_subjects, n_pres,
                        it, n_it):
    """Calculate one pair of credibility results
    for the quality difference for a random INDIVIDUAL in the simulated population.
    :param pcf: single PairedCompFrame instance to define experimental layout.
    :param m_diff: scalar assumed mean quality difference between two objects in a population
    :param q_std: scalar assumed inter-individual standard deviations for both (q_A, q_B)
    :param n_subjects: number of test participants
    :param n_pres: number of pair presentations for each participant
    :param it: current iteration round
    :param n_it: total number of iteration rounds

    :return: tuple(p_true_pos, p_false_pos) where
        p_true_pos = prob[ q_B - q_A > 0 | given true diff = m_diff
        p_false_pos  = prob[ (q_B - q_A | true diff = 0) > (q_B - q_A | true diff = m_diff) ]
    """
    logger.info(f'Done {it} of {n_it} simulations with {n_subjects} subjects')
    pcm_d = _one_sim_ab(pcf, m_diff, q_std, n_subjects, n_pres)  # test group
    # = pc_model.PairedCompResultSet with ONE group, ONE attribute
    pcm_0 = _one_sim_ab(pcf, 0., q_std, n_subjects, n_pres)  # ref group with zero difference
    # = pc_model.PairedCompResultSet similarly, for NULL hypothesis
    pred_d = pcm_d.models[''][pcf.attributes[0]].pred_population_ind()
    # = predictive model for population Random Individual, given true difference = m_diff
    pred_0 = pcm_0.models[''][pcf.attributes[0]].pred_population_ind()
    # = predictive model for population Individual, given NULL hypothesis: true difference = 0
    q_d = pred_d.quality_samples[:, 0, 1]
    q_0 = pred_0.quality_samples[:, 0, 1]
    return ((0.5 + np.sum(q_d > 0.)) / (1 + len(q_d)),
            (0.5 + np.sum(q_0 > m_diff)) / (1 + len(q_0)))


def _cred_ab_mean(pcf, m_diff, q_std, n_subjects, n_pres,
                  it=0, n_it=0):
    """Calculate one pair of credibility results
    for the MEAN quality difference in the simulated population.
    :param pcf: single PairedCompFrame instance to define experimental layout.
    :param m_diff: scalar assumed mean quality difference between two objects in a population
    :param q_std: scalar assumed inter-individual standard deviations for both (q_A, q_B)
    :param n_subjects: number of test participants
    :param n_pres: number of pair presentations for each participant
    :param it: current iteration round
    :param n_it: total number of iteration rounds

    :return: tuple(p_true_pos, p_false_pos) where
        p_true_pos = prob[ q_B - q_A > 0 | given true diff = m_diff
        p_false_pos  = prob[ (q_B - q_A | true diff = 0) > (q_B - q_A | true diff = m_diff) ]
    """
    if n_it > 0:
        logger.info(f'Done {it} of {n_it} simulations with {n_subjects} subjects')
    pcm_d = _one_sim_ab(pcf, m_diff, q_std, n_subjects, n_pres)  # test group
    # = pc_model.PairedCompResultSet with ONE group, ONE attribute
    pcm_0 = _one_sim_ab(pcf, 0., q_std, n_subjects, n_pres)  # ref group with zero difference
    # = pc_model.PairedCompResultSet similarly, for NULL hypothesis
    pred_d = pcm_d.models[''][pcf.attributes[0]].pred_population_mean()
    # = predictive model for population Mean, given true difference = m_diff
    pred_0 = pcm_0.models[''][pcf.attributes[0]].pred_population_mean()
    # = predictive model for population Mean, given NULL hypothesis: true difference = 0
    q_d = pred_d.quality_samples[:, 0, 1]  # samples of q_B
    q_0 = pred_0.quality_samples[:, 0, 1]
    return ((0.5 + np.sum(q_d > 0.)) / (1 + len(q_d)),
            (0.5 + np.sum(q_0 > m_diff)) / (1 + len(q_0)))


def _one_sim_ab(pcf, m_diff, q_std, n_subjects, n_pres):
    """Simulate ONE subject group with given properties for ONE attribute
    :param pcf: single PairedCompFrame instance to define experimental layout.
    :param m_diff: scalar assumed mean quality difference between two objects in a population
    :param q_std: scalar assumed inter-individual standard deviations for both (q_A, q_B)
    :param n_subjects: number of test participants
    :param n_pres: number of pair presentations for each participant
    :return: one learned PairedCompResultSet
    """
    ds = gen_dataset(pcf,
                     n_subjects=n_subjects,
                     quality_mean=[0., m_diff],
                     quality_std=q_std,
                     n_replications=n_pres // 2,
                     log_response_width_std=0.,  # fixed default response intervals
                     lapse_prob_range=(0., 0.))  # no lapses
    return PairedCompResultSet.learn(ds)
