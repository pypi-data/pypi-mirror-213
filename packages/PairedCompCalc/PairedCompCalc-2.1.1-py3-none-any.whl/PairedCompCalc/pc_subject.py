"""This module defines classes and functions for
individual participants in a paired-comparison experiment.

*** Main Classes:

PairedCompIndModel: probability distribution of quality parameters for
    two or more sound-presentation objects, as judged by
    ONE SUBJECT, for ONE perceptual attribute, in ALL selected test conditions.
    Models may be joined later to include data from several subjects,
    thus representing a single mixture distribution for all individuals in a group.

*** Version History:
** Version 2.0.1:
2022-03-12, subject sample entropy calculation -> PairedCompIndModel.adapt()
2022-03-10, this module created separate from pc_model, for easier reading
"""
# *** save IndividualModel sampler as property to preserve state between VI steps ?

import numpy as np
from scipy.optimize import minimize
from scipy.special import logit

import logging

from samppy import hamiltonian_sampler as ham
from samppy.sample_entropy import entropy_nn_approx as entropy

N_SAMPLES = 1000  # number of samples for each subject model

logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)  # test


# -------------------------------------------------------------------
class PairedCompIndModel:
    """A PairedCompIndModel instance represents a probabilistic model of
    psycho-acoustic paired-comparison evaluations
    of ONE perceptual attribute by ONE listener,
    for a set of N different presentation OBJECTS.

    Each instance represents the posterior distribution of parameters
    in a Thurstone Case V model OR a Bradley-Terry-Luce model,
    adapted to the paired-comparison responses from ONE listener.
    """
    def __init__(self, pcf, x_samples, x_map, rv_class):
        """
        :param pcf: reference to a PairedCompFrame instance,
            common for all model instances.
        :param x_samples: 2D array of equally probable sample vectors with parameters
        :param x_map: 2D array with a single row with max-a-posteriori probable parameter vector
            parameter vectors include both quality and response-interval width parameters.
        :param rv_class: probability-distribution class for the model latent variable, with METHODS
            rv_class.log_cdf_diff, d_log_cdf_diff
            rv_class is Gaussian for the Thurstone Case V model type, and
            logistic for the Bradley-Terry-Luce model type

        NOTE: quality parameters are self.x_samples[:, :self.n_q]
        response-category intervals are defined by a transform function, as
        (b_low, b_high) = cat_limits(self.x_samples[:, self.n_q:] )
        """
        self.pcf = pcf
        self.x_samples = x_samples
        self.x_map = x_map
        self.rv_class = rv_class

    def __repr__(self):
        return (self.__class__.__name__ + '(' +
                '\n\tpcc=pcf,' +
                '\n\tx_samples=x_samples,' +
                '\n\tx_map=x_map,' +
                f'\n\trv_class={repr(self.rv_class)})')

    @property
    def n_q(self):
        """number of quality parameters in self.x_samples and self.x_map
        """
        return self.pcf.n_quality_params

    @property
    def quality_samples(self):
        """extract quality parameters from self.x_samples
        Returns: 3D array q, with quality samples stored as
            q[n, t, s] = n-th sample of quality estimated for
            pcf.test_conditions()[t], pcf.objects[s]
        """
        q = self.x_samples[:, :self.n_q].reshape((-1,
                                                  self.pcf.n_test_conditions,
                                                  self.pcf.n_objects - 1))
        zero_shape = (*q.shape[:-1], 1)
        # include fixed q == 0. for self.objects[0]
        return np.concatenate((np.zeros(zero_shape), q), axis=-1)

    @property
    def quality_map(self):
        """extract MAP estimate(s) of quality parameters
        :return: 3D array q, with quality samples stored as
            q[n, t, s] = map quality estimated for n-th subject in
            pcf.test_conditions()[t], pcf.objects[s]
        """
        q = self.x_map[..., :self.n_q].reshape((-1,
                                                self.pcf.n_test_conditions,
                                                self.pcf.n_objects - 1))
        zero_shape = (*q.shape[:-1], 1)
        return np.concatenate((np.zeros(zero_shape), q), axis=-1)

    @property
    def cat_limit_samples(self):
        """extract UPPER response-interval boundaries from self.x_samples
        """
        return cat_limits_transform(self.x_samples[:, self.n_q:])

    def adapt(self, md, prior):
        """
        Adapt self to given paired-comparison data, also considering the prior,
        representing the current estimate of the distribution in the population.
        :param md: a PairedCompMdata instance, with paired-comparison data for
            one subject, one attribute, in all test conditions.
        :param prior: a single GaussianRV instance, same for all subjects.
        :return: scalar LL = current log-likelihood of observed data
                + sample-estimated entropy of parameters
            = E_q{ ln p(md | self.x_samples) }
                + E_q{ ln p(x_samples | prior) }
                - E_q( ln q(self.x_samples),
            where q() is the current distribution of model parameters,
            represented by self.x_samples with equally probable sample vectors,
            so E{ f(X) } is calculated as mean( f(x_samples) ) for any f().

        Arne Leijon, 2018-04-20, no re-scaling of parameter data,
            for correct prior adaptation and correct LL calculation
        """
        # --------------------------------------------
        def neg_ll(x):
            return - prior.mean_logpdf(x) - md.log_likelihood(x, self.rv_class)

        def grad_neg_ll(x):
            return - prior.grad_mean_logpdf(x) - md.grad_log_likelihood(x, self.rv_class)
        # --------------------------------------------
        # find MAP point first:
        # n_s = self.pcf.n_objects
        # n_tct = self.pcf.n_test_conditions
        n_cw = self.pcf.n_difference_grades
        n_q = self.n_q
        n_param = n_q + n_cw
        # ------------------------------------------------- TEST grad_neg_ll
        # from scipy.optimize import approx_fprime, check_grad
        # x0 = np.zeros(n_param)
        # print(f'neg_ll({x0}) = {neg_ll(x0)}')
        # x0_plus = x0 + [0., 0., 1.,1.,1.]
        # print(f'neg_ll({x0_plus}) = {neg_ll(x0_plus)}')
        # print('approx prior.grad_mean_logpdf = ', approx_fprime(x0, prior.mean_logpdf, epsilon=1e-6))
        # print('exact  prior.grad_mean_logpdf = ', prior.grad_mean_logpdf(x0))
        #
        # def fun(x):
        #     return md.log_likelihood(x, self.rv_class)
        #
        # def jac(x):
        #     return md.grad_log_likelihood(x, self.rv_class)
        #
        # print('approx md.grad_log_likelihood = ', approx_fprime(x0, fun, epsilon=1e-6))
        # print('exact  md.grad_log_likelihood = ', jac(x0))
        # print('approx grad_neg_ll = ', approx_fprime(x0, neg_ll, epsilon=1e-6))
        # print('exact  grad_neg_ll = ', grad_neg_ll(x0))
        # err = check_grad(neg_ll, grad_neg_ll, x0, epsilon=1e-6)
        # print('check_grad err = ', err)
        # -------------------------------------------- OK 2018-07-09
        res = minimize(fun=neg_ll,
                       jac=grad_neg_ll,
                       x0=np.zeros(n_param))
        # **** use Hessian to set sampler.epsilon ???
        if res.success:
            x_map = res.x.reshape((1, -1))
        else:
            print('minimize res:', res)
            raise RuntimeError('MAP search did not converge')

        if len(self.x_samples) != N_SAMPLES:
            # run sampler starting from x_map
            x0 = x_map
        else:
            # we have sampled before, start from those samples
            x0 = self.x_samples + x_map - self.x_map
        # ********* OR keep sampler as self attribute ???
        sampler = ham.HamiltonianSampler(x=x0,
                                         fun=neg_ll,
                                         jac=grad_neg_ll,
                                         epsilon=0.1
                                         )
        sampler.safe_sample(n_samples=N_SAMPLES, min_steps=2)
        logger.debug(f'sampler accept_rate = {sampler.accept_rate:.1%}, ' +
                     f'n_steps = {sampler.n_steps:.0f}, ' +
                     f'epsilon = {sampler.epsilon:.2f}')
        self.x_samples = sampler.x
        self.x_map = x_map
        h_xi = entropy(self.x_samples)
        # approx = E{ - ln q_n(x_samples[n]) }, with E{} = mean across samples
        return - np.mean(sampler.U) + h_xi


