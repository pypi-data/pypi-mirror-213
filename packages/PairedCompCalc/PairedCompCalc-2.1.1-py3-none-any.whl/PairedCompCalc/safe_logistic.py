"""Numerically safer version of scipy.stats.logistic distribution.
May be replaced by future improved version of scipy.stats.logistic.

Arne Leijon, 2017-03-13
2019-04-28, fix method signature to agree with scipy.stats.rv_continuous, no real change
2021-09-24, fix _rvs signature again...

"""
import numpy as np
from scipy.stats import rv_continuous
from scipy.special import expit, logit


class logistic_gen(rv_continuous):
    """Safer version with central methods re-implemented.
    Method signatures copied from scipy.stats.logistic_gen
    """
    def _logpdf(self, x, *args):
        """logistic pdf(x) = exp(-x)/(1+exp(-x))**2
        Thus, logpdf(x) = -x - 2 * log((1+exp(-x))
        This is fine for large positive x, but pdf is symmetric,
        so we use abs(x) to avoid overflow for large negative x.
        :param x: array-like input values
        :param args: not used
        :return: lp = array of logpdf values
            lp.shape == x.shape
        """
        nax = -np.abs(x)
        return nax - 2. * np.log1p(np.exp(nax))

    def _logcdf(self, x, *args):
        """log logistic.cdf = -log(1 + exp(-x))
        = -x - log(1 + exp(x)), for x < 0.
        safer than scipy.stats.logistic.logcdf
        :param x: array-like input values
        :param args: not used
        :return: lp = array of logcdf values
            lp.shape == x.shape
        """
        x = np.asarray(x)
        ax = np.abs(x)
        lP = -np.log1p(np.exp(-ax))
        negx = x < 0
        lP[negx] -= ax[negx]
        return lP

    # ----------------------------------------------------
    # following private methods copied from scipy.stats.logistic_gen

    def _rvs(self, *args, size=None, random_state=None):
        return random_state.logistic(size=size)

    def _pdf(self, x, *args):
        return np.exp(self._logpdf(x))

    def _cdf(self, x, *args):
        return expit(x)

    def _ppf(self, q, *args):
        return logit(q)

    def _sf(self, x, *args):
        return expit(-x)

    def _isf(self, q, *args):
        return - logit(q)

    def _stats(self):
        return 0, np.pi * np.pi / 3.0, 0, 6.0 / 5.0

    def _entropy(self):
        # http://en.wikipedia.org/wiki/Logistic_distribution
        return 2.0
# ---------------------------------------------------------


logistic = logistic_gen(name='logistic')


# --------------------------------------------------------- TEST:
if __name__ == '__main__':
    from scipy.stats import logistic as sc_logistic

    x = np.array([0., 2., 1000., np.inf])

    print('x= ', x)
    print('\nImproved logistic version:')
    print('logistic.logpdf(x) = ', logistic.logpdf(x))
    print('logistic.logpdf(-x)= ', logistic.logpdf(-x))
    print('logistic.pdf(x) = ', logistic.pdf(x))
    print('logistic.pdf(-x)= ', logistic.pdf(-x))
    print('logistic.cdf(x) = ', logistic.cdf(x))
    print('logistic.cdf(-x)= ', logistic.cdf(-x))
    print('logistic.logcdf(x) = ', logistic.logcdf(x))
    print('logistic.logcdf(-x)= ', logistic.logcdf(-x))
    print('logistic.ppf(cdf(x)) = ', logistic.ppf(logistic.cdf(x)))
    print('logistic.ppf(cdf(-x))= ', logistic.ppf(logistic.cdf(-x)))

    print('logistic.pdf(x, loc=2.)', logistic.pdf(x, loc=2.))
    print('logistic.logcdf(x, scale=0.02)', logistic.logcdf(x, scale=0.02))

    print('logistic.rvs(size=10)', logistic.rvs(size=10))

    print('')
    print('scipy.stats version:')
    print('scipy.stats.logistic.logpdf(x) = ', sc_logistic.logpdf(x))
    print('scipy.stats.logistic.logpdf(-x)= ', sc_logistic.logpdf(-x))
    print('scipy.stats.logistic.logcdf(x) = ', sc_logistic.logcdf(x))
    print('scipy.stats.logistic.logcdf(-x)= ', sc_logistic.logcdf(-x))


