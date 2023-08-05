import warnings
from abc import ABCMeta, abstractmethod

import numpy as np
from scipy.linalg import pinv2
from sklearn.base import (
    TransformerMixin,
    RegressorMixin,
    MultiOutputMixin,
    BaseEstimator,
)
from sklearn.cross_decomposition._pls import (
    _center_scale_xy,
    _get_first_singular_vectors_power_method,
    _svd_flip_1d,
    _get_first_singular_vectors_svd,
    PLSRegression,
)
from sklearn.utils import check_consistent_length, check_array
from sklearn.utils.validation import check_is_fitted

from skbel.utils import FLOAT_DTYPES

from scipy.spatial.distance import pdist, squareform


class KCCA(
    TransformerMixin, RegressorMixin, MultiOutputMixin, BaseEstimator, metaclass=ABCMeta
):
    """Partial Least Squares (PLS)

    This class implements the generic PLS algorithm.

    Main ref: Wegelin, a survey of Partial Least Squares (PLS) methods,
    with emphasis on the two-block case
    https://www.stat.washington.edu/research/reports/2000/tr371.pdf
    """

    @abstractmethod
    def __init__(
        self,
        n_components=2,
        *,
        scale=True,
        deflation_mode="regression",
        mode="A",
        algorithm="nipals",
        max_iter=500,
        tol=1e-06,
        copy=True,
    ):
        self.n_components = n_components
        self.deflation_mode = deflation_mode
        self.mode = mode
        self.scale = scale
        self.algorithm = algorithm
        self.max_iter = max_iter
        self.tol = tol
        self.copy = copy

    def fit(self, X, Y):
        """Fit model to data.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training vectors, where `n_samples` is the number of samples and
            `n_features` is the number of predictors.

        Y : array-like of shape (n_samples,) or (n_samples, n_targets)
            Target vectors, where `n_samples` is the number of samples and
            `n_targets` is the number of response variables.
        """

        check_consistent_length(X, Y)
        X = self._validate_data(
            X, dtype=np.float64, copy=self.copy, ensure_min_samples=2
        )
        Y = check_array(Y, dtype=np.float64, copy=self.copy, ensure_2d=False)
        if Y.ndim == 1:
            Y = Y.reshape(-1, 1)

        n = X.shape[0]
        p = X.shape[1]
        q = Y.shape[1]

        n_components = self.n_components
        if self.deflation_mode == "regression":
            # With PLSRegression n_components is bounded by the rank of (X.T X)
            # see Wegelin page 25
            rank_upper_bound = p
            if not 1 <= n_components <= rank_upper_bound:
                # TODO: raise an error in 1.1
                warnings.warn(
                    f"As of version 0.24, n_components({n_components}) should "
                    f"be in [1, n_features]."
                    f"n_components={rank_upper_bound} will be used instead. "
                    f"In version 1.1 (renaming of 0.26), an error will be "
                    f"raised.",
                    FutureWarning,
                )
                n_components = rank_upper_bound
        else:
            # With CCA and PLSCanonical, n_components is bounded by the rank of
            # X and the rank of Y: see Wegelin page 12
            rank_upper_bound = min(n, p, q)
            if not 1 <= self.n_components <= rank_upper_bound:
                # TODO: raise an error in 1.1
                warnings.warn(
                    f"As of version 0.24, n_components({n_components}) should "
                    f"be in [1, min(n_features, n_samples, n_targets)] = "
                    f"[1, {rank_upper_bound}]. "
                    f"n_components={rank_upper_bound} will be used instead. "
                    f"In version 1.1 (renaming of 0.26), an error will be "
                    f"raised.",
                    FutureWarning,
                )
                n_components = rank_upper_bound

        if self.algorithm not in ("svd", "nipals"):
            raise ValueError(
                "algorithm should be 'svd' or 'nipals', got " f"{self.algorithm}."
            )

        self._norm_y_weights = self.deflation_mode == "canonical"  # 1.1
        norm_y_weights = self._norm_y_weights

        # Kernelization

        gausigma = 1
        pairwise_dists = squareform(pdist(X, Y, "euclidean"))
        kernel = np.exp((-(pairwise_dists ** 2)) / (2 * gausigma ** 2))
        kernel = (kernel + kernel.T) / 2.0

        # Scale (in place)
        Xk, Yk, self._x_mean, self._y_mean, self._x_std, self._y_std = _center_scale_xy(
            X, Y, self.scale
        )

        self.x_weights_ = np.zeros((p, n_components))  # U
        self.y_weights_ = np.zeros((q, n_components))  # V
        self._x_scores = np.zeros((n, n_components))  # Xi
        self._y_scores = np.zeros((n, n_components))  # Omega
        self.x_loadings_ = np.zeros((p, n_components))  # Gamma
        self.y_loadings_ = np.zeros((q, n_components))  # Delta
        self.n_iter_ = []

        # This whole thing corresponds to the algorithm in section 4.1 of the
        # review from Wegelin. See above for a notation mapping from code to
        # paper.
        Y_eps = np.finfo(Yk.dtype).eps
        for k in range(n_components):
            # Find first left and right singular vectors of the X.T.dot(Y)
            # cross-covariance matrix.
            if self.algorithm == "nipals":
                # Replace columns that are all close to zero with zeros
                Yk_mask = np.all(np.abs(Yk) < 10 * Y_eps, axis=0)
                Yk[:, Yk_mask] = 0.0

                try:
                    (
                        x_weights,
                        y_weights,
                        n_iter_,
                    ) = _get_first_singular_vectors_power_method(
                        Xk,
                        Yk,
                        mode=self.mode,
                        max_iter=self.max_iter,
                        tol=self.tol,
                        norm_y_weights=norm_y_weights,
                    )
                except StopIteration as e:
                    if str(e) != "Y residual is constant":
                        raise
                    warnings.warn(f"Y residual is constant at iteration {k}")
                    break

                self.n_iter_.append(n_iter_)

            elif self.algorithm == "svd":
                x_weights, y_weights = _get_first_singular_vectors_svd(Xk, Yk)

            # inplace sign flip for consistency across solvers and archs
            _svd_flip_1d(x_weights, y_weights)

            # compute scores, i.e. the projections of X and Y
            x_scores = np.dot(Xk, x_weights)
            if norm_y_weights:
                y_ss = 1
            else:
                y_ss = np.dot(y_weights, y_weights)
            y_scores = np.dot(Yk, y_weights) / y_ss

            # Deflation: subtract rank-one approx to obtain Xk+1 and Yk+1
            x_loadings = np.dot(x_scores, Xk) / np.dot(x_scores, x_scores)
            Xk -= np.outer(x_scores, x_loadings)

            if self.deflation_mode == "canonical":
                # regress Yk on y_score
                y_loadings = np.dot(y_scores, Yk) / np.dot(y_scores, y_scores)
                Yk -= np.outer(y_scores, y_loadings)
            if self.deflation_mode == "regression":
                # regress Yk on x_score
                y_loadings = np.dot(x_scores, Yk) / np.dot(x_scores, x_scores)
                Yk -= np.outer(x_scores, y_loadings)

            self.x_weights_[:, k] = x_weights
            self.y_weights_[:, k] = y_weights
            self._x_scores[:, k] = x_scores
            self._y_scores[:, k] = y_scores
            self.x_loadings_[:, k] = x_loadings
            self.y_loadings_[:, k] = y_loadings

        # X was approximated as Xi . Gamma.T + X_(R+1)
        # Xi . Gamma.T is a sum of n_components rank-1 matrices. X_(R+1) is
        # whatever is left to fully reconstruct X, and can be 0 if X is of rank
        # n_components.
        # Similiarly, Y was approximated as Omega . Delta.T + Y_(R+1)

        # Compute transformation matrices (rotations_). See User Guide.
        self.x_rotations_ = np.dot(
            self.x_weights_,
            pinv2(np.dot(self.x_loadings_.T, self.x_weights_), check_finite=False),
        )
        self.y_rotations_ = np.dot(
            self.y_weights_,
            pinv2(np.dot(self.y_loadings_.T, self.y_weights_), check_finite=False),
        )

        self.coef_ = np.dot(self.x_rotations_, self.y_loadings_.T)
        self.coef_ = self.coef_ * self._y_std
        return self

    def transform(self, X, Y=None, copy=True):
        """Apply the dimension reduction.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Samples to transform.

        Y : array-like of shape (n_samples, n_targets), default=None
            Target vectors.

        copy : bool, default=True
            Whether to copy `X` and `Y`, or perform in-place normalization.

        Returns
        -------
        `x_scores` if `Y` is not given, `(x_scores, y_scores)` otherwise.
        """
        check_is_fitted(self)
        X = check_array(X, copy=copy, dtype=FLOAT_DTYPES)
        # Normalize
        X -= self._x_mean
        X /= self._x_std
        # Apply rotation
        x_scores = np.dot(X, self.x_rotations_)
        if Y is not None:
            Y = check_array(Y, ensure_2d=False, copy=copy, dtype=FLOAT_DTYPES)
            if Y.ndim == 1:
                Y = Y.reshape(-1, 1)
            Y -= self._y_mean
            Y /= self._y_std
            y_scores = np.dot(Y, self.y_rotations_)
            return x_scores, y_scores

        return x_scores

    def inverse_transform(self, X):
        """Transform data back to its original space.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_components)
            New data, where `n_samples` is the number of samples
            and `n_components` is the number of pls components.

        Returns
        -------
        x_reconstructed : array-like of shape (n_samples, n_features)

        Notes
        -----
        This transformation will only be exact if `n_components=n_features`.
        """
        check_is_fitted(self)
        X = check_array(X, dtype=FLOAT_DTYPES)
        # From pls space to original space
        X_reconstructed = np.matmul(X, self.x_loadings_.T)

        # Denormalize
        X_reconstructed *= self._x_std
        X_reconstructed += self._x_mean
        return X_reconstructed

    def predict(self, X, copy=True):
        """Predict targets of given samples.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Samples.

        copy : bool, default=True
            Whether to copy `X` and `Y`, or perform in-place normalization.

        Notes
        -----
        This call requires the estimation of a matrix of shape
        `(n_features, n_targets)`, which may be an issue in high dimensional
        space.
        """
        check_is_fitted(self)
        X = check_array(X, copy=copy, dtype=FLOAT_DTYPES)
        # Normalize
        X -= self._x_mean
        X /= self._x_std
        Ypred = np.dot(X, self.coef_)
        return Ypred + self._y_mean

    def fit_transform(self, X, y=None):
        """Learn and apply the dimension reduction on the train data.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training vectors, where n_samples is the number of samples and
            n_features is the number of predictors.

        y : array-like of shape (n_samples, n_targets), default=None
            Target vectors, where n_samples is the number of samples and
            n_targets is the number of response variables.

        Returns
        -------
        x_scores if Y is not given, (x_scores, y_scores) otherwise.
        """
        return self.fit(X, y).transform(X, y)

    # mypy error: Decorated property not supported
    @deprecated(  # type: ignore
        "Attribute norm_y_weights was deprecated in version 0.24 and "
        "will be removed in 1.1 (renaming of 0.26)."
    )
    @property
    def norm_y_weights(self):
        return self._norm_y_weights

    @deprecated(  # type: ignore
        "Attribute x_mean_ was deprecated in version 0.24 and "
        "will be removed in 1.1 (renaming of 0.26)."
    )
    @property
    def x_mean_(self):
        return self._x_mean

    @deprecated(  # type: ignore
        "Attribute y_mean_ was deprecated in version 0.24 and "
        "will be removed in 1.1 (renaming of 0.26)."
    )
    @property
    def y_mean_(self):
        return self._y_mean

    @deprecated(  # type: ignore
        "Attribute x_std_ was deprecated in version 0.24 and "
        "will be removed in 1.1 (renaming of 0.26)."
    )
    @property
    def x_std_(self):
        return self._x_std

    @deprecated(  # type: ignore
        "Attribute y_std_ was deprecated in version 0.24 and "
        "will be removed in 1.1 (renaming of 0.26)."
    )
    @property
    def y_std_(self):
        return self._y_std

    @property
    def x_scores_(self):
        # TODO: raise error in 1.1 instead
        if not isinstance(self, PLSRegression):
            pass
            warnings.warn(
                "Attribute x_scores_ was deprecated in version 0.24 and "
                "will be removed in 1.1 (renaming of 0.26). Use "
                "est.transform(X) on the training data instead.",
                FutureWarning,
            )
        return self._x_scores

    @property
    def y_scores_(self):
        # TODO: raise error in 1.1 instead
        if not isinstance(self, PLSRegression):
            warnings.warn(
                "Attribute y_scores_ was deprecated in version 0.24 and "
                "will be removed in 1.1 (renaming of 0.26). Use "
                "est.transform(X) on the training data instead.",
                FutureWarning,
            )
        return self._y_scores

    def _more_tags(self):
        return {"poor_score": True, "requires_y": False}
