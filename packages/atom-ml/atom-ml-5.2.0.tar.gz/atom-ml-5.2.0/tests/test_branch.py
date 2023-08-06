# -*- coding: utf-8 -*-

"""
Automated Tool for Optimized Modelling (ATOM)
Author: Mavs
Description: Unit tests for branch.py

"""

import pandas as pd
import pytest

from atom import ATOMClassifier, ATOMRegressor
from atom.branch import Branch
from atom.utils import merge

from .conftest import (
    X10, X10_str, X_bin, X_bin_array, X_class, X_idx, y10, y10_str, y_bin,
    y_bin_array, y_idx, y_multiclass,
)


# Test magic methods =============================================== >>

def test_init_pipeline_to_empty_series():
    """Assert that when starting atom, the estimators are empty."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    assert atom.branch.pipeline.empty


def test_init_attrs_are_passed():
    """Assert that the attributes from the parent are passed."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    atom.balance()
    atom.branch = "b2"
    assert atom.b2._idx is not atom.master._idx
    assert atom.b2.adasyn is atom.master.adasyn


def test_repr():
    """Assert that the __repr__  method returns the list of available branches."""
    branch = Branch(name="master")
    assert str(branch) == "Branch(master)"


def test_bool():
    """Assert that the __bool__  method checks if there's data."""
    branch = Branch(name="master")
    assert not branch
    branch = Branch(name="master", data=X_bin)
    assert branch


# Test name property =============================================== >>

def test_name_empty_name():
    """Assert that an error is raised when name is empty."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    with pytest.raises(ValueError, match=".*can't have an empty name!.*"):
        atom.branch.name = ""


def test_name_model_name():
    """Assert that an error is raised when name is a model's acronym."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    with pytest.raises(ValueError, match=".*model's acronym.*"):
        atom.branch.name = "Lda"


def test_name_setter():
    """Assert that the branch name changes correctly."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    atom.branch.name = "b1"
    assert atom.branch.name == "b1"
    assert atom.branch.pipeline.name == "b1"


# Test data properties ============================================= >>

def test_pipeline_property():
    """Assert that the pipeline property returns the current pipeline."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    atom.scale()
    assert len(atom.branch.pipeline) == 1


def test_mapping_property():
    """Assert that the dataset property returns the target's mapping."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    assert atom.branch.mapping == {}


def test_dataset_property():
    """Assert that the dataset property returns the data in the branch."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    assert atom.branch.dataset is atom.branch._data


def test_train_property():
    """Assert that the train property returns the training set."""
    atom = ATOMClassifier(X_bin, y_bin, test_size=0.3, random_state=1)
    n_rows, ncols = int((1 - 0.3) * len(X_bin)) + 1, X_bin.shape[1] + 1
    assert atom.branch.train.shape == (n_rows, ncols)


def test_test_property():
    """Assert that the test property returns the test set."""
    atom = ATOMClassifier(X_bin, y_bin, test_size=0.3, random_state=1)
    assert atom.branch.test.shape == (int(0.3 * len(X_bin)), X_bin.shape[1] + 1)


def test_holdout_property():
    """Assert that the holdout property returns a transformed holdout set."""
    atom = ATOMClassifier(X_bin, y_bin, holdout_size=0.1, random_state=1)
    atom.scale()
    assert not atom.holdout.equals(atom.branch.holdout)


def test_X_property():
    """Assert that the X property returns the feature set."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    assert atom.branch.X.shape == (len(X_bin), X_bin.shape[1])


def test_y_property():
    """Assert that the y property returns the target column."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    assert atom.branch.y.shape == (len(y_bin),)


def test_X_train_property():
    """Assert that the X_train property returns the training feature set."""
    test_size = 0.3
    atom = ATOMClassifier(X_bin, y_bin, test_size=test_size, random_state=1)
    nrows, ncols = int((1 - test_size) * len(X_bin)) + 1, X_bin.shape[1]
    assert atom.branch.X_train.shape == (nrows, ncols)


def test_X_test_property():
    """Assert that the X_test property returns the test feature set."""
    test_size = 0.3
    atom = ATOMClassifier(X_bin, y_bin, test_size=test_size, random_state=1)
    assert atom.branch.X_test.shape == (int(test_size * len(X_bin)), X_bin.shape[1])


def test_y_train_property():
    """Assert that the y_train property returns the training target column."""
    test_size = 0.3
    atom = ATOMClassifier(X_bin, y_bin, test_size=test_size, random_state=1)
    assert atom.branch.y_train.shape == (int((1 - test_size) * len(X_bin)) + 1,)


