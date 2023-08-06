import json
import os
from pprint import pprint
import sys
import uuid

import diveplane
from diveplane.client import DiveplaneClient, get_configuration_path
from diveplane.client.exceptions import (
    DiveplaneApiError,
    DiveplaneConfigurationError,
    DiveplaneError,
    DiveplaneTimeoutError,
)
from diveplane.client.protocols import ProjectClient
from diveplane.openapi.models import (
    AsyncActionAccepted,
    AsyncActionStatus,
    DiveplanePlatformVersion,
    Trainee,
    TrainResponse,
)
import numpy as np
import pandas as pd
import pytest
from semantic_version import Version

from . import get_test_options

TEST_OPTIONS = get_test_options()

np.random.default_rng(2018)

client = DiveplaneClient(verbose=True, debug=True)


IRIS_FILE_PATH = os.path.join(
    os.path.dirname(diveplane.client.__file__),
    "../utilities/tests/data/iris.csv"
)


def test_xdg_configuration_path(mocker):
    """Tests for expected behavior when XDG_CONFIG_HOME is set."""
    fake_xdg_config_path = '/tmp/xdg/path'
    fake_xdg_path = '/diveplane/'
    target_path = fake_xdg_config_path + fake_xdg_path + 'diveplane.yaml'
    names_to_remove = ('XDG_CONFIG_HOME', 'DP_CONFIG')
    modified_environ = {k: v for k, v in os.environ.items() if k not in names_to_remove}
    modified_environ["XDG_CONFIG_HOME"] = fake_xdg_config_path

    # Only return true if our mock xdg path is set
    def os_isfile(filepath):
        if filepath == target_path:
            return True
        return False

    mocker.patch('os.path.isfile', side_effect=os_isfile)
    mocker.patch.dict(os.environ, modified_environ, clear=True)
    path = get_configuration_path()
    assert path == target_path


def test_xdg_not_abs_error(mocker):
    """Tests for expected error when XDG_CONFIG_HOME is not an absolute path."""
    fake_xdg_config_path = 'tmp/xdg/path'
    fake_xdg_path = '/diveplane/'
    target_path = fake_xdg_config_path + fake_xdg_path + 'diveplane.yaml'
    names_to_remove = ('XDG_CONFIG_HOME', 'DP_CONFIG')
    modified_environ = {k: v for k, v in os.environ.items() if k not in names_to_remove}
    modified_environ["XDG_CONFIG_HOME"] = fake_xdg_config_path

    # Only return true if our mock xdg path is set
    def os_isfile(filepath):
        if filepath == target_path:
            return True
        return False

    mocker.patch('os.path.isfile', side_effect=os_isfile)
    mocker.patch.dict(os.environ, modified_environ, clear=True)
    with pytest.raises(DiveplaneConfigurationError) as exc:
        get_configuration_path()
    assert 'The path set in the XDG_CONFIG_HOME environment' in str(exc.value)


class TraineeBuilder:
    """Define a TraineeBuilder."""

    def __init__(self):
        """Initialize the TraineeBuilder."""
        self.trainees = []

    def create(self, trainee, overwrite_trainee=False):
        """Create a new trainee."""
        new_trainee = client.create_trainee(
            trainee, overwrite_trainee=overwrite_trainee)
        self.trainees.append(new_trainee)
        return new_trainee

    def copy(self, trainee_id, new_trainee_name=None, project_id=None):
        """Copy an existing trainee."""
        if isinstance(client, ProjectClient):
            new_trainee = client.copy_trainee(trainee_id, new_trainee_name,
                                              project_id)
        else:
            new_trainee = client.copy_trainee(trainee_id, new_trainee_name)
        self.trainees.append(new_trainee)
        return new_trainee

    def delete(self, trainee):
        """Delete a single trainee created by the builder."""
        if trainee in self.trainees:
            try:
                client.delete_trainee(trainee.id)
                self.trainees.remove(trainee)
            except DiveplaneApiError as err:
                if err.status == 404:
                    self.trainees.remove(trainee)
                else:
                    raise

    def delete_all(self):
        """Delete all trainees created by the builder."""
        for trainee in reversed(self.trainees):
            self.delete(trainee)

    def unload_all(self):
        """Unload all trainees created by the builder."""
        for trainee in self.trainees:
            client.release_trainee_resources(trainee.id)


@pytest.fixture(name='trainee_builder', scope='module')
def trainee_builder():
    """Define a fixture."""
    return TraineeBuilder()


@pytest.fixture(scope="function")
def dp_client():
    """Return a non-shared client."""
    return DiveplaneClient(verbose=True, debug=True)


