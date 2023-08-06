"""Tests the `infer_feature_attributes` package."""
from collections import OrderedDict
from copy import copy
import datetime
import json
from pathlib import Path
import warnings

from diveplane.utilities.feature_attributes import infer_feature_attributes
from diveplane.utilities.feature_attributes.pandas import InferFeatureAttributesDataFrame
from diveplane.utilities.features import FeatureType
import numpy as np
import pandas as pd
import pytest
import pytz


cwd = Path(__file__).parent.parent.parent.parent
iris_path = Path(cwd, 'utilities', 'tests', 'data', 'iris.csv')
int_path = Path(cwd, 'utilities', 'tests', 'data', 'integers.csv')
stock_path = Path(cwd, 'utilities', 'tests', 'data', 'mini_stock_data.csv')

# Partially defined dictionary-1
features_1 = {
    "sepal_length": {
        "type": "continuous",
        'bounds': {
            'min': 2.72,
            'max': 3,
            'allow_null': True
        },
    },
    "sepal_width": {
        "type": "continuous"
    }
}

# Partially defined dictionary-2
features_2 = {
    "sepal_length": {
        "type": "continuous"
    },
    "sepal_width": {
        "type": "continuous"
    }
}

# Partially defined dictionary-3
features_3 = {
    "sepal_length": {
        "type": "nominal"
    },
    "sepal_width": {
        "type": "continuous"
    }
}

# Partially defined "ordered" dict
features_4 = OrderedDict(
    (f_name, features_3[f_name]) for f_name in features_3
)


def test_infer_features_attributes():
    """Litmus test for infer feature types for iris dataset."""
    df = pd.read_csv(iris_path)

    expected_types = {
        "sepal_length": "continuous",
        "sepal_width": "continuous",
        "petal_length": "continuous",
        "petal_width": "continuous",
        "class": "nominal"
    }

    features = infer_feature_attributes(df)

    for feature, attributes in features.items():
        assert expected_types[feature] == attributes['type']


@pytest.mark.parametrize(
    "features",
    [features_1, features_2, features_3, features_4]
)
def test_partially_filled_feature_types(features: dict) -> None:
    """
    Make sure the partially filled feature types remain intact.

    Parameters
    ----------
    df: pandas.DataFrame
    features
    """
    df = pd.read_csv(iris_path)
    pre_inferred_features = features.copy()

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        inferred_features = infer_feature_attributes(df, features=features)

    for k, v in pre_inferred_features.items():
        assert v['type'] == inferred_features[k]['type']

        if 'bounds' in v:
            # Make sure the bounds are not altered
            # by _process()
            assert v['bounds'] == inferred_features[k]['bounds']


@pytest.mark.parametrize(
    'feature, nominality', [
        # "id_no" _would_ be inferred "continuous", but we specifically tell
        # `_process()` that it is indeed an ID feature, so it
        # will be set to "nominal".
        ('id_no', 'nominal'),

        # The "badge_no" feature contains ALL unique values so it exceeds the
        # sqrt(total num. rows) test, but they are all the same length
        # integers, so it passes "all the same length" check.
        ('badge_no', 'nominal'),

        # The "salary" feature has mostly uniques (some duplicates) but too
        # many that it readily exceeds the threshold of sqrt(total num. rows)
        # and they are not all the same length, so, "continuous".
        ('salary', 'continuous'),

        # The "dept_no" feature has a number of uniques that exceed the
        # sqrt(total num. rows) but all the integers are the same length,
        # so "nominal".
        ('dept_no', 'nominal'),

        # This column is all None, will be returned as "continuous".
        ('hat_size', 'continuous'),
    ]
)
def test_integer_nominality(feature, nominality):
    """Exercise infer_feature_attributes for integers and their nominality."""
    df = pd.read_csv(int_path)
    inferred_features = infer_feature_attributes(df, id_feature_name=['id_no'])
    assert inferred_features[feature]['type'] == nominality


