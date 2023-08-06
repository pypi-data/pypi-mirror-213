from sklearn.mixture import GaussianMixture
import numpy as np


class WeightedGaussianMixture(GaussianMixture):
    """
    Extends sklearn.mixture.GaussianMixture to support weighted data set.
    Its methods and attributes are identical to the parent's, except for
    the fit() method.

    Parameters
    ----------
        See sklearn.mixture.GaussianMixture
    """

    def __init__(self, n_components=1, covariance_type='full', tol=1e-3,
                 reg_covar=1e-6, max_iter=100, n_init=1, init_params='kmeans',
                 weights_init=None, means_init=None, precisions_init=None,
                 random_state=None, warm_start=False,
                 verbose=0, verbose_interval=10):
        super(WeightedGaussianMixture, self).__init__(
            n_components=n_components, covariance_type=covariance_type, tol=tol,
            reg_covar=reg_covar, max_iter=max_iter, n_init=n_init, init_params=init_params,
            weights_init=weights_init, means_init=means_init, precisions_init=precisions_init,
            random_state=random_state, warm_start=warm_start, verbose=verbose,
            verbose_interval=verbose_interval)

    def _initialize(self, X, resp):
        self.weight_mat = self.weights.repeat(self.n_components).reshape(X.shape[0], self.n_components)
        self.log_weight_mat = np.log(self.weight_mat)
        resp_w = resp * self.weight_mat
        super(WeightedGaussianMixture, self)._initialize(X, resp_w)

    def fit(self, X, weights=None, y=None):
        if weights is None:
            weights = np.ones(X.shape[0])
        if X.shape[0] != weights.shape[0]:
            raise ValueError("The number of weights must match the number of data points.")
        self.weights = weights
        super(WeightedGaussianMixture, self).fit(X, y)

    def _e_step(self, X):
        log_prob_norm, log_responsibility = super(WeightedGaussianMixture, self)._e_step(X)
        return log_prob_norm, log_responsibility + self.log_weight_mat
