import copy
import warnings
from abc import abstractmethod
from typing import Union, List

import numpy as np

from .cca_base import _CCA_Base
from .innerloop import PLSInnerLoop, PMDInnerLoop, ParkhomenkoInnerLoop, ElasticInnerLoop, ADMMInnerLoop, \
    SpanCCAInnerLoop, SWCCAInnerLoop


class _Iterative(_CCA_Base):
    """
    A class used as the base for iterative CCA methods i.e. those that optimize for each dimension one at a time with deflation.

    """

    def __init__(self, latent_dims: int = 1, scale: bool = True, centre=True, copy_data=True, deflation='cca',
                 max_iter: int = 100,
                 generalized: bool = False,
                 initialization: str = 'unregularized', tol: float = 1e-9):
        """
        Constructor for _Iterative

        :param latent_dims: number of latent dimensions
        :param scale: scale data by column variances before optimisation
        :param deflation: the type of deflation.
        :param max_iter: the maximum number of iterations to perform in the inner optimization loop
        :param generalized: use auxiliary variables (required for >2 views)
        :param initialization: intialization for optimisation. 'unregularized' uses CCA or PLS solution,'random' uses random initialization,'uniform' uses uniform initialization of weights and scores
        :param tol: if the cosine similarity of the weights between subsequent iterations is greater than 1-tol the loop is considered converged
        """
        super().__init__(latent_dims=latent_dims, scale=scale, centre=centre, copy_data=copy_data, accept_sparse=True)
        self.max_iter = max_iter
        self.generalized = generalized
        self.initialization = initialization
        self.tol = tol
        self.deflation = deflation

    def fit(self, *views: np.ndarray, ):
        """
        Fits the model by running an inner loop to convergence and then using deflation (currently only supports CCA deflation)

        :param views: numpy arrays with the same number of rows (samples) separated by commas
        """
        self.set_loop_params()
        train_views = self.centre_scale(*views)
        n = train_views[0].shape[0]
        p = [view.shape[1] for view in train_views]
        # list of d: p x k
        self.weights_list = [np.zeros((p_, self.latent_dims)) for p_ in p]
        self.loading_list = [np.zeros((p_, self.latent_dims)) for p_ in p]

        # list of d: n x k
        self.score_list = [np.zeros((n, self.latent_dims)) for _ in train_views]

        residuals = copy.deepcopy(list(train_views))

        self.objective = []
        # For each of the dimensions
        for k in range(self.latent_dims):
            self.loop = self.loop.fit(*residuals)
            for i, residual in enumerate(residuals):
                self.weights_list[i][:, k] = self.loop.weights[i]
                self.score_list[i][:, k] = self.loop.scores[i]
                self.loading_list[i][:, k] = np.dot(self.loop.scores[i], residual)
                # TODO This is CCA deflation (https://ars.els-cdn.com/content/image/1-s2.0-S0006322319319183-mmc1.pdf)
                residuals[i] = self.deflate(residuals[i], self.score_list[i][:, k], self.weights_list[i][:, k])
            self.objective.append(self.loop.track_objective)
        self.train_correlations = self.predict_corr(*views)
        return self

    def deflate(self, residual, score, loading):
        """
        Deflate view residual by CCA deflation (https://ars.els-cdn.com/content/image/1-s2.0-S0006322319319183-mmc1.pdf)

        :param residual:
        :param score:

        """
        if self.deflation == 'cca':
            return residual - np.outer(score, score) @ residual / np.dot(score, score).item()
        elif self.deflation == 'pls':
            return residual - np.outer(score, loading)

    @abstractmethod
    def set_loop_params(self):
        """
        Sets up the inner optimization loop for the method. By default uses the PLS inner loop.
        """
        self.loop = PLSInnerLoop(max_iter=self.max_iter, generalized=self.generalized,
                                 initialization=self.initialization)


