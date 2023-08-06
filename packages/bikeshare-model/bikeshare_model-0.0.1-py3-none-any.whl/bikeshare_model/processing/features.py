from typing import List
import sys
import pandas as pd
import numpy as np

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder


class bikeshareImputer(BaseEstimator, TransformerMixin):
    """bikeshare column Imputer"""

    def __init__(self, variables: str):

        if not isinstance(variables, str):
            raise ValueError("variables should be a str")

        self.variables = variables

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        # we need the fit statement to accomodate the sklearn pipeline
        self.fill_value=X[self.variables].mode()[0]
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X = X.copy()
        X[self.variables]=X[self.variables].fillna(self.fill_value)
        #print(" Print Feature:", self.variables)
        return X
    
    
class Mapper(BaseEstimator, TransformerMixin):
    """Categorical variable mapper."""

    def __init__(self, variables: str, mappings: dict):

        if not isinstance(variables, str):
            raise ValueError("variables should be a str")

        self.variables = variables
        self.mappings = mappings

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X = X.copy()
        #print("error",self.variables)
        #print(X.head)
        X[self.variables] = X[self.variables].map(self.mappings).astype(int)
        return X
    
class OutlierHandler(BaseEstimator, TransformerMixin):
    def __init__(self, column, lower_quantile=0.05, upper_quantile=0.95, lower_bound=None, higher_bound=None):
        self.column = column
        self.lower_quantile = lower_quantile
        self.upper_quantile = upper_quantile
        self.lower_bound = lower_bound
        self.higher_bound = higher_bound

    def fit(self, X, y=None):
        if self.lower_bound is None:
            self.lower_bound = X[self.column].quantile(self.lower_quantile)
        if self.higher_bound is None:
            self.higher_bound = X[self.column].quantile(self.upper_quantile)
        return self

    def transform(self, X, y=None):
        X[self.column] = np.where(X[self.column] < self.lower_bound, self.lower_bound,
                                  np.where(X[self.column] > self.higher_bound, self.higher_bound, X[self.column]))
        return X
    
    
class WeekdayOneHotEncoder(BaseEstimator, TransformerMixin):
    """ One-hot encode weekday column """
    def __init__(self, column):
        self.column = column
        self.encoder = OneHotEncoder(sparse_output=False)

    def fit(self, X, y=None):
        self.encoder.fit(X[[self.column]])
        return self

    def transform(self, X, y=None):
        encoded = self.encoder.transform(X[[self.column]])
        column_names = self.encoder.get_feature_names_out([self.column])
        encoded_df = pd.DataFrame(encoded, columns=column_names, index=X.index)
        encoded_df = encoded_df.astype(object)
        return pd.concat([X.drop(self.column, axis=1), encoded_df], axis=1)
