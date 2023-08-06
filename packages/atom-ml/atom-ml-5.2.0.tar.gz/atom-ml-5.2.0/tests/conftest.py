# -*- coding: utf-8 -*-

"""
Automated Tool for Optimized Modelling (ATOM)
Author: Mavs
Description: Global fixtures and variables for the tests.

"""

from __future__ import annotations

from typing import Callable

import numpy as np
import pandas as pd
import pytest
from sklearn.datasets import (
    load_breast_cancer, load_diabetes, load_wine,
    make_multilabel_classification,
)
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle

from atom.utils import (
    DATAFRAME, FEATURES, TARGET, merge, n_cols, to_df, to_pandas,
)


class DummyTransformer:
    """Transformer class for testing name keeping of arrays.

    Parameters
    ----------
    strategy: str
        What to do with the feature set during transformation.
        Choose from:

        - "equal": Return the dataset unchanged.
        - "drop" Drop a column from the dataset.
        - "add": Add a column to the dataset.

    """

    def __init__(self, strategy: str):
        self.strategy = strategy

    def transform(self, X: DATAFRAME) -> np.ndarray:
        if self.strategy == "equal":
            return X.to_numpy()
        elif self.strategy == "drop":
            return X.drop(X.columns[1], axis=1).to_numpy()
        elif self.strategy == "add":
            X["new_col"] = list(range(len(X)))
            return X.to_numpy()


@pytest.fixture(autouse=True)
def change_current_dir(tmp_path: Callable, monkeypatch: Callable):
    """Changes the directory of the test to a temporary dir."""
    monkeypatch.chdir(tmp_path)


def get_train_test(X: FEATURES, y: TARGET) -> tuple[DATAFRAME, DATAFRAME]:
    """Get train and test sets from X and y.

    Parameters
    ----------
    X: dataframe-like
        Feature set.

    y: int, str, dict, sequence or dataframe
        Target column corresponding to X.

    Returns
    -------
    dataframe
        Training set.

    dataframe
        Test set.

    """
    return train_test_split(
        merge(to_df(X), to_pandas(y, columns=[f"y{i}" for i in range(n_cols(y))])),
        test_size=0.3,
        random_state=1,
    )


# Sklearn datasets as np.array
X_bin_array, y_bin_array = load_breast_cancer(return_X_y=True)

# Sklearn datasets for all three tasks as pd.DataFrame
X_bin, y_bin = load_breast_cancer(return_X_y=True, as_frame=True)
X_class, y_class = load_wine(return_X_y=True, as_frame=True)
X_reg, y_reg = load_diabetes(return_X_y=True, as_frame=True)

# Multilabel classification data
X_label, y_label = make_multilabel_classification(n_samples=100, n_classes=3)

# Sparse data
X_sparse = pd.DataFrame(
    data={
        "feature 1": pd.arrays.SparseArray([1, 0, 0, 0, 0, 0, 1, 0, 1, 0]),
        "feature 2": pd.arrays.SparseArray([1, 0, 1, 0, 0, 1, 0, 0, 1, 0]),
        "feature 3": pd.arrays.SparseArray([1, 1, 1, 0, 0, 0, 1, 0, 0, 0]),
    }
)

# Text data
X_text = [
    ["I àm in ne'w york"],
    ["New york is nice"],
    ["hi new york"],
    ["hi hello test"],
    ["oui si 12"],
    ["new york vs washington"],
    ["this is a random test"],
    ["test is random this"],
    ["nice random test"],
    ["test target for text"],
]

# Dataset wth string indices
X_idx = X_bin.set_index(pd.Index([f"index_{i}" for i in range(len(X_bin))]))
y_idx = y_bin.set_axis(X_idx.index)

# Small dimensional dataset
X10 = [
    [0.2, 2, 1],
    [0.2, 2, 1],
    [0.2, 2, 2],
    [0.24, 2, 1],
    [0.23, 2, 2],
    [0.19, 0.01, 1],
    [0.21, 3, 2],
    [0.2, 2, 1],
    [0.2, 2, 1],
    [0.2, 2, 0.01],
]

# Dataset with missing value
X10_nan = [
    [np.NaN, 2, 1],
    [0.2, 2, 1],
    [4, 2, 2],
    [3, 2, 1],
    [3, 2, 2],
    [1, 0, 1],
    [0, 3, 2],
    [4, np.NaN, 1],
    [5, 2, 1],
    [3, 2, 0],
]

