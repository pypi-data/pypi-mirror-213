import pytest

from diveplane.reactor import Trainee


class TestReactor:
    @pytest.fixture(autouse=True)
    def trainee(self, data, features):
        t = Trainee(features=features)
        t.train(data)

        try:
            yield t
        except Exception:
            raise
        finally:
            t.delete()

    @pytest.mark.parametrize(
        "from_values,to_values,expected",
        [
            ([[0]], [[0]], 0),
            ([[0]], [[1]], 1),
            ([[0, 0, 0]], [[0, 0, 0]], 0),
            ([[0, 0]], [[1, 0]], 1),
        ],
    )
    def test_pairwise_distances(self, trainee, from_values, to_values, expected):
        """
        Tests that get_pairwise_distances returns values as expected from simple
        vectors.
        """
        features_list = [str(i) for i in range(len(from_values[0]))]
        result = trainee.get_pairwise_distances(
            features=features_list, from_values=from_values, to_values=to_values
        )
        assert result[0] == expected

    @pytest.mark.parametrize(
        "case_indices,expected",
        [
            ([19, 122], [[0, 0], [0, 0]]),
            ([11, 41, 102], [[0, 0, 0], [0, 0, 0], [0, 0, 0]]),
        ],
    )
    def test_distances_same(self, trainee, features, case_indices, expected):
        """
        Test that get_distances returns values as expected.

        Note that, in the iris dataset, rows 19 and 122 are identical
        and rows 11, 41, and 102 are identical and as such their distances
        should be zero.
        """
        sessions = trainee.get_sessions()
        session = sessions[0]
        session_case_indices = []
        for case_index in case_indices:
            session_case_indices.append((session['id'], case_index))

        result = trainee.get_distances(case_indices=session_case_indices)
        result = result['distances'].values.tolist()

        assert result == expected

    @pytest.mark.parametrize(
        "case_indices,unexpected",
        [
            ([0, 1], [[0, 0], [0, 0]]),
            ([2, 3, 4], [[0, 0, 0], [0, 0, 0], [0, 0, 0]]),
        ],
    )
    def test_distances_different(self, trainee, features, case_indices, unexpected):
        """
        Test that get_distances returns values as expected.

        The indices 0, 1 and 2, 3, and 4 are not the same, so the distance
        should be nonzero.
        """
        sessions = trainee.get_sessions()
        session = sessions[0]
        session_case_indices = []
        for case_index in case_indices:
            session_case_indices.append((session['id'], case_index))

        result = trainee.get_distances(case_indices=session_case_indices)
        result = result['distances'].values.tolist()

        assert result != unexpected

    def test_get_cases(self, trainee):
        """
        Test that get_cases works with and without a session ID to
        get the cases in the order they were trained. This functionality
        only works in a single-user environment and assumes a single session.
        """
        c1 = trainee.get_cases()

        sessions = trainee.get_sessions()
        session = sessions[0]
        c2 = trainee.get_cases(session=session['id'])

        assert c1.equals(c2)