def test_y_test_property():
    """Assert that the y_test property returns the training target column."""
    test_size = 0.3
    atom = ATOMClassifier(X_bin, y_bin, test_size=test_size, random_state=1)
    assert atom.branch.y_test.shape == (int(test_size * len(X_bin)),)


def test_shape_property():
    """Assert that the shape property returns the shape of the dataset."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    assert atom.branch.shape == (len(X_bin), X_bin.shape[1] + 1)


def test_columns_property():
    """Assert that the columns property returns the columns of the dataset."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    assert list(atom.branch.columns) == list(X_bin.columns) + [y_bin.name]


def test_n_columns_property():
    """Assert that the n_columns property returns the number of columns."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    assert atom.branch.n_columns == len(X_bin.columns) + 1


def test_features_property():
    """Assert that the features property returns the features of the dataset."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    assert list(atom.branch.features) == list(X_bin.columns)


def test_n_features_property():
    """Assert that the n_features property returns the number of features."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    assert atom.branch.n_features == len(X_bin.columns)


def test_target_property():
    """Assert that the target property returns the last column in the dataset."""
    atom = ATOMRegressor(X_bin, "mean radius", random_state=1)
    assert atom.branch.target == "mean radius"


# Test property setters ============================================ >>

def test_dataset_setter():
    """Assert that the dataset setter changes the whole dataset."""
    new_dataset = merge(X_bin, y_bin)
    new_dataset.iat[0, 3] = 4  # Change one value

    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    atom.dataset = new_dataset
    assert atom.dataset.iat[0, 3] == 4  # Check the value is changed


def test_train_setter():
    """Assert that the train setter changes the training set."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    atom.train = atom.train.iloc[:100, :]
    assert atom.train.shape == (100, X_bin.shape[1] + 1)


def test_test_setter():
    """Assert that the test setter changes the test set."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    atom.test = atom.test.iloc[:100, :]
    assert atom.test.shape == (100, X_bin.shape[1] + 1)


def test_X_setter():
    """Assert that the X setter changes the feature set."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    atom.X = atom.X.iloc[:, :10]
    assert atom.X.shape == (len(X_bin), 10)


def test_y_setter():
    """Assert that the y setter changes the target column."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    assert atom.y[0] == 0  # First value is 1 in original
    atom.y = [1] + list(y_bin.values[1:])
    assert atom.y[0] == 1  # First value changed to 0


def test_X_train_setter():
    """Assert that the X_train setter changes the training feature set."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    new_X_train = atom.X_train
    new_X_train.iat[0, 0] = 999
    atom.X_train = new_X_train.to_numpy()  # To numpy to test dtypes are maintained
    assert atom.X_train.iat[0, 0] == 999
    assert list(atom.X_train.dtypes) == list(atom.X_test.dtypes)


def test_X_test_setter():
    """Assert that the X_test setter changes the test feature set."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    new_X_test = atom.X_test
    new_X_test.iat[0, 0] = 999
    atom.X_test = new_X_test
    assert atom.X_test.iat[0, 0] == 999


def test_y_train_setter():
    """Assert that the y_train setter changes the training target column."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    assert atom.y_train.iat[0] == 0  # First value is 1 in original
    atom.y_train = [1] + list(atom.y_train.values[1:])
    assert atom.y_train.iat[0] == 1  # First value changed to 0


def test_y_test_setter():
    """Assert that the y_test setter changes the training target column."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    assert atom.y_test.iat[0] == 1  # First value is 0 in original
    atom.y_test = [0] + list(atom.y_test[1:])
    assert atom.y_test.iat[0] == 0  # First value changed to 1


def test_data_properties_to_df():
    """Assert that the data attributes are converted to a df at setter."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    atom.X = X_bin_array
    assert isinstance(atom.X, pd.DataFrame)


def test_data_properties_to_series():
    """Assert that the data attributes are converted to a series at setter."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    atom.y = y_bin_array
    assert isinstance(atom.y, pd.Series)


def test_setter_error_unequal_rows():
    """Assert that an error is raised when the setter has unequal rows."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    with pytest.raises(ValueError, match="number of rows"):
        atom.X_train = X_bin


def test_setter_error_unequal_index():
    """Assert that an error is raised when the setter has unequal indices."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    with pytest.raises(ValueError, match="the same indices"):
        atom.y = pd.Series(y_bin_array, index=range(10, len(y_bin_array) + 10))


def test_setter_error_unequal_columns():
    """Assert that an error is raised when the setter has unequal columns."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    with pytest.raises(ValueError, match="number of columns"):
        new_X = atom.train
        new_X.insert(0, "new_column", 1)
        atom.train = new_X


