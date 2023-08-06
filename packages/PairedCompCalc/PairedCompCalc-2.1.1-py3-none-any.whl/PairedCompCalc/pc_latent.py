"""Help classes for distribution of latent sensory variable

*** Version history:
* Version 2.1.1:
2023-06-14, New module, with methods copied from EmaCalc.
            Defining classes Bradley, Thurstone, moved from pc_model.py.
"""
import numpy as np
from scipy.special import expit, log_expit, log_ndtr
import logging

logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)  # *** TEST


# ------------------------------------------------------------------
class Bradley:
    """Distribution of latent decision variable = standard logistic
    cdf(x) = 1 / (1 + exp(-x)) = expit(x)
    Implementing the Bradley-Terry-Luce model of paired comparisons.
    """
    unit_label = 'BTL unit'
    # for axis label in quality plots
    scale = np.pi / np.sqrt(3.)
    # = st.dev. of standard logistic distribution
    # may be used to standardize result scale in displays

    @staticmethod
    def log_cdf_diff(a, b):
        """log prob( a < Z <= b)
        where Z is a standard logistic random variable
        :param a: = array with LOWER interval limits
        :param b: = arrays with UPPER interval limits
            a.shape == b.shape
            all( -inf <= a < b <= +inf)
        :return: log_p = array with log probabilities, element-wise
            log_p.shape == a.shape == b.shape
        """
        # p = expit(b) - expit(a)
        # *** may be inaccurately == 0. if 36.7. < a < b in double prec.
        # *** problem when b = inf and a > 36.7  -> d == 0.
        # *** No problem with b = -100. and a = -inf

        d = b - a
        zero_d = d == 0.
        if np.any(zero_d):  # *** precaution to detect numerical underflow
            logger.warning(f'Bradley.log_cdf_diff: {np.sum(zero_d)} non-positive interval width. '
                           + 'Should never happen! Contact the author.')
            logger.warning(f'a =\n' + np.array_str(a[zero_d]))
            logger.warning(f'b =\n' + np.array_str(b[zero_d]))
            logger.warning(f'd = b-a =\n' + np.array_str(d[zero_d]))
            d[zero_d] = np.finfo(float).tiny  # to avoid expm1(0.) -> 1 / 0.
        # *** Safe method for -inf < b <= +inf;  -inf <= a < +inf; 0 < d == b-a <= +inf:
        # log(expit(b) - expit(a)) = log_expit(b) + log_expit(-a) + log[1. - exp(-(b-a))]
        lp = log_expit(b) + log_expit(-a)
        log_1mexp = np.log1p(-np.exp(-d))
        # but log[1. - exp(-(b-a))] may still get truncated -> 0. for very small d = b-a
        small_d = d < 0.001
        log_1mexp[small_d] = np.log(np.expm1(d[small_d])) - d[small_d]
        lp += log_1mexp
        return lp

    @staticmethod
    def d_log_cdf_diff(a, b):
        """Element-wise partial derivatives of log_cdf_diff(a, b)
        :param a: = array with LOWER interval limits
        :param b: = arrays with UPPER interval limits
            a.shape == b.shape
            all( a < b )
        :return: tuple (dll_da, dll_db) of arrays, where
            dll_da[...] = d log_cdf_diff(a[...], b[...]) / d a[...]
            dll_db[...] = d log_cdf_diff(a[...], b[...]) / d b[...]
            dll_da.shape == dll_db.shape == a.shape == b.shape
        2023-06-08, tested by finite-diff comparison
        """
        d = b - a
        zero_d = d == 0.
        if np.any(zero_d):  # *** precaution to detect numerical underflow
            logger.warning(f'Bradley.log_cdf_diff: {np.sum(zero_d)} non-positive interval width. '
                           + 'Should never happen! Contact the author.')
            d[zero_d] = np.finfo(float).tiny  # to avoid expm1(0.) -> 0.
            # No problem if this tiny logprob multiplied by zero count later
        # log_cdf_diff(a,b) = log_expit(b) + log_expit(-a) + log[1. - exp(-(b-a))]
        # d log_expit(-a) / d a = - expit(a)
        # d log_expit(b) / d b = expit(-b)
        # d log[1. - exp(-(b - a))] / d a = - 1. / expm1(d)
        # d log[1. - exp(-(b - a))] / d b =   1. / expm1(d)
        d_log_1mexp = 1. / np.expm1(d)
        return - expit(a) - d_log_1mexp, expit(-b) + d_log_1mexp


_log_sqrt_2pi = np.log(2 * np.pi) / 2
# = module constant