class TestDatetimeSerialization:
    """Define a DateTimeSerialization tetst class."""

    @pytest.fixture(autouse=True)
    def trainee(self, trainee_builder):
        """Define a trainee fixture."""
        features = {'nom': {'type': 'nominal'},
                    'datetime': {'type': 'continuous',
                                 'date_time_format': '%Y-%m-%dT%H:%M:%S.%f'}
                    }
        trainee = Trainee(features=features,
                          default_action_features=['nom'],
                          default_context_features=['datetime'])
        trainee_builder.create(trainee, overwrite_trainee=True)
        try:
            yield trainee
        except Exception:
            raise
        finally:
            trainee_builder.delete(trainee)

    def test_train(self, trainee):
        """Test that train works as expected."""
        df = pd.DataFrame(data=np.asarray([
            ['a', 'b', 'c', 'd'],
            ['2020-9-12T9:09:09.123', '2020-10-12T10:10:10.123', '2020-12-12T12:12:12.123',
             '2020-10-11T11:11:11.123']
        ]).transpose(), columns=['nom', 'datetime'])
        client.train(trainee.id, cases=df.values.tolist(),
                     features=df.columns.tolist())
        case_response = client.get_cases(trainee.id,
                                         session=client.active_session.id)
        for case in case_response.cases:
            print(case)
        assert len(case_response.cases) == 4
        # datetime is fixed: zero-padded and has fractional seconds
        assert case_response.cases[0][1].rstrip("0") == '2020-09-12T09:09:09.123'

    def test_train_warn_fix(self, trainee_builder):
        """Test that train warns when it should."""
        features = {'nom': {'type': 'nominal'},
                    'datetime': {'type': 'continuous',
                                 'date_time_format': '%Y-%m-%dT%H:%M:%S'}
                    }
        trainee = Trainee(features=features,
                          default_action_features=['nom'],
                          default_context_features=['datetime'])
        trainee_builder.create(trainee, overwrite_trainee=True)
        df = pd.DataFrame(data=np.asarray([
            ['a', 'b', 'c', 'd'],
            # missing seconds in the provided values, don't match format
            ['2020-9-12T9:09', '2020-10-12T10:10', '2020-12-12T12:12',
             '2020-10-11T11:11']
        ]).transpose(), columns=['nom', 'datetime'])
        with pytest.warns(UserWarning) as warning_list:
            client.train(trainee.id, cases=df.values.tolist(),
                         features=df.columns.tolist())
            # There might be other UserWarnings but assert that at least one
            # of them has the correct message.
            assert any([str(warning.message) == (
                "datetime has values with incorrect datetime format, should "
                "be %Y-%m-%dT%H:%M:%S. This feature may not work properly.")
                for warning in warning_list])

        case_response = client.get_cases(trainee.id,
                                         session=client.active_session.id)
        for case in case_response.cases:
            print(case)
        assert len(case_response.cases) == 4
        # datetime is fixed: zero-padded and has seconds to adhere to format
        assert case_response.cases[0][1] == '2020-09-12T09:09:00'

    def test_train_warn_bad_feature(self, trainee_builder):
        """Test that train warns on bad features."""
        features = {'nom': {'type': 'nominal'},
                    'datetime': {'type': 'continuous',
                                 'date_time_format': '%H %Y'}
                    }
        trainee = Trainee(features=features,
                          default_action_features=['date_time_format'],
                          default_context_features=['nom'])
        trainee_builder.create(trainee, overwrite_trainee=True)
        df = pd.DataFrame(data=np.asarray([
            ['a', 'b', 'c', 'd'],
            # missing seconds in the provided values, don't match format
            ['2020-10-11T11:11', '2020-10-11T11:11', '2020-10-11T11:11',
             '2020-10-11T11:11']
        ]).transpose(), columns=['nom', 'datetime'])
        with pytest.warns(UserWarning) as warning_list:
            client.train(trainee.id, df.values.tolist(), df.columns.tolist())
            assert any([str(warning.message) == (
                "datetime has values with incorrect datetime format, should "
                "be %H %Y. This feature may not work properly.")
                for warning in warning_list])

        case_response = client.get_cases(trainee.id,
                                         session=client.active_session.id)
        for case in case_response.cases:
            print(case)
        assert len(case_response.cases) == 4
        # datetime is not fixed and the value returned doesn't match originals
        assert case_response.cases[0][1] != '2020-10-11T11:11'

    def test_react(self, trainee):
        """Test that react works as expected."""
        df = pd.DataFrame(data=np.asarray([
            ['a', 'b', 'c', 'd'],
            ['2020-9-12T9:09:09.123', '2020-10-12T10:10:10.333',
             '2020-12-12T12:12:12.444', '2020-10-11T11:11:11.222']
        ]).transpose(), columns=['nom', 'datetime'])
        client.train(trainee.id, cases=df.values.tolist(),
                     features=df.columns.tolist())
        response = client.react(trainee.id,
                                contexts=[["2020-10-12T10:10:10.333"]])
        assert response['action'][0]['nom'] == "b"

        response = client.react(trainee.id, contexts=[["b"]],
                                context_features=["nom"],
                                action_features=["datetime"])
        assert "2020-10-12T10:10:10.333000" in response['action'][0]['datetime']