def test_setter_error_unequal_column_names():
    """Assert that an error is raised with different column names."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    with pytest.raises(ValueError, match="the same columns"):
        new_X = atom.train.drop(atom.train.columns[0], axis=1)
        new_X.insert(0, "new_column", 1)
        atom.train = new_X


def test_setter_error_unequal_target_names():
    """Assert that an error is raised with different target names."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    with pytest.raises(ValueError, match="the same name"):
        new_y_train = atom.y_train
        new_y_train.name = "different_name"
        atom.y_train = new_y_train


# Test utility methods ============================================= >>

def test_get_rows_is_None():
    """Assert that all indices are returned."""
    atom = ATOMClassifier(X_idx, y_idx, index=True, random_state=1)
    assert len(atom.branch._get_rows(index=None, return_test=True)) < len(X_idx)
    assert len(atom.branch._get_rows(index=None, return_test=False)) == len(X_idx)


def test_get_rows_is_slice():
    """Assert that a slice of rows is returned."""
    atom = ATOMClassifier(X_idx, y_idx, index=True, random_state=1)
    assert len(atom.branch._get_rows(index=slice(20, 100, 2))) == 40


def test_get_rows_by_exact_match():
    """Assert that a row can be selected by name."""
    atom = ATOMClassifier(X_idx, y_idx, index=True, random_state=1)
    assert atom.branch._get_rows(index="index_23") == ["index_23"]


def test_get_rows_by_int():
    """Assert that rows can be retrieved by their index position."""
    atom = ATOMClassifier(X_idx, y_idx, index=True, random_state=1)
    with pytest.raises(ValueError, match=".*out of range.*"):
        atom.branch._get_rows(index=1000)
    assert atom.branch._get_rows(index=100) == [atom.X.index[100]]


def test_get_rows_by_str():
    """Assert that rows can be retrieved by name or regex."""
    atom = ATOMClassifier(X_idx, y_idx, index=True, random_state=1)
    assert len(atom.branch._get_rows(index="index_34+index_58")) == 2
    assert len(atom.branch._get_rows(index=["index_34+index_58", "index_57"])) == 3
    assert len(atom.branch._get_rows(index="index_3.*")) == 111
    assert len(atom.branch._get_rows(index="!index_3")) == len(X_idx) - 1
    assert len(atom.branch._get_rows(index="!index_3.*")) == len(X_idx) - 111
    with pytest.raises(ValueError, match=".*any row that matches.*"):
        atom.branch._get_rows(index="invalid")


def test_get_rows_invalid_type():
    """Assert that an error is raised when the type is invalid."""
    atom = ATOMClassifier(X_idx, y_idx, index=True, random_state=1)
    with pytest.raises(TypeError, match=".*Invalid type for the index.*"):
        atom.branch._get_rows(index=[3.2])


def test_get_rows_none_selected():
    """Assert that an error is raised when no rows are selected."""
    atom = ATOMClassifier(X_idx, y_idx, index=True, random_state=1)
    with pytest.raises(ValueError, match=".*has to be selected.*"):
        atom.branch._get_rows(index=slice(1000, 2000))


def test_get_rows_include_or_exclude():
    """Assert that an error is raised when rows are included and excluded."""
    atom = ATOMClassifier(X_idx, y_idx, index=True, random_state=1)
    with pytest.raises(ValueError, match=".*either include or exclude rows.*"):
        atom.branch._get_rows(index=["index_34", "!index_36"])


def test_get_columns_is_None():
    """Assert that all columns are returned."""
    atom = ATOMClassifier(X10_str, y10, random_state=1)
    assert len(atom.branch._get_columns(columns=None)) == 5
    assert len(atom.branch._get_columns(columns=None, only_numerical=True)) == 4
    assert len(atom.branch._get_columns(columns=None, include_target=False)) == 4


def test_get_columns_by_slice():
    """Assert that a slice of columns is returned."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    assert len(atom.branch._get_columns(columns=slice(2, 6))) == 4


def test_get_columns_by_int():
    """Assert that columns can be retrieved by index."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    with pytest.raises(ValueError, match=".*out of range for a dataset.*"):
        atom.branch._get_columns(columns=40)
    assert atom.branch._get_columns(columns=0) == ["mean radius"]