# Dataset with categorical column
X10_str = [
    [1, 0, "b", 2],
    [1, 3, "a", 1],
    [0, 2, "b", 5],
    [1, 2, "a", 1],
    [1, 2, "c", 7],
    [0, 0, "d", 5],
    [1, 3, "d", 1],
    [0, 2, "d", 2],
    [1, 2, "a", 3],
    [1, 2, "d", 2],
]

# Dataset with categorical column (only two classes)
X10_str2 = [
    [2, 0, "a", True],
    [2, 3, "a", False],
    [5, 2, "b", True],
    [1, 2, "a", True],
    [1, 2, "a", False],
    [2, 0, "a", False],
    [2, 3, "b", False],
    [5, 2, "b", True],
    [1, 2, "a", True],
    [1, 2, "a", False],
]

# Dataset with missing value in categorical column
X10_sn = [
    [2, 0, np.NaN],
    [2, 3, "a"],
    [5, 2, "b"],
    [1, 2, "a"],
    [1, 2, "c"],
    [2, 0, "d"],
    [2, 3, "d"],
    [5, 2, "d"],
    [1, 2, "a"],
    [1, 2, "d"],
]

# Dataset with dates
X10_dt = [
    [2, "21", "13/02/2021", 4],
    [2, "12", "31/3/2020", 22],
    [5, "06", "30/3/2020", 21],
    [1, "03", "31/5/2020", 2],
    [1, "202", np.NaN, 4],
    [2, "11", "06/6/2000", 6],
    [2, "01", "31/3/2020", 7],
    [5, "22", "9/12/2020", 6],
    [1, "24", "5/11/2020", 8],
    [1, "00", "22/03/2018", 9],
]

# Dataset with outliers
X20_out = [
    [2, 0, 2],
    [2, 3, 1],
    [3, 2, 2],
    [1, 2, 1],
    [1, 2, 1],
    [1, 2, 1],
    [1, 2, 1],
    [1, 2, 1],
    [1, 2, 1],
    [1, 2, 1],
    [1, 2, 1],
    [1, 2, 1],
    [1, 2, 1],
    [1, 2, 1],
    [1, 1e6, 2],
    [2, 0, 2],
    [2, 3, 2],
    [3, 2, 1],
    [1, 2, 2],
    [1e6, 2, 1],
]

# Target columns (int, missing, categorical and mixed)
y10 = [0, 1, 0, 1, 1, 0, 1, 0, 1, 1]
y10_nan = [0, 1, 0, np.NaN, 1, 0, 1, 0, 1, 1]
y10_str = ["y", "n", "y", "y", "n", "y", "n", "y", "n", "n"]
y10_sn = ["y", "n", np.NaN, "y", "n", "y", "n", "y", "n", "n"]

y10_label = [
    ["politics"],
    ["finance", "religion"],
    ["education", "finance", "politics"],
    [],
    ["finance"],
    ["finance", "religion"],
    ["finance"],
    ["finance", "religion"],
    ["education"],
    ["finance", "politics", "religion"],
]

# Multilabel data with categorical
y10_label2 = merge(
    pd.Series(shuffle(y10, random_state=1), name="a"),
    pd.Series(shuffle(y10_str, random_state=2), name="b"),
    pd.Series(shuffle(y10_str, random_state=3), name="c"),
)


# Multiclass-multioutput classification data
y_multiclass = merge(
    pd.Series(shuffle(y_class.values, random_state=1), name="a"),
    pd.Series(shuffle(y_class.values, random_state=2), name="b"),
    pd.Series(shuffle(y_class.values, random_state=3), name="c"),
)

# Multioutput regression data
y_multireg = merge(
    pd.Series(shuffle(y_reg.values, random_state=1), name="a"),
    pd.Series(shuffle(y_reg.values, random_state=2), name="b"),
    pd.Series(shuffle(y_reg.values, random_state=3), name="c"),
)

# Train and test sets per task
bin_train, bin_test = get_train_test(X_bin, y_bin)
class_train, class_test = get_train_test(X_class, y_class)
reg_train, reg_test = get_train_test(X_reg, y_reg)
label_train, label_test = get_train_test(X_label, y_label)