class PLS(_Iterative):
    """
    A class used to fit a PLS model

    Fits a partial least squares model with CCA deflation by NIPALS algorithm

    :Example:

    >>> from cca_zoo.models import PLS
    >>> X1 = np.random.rand(10,5)
    >>> X2 = np.random.rand(10,5)
    >>> model = PLS()
    >>> model.fit(X1,X2)
    """

    def __init__(self, latent_dims: int = 1, scale: bool = True, centre=True, copy_data=True, deflation='cca',
                 max_iter: int = 100,
                 generalized: bool = False,
                 initialization: str = 'unregularized', tol: float = 1e-9):
        """
        Constructor for PLS

        :param latent_dims: number of latent dimensions
        :param scale: scale data by column variances before optimisation
        :param deflation: the type of deflation.
        :param max_iter: the maximum number of iterations to perform in the inner optimization loop
        :param generalized: use auxiliary variables (required for >2 views)
        :param initialization: intialization for optimisation. 'unregularized' uses CCA or PLS solution,'random' uses random initialization,'uniform' uses uniform initialization of weights and scores
        :param tol: if the cosine similarity of the weights between subsequent iterations is greater than 1-tol the loop is considered converged
        """
        super().__init__(latent_dims=latent_dims, scale=scale, centre=centre, deflation=deflation, max_iter=max_iter,
                         generalized=generalized,
                         initialization=initialization, tol=tol)

    def set_loop_params(self):
        self.loop = PLSInnerLoop(max_iter=self.max_iter, generalized=self.generalized,
                                 initialization=self.initialization, tol=self.tol)


class ElasticCCA(_Iterative):
    """
    Fits an elastic CCA by iterative rescaled elastic net regression

    Citation
    --------
    Waaijenborg, Sandra, Philip C. Verselewel de Witt Hamer, and Aeilko H. Zwinderman. "Quantifying the association between gene expressions and DNA-markers by penalized canonical correlation analysis." Statistical applications in genetics and molecular biology 7.1 (2008).

    :Example:

    >>> from cca_zoo.models import ElasticCCA
    >>> X1 = np.random.rand(10,5)
    >>> X2 = np.random.rand(10,5)
    >>> model = ElasticCCA()
    >>> model.fit(X1,X2)
    """

    def __init__(self, latent_dims: int = 1, scale: bool = True, centre=True, copy_data=True, deflation='cca',
                 max_iter: int = 100,
                 generalized: bool = False,
                 initialization: str = 'unregularized', tol: float = 1e-9,
                 c: Union[List[float], float] = None,
                 l1_ratio: Union[List[float], float] = None,
                 constrained: bool = False, stochastic=False,
                 positive: Union[List[bool], bool] = None):
        """
        Constructor for ElasticCCA

        :param latent_dims: number of latent dimensions
        :param scale: scale data by column variances before optimisation
        :param deflation: the type of deflation.
        :param max_iter: the maximum number of iterations to perform in the inner optimization loop
        :param generalized: use auxiliary variables (required for >2 views)
        :param initialization: intialization for optimisation. 'unregularized' uses CCA or PLS solution,'random' uses random initialization,'uniform' uses uniform initialization of weights and scores
        :param tol: if the cosine similarity of the weights between subsequent iterations is greater than 1-tol the loop is considered converged
        :param c: lasso alpha
        :param l1_ratio: l1 ratio in lasso subproblems
        :param constrained: force unit norm constraint with binary search
        :param stochastic: use stochastic regression optimisers for subproblems
        :param positive: constrain model weights to be positive
        """
        self.c = c
        self.l1_ratio = l1_ratio
        self.constrained = constrained
        self.stochastic = stochastic
        self.positive = positive
        if self.positive is not None and stochastic:
            self.stochastic = False
            warnings.warn(
                'Non negative constraints cannot be used with stochastic regressors. Switching to stochastic=False')
        super().__init__(latent_dims=latent_dims, scale=scale, centre=centre, copy_data=copy_data, deflation=deflation,
                         max_iter=max_iter,
                         generalized=generalized,
                         initialization=initialization, tol=tol)

    def set_loop_params(self):
        self.loop = ElasticInnerLoop(max_iter=self.max_iter, c=self.c, l1_ratio=self.l1_ratio,
                                     generalized=self.generalized, initialization=self.initialization,
                                     tol=self.tol, constrained=self.constrained,
                                     stochastic=self.stochastic, positive=self.positive)


class CCA_ALS(ElasticCCA):
    """
    Fits a CCA model with CCA deflation by NIPALS algorithm. Implemented by ElasticCCA with 0 regularisation

    Citation
    --------
    Golub, Gene H., and Hongyuan Zha. "The canonical correlations of matrix pairs and their numerical computation." Linear algebra for signal processing. Springer, New York, NY, 1995. 27-49.

    :Example:

    >>> from cca_zoo.models import CCA_ALS
    >>> X1 = np.random.rand(10,5)
    >>> X2 = np.random.rand(10,5)
    >>> model = CCA_ALS()
    >>> model.fit(X1,X2)
    """

    def __init__(self, latent_dims: int = 1, scale: bool = True, centre=True, copy_data=True, max_iter: int = 100,
                 generalized: bool = False,
                 initialization: str = 'random', tol: float = 1e-9, stochastic=True,
                 positive: Union[List[bool], bool] = None):
        """
        Constructor for CCA_ALS

        """

        super().__init__(latent_dims=latent_dims, max_iter=max_iter, generalized=generalized,
                         initialization=initialization, tol=tol, constrained=False, stochastic=stochastic,
                         centre=centre, copy_data=copy_data, scale=scale,
                         positive=positive)