def test_get_columns_by_str():
    """Assert that columns can be retrieved by name or regex."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    assert len(atom.branch._get_columns("mean radius+mean texture")) == 2
    assert len(atom.branch._get_columns(["mean radius+mean texture", "mean area"])) == 3
    assert len(atom.branch._get_columns("mean .*")) == 10
    assert len(atom.branch._get_columns("!mean radius")) == X_bin.shape[1]
    assert len(atom.branch._get_columns("!mean .*")) == X_bin.shape[1] - 9
    with pytest.raises(ValueError, match=".*any column that matches.*"):
        atom.branch._get_columns("invalid")


def test_get_columns_by_type():
    """Assert that columns can be retrieved by type."""
    atom = ATOMClassifier(X10_str, y10, random_state=1)
    assert len(atom.branch._get_columns(columns="number")) == 4
    assert len(atom.branch._get_columns(columns="!number")) == 1


def test_get_columns_invalid_type():
    """Assert that an error is raised when the type is invalid."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    with pytest.raises(TypeError, match=".*Invalid type for the columns.*"):
        atom.branch._get_columns(columns=[3.2])


def test_get_columns_exclude():
    """Assert that columns can be excluded using `!`."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    with pytest.raises(ValueError, match=".*not find any column.*"):
        atom.branch._get_columns(columns="!invalid")
    assert len(atom.branch._get_columns(columns="!mean radius")) == 30
    assert len(atom.branch._get_columns(columns=["!mean radius", "!mean texture"])) == 29


def test_get_columns_none_selected():
    """Assert that an error is raised when no columns are selected."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    with pytest.raises(ValueError, match=".*At least one column.*"):
        atom.branch._get_columns(columns="datetime")


def test_get_columns_include_or_exclude():
    """Assert that an error is raised when cols are included and excluded."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    with pytest.raises(ValueError, match=".*either include or exclude columns.*"):
        atom.branch._get_columns(columns=["mean radius", "!mean texture"])


def test_get_columns_return_inc_exc():
    """Assert that included and excluded columns can be returned."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    assert isinstance(atom.branch._get_columns("number", return_inc_exc=True), tuple)


def test_get_columns_remove_duplicates():
    """Assert that duplicate columns are ignored."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    assert atom.branch._get_columns(columns=[0, 1, 0]) == ["mean radius", "mean texture"]


def test_get_target_column():
    """Assert that the target column can be retrieved."""
    atom = ATOMClassifier(X_class, y=y_multiclass, random_state=1)
    assert atom.branch._get_target(target="c", only_columns=True) == "c"
    assert atom.branch._get_target(target=1, only_columns=True) == "b"


def test_get_target_column_str_invalid():
    """Assert that an error is raised when the column is invalid."""
    atom = ATOMClassifier(X_class, y=y_multiclass, random_state=1)
    with pytest.raises(ValueError, match=".*is not one of the target columns.*"):
        atom.branch._get_target(target="invalid", only_columns=True)


def test_get_target_column_int_invalid():
    """Assert that an error is raised when the column is invalid."""
    atom = ATOMClassifier(X_class, y=y_multiclass, random_state=1)
    with pytest.raises(ValueError, match=".*There are 3 target columns.*"):
        atom.branch._get_target(target=3, only_columns=True)


def test_get_target_class():
    """Assert that the target class can be retrieved."""
    atom = ATOMClassifier(X10, y10_str, random_state=1)
    atom.clean()
    assert atom.branch._get_target(target="y")[1] == 1
    assert atom.branch._get_target(target=0)[1] == 0


def test_get_target_class_str_invalid():
    """Assert that an error is raised when the target is invalid."""
    atom = ATOMClassifier(X10, y10_str, random_state=1)
    with pytest.raises(ValueError, match=".*not found in the mapping.*"):
        atom.branch._get_target(target="invalid")


def test_get_target_class_int_invalid():
    """Assert that an error is raised when the value is invalid."""
    atom = ATOMClassifier(X10, y10_str, random_state=1)
    with pytest.raises(ValueError, match=".*There are 2 classes.*"):
        atom.branch._get_target(target=3)


def test_get_target_tuple_no_multioutput():
    """Assert that the target class can be retrieved."""
    atom = ATOMClassifier(X10, y10_str, random_state=1)
    with pytest.raises(ValueError, match=".*only accepted for multioutput tasks.*"):
        atom.branch._get_target(target=(2, 1))


def test_get_target_tuple():
    """Assert that the target column and class can be retrieved."""
    atom = ATOMClassifier(X_class, y=y_multiclass, random_state=1)
    assert atom.branch._get_target(target=(2,)) == (2, 0)
    assert atom.branch._get_target(target=("a", 2)) == (0, 2)


def test_get_target_tuple_invalid_length():
    """Assert that the target class can be retrieved."""
    atom = ATOMClassifier(X_class, y=y_multiclass, random_state=1)
    with pytest.raises(ValueError, match=".*a tuple of length 2.*"):
        atom.branch._get_target(target=(2, 1, 2))
