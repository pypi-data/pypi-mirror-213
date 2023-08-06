#from __future__ import annotations

import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import QuantileTransformer

STRATEGIES = ["pass_through", "minmax", "standard", "simple_quantile", "weighted_quantile"]


class LbColTransformer:   # TODO add docstring
  def __init__ (self, *args, **kwargs):

    if (len(args) == 1) and isinstance (args[0], ColumnTransformer):
      self._col_transformer = args[0]
    else:
      self._col_transformer = ColumnTransformer (*args, **kwargs)

  def fit (self, X, y = None, sample_weight = None):
    if sample_weight is None:
      return self._col_transformer.fit (X, y = y)

    else:
      transformers = list()

      ## ColumnTransformer stuff
      self._col_transformer . _check_n_features (X, reset = True)
      self._col_transformer . _validate_transformers()
      self._col_transformer . _validate_column_callables (X)
      self._col_transformer . _validate_remainder (X)
      self._col_transformer . _validate_transformers()
      self._col_transformer . _validate_column_callables (X)

      for key, scaler, cols in self._col_transformer.transformers:
        if key in ["standard", "weighted_quantile"]:   # sample_weight supported
          scaler . fit ( X = X[:,cols], sample_weight = sample_weight )
        else:
          scaler . fit ( X = X[:,cols] )
        transformers . append ( scaler )   # fitted transformers

      self._col_transformer . _update_fitted_transformers (transformers)
      return self._col_transformer

  def fit_transform (self, X, y = None, sample_weight = None):
    if sample_weight is None:
      return self._col_transformer.fit_transform (X, y = y)
    else:
      return self . fit (X, y = y, sample_weight = sample_weight) . transform (X)

  def transform (self, X):
    X_tr = list()
    for key, scaler, cols in self._col_transformer.transformers_:
      if key == "pass_through":
        X_tr . append ( X[:,cols] )
      else:
        X_tr . append ( scaler . transform (X[:,cols]) )
    return np.concatenate ( X_tr, axis = 1 )

  def inverse_transform (self, X):
    perm_indices = list()
    for _, _, cols in self._col_transformer.transformers_: 
      perm_indices += list(cols)

    X_perm = np.zeros_like (X)
    for i, j in enumerate(perm_indices):
      X_perm[:,j] = X[:,i]

    X_tr = np.zeros_like (X_perm)
    for key, scaler, cols in self._col_transformer.transformers_:
      if key == "pass_through":
        X_tr[:,cols] = X_perm[:,cols]
      else:
        X_tr[:,cols] = scaler . inverse_transform (X_perm[:,cols])

    return X_tr

  @property
  def sklearn_transformer (self) -> ColumnTransformer:
    for i, transf in enumerate (self._col_transformer.transformers_):
      if transf[0] == "weighted_quantile":
        downcasted_scaler = QuantileTransformer()   # downcasting to QuantileTransformer
        for k, v in transf[1].__dict__.items():
          downcasted_scaler.__dict__[k] = v
        self._col_transformer.transformers_[i][1] = downcasted_scaler
    return self._col_transformer
