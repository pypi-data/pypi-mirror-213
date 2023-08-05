# License: Apache-2.0
from abc import ABC
from typing import List, Dict, Union

import numpy as np
import pandas as pd

from gators import DataFrame


EPSILON = 1e-10


class BinFactory(ABC):
    def bin(self) -> DataFrame:
        """Add the binned columns to the input dataframe."""

    def bin_inplace(self) -> DataFrame:
        """Add in-place the binned columns to the input dataframe."""


class BinPandas(BinFactory):
    def bin(
        self,
        X: DataFrame,
        bins_dict: Dict[str, List],
        labels: Dict[str, str],
        columns: List[str],
        column_names: List[str],
    ) -> DataFrame:
        """Add the binned columns to the input Pandas dataframe.

        Parameters
        ----------
        X : DataFrame
            Input dataframe.
        bins_dict : Dict[str, List]
            Dictionary of bins_dict. The keys are the column names, the values are the split arrays.
        labels : Dict[str, str]
            Dictionary of labels. The keys are the column names, the values are the label arrays.
        columns : List[str]
            List of columns.
        column_names : List[str]
             List of output columns, only used where `inplace=True`.

        Returns
        -------
        DataFrame
            Transformed dataframe.
        """

        for c, name in zip(columns, column_names):
            n_bins = len(bins_dict[c])
            dummy = X[c].where(~(X[c] < X.bins_dict[c][1]), X.labels[c][0])
            for j in range(1, n_bins - 1):
                dummy = dummy.where(
                    ~((X[c] >= X.bins_dict[c][j]) & (X[c] < X.bins_dict[c][j + 1])),
                    X.labels[c][j],
                )
            dummy = dummy.where(~(X[c] > X.bins_dict[c][-2]), X.labels[c][-1])
            X[name] = dummy

        # for name, col in zip(column_names, columns):
        #     X[name] = pd.cut(
        #         X[col],
        #         bins=bins_dict[col],
        #         labels=labels[col],
        #         duplicates="drop",
        #         include_lowest=True,
        #         right=False,
        #     )
        # X[column_names] = X[column_names].astype(str)
        return X

    def bin_inplace(
        self,
        X: DataFrame,
        bins_dict: pd.DataFrame,
        labels: Dict[str, str],
        columns: List[str],
        column_names: List[str],
    ) -> DataFrame:
        """Add in-place the binned columns to the input Pandas dataframe.

        Parameters
        ----------
        X : DataFrame
            Input dataframe.
        bins_dict : pd.DataFrame
            Dictionary of bins_dict. The keys are the column names, the values are the split arrays.
        labels : Dict[str, str]
            Dictionary of labels. The keys are the column names, the values are the label arrays.
        columns : List[str]
            List of columns.
        column_names : List[str]
             List of output columns, only used where `inplace=True`.

        Returns
        -------
        DataFrame
            Transformed dataframe.
        """
        # for _, col in zip(column_names, columns):
        #     X[col] = pd.cut(
        #         X[col],
        #         bins=bins_dict[col],
        #         labels=labels[col],
        #         duplicates="drop",
        #         include_lowest=True,
        #         right=False,
        #     )
        # X[columns] = X[columns].astype(str)
        for c in columns:
            n_bins = len(bins_dict[c])
            dummy = X[c].where(~(X[c] < X.bins[c][1]), X.mapping[c][0])
            for j in range(1, n_bins - 1):
                dummy = dummy.where(
                    ~((X[c] >= X.bins[c][j]) & (X[c] < X.bins[c][j + 1])),
                    X.mapping[c][j],
                )
            dummy = dummy.where(~(X[c] > X.bins[c][-2]), X.mapping[c][-1])
            X[c] = dummy

        return X