@pytest.mark.parametrize("data, expected_type", [
    # Integer
    (pd.DataFrame([[1], [None]], dtype='Int8', columns=['a']),
     {'data_type': str(FeatureType.INTEGER), 'size': 1}),
    (pd.DataFrame([[1], [16]], dtype='int', columns=['a']),
     {'data_type': str(FeatureType.INTEGER), 'size': 8}),
    # Float
    (pd.DataFrame([[1.0], [4.4]], dtype='float', columns=['a']),
     {'data_type': str(FeatureType.NUMERIC), 'size': 8}),
    (pd.DataFrame([[None], [4.4]], dtype='float32', columns=['a']),
     {'data_type': str(FeatureType.NUMERIC), 'size': 4}),
    # Boolean
    (pd.DataFrame([[True], [False], [None]], dtype='bool', columns=['a']),
     {'data_type': str(FeatureType.BOOLEAN)}),
    # String
    (pd.DataFrame([["test"], [None]], columns=['a']),
     {'data_type': str(FeatureType.STRING)}),
    (pd.DataFrame([["test"], [None]], dtype='string', columns=['a']),
     {'data_type': str(FeatureType.STRING)}),
    (pd.DataFrame([["test"], [None]], dtype=np.string_, columns=['a']),
     {'data_type': str(FeatureType.STRING)}),
    (pd.DataFrame([["test"]], dtype='S', columns=['a']),
     {'data_type': str(FeatureType.STRING)}),
    (pd.DataFrame([["test"]], dtype='U', columns=['a']),
     {'data_type': str(FeatureType.STRING)}),
    # Datetime
    (pd.DataFrame([["2020-01-01T10:00:00"]], dtype='datetime64[ns]', columns=['a']),
     {'data_type': str(FeatureType.DATETIME)}),
    (pd.DataFrame([["2020-01-01"]], dtype='datetime64[ns]', columns=['a']),
     {'data_type': str(FeatureType.DATETIME)}),
    (pd.DataFrame([[datetime.datetime.now()]], columns=['a']),
     {'data_type': str(FeatureType.DATETIME)}),
    (pd.DataFrame([[datetime.datetime.now(pytz.timezone('US/Eastern'))]], columns=['a']),
     {'data_type': str(FeatureType.DATETIME), 'timezone': 'US/Eastern'}),
    (pd.DataFrame([[datetime.datetime.now(pytz.FixedOffset(300))]], columns=['a']),
     {'data_type': str(FeatureType.DATETIME)}),
    # Date
    (pd.DataFrame([[datetime.date(2020, 1, 1)]], columns=['a']),
     {'data_type': str(FeatureType.DATE)}),
    # Timedelta
    (pd.DataFrame([[datetime.timedelta(days=1)]], columns=['a']),
     {'data_type': str(FeatureType.TIMEDELTA), 'unit': 'seconds'}),
    (pd.DataFrame([[np.timedelta64(5, 'D')]], columns=['a']),
     {'data_type': str(FeatureType.TIMEDELTA), 'unit': 'seconds'}),
    (pd.DataFrame([[np.timedelta64(5, 'Y')]], columns=['a']),
     {'data_type': str(FeatureType.TIMEDELTA), 'unit': 'seconds'}),
    (pd.DataFrame([[np.timedelta64(5000, 'ns')]], columns=['a']),
     {'data_type': str(FeatureType.TIMEDELTA), 'unit': 'seconds'}),
    (pd.DataFrame([[np.timedelta64(5000, 's')]], columns=['a']),
     {'data_type': str(FeatureType.TIMEDELTA), 'unit': 'seconds'}),
    (pd.DataFrame([[np.timedelta64(60, 'm')]], columns=['a']),
     {'data_type': str(FeatureType.TIMEDELTA), 'unit': 'seconds'}),
])
def test_get_feature_type(data, expected_type):
    """Test get_feature_type returns expected data types."""
    infer = InferFeatureAttributesDataFrame(data)
    feature_type, original_type = infer._get_feature_type('a')
    expected_feature_type = expected_type.pop('data_type')
    assert str(feature_type) == expected_feature_type
    assert original_type == expected_type


@pytest.mark.parametrize('data, data_type', [
    (123, 'float128'),
])
def test_get_feature_type_raises(data, data_type):
    """Test get_feature_type raises exception."""
    # Place this here to avoid circular import
    from diveplane.client.exceptions import DiveplaneError
    if not hasattr(np, data_type):
        pytest.skip('Unsupported platform')

    with pytest.raises(DiveplaneError):
        df = pd.DataFrame([[getattr(np, data_type)(data)]], columns=['a'])
        infer_feature_attributes(df)