# --------------------------------------------------- general module helper stuff

def cat_limits_transform(log_w):  # *** -> separate module?  ***************
    """Transform given log-category-width parameters to response-category interval limits.
    :param log_w: 1D or 2D array with
        log_w[..., m] = ...-th sample of log non-normalized width of m-th interval.
        (called eta_{nm} in JASA paper)
        (OR log_w[m] = m-th element of single vector)
        log_w.shape[-1] == M == number of response-scale intervals.

    :return: 1D or 2D array b, with all elements in (0, +inf]
        b[..., m] = UPPER limit for m-th interval,
            = LOWER limit for the (m+1)-th interval,
        b.shape == log_w.shape

    NOTE: lower limit for the first interval is NOT included
        lower limit for first interval == 0. if forced_choice,
        lower limit for first interval == - upper limit, if not forced_choice
        upper limit for highest interval always == + inf

    Method:
        Normalized widths and interval limits are defined in transformed domain (0, 1.),
        using a symmetric logistic mapping function,
        y = 2 * expit(b) - 1, where b in (0, inf]; y in (0, 1]
            y_{:, m} =  (w_0 +...+ w_m) / (w_0 + ... + w_{M-1};  0 <= m <= M-1
            w_m = exp(log_w[..., m])
        Thus, cat_limits b are calculated with the inverse transform
        b = logit( (1+y)/2 )
        which gives b[..., M-1] == + inf, where y == 1.
    """
    # w = np.exp(CAT_WIDTH_SCALE * log_w)
    # w = np.exp(log_w)
    # = non-normalized width of transformed intervals, always > 0
    cum_w = np.cumsum(np.exp(log_w), axis=-1)
    # sum_w = cum_w[..., -1:]
    # ************************* check timing for errstate *****************
    # alt 1:
    #  with np.errstate(divide='ignore'):  # allow b[..., -1] = inf without warning
    #     b = np.log((sum_w + cum_w) / (sum_w - cum_w))

    # alt 2:
    # b = np.log((sum_w + cum_w) / (sum_w - cum_w))

    # alt 4: **** simplest and probably fastest
    b = logit((1. + cum_w / cum_w[..., -1:]) / 2)
    return b


