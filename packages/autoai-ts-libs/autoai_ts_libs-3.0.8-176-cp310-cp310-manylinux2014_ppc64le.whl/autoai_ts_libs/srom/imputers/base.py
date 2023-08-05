################################################################################
# IBM Confidential
# OCO Source Materials
# 5737-H76, 5725-W78, 5900-A1R
# (c) Copyright IBM Corp. 2021, 2022. All Rights Reserved.
# The source code for this program is not published or otherwise divested of its trade secrets,
# irrespective of what has been deposited with the U.S. Copyright Office.
################################################################################

from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np
from sklearn.utils.validation import check_array
from autoai_ts_libs.srom.imputers.extended_iterative_imputer import ExtendedIterativeImputer
from autoai_ts_libs.srom.imputers.utils import (
    _fit_decomposition,
    _transform_decomposition,
)
from sklearn.impute import SimpleImputer
from sklearn.decomposition import PCA
from sklearn.base import clone
from autoai_ts_libs.utils.messages.messages import Messages
import pandas as pd


class TSImputer(BaseEstimator, TransformerMixin):
    """
    Base class for time series based imputer.
    Parameters:
        time_column (int): time column.
        missing_values (obj): missing value to be imputed.
        enable_fillna (boolean): fill the backword and forward.
    """

    def __init__(self, time_column=-1, missing_values=np.nan, enable_fillna=True):

        self.time_column = time_column
        self.missing_values = missing_values
        self.enable_fillna = enable_fillna
        # this i shifted to fit
        # self._check_param_values()

    def _check_param_values(self):
        if self.time_column < -1:
            raise (ValueError)
        elif self.time_column >= 0:
            raise Exception(Messages.get_message(message_id="AUTOAITSLIBS0058E"))

    def fit(self, X, y=None, **fit_params):
        """
        Fit the imputer
        Parameters:
            X(array like): input.
        """
        if 'skip_fit' in fit_params.keys() and fit_params['skip_fit']:
            return self

        self._check_param_values()
        return self

    def transform(self, X):
        """
        Transform the imputer
        Parameters:
            X(array like): input.
        """
        return X


