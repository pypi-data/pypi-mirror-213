import gc
import pickle
import uuid

from diveplane import reactor
from diveplane.client.exceptions import DiveplaneNotUniqueError
from diveplane.client.tests import get_test_options
from diveplane.direct import DiveplaneDirectClient
from diveplane.scikit import (
    CLASSIFICATION,
    DiveplaneClassifier,
    DiveplaneEstimator,
    DiveplaneRegressor,
)
import numpy as np
import pytest
from sklearn.base import clone
from sklearn.model_selection import cross_validate

TEST_OPTIONS = get_test_options()


@pytest.fixture(scope='function')
def classifier():
    """
    Creates a pre-populated Diveplane estimator.
    """
    # Let's learn how to classify the XOR operation.
    X = np.array([[0, 0], [1, 0], [0, 1], [1, 1],
                  [0, 0], [1, 0], [0, 1], [1, 1]])
    y = np.array([0, 1, 1, 0, 0, 1, 1, 0])
    dp = DiveplaneClassifier()
    dp.fit(X, y)
    return dp


class TestDiveplane:

    def test_regressor(self):
        """
        Tests the DiveplaneRegressor from the external client.
        """
        X = np.array([1, 2, 3])
        y = np.array([4, 5, 6])
        dp = DiveplaneRegressor()
        dp.fit(X, y)
        print(dp.score(X, y))
        print(dp.predict(np.array([[4], [5], [6]])))
        # Ensure that the trainee is unnamed, so it will be deleted.
        dp.trainee_name = None

    def test_classifier(self):
        """
        Tests the DiveplaneClassifier from the external client.
        """
        # Use two instances of data indicating the xor operation to make sure
        # it is able to learn it.
        X = np.array([[0, 0], [1, 0], [0, 1], [1, 1],
                      [0, 0], [1, 0], [0, 1], [1, 1]])
        y = np.array([0, 1, 1, 0, 0, 1, 1, 0])
        dp = DiveplaneClassifier()
        dp.fit(X, y)
        assert dp.score(X, y) == 1.0
        assert dp.predict(np.array([[1, 1]])).sum() == 0
        # Ensure that the trainee is unnamed, so it will be deleted.
        dp.trainee_name = None

    def test_trainee_name_getter_setter(self, classifier):
        """
        Test that the trainee_name setter works as expected.
        """
        assert classifier.trainee_name is None
        new_name = str(uuid.uuid4())
        # Invoke and test setter
        classifier.trainee_name = new_name
        # Invoke and test getter
        assert classifier.trainee_name == new_name
        # Ensure that the trainee is unnamed, so it will be deleted.
        classifier.trainee_name = None

    @pytest.mark.parametrize('trainee_is_named', [True, False])
    def test_destructor(self, mocker, trainee_is_named):
        """
        Ensure that the destructor properly unloads or deletes the trainee.

        When the trainee is named, it should unload and NOT delete and
        when the trainee is unnamed, it should delete and NOT unload.

        Since this is going to explicitly destroy the classifier, it should
        create its own.
        """
        X = np.array([[0, 0], [1, 0], [0, 1], [1, 1]])
        y = np.array([0, 1, 1, 0])
        dp = DiveplaneClassifier()
        dp.fit(X, y)

        if trainee_is_named:
            dp.trainee_name = str(uuid.uuid4())
        else:
            dp.trainee_name = None

        # Let's spy on the delete_trainee and release_trainee_resources methods
        delete_spy = mocker.spy(reactor.Trainee, 'delete')
        unload_spy = mocker.spy(reactor.Trainee, 'release_resources')

        # Capture their initial state (should be zero though)
        delete_count = delete_spy.call_count
        unload_count = unload_spy.call_count

        # Delete the estimator and ensure that garbage collection has occurred.
        del dp
        gc.collect()

        if trainee_is_named:
            assert delete_spy.call_count >= delete_count
            assert unload_spy.call_count > unload_count
        else:
            assert delete_spy.call_count > delete_count
            assert unload_spy.call_count >= unload_count

        # If the trainee was named, it would have been simply unloaded. Now
        # that testing has completed, ensure it is manually removed. For this
        # a new DiveplaneClassifier is used.
        if trainee_is_named:
            dp = DiveplaneClassifier()
            dp.delete()

    def test_save(self, classifier):
        """
        Test that save works as intended.

        In particular, we should ensure that calling save() sets the trainee
        name, if necessary.
        """
        assert classifier.trainee_name is None
        # If this raises, obviously the test fails.
        classifier.save()
        assert classifier.trainee_name is not None

        # Testing has completed, ensure the name is reset so the estimator will
        # delete it as it is destructed.
        classifier.trainee_name = None

    def test_uniqueness_check(self, classifier):
        """
        Test that setting the `trainee_name` to a used name fails as expected.
        """

        # Create a (degenerate) trainee with a known name outside of the
        # estimator (but using the same client for convenience).
        known_name = f'known-name-{uuid.uuid4()}'
        rogue_trainee = reactor.Trainee(
            default_action_features=['a', 'b'],
            default_context_features=['c', 'd'],
            metadata={'fake-trainee': True},
            features={
                'a': {'type': 'nominal'},
                'b': {'type': 'nominal'},
                'c': {'type': 'nominal'},
                'd': {'type': 'nominal'}
            }
        )
        rogue_trainee.name = known_name
        # NOTE: This just uses the client embedded in the classifier here.
        #       This does not create a trainee for the classifier. And because
        #       of this, this test needs to explicitly delete this trainee
        #       when it is done with it.

        # Attempt to set name to existing name
        if not isinstance(classifier.client, DiveplaneDirectClient):
            with pytest.raises(DiveplaneNotUniqueError) as exc_info:
                rogue_trainee.name = known_name
            assert "Please use a unique name" in str(exc_info.value)
        else:
            # Ensure this doesn't raise
            rogue_trainee.name = known_name

        # Explicitly delete the rogue_trainee
        rogue_trainee.delete()
        # Reset to none so it won't be saved.
        rogue_trainee.name = None

    @pytest.mark.skipif('WIP' not in TEST_OPTIONS, reason='Local devs only')
    def test_pickle(self):
        """
        Test the pickling function with DiveplaneEstimator scikit Estimator.
        """
        # Test estimator; ensure it functions and has access to the client.
        X = np.array([[0, 0], [1, 0], [0, 1], [1, 1],
                      [0, 0], [1, 0], [0, 1], [1, 1]])
        y = np.array([0, 1, 1, 0, 0, 1, 1, 0])
        dp = DiveplaneEstimator(method=CLASSIFICATION)
        dp.fit(X, y)
        assert dp.score(X, y) == 1.0
        assert dp.predict(np.array([[1, 1]])).sum() == 0
        assert type(dp.client) is DiveplaneDirectClient

        # Pickle the Estimator; this should call dp.client.save which should
        # give the trainee a name save the trainee in the cloud.
        pickle_string = pickle.dumps(dp)
        print(f'Trainee name: {dp.trainee_name}')

        # Explicitly delete the estimator, which in turn will delete the
        # trainee and clear the variable that held the Estimator.
        dp.client.release_trainee_resources(dp.trainee_id)
        del dp

        # Load the estimator from the pickle to a new variable and conduct
        # the same assertion tests.
        dp2 = pickle.loads(pickle_string)
        assert dp2.score(X, y) == 1.0
        assert dp2.predict(np.array([[1, 1]])).sum() == 0
        assert type(dp2.client) is DiveplaneDirectClient

        # Delete the saved trainee to save resources.
        dp2.delete()

    def test_regressor_cv(self):
        """
        Test that DiveplaneRegressor works using cross-validation.
        """
        X = np.array([1, 2, 3])
        y = np.array([4, 5, 6])
        dp = DiveplaneRegressor()
        results = cross_validate(dp, X, y, cv=3)
        print(results["test_score"])

    def test_classifier_cv(self):
        """
        Test the DiveplaneClassifier works using cross-validation.
        """
        X = np.array([[0, 0], [1, 0], [0, 1], [1, 1]])
        y = np.array([0, 1, 1, 0])
        dp = DiveplaneClassifier()
        results = cross_validate(dp, X, y, cv=3)
        print(results["test_score"])

    def test_clone(self):
        """
        Tests the ability of DiveplaneClassifier to be cloned by sklearn.
        """
        dp = DiveplaneClassifier()
        new_dp = clone(dp)
        assert dp.get_params() == new_dp.get_params()