@pytest.mark.parametrize('should_fail, data', [
    (True, [[1]]),
    (True, {3: [1]}),
    (False, {'col1': [1]}),
])
def test_column_names(should_fail, data):
    """Test invalid column names raises."""
    df = pd.DataFrame(data)
    if should_fail:
        expected_msg = r"Unexpected DataFrame column name format"
        with pytest.raises(ValueError, match=expected_msg):
            infer_feature_attributes(df)
    else:
        features = infer_feature_attributes(df)
        assert features is not None


@pytest.mark.parametrize('should_include, base_features, dependent_features', [
    (False, None, None),
    (True, None, {'sepal_length': ['sepal_width', 'class']}),
    (True, {"sepal_length": {"type": "continuous"}},
     {'sepal_width': ['sepal_length']}),
    (True, {"sepal_length": {"type": "continuous"}},
     {'sepal_length': ['class']}),
    (False, {"sepal_length": {"type": "continuous"}},
     None),
    (True, {"sepal_length": {"dependent_features": ["class"]}},
     None),
])
def test_dependent_features(should_include, base_features, dependent_features):
    """Test depdendent features are added to feature attributes dict."""
    df = pd.read_csv(iris_path)
    features = infer_feature_attributes(df, features=base_features, dependent_features=dependent_features)

    if should_include:
        # Should include dependent features
        if dependent_features:
            for feat, dep_feats in dependent_features.items():
                assert 'dependent_features' in features[feat]
                for dep_feat in dep_feats:
                    assert dep_feat in features[feat]['dependent_features']
        # Make sure dependent features provided in the base dict are also included
        if base_features:
            for feat in base_features.keys():
                if 'dependent_features' in base_features[feat]:
                    assert 'dependent_features' in features[feat]
                    for dep_feat in base_features[feat]['dependent_features']:
                        assert dep_feat in features[feat]['dependent_features']
    else:
        # Should not include dependent features
        for attributes in features.values():
            assert 'dependent_features' not in attributes