class BinKoalas(BinFactory):
    def bin(
        self,
        X: DataFrame,
        bins_dict: pd.DataFrame,
        labels: Dict[str, str],
        columns: List[str],
        column_names: List[str],
    ) -> DataFrame:
        """Add the binned columns to the input Koalas dataframe.

        Parameters
        ----------
        X : DataFrame
            Input dataframe.
        bins_dict : pd.DataFrame
            Dictionary of bins_dict. The keys are the column names, the values are the split arrays.
        labels : Dict[str, str]
            Dictionary of labels. The keys are the column names, the values are the label arrays.
        columns : List[str]
            List of columns.
        column_names : List[str]
             List of output columns, only used where `inplace=True`.

        Returns
        -------
        DataFrame
            Transformed dataframe.
        """
        from pyspark.ml.feature import Bucketizer

        bins_np = [np.unique(b) - 1e-10 for b in bins_dict.values()]
        X = (
            Bucketizer(
                bins_dictArray=bins_np, inputCols=columns, outputCols=column_names
            )
            .transform(X.to_spark())
            .to_koalas()
        )
        X[column_names] = "_" + X[column_names].astype(int).astype(str)
        return X

    def bin_inplace(
        self,
        X: DataFrame,
        bins_dict: pd.DataFrame,
        labels: Dict[str, str],
        columns: List[str],
        column_names: List[str],
    ) -> DataFrame:
        """Add in-place the binned columns to the input Koalas dataframe.

        Parameters
        ----------
        X : DataFrame
            Input dataframe.
        bins_dict : pd.DataFrame
            Dictionary of bins_dict. The keys are the column names, the values are the split arrays.
        labels : Dict[str, str]
            Dictionary of labels. The keys are the column names, the values are the label arrays.
        columns : List[str]
            List of columns.
        column_names : List[str]
             List of output columns, only used where `inplace=True`.

        Returns
        -------
        DataFrame
            Transformed dataframe.
        """
        from pyspark.ml.feature import Bucketizer

        bins_np = [np.unique(b) - 1e-10 for b in bins_dict.values()]
        ordered_columns = X.columns
        X = (
            Bucketizer(
                bins_dictArray=bins_np, inputCols=columns, outputCols=column_names
            )
            .transform(X.to_spark())
            .to_koalas()
            .drop(columns, axis=1)
            .rename(columns=dict(zip(column_names, columns)))
        )
        X[columns] = "_" + X[columns].astype(int).astype(str)
        return X[ordered_columns]


class BinDask(BinFactory):
    def bin(
        self,
        X: DataFrame,
        bins_dict: pd.DataFrame,
        labels: Dict[str, str],
        columns: List[str],
        column_names: List[str],
    ) -> DataFrame:
        """Add the binned columns to the input Dask dataframe.

        Parameters
        ----------
        X : DataFrame
            Input dataframe.
        bins_dict : pd.DataFrame
            Dictionary of bins_dict. The keys are the column names, the values are the split arrays.
        labels : Dict[str, str]
            Dictionary of labels. The keys are the column names, the values are the label arrays.
        columns : List[str]
            List of columns.
        column_names : List[str]
             List of output columns, only used where `inplace=True`.

        Returns
        -------
        DataFrame
            Transformed dataframe.
        """
        for name, col in zip(column_names, columns):
            X[name] = X[col].map_partitions(
                pd.cut,
                bins=bins_dict[col],
                labels=labels[col],
                duplicates="drop",
                include_lowest=True,
                right=False,
            )
        X[column_names] = X[column_names].astype(str)
        return X

    def bin_inplace(
        self,
        X: DataFrame,
        bins_dict: pd.DataFrame,
        labels: Dict[str, str],
        columns: List[str],
        column_names: List[str],
    ) -> DataFrame:
        """Add in-place the binned columns to the input Dask dataframe.

        Parameters
        ----------
        X : DataFrame
            Input dataframe.
        bins_dict : pd.DataFrame
            Dictionary of bins_dict. The keys are the column names, the values are the split arrays.
        labels : Dict[str, str]
            Dictionary of labels. The keys are the column names, the values are the label arrays.
        columns : List[str]
            List of columns.
        column_names : List[str]
             List of output columns, only used where `inplace=True`.

        Returns
        -------
        DataFrame
            Transformed dataframe.
        """
        for name, col in zip(column_names, columns):
            X[col] = (
                X[col]
                .map_partitions(
                    pd.cut,
                    bins=bins_dict[col],
                    labels=labels[col],
                    duplicates="drop",
                    include_lowest=True,
                    right=False,
                )
                .astype(object)
            )
        X[columns] = X[columns].astype(str)
        return X


def get_bin(X: DataFrame) -> Union[BinPandas, BinKoalas, BinDask]:
    """Return the `Bin` class based on the dataframe library.

    Parameters
    ----------
    X : DataFrame
        Dataframe.

    Returns
    -------
    Union[BinPandas, BinKoalas, BinDask]
        `Bin` class assocaited to the dataframe librarry.
    """
    factories = {
        "<class 'pandas.core.frame.DataFrame'>": BinPandas(),
        "<class 'databricks.koalas.frame.DataFrame'>": BinKoalas(),
        "databricks.koalas.frame.DataFrame": BinKoalas(),  # needed for python3.6
        "<class 'dask.dataframe.core.DataFrame'>": BinDask(),
    }
    return factories[str(type(X))]