def d_cat_limits_transform(log_w):
    """gradient of cat_limits with respect to log_w
    :param log_w: 1D or 2D array with
        log_w[..., m] = log non-normalized width of m-th interval,
        log_w.shape[-1] = M = number of response intervals

    :return: 2D or 3D array db_dlogw, with
    db_dlogw[..., m, i] = db[..., m] / d log_w[..., i]; m = 0,..., M-2; i = 0, ..., M-1
        where b[..., m] = UPPER limit of m-th response interval
    db_dlogw.shape[-2:] == (M-1, M)

    Arne Leijon, 2017-12-07, checked with scipy check_grad
    2018-08-04, simplified code, checked
    """
    # w = np.exp(CAT_WIDTH_SCALE * log_w)
    w = np.exp(log_w)
    len_w = w.shape[-1]
    cum_w = np.cumsum(w, axis=-1)
    cw = cum_w[..., :-1, np.newaxis]
    sw = cum_w[..., -1:, np.newaxis]
    # b = logit((1+y)/2) = log(sw+cw) - log(sw-cw) = b1 - b2, where
    # cw[..., m] (w_0 +...+ w_m); m = 0, ..., len_2-2
    # sw[...] = (w_0 +...+ w_{len_w-1})
    # dcw_dw[..., m, i] = dcw[..., m] /dw[..., i]  = [1. if i <= m else 0.
    # dsw[...] / dw[..., i] = 1, all i
    dcw_dw = np.tril(np.ones((len_w-1, len_w)))
    db_dw = (1. + dcw_dw) / (sw + cw) - (1. - dcw_dw) / (sw - cw)
    return db_dw * w[..., np.newaxis, :]  # = db_dlogw


# --------------------------------------------------------------- TEST:
if __name__ == '__main__':

    print('*** test d_cat_limit_transform')
    from scipy.optimize import approx_fprime, check_grad

    x0 = np.zeros(3)
    # x0 = np.array([1.,2., -3.])
    # x0 = np.array([-0.1, -0.25, +0.28])

    def fun(x):
        return cat_limits_transform(x)[1]

    def jac(x):
        return d_cat_limits_transform(x)[1]

    eps = 1.e-6
    print(f'cat_limits_transform{x0} = {cat_limits_transform(x0)}')
    print(f'cat_limits_transform(x0+eps) = {cat_limits_transform(x0+eps)} Should remain the same')

    print('approx gradient = ', approx_fprime(x0, fun, epsilon=1e-6))
    print('exact  gradient = ', jac(x0))
    err = check_grad(fun, jac, x0, epsilon=1e-6)
    print('check_grad err = ', err)
    # ------------------------------------- OK