@pytest.mark.parametrize('is_tight, data, expected_bounds', [
    (False, [2, 3, 4, 5, 6, 7], {'min': 1, 'max': 7.38905609893065, 'allow_null': False}),
    (False, [2, 3, 4, 4, 5, 6, 6, 6, 6], {'min': 1, 'max': 6, 'allow_null': False}),
    (False, [2, 3, 4, 4, 4, 4, 6, 6, 6, 6], {'min': 1, 'max': 6, 'allow_null': False}),
    (False, [2, 2, 2, 2, 4, 5, 6, 6, 6, 6], {'min': 2, 'max': 6, 'allow_null': False}),
    (False, [2, 2, 2, 2, 4, 5, 6, 6, 6, 6, 6], {'min': 1, 'max': 6, 'allow_null': False}),
    (False, [2, 2, 2, 2, 4, 5, 6, 7], {'min': 2, 'max': 7.38905609893065, 'allow_null': False}),
    (True, [2, 3, 4, 5, 6, 7], {'min': 2, 'max': 7, 'allow_null': False}),
    (True, [2, 3, 4, None, 6, 7], {'min': 2, 'max': 7}),
    (
        True,
        ['1905-01-01', '1904-05-03', '2020-01-15', '2000-04-26', '2000-04-24'],
        {'min': '1904-05-03', 'max': '2020-01-15'}
    ),
    (
        False,
        ['1905-01-01', '1904-05-03', '2020-01-15', '2000-04-26', '2000-04-24'],
        {'min': '1856-05-25', 'max': '2083-08-08'}
    ),
    (
        False,
        ['1905-01-01', '1904-05-03', '2020-01-15', '2020-01-15', '2020-01-15',
         '2020-01-15', '2000-04-26', '2000-04-24'],
        {'min': '1856-05-25', 'max': '2020-01-15'}
    ),
    (
        False,
        ['1905-01-01', '1904-05-03', '1904-05-03', '1904-05-03', '1904-05-03',
         '2020-01-15', '2020-01-15', '2020-01-15', '2020-01-15', '2000-04-26',
         '2000-04-24'],
        {'min': '1904-05-03', 'max': '2020-01-15'}
    ),
    (
        False,
        ["1905-01-01T00:00:00+0100", "2022-03-26T00:00:00+0500",
         "1904-05-03T00:00:00+0500", "1904-05-03T00:00:00+0500",
         "1904-05-03T00:00:00+0500", "1904-05-03T00:00:00-0200",
         "1904-05-03T00:00:00+0500", "2022-01-15T00:00:00+0500"],
        {'min': '1904-05-03T00:00:00+0500', 'max': '2083-08-08T01:07:26+0500'}
    ),
    (
        True,
        [datetime.datetime(1905, 1, 1), datetime.datetime(1904, 5, 3),
         datetime.datetime(2020, 1, 15), datetime.datetime(2022, 3, 26)],
        {'min': '1904-05-03T00:00:00', 'max': '2022-03-26T00:00:00'}
    ),
    (
        False,
        [datetime.datetime(1905, 1, 1), datetime.datetime(1904, 5, 3),
         datetime.datetime(2020, 1, 15), datetime.datetime(2022, 3, 26)],
        {'min': '1856-05-25T22:52:33', 'max': '2083-08-08T01:07:26'}
    ),
    (
        False,
        [datetime.datetime(1905, 1, 1), datetime.datetime(1904, 5, 3),
         datetime.datetime(1904, 5, 3), datetime.datetime(1904, 5, 3),
         datetime.datetime(1904, 5, 3), datetime.datetime(1904, 5, 3),
         datetime.datetime(2020, 1, 15), datetime.datetime(2022, 3, 26)],
        {'min': '1904-05-03T00:00:00', 'max': '2083-08-08T01:07:26'}
    ),
    (
        False,
        [datetime.datetime(1905, 1, 1, tzinfo=pytz.FixedOffset(300)),
         datetime.datetime(1904, 5, 3, tzinfo=pytz.FixedOffset(300)),
         datetime.datetime(1904, 5, 3, tzinfo=pytz.FixedOffset(300)),
         datetime.datetime(1904, 5, 3, tzinfo=pytz.FixedOffset(300)),
         datetime.datetime(1904, 5, 3, tzinfo=pytz.FixedOffset(300)),
         datetime.datetime(1904, 5, 3, tzinfo=pytz.FixedOffset(300)),
         datetime.datetime(2020, 1, 15, tzinfo=pytz.FixedOffset(300)),
         datetime.datetime(2022, 3, 26, tzinfo=pytz.FixedOffset(300))],
        {'min': '1904-05-03T00:00:00+0500', 'max': '2083-08-08T01:07:26+0500'}
    ),
    (
        False,
        [datetime.datetime(1905, 1, 1, tzinfo=pytz.FixedOffset(100)),
         datetime.datetime(1904, 5, 3, tzinfo=pytz.FixedOffset(300)),
         datetime.datetime(1904, 5, 3, tzinfo=pytz.FixedOffset(-400)),
         datetime.datetime(1904, 5, 3, tzinfo=pytz.FixedOffset(300)),
         datetime.datetime(1904, 5, 3, tzinfo=pytz.FixedOffset(300)),
         datetime.datetime(1904, 5, 3, tzinfo=pytz.FixedOffset(300)),
         datetime.datetime(2020, 1, 15, tzinfo=pytz.FixedOffset(300)),
         datetime.datetime(2022, 3, 26, tzinfo=pytz.FixedOffset(300))],
        {'min': '1904-05-03T00:00:00+0500', 'max': '2083-08-08T01:07:26+0500'}
    ),
    (
        True,
        [datetime.timedelta(days=1), datetime.timedelta(days=1),
         datetime.timedelta(seconds=5), datetime.timedelta(days=1, seconds=30),
         datetime.timedelta(minutes=50), datetime.timedelta(days=5)],
        {'min': 5, 'max': 5 * 24 * 60 * 60}
    ),
    (
        False,
        [datetime.timedelta(days=1), datetime.timedelta(days=1),
         datetime.timedelta(seconds=5), datetime.timedelta(days=1, seconds=30),
         datetime.timedelta(minutes=50), datetime.timedelta(days=5),
         datetime.timedelta(days=5), datetime.timedelta(days=5),
         datetime.timedelta(days=5)],
        {'min': 2.718281828459045, 'max': 5 * 24 * 60 * 60}
    ),
    (
        False,
        [datetime.time(hour=1), datetime.time(hour=5),
         datetime.time(minute=1, second=30), datetime.time(minute=10),
         datetime.time(second=15), datetime.time(second=15),
         datetime.time(second=15), datetime.time(second=15)],
        {'min': 15, 'max': 22026.465794806718}
    ),
])
def test_infer_feature_bounds(data, is_tight, expected_bounds):
    """Test the infer_feature_bounds() method."""
    df = pd.DataFrame([[cell] for cell in data], columns=['a'])
    features = infer_feature_attributes(df, tight_bounds=is_tight)
    assert features['a']['type'] == 'continuous'
    assert 'bounds' in features['a']
    assert features['a']['bounds'] == expected_bounds