class DecompositionImputer(BaseEstimator, TransformerMixin):
    """
    Base class for deecomposition based imputer.
    Parameters:
        time_column(int): time column.
        missing_values (obj): missing value to be imputed.
        enable_fillna(boolean): fill the backword and forward.
        order(int): lookback in case of time series imputer.
        base_imputer(obj): object of sklearn Imputer or srom. 
        scaler(obj): data scaler object necessary for decomposition.
        decomposer(obj): object of sklearn.decomposition.
        max_iter(int): Number of iteration to run the decomposition.
        tol(float): the tolerance of the imputed value on each iteration.
    """

    def __init__(
        self,
        time_column=-1,
        missing_values=np.nan,
        enable_fillna=True,
        order=-1,
        base_imputer=SimpleImputer(),
        scaler=None,
        decomposer=PCA(),
        max_iter=None,
        tol=None,
    ):
        self.time_column = time_column
        self.missing_values = missing_values
        self.enable_fillna = enable_fillna
        self.order = order
        self.base_imputer = base_imputer
        self.scaler = scaler
        self.decomposer = decomposer
        self.max_iter = max_iter
        self.tol = tol
        self._check_param_values()

    def _check_param_values(self):
        if self.time_column < -1:
            raise (ValueError)
        elif self.time_column >= 0:
            raise Exception(Messages.get_message(message_id="AUTOAITSLIBS0058E"))

    def __setstate__(self, state):
        super().__setstate__(state)
        ### Backward compatibility for imputer
        if not hasattr(self, "_base_imputer"):
            self._base_imputer = self.base_imputer
            self._decomposer = self.decomposer

    def fit(self, X, y=None, **fit_params):
        """
        Fit the imputer
        Parameters:
            X(array like): input.
        """
        if 'skip_fit' in fit_params.keys() and fit_params['skip_fit']:
            return self

        self._base_imputer = clone(self.base_imputer)
        self._decomposer = clone(self.decomposer)

        X = check_array(X, dtype=np.float64, force_all_finite=False)

        if isinstance(X, pd.DataFrame):
            X = X.to_numpy()
        if not np.isnan(self.missing_values):
            X[X == self.missing_values] = np.NaN

        if isinstance(self._base_imputer, TSImputer):
            X_nan = np.isnan(self._base_imputer.get_X(X, order=self.order))
            imputed = self._base_imputer.fit_transform(X)
            imputed = self._base_imputer.get_X(imputed, order=self.order)
        else:
            X_nan = np.isnan(X)
            imputed = self._base_imputer.fit_transform(X)
        new_imputed = imputed.copy()

        if self.scaler:
            imputed = self.scaler.fit_transform(imputed)
            new_imputed = imputed.copy()

        self._decomposer = _fit_decomposition(
            self._decomposer, imputed, new_imputed, X_nan, self.max_iter, self.tol
        )

        return self

    def transform(self, X):
        """
        Transform the imputer
        Parameters:
            X(array like): input.
        """
        if X is None:
            return X
        X = check_array(X, dtype=np.float64, force_all_finite=False)

        if isinstance(X, pd.DataFrame):
            X = X.to_numpy()
        if not np.isnan(self.missing_values):
            X[X == self.missing_values] = np.NaN

        if isinstance(self._base_imputer, TSImputer):
            if len(X) < self.order:
                if np.count_nonzero(np.isnan(X)) > 0:
                    raise Exception(
                        Messages.get_message(message_id="AUTOAITSLIBS0057E")
                    )
                else:
                    return X
            X_nan = np.isnan(self._base_imputer.get_X(X, order=self.order))
            imputed = self._base_imputer.fit_transform(X)
            X = self._base_imputer.get_X(imputed, order=self.order)
        else:
            X_nan = np.isnan(X)
            X = self._base_imputer.transform(X)

        X = _transform_decomposition(self._decomposer, self.scaler, X, X_nan)
        if isinstance(self._base_imputer, TSImputer):
            X = self._base_imputer.get_TS(X, order=self.order)
        return X

    def set_params(self, **kwarg):
        """
        Set params.
        Parameters:
            kwarg(dict): keyword arguments.
        """
        super(DecompositionImputer, self).set_params(**kwarg)
        decomposer_param = {}

        for item in self.decomposer.get_params().keys():
            if item in kwarg.keys():
                decomposer_param[item] = kwarg[item]
        if len(decomposer_param) > 0:
            self.decomposer.set_params(**decomposer_param)