class SCCA(ElasticCCA):
    """
    Fits a sparse CCA model by iterative rescaled lasso regression. Implemented by ElasticCCA with l1 ratio=1

    Citation
    --------
    Mai, Qing, and Xin Zhang. "An iterative penalized least squares approach to sparse canonical correlation analysis." Biometrics 75.3 (2019): 734-744.

    :Example:

    >>> from cca_zoo.models import SCCA
    >>> X1 = np.random.rand(10,5)
    >>> X2 = np.random.rand(10,5)
    >>> model = SCCA(c=[0.001,0.001])
    >>> model.fit(X1,X2)
    """

    def __init__(self, latent_dims: int = 1, scale: bool = True, centre=True, copy_data=True,
                 c: Union[List[float], float] = None,
                 max_iter: int = 100,
                 generalized: bool = False,
                 initialization: str = 'unregularized', tol: float = 1e-9, stochastic=False,
                 positive: Union[List[bool], bool] = None):
        """
        Constructor for SCCA

        """
        super().__init__(latent_dims=latent_dims, scale=scale, centre=centre, copy_data=copy_data, max_iter=max_iter,
                         generalized=generalized,
                         initialization=initialization, tol=tol, c=c, l1_ratio=1, constrained=False,
                         stochastic=stochastic, positive=positive)


class PMD(_Iterative):
    """
    Fits a Sparse CCA (Penalized Matrix Decomposition) model.

    Citation
    --------
    Witten, Daniela M., Robert Tibshirani, and Trevor Hastie. "A penalized matrix decomposition, with applications to sparse principal components and canonical correlation analysis." Biostatistics 10.3 (2009): 515-534.

    :Example:

    >>> from cca_zoo.models import PMD
    >>> X1 = np.random.rand(10,5)
    >>> X2 = np.random.rand(10,5)
    >>> model = PMD(c=[1,1])
    >>> model.fit(X1,X2)
    """

    def __init__(self, latent_dims: int = 1, scale: bool = True, centre=True, copy_data=True,
                 c: Union[List[float], float] = None,
                 max_iter: int = 100,
                 generalized: bool = False, initialization: str = 'unregularized', tol: float = 1e-9,
                 positive: Union[List[bool], bool] = None):
        """
        Constructor for PMD

        :param c: l1 regularisation parameter between 1 and sqrt(number of features) for each view
        :param positive: constrain model weights to be positive
        """
        self.c = c
        self.positive = positive
        super().__init__(latent_dims=latent_dims, scale=scale, centre=centre, copy_data=copy_data, max_iter=max_iter,
                         generalized=generalized,
                         initialization=initialization, tol=tol)

    def set_loop_params(self):
        self.loop = PMDInnerLoop(max_iter=self.max_iter, c=self.c, generalized=self.generalized,
                                 initialization=self.initialization, tol=self.tol, positive=self.positive)


class ParkhomenkoCCA(_Iterative):
    """
    Fits a sparse CCA (penalized CCA) model

    Citation
    --------
    Parkhomenko, Elena, David Tritchler, and Joseph Beyene. "Sparse canonical correlation analysis with application to genomic data integration." Statistical applications in genetics and molecular biology 8.1 (2009).

    :Example:

    >>> from cca_zoo.models import ParkhomenkoCCA
    >>> X1 = np.random.rand(10,5)
    >>> X2 = np.random.rand(10,5)
    >>> model = ParkhomenkoCCA(c=[0.001,0.001])
    >>> model.fit(X1,X2)
    """

    def __init__(self, latent_dims: int = 1, scale: bool = True, centre=True, copy_data=True,
                 c: Union[List[float], float] = None,
                 max_iter: int = 100,
                 generalized: bool = False, initialization: str = 'unregularized', tol: float = 1e-9):
        """
        Constructor for ParkhomenkoCCA

        :param c: l1 regularisation parameter
        """
        self.c = c
        super().__init__(latent_dims=latent_dims, scale=scale, centre=centre, copy_data=copy_data, max_iter=max_iter,
                         generalized=generalized,
                         initialization=initialization, tol=tol)

    def set_loop_params(self):
        self.loop = ParkhomenkoInnerLoop(max_iter=self.max_iter, c=self.c,
                                         generalized=self.generalized,
                                         initialization=self.initialization, tol=self.tol)