@pytest.mark.parametrize(
    "features",
    [features_1, features_2, features_3, features_4]
)
def test_to_json(features: dict) -> None:
    """Test that to_json() method returns a JSON representation of the object."""
    df = pd.read_csv(iris_path)
    pre_inferred_features = features.copy()

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        inferred_features = infer_feature_attributes(df, features=features)

    to_json = inferred_features.to_json()
    assert isinstance(to_json, str)
    features = json.loads(to_json)

    # Make sure the json representation has expected data
    for k, v in pre_inferred_features.items():
        assert v['type'] == features[k]['type']
        if 'bounds' in v:
            assert v['bounds'] == features[k]['bounds']


@pytest.mark.parametrize('partial_features', [
    {"sepal_length": {"type": "continuous"},
     'sepal_width': {"dependent_features": ['sepal_length']}}
])
def test_get_parameters(partial_features):
    """Test the get_parameters() method."""
    df = pd.read_csv(iris_path)
    features = infer_feature_attributes(df, dropna=False, features=partial_features)

    assert features.get_parameters()['dropna'] is False

    # Verify dependent_features
    assert 'features' in features.get_parameters()
    for key, value in partial_features.items():
        assert features.get_parameters()['features'][key] == value


def test_get_names_without():
    """Test the get_names() method."""
    df = pd.read_csv(iris_path)
    features = infer_feature_attributes(df)

    all_features = list(df)

    # Test get all feature names
    assert features.get_names() == all_features

    # Test get feature names without
    without = ['sepal_length', 'petal_length', 'petal_width']
    assert features.get_names(without=without) == [f for f in all_features if f not in without]

    # Test a feature in 'without' that is not in the features list
    with pytest.raises(ValueError):
        without = ['sepal_length', 'petal_length', 'personality']
        features.get_names(without=without)


@pytest.mark.parametrize("types, num", [
    ("continuous", 4),
    ({"continuous"}, 4),
    (('nominal'), 1),
    (['continuous', 'nominal'], 5),
])
def test_get_names_types(types, num):
    """Test the get_names() method with the types parameter."""
    df = pd.read_csv(iris_path)
    features = infer_feature_attributes(df)
    names = features.get_names(types=types)
    print(names)
    assert len(names) == num


def test_copy():
    """Test that copy works as expected."""
    df = pd.read_csv(iris_path)
    f_orig = infer_feature_attributes(df)
    f_copy = copy(f_orig)

    print(f_copy.keys())
    assert f_copy.params == f_orig.params
    orig = f_orig['sepal_width']['bounds']['min']
    assert f_copy['sepal_width']['bounds']['min'] == orig

    # Now, change the orig, so we can ensure that f_copy is independent.
    f_orig['sepal_width']['bounds']['min'] = -2
    # Assert that f_copy was unaffected
    assert f_copy['sepal_width']['bounds']['min'] == orig


@pytest.mark.parametrize("features", [
    ({'OPEN': {'type': 'continuous', 'decimal_places': 3}}),
    ({'VWAP': {'decimal_places': 5}}),
    ({'DATE': {'type': 'continuous', 'date_time_format': '%Y-%m-%f'}}),
    ({'DATE': {'date_time_format': '%Y-%m-%f'}}),
    ({'CLOSE': {'type': 'continuous', 'dependent_features': ['OPEN', 'DATE']}}),
])
def test_partial_features(features):
    """Test that filling a partial features dict works as expected."""
    df = pd.read_csv(stock_path)
    feature_attributes = infer_feature_attributes(df, time_feature_name='DATE', features=features)

    # Ensure that the partial features remain
    for feature in features.keys():
        for k, v in features[feature].items():
            assert k in feature_attributes[feature]
            assert feature_attributes[feature][k] == v