class TestClient:
    """Define a Client test class."""

    @pytest.fixture(autouse=True)
    def trainee(self, trainee_builder):
        """Define a trainee fixture."""
        feats = {
            "penguin": {"type": "nominal"},
            "play": {"type": "nominal"},
        }
        actions = ['play']
        contexts = ['penguin']
        trainee_name = uuid.uuid4().hex
        trainee = Trainee(trainee_name, features=feats, default_action_features=actions,
                          default_context_features=contexts, metadata={'ttl': 600000})
        trainee_builder.create(trainee)
        try:
            yield trainee
        except Exception:
            raise
        finally:
            trainee_builder.delete(trainee)

    def _train(self, trainee):
        """
        Trains default cases.

        Parameters
        ----------
        trainee
        """
        # Add more cases
        cases = [['5', '6'],
                 ['7', '8'],
                 ['9', '10'],
                 ['11', '12'],
                 ['13', '14'],
                 ['15', '16'],
                 ['17', '18'],
                 ['19', '20'],
                 ['21', '22'],
                 ['23', '24'],
                 ['25', '26']]
        client.train(trainee.id, cases, features=['penguin', 'play'])

    def test_constructor(self):
        """Test that the client instantiates without issue."""
        assert client

    def test_get(self, trainee):
        """
        Test the /get endpoint.

        Parameters
        ----------
        trainee
        """
        returned_trainee = client.get_trainee(trainee.id)
        assert returned_trainee == trainee

    def test_update(self, trainee):
        """
        Test the PATCH / endpoint to update a trainee.

        Parameters
        ----------
        trainee
        """
        feats = {
            "dog": {"type": "nominal"},
            "cat": {"type": "continuous"}
        }
        actions = ['cat']
        contexts = ['dog']
        updated_trainee = Trainee(
            trainee.name,
            features=feats,
            default_action_features=actions,
            default_context_features=contexts,
            metadata={'date': 'now'}
        )
        updated_trainee = client.update_trainee(updated_trainee)
        trainee2 = client.get_trainee(trainee.id)
        assert trainee2.to_dict() == updated_trainee.to_dict()
        client.update_trainee(trainee)
        trainee3 = client.get_trainee(trainee.id)
        assert trainee3.to_dict() == trainee.to_dict()

    def test_train_and_react(self, trainee):
        """
        Test the /train and /react endpoint.

        Parameters
        ----------
        trainee
        """
        cases = [['1', '2'], ['3', '4']]
        client.train(trainee.id, cases, features=['penguin', 'play'])
        react_response = client.react(trainee.id, contexts=[['1']])
        assert react_response['action'][0]['play'] == '2'
        case_response = client.get_cases(trainee.id,
                                         session=client.active_session.id)
        for case in case_response.cases:
            print(case)
        assert len(case_response.cases) == 2

    def test_copy(self, trainee, trainee_builder):
        """
        Test the /copy/{trainee_id} endpoint.

        Parameters
        ----------
        trainee
        """
        new_trainee = trainee_builder.copy(trainee.id, trainee.name + "_copy")
        trainee_bob = client.get_trainee(new_trainee.id)
        orig = trainee.to_dict()
        copy_bob = trainee_bob.to_dict()
        assert orig['features'] == copy_bob['features']

    def test_trainee_conviction(self, trainee, trainee_builder):
        """
        Test the /copy/{trainee_id} endpoint.

        Parameters
        ----------
        trainee
        """
        cases = [['5', '6'],
                 ['7', '8'],
                 ['9', '10'],
                 ['11', '12'],
                 ['13', '14'],
                 ['15', '16'],
                 ['17', '18'],
                 ['19', '20'],
                 ['21', '22'],
                 ['23', '24'],
                 ['25', '26']]
        client.train(trainee.id, cases, features=['penguin', 'play'])
        trainee_copy = trainee_builder.copy(trainee.id, trainee.name + "_copy")
        cases2 = [['5', '6'],
                  ['7', '8'],
                  ['9', '10'],
                  ['11', '12'],
                  ['13', '14'],
                  ['15', '16'],
                  ['17', '18'],
                  ['19', '20'],
                  ['21', '22'],
                  ['23', '24'],
                  ['25', '26'],
                  ['27', '28']]
        client.train(trainee.name + "_copy", cases2,
                     features=['penguin', 'play'])
        conviction = client.react_group(trainee.id,
                                        trainees_to_compare=[trainee_copy.id])
        assert conviction is not None

    def test_impute(self, trainee):
        """
        Test the /impute endpoint.

        Parameters
        ----------
        trainee
        """
        self._train(trainee)
        features = ['penguin', 'play']
        try:
            session = client.begin_session('impute')
            client.train(trainee.id, [['15', None]], features=features)
            client.impute(trainee.id, features=features, batch_size=2)
            imputed_session = client.get_cases(trainee.id, session.id,
                                               indicate_imputed=True)
            assert imputed_session.cases[0][1] is not None
            assert '.imputed' in imputed_session.features
        finally:
            client.begin_session()  # Reset session

    def test_conviction_store(self, trainee):
        """
        Test the /conviction/store endpoint.

        Parameters
        ----------
        trainee
        """
        self._train(trainee)
        client.react_into_features(trainee.id, familiarity_conviction_addition=True)
        cases = client.get_cases(trainee.id,
                                 features=['play', 'penguin', 'familiarity_conviction_addition'],
                                 session=client.active_session.id)
        pprint(cases.__dict__)
        assert 'familiarity_conviction_addition' in cases.features

    def test_save(self, trainee):
        """
        Test the /save endpoint.

        Parameters
        ----------
        trainee
        """
        client.persist_trainee(trainee.id)

    def test_a_la_cart_data(self, trainee):
        """
        Test a-la-cart data.

        Systematically test a la cart options to ensure only the specified
        options are returned in the explanation data.

        Parameters
        ----------
        trainee : Trainee
            A trainee object to use.
        """
        # Add more cases
        cases = [['5', '6'],
                 ['7', '8'],
                 ['9', '10'],
                 ['11', '12'],
                 ['13', '14'],
                 ['15', '16'],
                 ['17', '18'],
                 ['19', '20'],
                 ['21', '22'],
                 ['23', '24'],
                 ['25', '26']]
        client.train(trainee.id, cases, features=['penguin', 'play'])

        details_sets = [
            (
                {'categorical_action_probabilities': True, },
                ['categorical_action_probabilities', ]
            ),
            (
                {'distance_contribution': True, },
                ['distance_contribution', ]
            ),
            (
                {'influential_cases': True, 'influential_cases_familiarity_convictions': True, },
                ['influential_cases', ]
            ),
            (
                {'num_boundary_cases': 1, 'boundary_cases_familiarity_conviction': True, },
                ['boundary_cases', ]
            ),
            (
                {'outlying_feature_values': True, },
                ['outlying_feature_values', ]
            ),
            (
                {'prediction_similarity_conviction': True, },
                ['prediction_similarity_conviction', ]
            ),
            (
                {'prediction_residual_conviction': True, },
                ['prediction_residual_conviction', ]
            ),
            (
                {'robust_computation': True, 'feature_residuals': True, },
                ['feature_residuals', ]
            ),
        ]
        for audit_detail_set, keys_to_expect in details_sets:
            response = client.react(trainee.id, contexts=[['1']],
                                    details=audit_detail_set)
            explanation = response['explanation']
            assert (all(explanation[key] is not None for key in keys_to_expect))

    def test_get_version(self):
        """Test get_version()."""
        version = client.get_version()
        assert version.api is not None
        assert version.client == diveplane.client.__version__

    def test_doublemax_to_infinity_translation(self):
        """Test the translation from Double.MAX_VALUE to Infinity."""
        from diveplane.utilities import replace_doublemax_with_infinity

        dat = {
            'familiarity_conviction': [sys.float_info.max],
            'influential_cases': [{
                'some_feature': {
                    'familiarity_conviction': sys.float_info.max
                }
            }]
        }
        dat = replace_doublemax_with_infinity(dat)
        assert (np.isinf(dat['familiarity_conviction'][0]))
        assert (np.isinf(dat['influential_cases'][0]['some_feature']['familiarity_conviction']))

    def test_number_overflow(self, trainee):
        """Test an exception is raised for a number that is too large."""
        # Should not raise
        client.train(trainee.id, [[1.8e307]], features=['penguin', 'play'])

        # Training with a number that is > 64bit should raise
        with pytest.raises(DiveplaneError):
            client.train(trainee.id, [[1.8e309, 2]],
                         features=['penguin', 'play'])

    def test_get_feature_mda(self, trainee, capsys):
        """
        Test get_feature_mda.

        Test for expected verbose output and expected return type when
        get_feature_mda is called.
        """
        self._train(trainee)
        client.react_into_trainee(
            trainee.id,
            mda=True,
            action_feature='play'
        )
        ret = client.get_feature_mda(
            trainee.id,
            action_feature='play')
        out, err = capsys.readouterr()
        assert (f'Getting mean decrease in accuracy for trainee with '
                f'id: {trainee.id}') in out
        assert type(ret) == dict
        assert len(ret) > 0

        with pytest.raises(DiveplaneError, match="Feature MDA for the"):
            ret = client.get_feature_mda(
                trainee.id,
                action_feature='invalid')

    def test_get_feature_residuals(self, trainee, capsys):
        """
        Test the /feature/residual endpoint in the python client.

        Parameters
        ----------
        trainee : Trainee
            A trainee object used or testing.
        """
        self._train(trainee)
        client.react_into_trainee(
            trainee_id=trainee.id,
            residuals=True,
            context_features=['penguin'],
            sample_model_fraction=1.0
        )
        ret = client.get_feature_residuals(trainee.id)
        assert (len(list(ret)) == 1)
        client.react_into_trainee(
            trainee_id=trainee.id,
            residuals=True,
            context_features=['penguin', 'play'],
            sample_model_fraction=1.0
        )
        ret = client.get_feature_residuals(trainee.id)
        assert len(list(ret)) == 2
        out, err = capsys.readouterr()
        assert f'Getting feature residuals for trainee with id: {trainee.id}' in out