class FlattenImputer(BaseEstimator, TransformerMixin):
    """
    Base class for imputer based on flatten transformer.
    Parameters:
        time_column (int): time column.
        missing_values (obj): missing value to be imputed.
        enable_fillna (boolean): fill the backword and forward.
        order (int): lookback in case of time series imputer.
        base_imputer (obj): object of sklearn Imputer or srom.
        model_imputer (obj): object of sklearn Imputer or srom. 
    """

    def __init__(
        self,
        time_column=-1,
        missing_values=np.nan,
        enable_fillna=True,
        order=-1,
        base_imputer=None,
        model_imputer=None,
    ):
        self.time_column = time_column
        self.missing_values = missing_values
        self.enable_fillna = enable_fillna
        self.order = order
        self.base_imputer = base_imputer
        self.model_imputer = model_imputer

    def fit(self, X, y=None, **fit_params):
        """
        Fit the imputer
        Parameters:
            X(array like): input.
        """
        if 'skip_fit' in fit_params.keys() and fit_params['skip_fit']:
            return self

        self._base_imputer = clone(self.base_imputer)
        self._model_imputer = clone(self.model_imputer)

        X = check_array(X, dtype=np.float64, force_all_finite=False)

        if isinstance(X, pd.DataFrame):
            X = X.to_numpy()
        if not np.isnan(self.missing_values):
            X[X == self.missing_values] = np.NaN

        # store incoming last order data point
        if self.order < X.shape[0]:
            self.X_order_ = X[(X.shape[0] - self.order) :, :]
        else:
            # I should raise an error here or pad a default value
            pass

        # added this fix to control the number of neighbour to be selected
        # this is conrolled
        if isinstance(self._model_imputer, ExtendedIterativeImputer) and self._model_imputer.n_nearest_features is None:
            self._model_imputer.n_nearest_features = min(1, self.order-1)

        X = self._base_imputer.get_X(X, order=self.order)
        for col in range(X.shape[1]):
            if(all(np.isnan(X[:,[col]]))):
                X[:,[col]] = 0.0
        self._model_imputer.fit(X)
        return self

    def __setstate__(self, state):
        super().__setstate__(state)
        ### Backward compatibility for imputer
        if not hasattr(self, "_base_imputer"):
            self._base_imputer = self.base_imputer
            self._model_imputer = self.model_imputer
    
    def transform(self, X):
        """
        Transform the imputer
        Parameters:
            X(array like): input.
        """
        if X is None:
            return X
        X = check_array(X, dtype=np.float64, force_all_finite=False)

        if isinstance(X, pd.DataFrame):
            X = X.to_numpy()
        if not np.isnan(self.missing_values):
            X[X == self.missing_values] = np.NaN

        is_appended = False
        if len(X) < self.order:
            if np.count_nonzero(np.isnan(X)) > 0:
                #raise Exception(Messages.get_message(message_id="AUTOAITSLIBS0057E"))
                X = np.concatenate([self.X_order_, X])
                is_appended = True
            else:
                return X
        X = self._base_imputer.get_X(X, order=self.order)
        X = self._model_imputer.transform(X)
        X = self._base_imputer.get_TS(X, order=self.order)

        if is_appended:
            X = X[(X.shape[0] - self.order) :, :]

        return X

    def set_params(self, **kwarg):
        """
        Set params.
        Parameters:
            kwarg(dic): keyword arguments.
        """
        super(FlattenImputer, self).set_params(**kwarg)

        """
        # techically parent class shd help
        if "base_imputer" in kwarg:
            self.base_imputer = kwarg["base_imputer"]
        if "model_imputer" in kwarg:
            self.model_imputer = kwarg["model_imputer"]
        if "time_column" in kwarg:
            self.time_column = kwarg["time_column"]
        if "missing_values" in kwarg:
            self.missing_values = kwarg["missing_values"]
        if "enable_fillna" in kwarg:
            self.enable_fillna = kwarg["enable_fillna"]
        if "order" in kwarg:
            self.order = kwarg["order"]
        """

        model_param = {}
        for d_item in kwarg:
            if "base_imputer__" in d_item:
                model_param[d_item.split("base_imputer__")[1]] = kwarg[d_item]
        if len(model_param) > 0:
            self.base_imputer.set_params(**model_param)

        model_param = {}
        for d_item in kwarg:
            if "model_imputer__" in d_item:
                model_param[d_item.split("model_imputer__")[1]] = kwarg[d_item]
        if len(model_param) > 0:
            self.model_imputer.set_params(**model_param)
        return self

    def get_params(self, deep=False):
        """
        Get params.
        Parameters:
            deep(boolean): flag to get nested parameters.
        
        """
        model_param = super(FlattenImputer, self).get_params(deep=deep)

        """
        model_param["base_imputer"] = self.base_imputer
        model_param["model_imputer"] = self.model_imputer
        model_param["time_column"] = self.time_column
        model_param["missing_values"] = self.missing_values
        model_param["order"] = self.order
        model_param["enable_fillna"] = self.enable_fillna
        """

        if deep:
            for item in self.base_imputer.get_params().keys():
                model_param["base_imputer__" + item] = self.base_imputer.get_params()[
                    item
                ]
            for item in self.model_imputer.get_params().keys():
                model_param["model_imputer__" + item] = self.model_imputer.get_params()[
                    item
                ]
        return model_param