class SCCA_ADMM(_Iterative):
    """
    Fits a sparse CCA model by alternating ADMM

    Citation
    --------
    Suo, Xiaotong, et al. "Sparse canonical correlation analysis." arXiv preprint arXiv:1705.10865 (2017).

    :Example:

    >>> from cca_zoo.models import SCCA_ADMM
    >>> X1 = np.random.rand(10,5)
    >>> X2 = np.random.rand(10,5)
    >>> model = SCCA_ADMM()
    >>> model.fit(X1,X2)
    """

    def __init__(self, latent_dims: int = 1, scale: bool = True, centre=True, copy_data=True,
                 c: Union[List[float], float] = None,
                 mu: Union[List[float], float] = None,
                 lam: Union[List[float], float] = None,
                 eta: Union[List[float], float] = None,
                 max_iter: int = 100,
                 generalized: bool = False, initialization: str = 'unregularized', tol: float = 1e-9):
        """
        Constructor for SCCA_ADMM


        :param c: l1 regularisation parameter
        :param mu:
        :param lam:
        :param: eta:
        """
        self.c = c
        self.mu = mu
        self.lam = lam
        self.eta = eta
        super().__init__(latent_dims=latent_dims, scale=scale, centre=centre, copy_data=copy_data, max_iter=max_iter,
                         generalized=generalized,
                         initialization=initialization, tol=tol)

    def set_loop_params(self):
        self.loop = ADMMInnerLoop(max_iter=self.max_iter, c=self.c, mu=self.mu, lam=self.lam,
                                  eta=self.eta, generalized=self.generalized,
                                  initialization=self.initialization, tol=self.tol)


class SpanCCA(_Iterative):
    """
    Fits a Sparse CCA model using SpanCCA.

    Citation
    --------
    Asteris, Megasthenis, et al. "A simple and provable algorithm for sparse diagonal CCA." International Conference on Machine Learning. PMLR, 2016.

    """

    def __init__(self, latent_dims: int = 1, scale: bool = True, centre=True, copy_data=True, max_iter: int = 100,
                 generalized: bool = False,
                 initialization: str = 'uniform', tol: float = 1e-9, regularisation='l0',
                 c: Union[List[Union[float, int]], Union[float, int]] = None, rank=1,
                 positive: Union[List[bool], bool] = None):
        super().__init__(latent_dims=latent_dims, scale=scale, centre=centre, copy_data=copy_data, max_iter=max_iter,
                         generalized=generalized,
                         initialization=initialization, tol=tol)
        self.c = c
        self.regularisation = regularisation
        self.rank = rank
        self.positive = positive

    def set_loop_params(self):
        self.loop = SpanCCAInnerLoop(max_iter=self.max_iter, c=self.c, generalized=self.generalized,
                                     initialization=self.initialization, tol=self.tol,
                                     regularisation=self.regularisation, rank=self.rank, positive=self.positive)


class SWCCA(_Iterative):
    """
    A class used to fit SWCCA model

    Citation
    --------
    Wenwen, M. I. N., L. I. U. Juan, and Shihua Zhang. "Sparse Weighted Canonical Correlation Analysis." Chinese Journal of Electronics 27.3 (2018): 459-466.


    """

    def __init__(self, latent_dims: int = 1, scale: bool = True, centre=True, copy_data=True, max_iter: int = 500,
                 generalized: bool = False,
                 initialization: str = 'uniform', tol: float = 1e-9, regularisation='l0',
                 c: Union[List[Union[float, int]], Union[float, int]] = None, sample_support=None,
                 positive: Union[List[bool], bool] = None):
        self.c = c
        self.sample_support = sample_support
        self.regularisation = regularisation
        self.positive = positive
        super().__init__(latent_dims=latent_dims, scale=scale, centre=centre, copy_data=copy_data, max_iter=max_iter,
                         generalized=generalized,
                         initialization=initialization, tol=tol)

    def set_loop_params(self):
        self.loop = SWCCAInnerLoop(max_iter=self.max_iter, generalized=self.generalized,
                                   initialization=self.initialization, tol=self.tol, regularisation=self.regularisation,
                                   c=self.c,
                                   sample_support=self.sample_support, positive=self.positive)