class TestBaseClient:
    """Define a BaseClient test class."""

    @pytest.fixture(autouse=True)
    def trainee(self, trainee_builder):
        """Define a trainee fixture."""
        df = pd.read_csv(IRIS_FILE_PATH)
        header = list(df.columns)
        features = {header[0]: {'type': 'continuous'},
                    header[1]: {'type': 'continuous'},
                    header[2]: {'type': 'continuous'},
                    header[3]: {'type': 'continuous'},
                    header[4]: {'type': 'nominal'}
                    }
        trainee = Trainee(features=features,
                          default_action_features=header[-1:],
                          default_context_features=header[:-1])
        trainee_builder.create(trainee, overwrite_trainee=True)
        try:
            yield trainee
        except Exception:
            raise
        finally:
            trainee_builder.delete(trainee)

    def test_configuration_exception(self):
        """Test the Configuration Exception Class Constructor."""
        message = "test message"
        configuration_exception = DiveplaneConfigurationError(message=message)
        assert configuration_exception.message == message

    @pytest.mark.skipif('WEB' not in TEST_OPTIONS, reason='Web client only')
    def test_batch_train_verbose(self, trainee, capsys):
        """
        Test that batch_train works in verbose mode.

        Test the verbose output expected during the execution of batch_train.
        """
        df = pd.read_csv(IRIS_FILE_PATH)
        data = df.values
        test_percent = 0.2
        data_train = data[:int(len(data) * (1 - test_percent))]
        cases = data_train.tolist()
        client.train(trainee.id, cases, features=df.columns.tolist(),
                     batch_size=1000)
        out, err = capsys.readouterr()
        assert (f'Batch training cases on trainee with '
                f'id: {trainee.id}') in out

    def test_impute_verbose(self, trainee, capsys):
        """Test the verbose output expected during the execution of impute."""
        client.impute(trainee.id)
        out, err = capsys.readouterr()
        assert f'Imputing trainee with id: {trainee.id}' in out

    @pytest.mark.skipif('WEB' not in TEST_OPTIONS, reason='Web client only')
    def test_move_cases_exception(self, trainee):
        """
        Test that move_cases raises when expected.

        Checks for the expected exception when num_cases=1 is passed in
        move_cases.
        """
        condition = {"feature_name": None}
        with pytest.warns(UserWarning) as warn:
            client.move_cases(trainee.id, trainee.id, 1, condition=condition)
            assert str(warn[0].message) == ("move_cases has been removed from "
                                            "this version of Diveplane.")

    def test_remove_cases_verbose(self, trainee, capsys):
        """
        Test that remove_cases has verbose output when enabled.

        Test for verbose output expected when remove_cases is called with.
        """
        condition = {"feature_name": None}
        client.remove_cases(trainee.id, 1, condition=condition)
        out, err = capsys.readouterr()
        assert f"Removing case(s) in trainee with id: {trainee.id}" in out

    @pytest.mark.skipif('WEB' not in TEST_OPTIONS, reason='Web client only')
    def test_move_cases_verbose(self, trainee, capsys):
        """
        Test that move_cases has verbose output when enabled.

        Tests for verbose output expected when move_cases is called.
        """
        condition = {"feature_name": None}
        client.move_cases(trainee.id, trainee.id, 1, condition=condition)
        out, err = capsys.readouterr()
        assert ('"move_cases" does not exist for this version of '
                'Diveplane.') in out

    def test_update_trainee_verbose(self, trainee_builder, capsys):
        """
        Test that update_trainee has verbose output when enabled.

        Test for verbose output expected when update_trainee is called.
        """
        df = pd.read_csv(IRIS_FILE_PATH)
        header = list(df.columns)
        features = {header[0]: {'type': 'continuous'},
                    header[1]: {'type': 'continuous'},
                    header[2]: {'type': 'continuous'},
                    header[3]: {'type': 'continuous'},
                    header[4]: {'type': 'nominal'}
                    }
        trainee = Trainee(features=features,
                          default_action_features=header[-1:],
                          default_context_features=header[:-1])
        trainee_builder.create(trainee, overwrite_trainee=True)
        trainee.name = 'test-update-verbose'
        updated_trainee = client.update_trainee(trainee)
        assert trainee.name == updated_trainee.name
        assert updated_trainee.name == 'test-update-verbose'
        out, err = capsys.readouterr()
        assert f'Updating trainee with id: {trainee.id}' in out

    def test_get_trainee_verbose(self, trainee, capsys):
        """
        Test that get_trainee has verbose output when enabled.

        Test for verbose output expected when get_trainee is called.
        """
        client.get_trainee(trainee.id)
        out, err = capsys.readouterr()
        assert f'Getting trainee with id: {trainee.id}' in out

    def test_set_feature_attributes(self, trainee, capsys):
        """Test that set_feature_attributes works as expected."""
        attributes = {
            "length": {"type": "continuous", "decimal_places": 1},
            "width": {"type": "continuous", "significant_digits": 4},
            "degrees": {"type": "continuous", "cycle_length": 360},
            "class": {"type": "nominal"}
        }
        client.set_feature_attributes(trainee.id,
                                      feature_attributes=attributes)
        out, err = capsys.readouterr()
        assert (f'Setting feature attributes for trainee '
                f'with id: {trainee.id}') in out

    def test_get_feature_attributes(self, trainee, capsys):
        """Test get_feature attributes returns the expected output."""
        attributes = {
            "length": {"type": "continuous", "decimal_places": 1},
            "width": {"type": "continuous", "significant_digits": 4},
            "degrees": {"type": "continuous", "cycle_length": 360},
            "class": {"type": "nominal"}
        }

        client.set_feature_attributes(trainee.id,
                                      feature_attributes=attributes)
        output = client.get_feature_attributes(trainee.id)
        out, err = capsys.readouterr()
        assert (f'Getting feature attributes from trainee '
                f'with id: {trainee.id}') in out
        assert output == attributes

    def test_get_trainee_sessions_verbose(self, trainee, capsys):
        """
        Test that get_trainee_sessions has verbose output when enabled.

        Test for verbose output expected when get_trainee_sessions is called.
        """
        client.get_trainee_sessions(trainee.id)
        out, err = capsys.readouterr()
        assert f'Getting sessions from trainee with id: {trainee.id}' in out

    def test_optimize_verbose(self, trainee, capsys):
        """Test for verbose output expected when optimize is called."""
        context_features = ['class']
        client.optimize(trainee.id, context_features)
        out, err = capsys.readouterr()
        assert f'Optimizing trainee with id: {trainee.id}' in out
        assert 'Optimizing trainee with parameters: ' in out

    @pytest.mark.skipif('WEB' not in TEST_OPTIONS, reason='Web client only')
    def test_wait_for_action_exception(self, mocker):
        """
        Test that wait_for_action raises when expected.

        Tests for expected exception to be raised when the max_wait_time
        keyword argument is set and time runs over.
        """
        mock_action_accepted = AsyncActionAccepted(
            action_id='test123',
            operation_type='react'
        )
        mock_action_status = AsyncActionStatus(
            action_id='test123',
            status='pending',
            operation_type='react'
        )
        mocker.patch(
            'diveplane.openapi.api.TaskOperationsApi.get_action_output',
            return_value=mock_action_status)

        with pytest.raises(DiveplaneTimeoutError) as exc:
            client.api_client.wait_for_action(
                mock_action_accepted, max_wait_time=0.5)
        expected_msg = (
            "Operation 'react' exceeded max wait time of 0.5 seconds")
        assert expected_msg in str(exc.value)

    def test_acquire_trainee_resources_verbose(self, trainee, capsys):
        """
        Test that acquire_trainee_resources is verbose when enabled.

        Test for the verbose output expected when acquiring trainee resources.
        """
        client.persist_trainee(trainee.id)
        client.acquire_trainee_resources(trainee.id)
        out, _ = capsys.readouterr()
        assert f'Acquiring resources for trainee with id: {trainee.id}' in out

    def test_save_trainee_verbose(self, trainee, capsys):
        """
        Test that save_trainee is verbose when enabled.

        Test for the verbose output expected when persist_trainee is called.
        """
        client.persist_trainee(trainee.id)
        out, _ = capsys.readouterr()
        assert f'Saving trainee with id: {trainee.id}' in out

    def test_release_trainee_resources_verbose(self, trainee, capsys):
        """
        Test that release_trainee_resources is verbose when enabled.

        Test for the verbose output expected when releasing trainee resources.
        """
        client.release_trainee_resources(trainee.id)
        out, _ = capsys.readouterr()
        assert f'Releasing resources for trainee with id: {trainee.id}' in out

    def copy_trainee_verbose(self, trainee, trainee_builder, capsys):
        """
        Test that copy_trainee is verbose when enabled.

        Test for the verbose output expected when copy_trainee is called.
        """
        trainee_builder.copy(trainee.id, f'new_{trainee.id}')
        out, _ = capsys.readouterr()
        assert f'Copying trainee {trainee.id} to new_{trainee.id}' in out

    def test_delete_trainee_verbose(self, trainee, capsys):
        """
        Test that delete_trainee is verbose when enabled.

        Test for the verbose output expected when delete_trainee is called.
        """
        client.delete_trainee(trainee.id)
        out, _ = capsys.readouterr()
        assert 'Deleting trainee' in out

    def test_remove_cases_exception(self, trainee):
        """
        Test that remove_cases raises when expected.

        Test for the expected exception when num_cases=0 is passed into
        remove cases. (num_cases must be a value greater than 0).
        """
        condition = {"feature_name": None}
        with pytest.raises(ValueError) as exc:
            client.remove_cases(trainee.id, 0, condition=condition)
        assert str(exc.value) == 'num_cases must be a value greater than 0'

    def test_react_exception(self, trainee):
        """
        Test that react raises when expected.

        Test for the expected Exception when contexts and case_indices are not
        specified when calling react.
        """
        with pytest.raises((ValueError, DiveplaneApiError)) as exc:
            client.react(trainee.id, desired_conviction=None, contexts=None)
        msg = ("If `contexts` are not specified, both `case_indices` and "
               "`preserve_feature_values` must be specified.")
        assert msg in str(exc.value)

    def test_get_num_training_cases(self, trainee):
        """Test the that output is the expected type: int."""
        number_cases = client.get_num_training_cases(trainee.id)
        assert type(number_cases) == int

    def test_react_group_exception(self, trainee):
        """
        Test that react_group raises when expected.

        Test the expected exception is raised when react_group
        gets parameters trainee_id and trainee_to_compare passed in as None.
        """
        with pytest.raises(ValueError) as exc:
            client.react_group(trainee.id)
        assert str(exc.value) == ("Either `new_cases` or `trainees_to_compare` "
                                  "must be provided.")

    def test_react_group_trainee_compare_verbose(self, trainee, capsys):
        """
        Test that react_group_trainee_compare is verbose when enabled.

        Test. the verbose output expected when react_group w/ trainee
        is called.
        """
        client.react_group(trainee.id, trainees_to_compare=[trainee.id])
        out, err = capsys.readouterr()
        assert 'Reacting to a set of cases on trainee with id' in out

    def test_react_into_features_verbose(self, trainee, capsys):
        """
        Test that react_into_features is verbose when enabled.

        Test the verbose output expected when react_into_features is called.
        """
        client.react_into_features(trainee.id, familiarity_conviction_addition=True)
        out, err = capsys.readouterr()
        assert ('Reacting into features on trainee with id') in out

    def test_get_feature_conviction_verbose(self, trainee, capsys):
        """
        Test that get_feature_conviction is verbose when enabled.

        Test for the verbose output expected when get_feature_conviction
        is called.
        """
        client.get_feature_conviction(trainee.id)
        out, err = capsys.readouterr()
        assert 'Getting conviction of features for trainee with id' in out

    def test_get_params_verbose(self, trainee, capsys):
        """
        Test that get_params is verbose when enabled.

        Test for the verbose output expected when get_params is called.
        """
        client.get_params(trainee.id)
        out, err = capsys.readouterr()
        assert (f'Getting model attributes from trainee with '
                f'id: {trainee.id}') in out

    def test_set_params_verbose(self, trainee, capsys):
        """Test for the verbose output expected when set_params is called."""
        params = {
            "hyperparameter_map": {
                ".targetless": {
                    "robust": {
                        ".none": {
                            "dwe": -1, "p": .1, "k": 8
                        }
                    }
                }
            },
            "optimize_threshold": 100,
            "optimize_growth_factor": 3,
            "auto_optimize_limit_size": 100000
        }
        client.set_params(trainee.id, params)
        out, err = capsys.readouterr()
        assert (f'Setting model attributes for trainee with '
                f'id: {trainee.id}') in out

    def test_get_configuration_path_exceptions(self, mocker):
        """
        Test that get_configuration_path raises when expected.

        Test for multiple expected when there are issues with the path passed
        in or the configuration yaml file.
        """
        with pytest.raises(DiveplaneConfigurationError) as exc:
            get_configuration_path(config_path='Fake/Path')
        assert 'Specified configuration file was not found' in str(exc.value)

    def test_base_client_initializer_exception(self):
        """
        Test that the base client initializer raises when expected.

        Tests for the expected exception when an instance of the
        DiveplaneClient is created with an invalid path
        """
        with pytest.raises(DiveplaneConfigurationError) as exc:
            DiveplaneClient(config_path="Fake/Path", verbose=True)
        assert "Specified configuration file was not found" in str(exc)

    @pytest.mark.skipif('WEB' not in TEST_OPTIONS, reason='Web client only')
    def test_train_optimizes(self, dp_client, trainee, mocker):
        """
        Test that traine optimizes when expected.

        Test that auto_optimize is also called when test_train is called
        using mocking.
        """
        df = pd.read_csv(IRIS_FILE_PATH)
        data = df.values
        # Ensure we don't trigger batch_train conditions...
        data_train = data[:dp_client._train_batch_threshold]
        return_value = TrainResponse(status="optimize")
        dp_client._train = mocker.Mock(return_value=return_value)

        spy = mocker.spy(dp_client, 'auto_optimize')
        dp_client.train(trainee.id, cases=data_train,
                        features=df.columns.tolist(), batch_size=None)
        spy.assert_called_once_with(trainee.id)

    def test_set_get_substitute_feature_values(self, trainee, capsys):
        """
        Test that set_substitute_feature_values works as expected.

        Test the functionality of both set_substitute_feature_values and
        get_feature_values as well as checks for expected verbose output.
        """
        df = pd.read_csv(IRIS_FILE_PATH)
        header = list(df.columns)
        substitution_value_map = {header[0]: {'type': 'continuous'},
                                  header[1]: {'type': 'continuous'},
                                  header[2]: {'type': 'continuous'},
                                  header[3]: {'type': 'continuous'},
                                  header[4]: {'type': 'nominal'}
                                  }
        client.set_substitute_feature_values(trainee.id,
                                             substitution_value_map)
        out, err = capsys.readouterr()
        assert (f'Setting substitute feature values for '
                f'trainee with id: {trainee.id}') in out
        ret = client.get_substitute_feature_values(trainee.id)
        out, err = capsys.readouterr()
        assert (f'Getting substitute feature values from trainee with '
                f'id: {trainee.id}') in out
        assert ret == substitution_value_map
        ret = client.get_substitute_feature_values(trainee.id)
        assert ret == {}

    def test_set_get_feature_attributes(self, trainee, capsys):
        """
        Test that set_- and get_feature_attributes work as expected.

        Test the the functionality of both set_substitute_feature_attributes
        and get_feature_attributes as well as checks for expected verbose
        output.
        """
        feats = {
            "length": {"type": "continuous", "decimal_places": 1},
            "width": {"type": "continuous", "significant_digits": 4},
            "degrees": {"type": "continuous", "cycle_length": 360},
            "class": {"type": "nominal"}
        }

        client.set_feature_attributes(trainee.id, feature_attributes=feats)
        out, err = capsys.readouterr()
        assert (f'Setting feature attributes for trainee '
                f'with id: {trainee.id}') in out

        ret = client.get_feature_attributes(trainee.id)
        out, err = capsys.readouterr()
        assert (f'Getting feature attributes from trainee with '
                f'id: {trainee.id}') in out
        assert ret == feats

    @pytest.mark.skipif('WEB' not in TEST_OPTIONS, reason='Web client only')
    def test_wait_for_action(self, capsys, mocker):
        """Test for expected exception and verbose output."""
        max_wait_time = 1.0
        operation_type = 'testing'

        mock_action_accepted = AsyncActionAccepted(
            action_id='test123',
            operation_type=operation_type
        )
        mock_action_status = AsyncActionStatus(
            action_id='test123',
            status='pending',
            operation_type=operation_type
        )
        mocker.patch(
            'diveplane.openapi.api.TaskOperationsApi.get_action_output',
            return_value=mock_action_status)

        with pytest.raises(DiveplaneTimeoutError) as exc:
            client.api_client.wait_for_action(
                mock_action_accepted, max_wait_time=max_wait_time)
        expected_msg = (f"Operation '{operation_type}' exceeded max wait time "
                        f"of {max_wait_time} seconds")
        assert expected_msg in str(exc.value)
        max_wait_time = 3

        with pytest.raises(DiveplaneTimeoutError) as exc:
            client.api_client.wait_for_action(
                mock_action_accepted, max_wait_time=max_wait_time)
        out, _ = capsys.readouterr()
        assert f"Operation '{operation_type}' is pending, waiting " in out

    def test_react_exceptions(self, trainee):
        """
        Test that react raises when expected.

        Test for expected exceptions when react is called with certain values
        passed in.
        """
        df = pd.read_csv(IRIS_FILE_PATH)
        features = list(df.columns)
        num_cases_to_generate = 10
        with pytest.raises(DiveplaneError) as exc:
            client.react(trainee.id,
                         desired_conviction=1.0,
                         preserve_feature_values=features,
                         case_indices=[('test', 1), ('test', 2)],
                         num_cases_to_generate=num_cases_to_generate)
        assert (
            "The number of `case_indices` provided does not match "
            "the number of cases to generate."
        ) in str(exc.value)
        num_cases_to_generate = 1
        with pytest.raises(DiveplaneError) as exc:
            client.react(trainee.id,
                         desired_conviction=1.0,
                         preserve_feature_values=features,
                         num_cases_to_generate=num_cases_to_generate,
                         contexts=[['test']])
            assert ("The number of provided context values in "
                    "`contexts` does not match the number of features in "
                    "`context_features`.") in str(exc.value)

    def test_get_cases_warning(self, trainee, capsys):
        """
        Test that get_cases issues warning when expected.

        Test for expected warning when get_cases is called without passing in
        a session id.
        """
        expected_message = ('Calling get_cases without session id does '
                            'not guarantee case order.')
        with pytest.warns(Warning, match=expected_message):
            client.get_cases(trainee.id)
            out, err = capsys.readouterr()
            assert 'Retrieving cases.' in out

    def test_react_group(self, trainee, capsys):
        """
        Test that react_group works as expected.

        Tests for expected verbose output and expected return type (list) when
        get_case_familiarity conviction is called.
        """
        new_cases = [[[1, 2, 3, 4, 5],
                      [4, 5, 6, 7, 8],
                      [7, 8, 9, 10, 11]],
                     [[1, 2, 3, 4, 5]]]
        features = ['sepal_length', 'sepal_width', 'petal_length',
                    'petal_width', 'class']
        ret = client.react_group(
            trainee.id, new_cases=new_cases, features=features)
        out, err = capsys.readouterr()
        assert type(ret) == dict

        df = pd.DataFrame([[1, 2, 4, 4, 4]], columns=features)
        new_cases = [df]
        ret = client.react_group(
            trainee.id, new_cases=new_cases, features=features)
        out, err = capsys.readouterr()
        assert type(ret) == dict

        # 2d list of cases, which is invalid
        new_cases = [[1, 2, 3, 4, 5],
                     [4, 5, 6, 7, 8],
                     [7, 8, 9, 10, 11]]
        with pytest.raises(ValueError) as exc:
            ret = client.react_group(
                trainee.id, new_cases=new_cases, features=features)
        assert (
            "Improper shape of `new_cases` values passed. "
            "`new_cases` must be a 3d list of object."
        ) in str(exc.value)

    def test_remove_feature_verbose(self, trainee, capsys):
        """Test for expected verbose output when remove_feature is called."""
        feature = 'test'
        client.remove_feature(trainee.id, feature=feature)
        out, err = capsys.readouterr()
        assert (f'Removing feature "{feature}" for trainee with id: '
                f'{trainee.id}') in out

    @pytest.mark.parametrize(
        'json_map, expected_output',
        [
            (
                json.loads('{"message":"java.lang.IllegalStateException: '
                           'Expected a", "code":0}'),
                'Diveplane Error: DiveplaneError /0'
            ),
            (
                json.loads('{"message":"java.lang.IllegalStateException: '
                           'Expected a "}'),
                'Diveplane Error:  DiveplaneError /-1'
            ),
            (
                json.loads('{"test":"general"}'),
                'General Exception DiveplaneError'
            )
        ]
    )
    def test_raise_diveplane_error(self, capsys, json_map, expected_output):
        """Test for various expected error outputs with various json_maps."""
        with pytest.raises(Exception):
            client._raise_diveplane_error(json_map)
            out, err = capsys.readouterr()
            assert expected_output in out

    def test_get_configuration_path(self, mocker):
        """
        Test that get_configuration_path works as expected.

        Tests for expected output when the mocked functions return None and
        True respectively.
        """
        mocker.patch('os.environ.get', return_value=None)
        mocker.patch('os.path.isfile', return_value=True)
        path = get_configuration_path()
        assert path == 'diveplane.yml'

    @pytest.mark.skipif('WEB' not in TEST_OPTIONS, reason='Web client only')
    @pytest.mark.parametrize('client_api_version, api_version, outcome', (
        ('2.0.0', '3.4.5', False),  # Client version too low
        ('4.0.0', '3.4.5', False),  # Client version too high
        ('4.0.0', None, None),  # Unknown version compatibility
        ('3.0.0', '3.4.5', True),  # Valid client version
    ))
    def test_check_service_compatibility(self, mocker, client_api_version,
                                         api_version, outcome):
        """
        Test that check_service_availablity works as expected.

        Ensure that the check_service_compatibility() works for a range of
        scenarios.
        """
        version_response = DiveplanePlatformVersion(
            platform='1.0.0',
            api=api_version
        )
        mocker.patch('diveplane.client.client.client_api_version',
                     client_api_version)
        mocker.patch.object(client, 'get_version',
                            return_value=version_response)

        def _has_warning(warnings, msg):
            return any([
                msg in str(warning.message) for warning in warnings
            ])

        if outcome:
            assert client._check_service_compatibility()
        else:
            with pytest.warns(UserWarning) as warning_list:
                assert not client._check_service_compatibility()

                if api_version is None:
                    assert len(warning_list)
                    assert _has_warning(warning_list, "Proceed with caution")
                elif int(Version(client_api_version).major) < int(Version(api_version).major):
                    assert len(warning_list)
                    assert _has_warning(warning_list,
                                        'Please upgrade the client software to a '
                                        'newer version.')
                elif int(Version(client_api_version).major) > int(Version(api_version).major):
                    assert len(warning_list)
                    assert _has_warning(warning_list,
                                        'Please upgrade the server, or downgrade '
                                        'the client, to compatible API versions.')

    @pytest.mark.skipif('WEB' not in TEST_OPTIONS, reason='Web client only')
    def test_check_service_compatibility_item_not_found(self, mocker):
        """
        Test check_service_compatibility_item raises warnings when expected.

        Test that a warning is raised if the service does not return a
        valid version item from its "/version" endpoint.
        """
        version_response = DiveplanePlatformVersion()
        mocker.patch.object(
            client, 'get_version', return_value=version_response)
        with pytest.warns(UserWarning) as record:
            assert client._check_service_compatibility() is None
            assert 'Proceed with caution.' in str(record[0].message)