class Thurstone:
    """Distribution of decision variable = Gaussian with variance = 2,
    i.e., Thurstone Case V.
    Variance = 2, because the latent decision variable is the difference
    between two standard normal variables.
    """
    unit_label = 'd-prime unit'
    scale = np.sqrt(2.)
    log_scale = np.log(scale)

    @classmethod
    def _log_pdf(cls, x):
        """log pdf of standard normal distribution
        :param x: scalar or array
        :return: lp = log pdf(x)
            lp.shape == x.shape
        """
        return - (x / cls.scale)**2 / 2 - _log_sqrt_2pi - cls.log_scale

    @classmethod
    def log_cdf_diff(cls, a, b):
        """log[ P( a < Z <= b) ], where Z is a Gaussian standard random variable.
        Numerically stable, avoiding numerical under- or over-flow for -inf <= a < b <= +inf.
        OK also for very small interval width (b - a).
        :param a: = array with LOWER interval limits
        :param b: = array with UPPER interval limits
            a.shape == b.shape
            all( a < b )
        :return: log_p = log(ndtr(b) - ndtr(a)) = log(ndtr(-a) - ndtr(-b))
            log_p.shape == a.shape == b.shape
        """
        a = a / cls.scale
        b = b / cls.scale
        low = np.minimum(a, -b)
        high = np.minimum(b, -a)
        # interval (low, high) = either (a, b) or (-b, -a)
        # same in theory, but lower variant is numerically more accurate
        ln_ndtr_low = log_ndtr(low)
        ln_ndtr_high= log_ndtr(high)
        zero_d = ln_ndtr_low >= ln_ndtr_high
        if np.any(zero_d):  # *** precaution to detect numerical underflow
            logger.warning(f'Thurstone.log_cdf_diff: {np.sum(zero_d)} non-positive probabilities. '
                           + 'Should never happen! Contact the author.')
            logger.warning(f'a =\n' + np.array_str(a[zero_d]))
            logger.warning(f'b =\n' + np.array_str(b[zero_d]))
            logger.warning(f'd = b-a =\n' + np.array_str((b-a)[zero_d]))
        return ln_ndtr_high + np.log1p(-np.exp(ln_ndtr_low - ln_ndtr_high))

    @classmethod
    def d_log_cdf_diff(cls, a, b):
        """Element-wise partial derivatives of log_cdf_diff(a, b)
        :param a: = array with LOWER interval limits
        :param b: = arrays with UPPER interval limits
            a.shape == b.shape
            all( a < b )
        :return: tuple (dll_da, dll_db), where
            dll_da[...] = d log_cdf_diff[a[...], b[...]) / d a[...]
            dll_db[...] = d log_cdf_diff[a[...], b[...]) / d b[...]
            dll_da.shape == dll_db.shape == a.shape == b.shape
        Arne Leijon, 2023-06-10, tested by finite-diff comparison
        """
        # cdf_diff(a, b) = ndtr(b) - ndtr(a)
        # d log(cdf_diff) / d a = - pdf(a) / cdf_diff(a, b)
        # d log(cdf_diff) / d b =   pdf(b) / cdf_diff(a, b),
        # where pdf(x) = pdf of standard normal (Gaussian)
        ln_cdf_diff = cls.log_cdf_diff(a, b)
        return (- np.exp(cls._log_pdf(a) - ln_cdf_diff),
                  np.exp(cls._log_pdf(b) - ln_cdf_diff))


# ------------------------------------------------- TEST:
if __name__ == '__main__':
    from scipy.optimize import approx_fprime, check_grad

    print('*** Simple test of Thurstone ***')  # same as old version pc_model
    a = np.array([2.])
    # b = np.array([np.inf])
    b = np.array([3.])

    print('Thurstone log_cdf_diff = ', Thurstone.log_cdf_diff(a, b))
    (da, db) = Thurstone.d_log_cdf_diff(a, b)
    print('dll_da =', da)
    print('dll_db =', db)
    eps = 1e-6
    print('approx dll_da: ', (Thurstone.log_cdf_diff(a+eps/2, b) -
                              Thurstone.log_cdf_diff(a-eps/2, b)) / eps)
    print('approx dll_db: ', (Thurstone.log_cdf_diff(a, b+eps/2) -
                              Thurstone.log_cdf_diff(a, b-eps/2)) / eps)
    # -------------------------------------- OK

    print('\n*** Testing Bradley and Thurstone derivatives')

    # --------------------------------------------------
    for cls in (Bradley, Thurstone):

        print(f'\nTesting {cls}.d_log_cdf_diff() with 1D (a, b) args')
        tau = np.array([-np.inf, 0., 1e-5, np.inf])  # 1.e-7 also OK with Bradley
        # tau = np.array([-50.1, -50.])
        # tau = np.array([50., 50.1])
        th = -0.  # 5000, -5000 also OK
        (a, b) = (tau[:-1] - th, tau[1:] - th)

        print(f'cls.log_cdf_diff({a}, {b}) = \n', cls.log_cdf_diff(a, b))

        for i in range(len(a)):
            ind = [i]
            def fun_a(a):
                return cls.log_cdf_diff(a, b[ind])

            def jac_a(a):
                return cls.d_log_cdf_diff(a, b[ind])[0]


            def fun_b(b):
                return cls.log_cdf_diff(a[ind], b)

            def jac_b(b):
                return cls.d_log_cdf_diff(a[ind], b)[1]

            print('')
            print(f'approx d_log_cdf_diff_da[{ind}] = ', approx_fprime(a[ind], fun_a, epsilon=1e-8))
            print(f'exact  d_log_cdf_diff_da[{ind}] = ', jac_a(a[ind]))
            err = check_grad(fun_a, jac_a, a[ind], epsilon=1e-8)
            print('check_grad err = ', err)

            print(f'approx d_log_cdf_diff_db[{ind}] = ', approx_fprime(b[ind], fun_b, epsilon=1e-8))
            print(f'exact  d_log_cdf_diff_db[{ind}] = ', jac_b(b[ind]))
            err = check_grad(fun_b, jac_b, b[ind], epsilon=1e-8)
            print('check_grad err = ', err)
