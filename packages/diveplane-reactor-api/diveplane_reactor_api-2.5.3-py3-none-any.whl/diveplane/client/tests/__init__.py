import os


def get_test_options():
    """
    Simply parses the ENV variable 'TEST_OPTIONS' into a list, if possible
    and returns it. This will be used with `pytest.skipif` to conditionally
    test some additional tests.

    Example:
        >>> from . import get_test_options
        >>> ...
        >>> @pytest.mark.skipif('FOO' not in get_test_options, reason='FOO not in ENV')  # noqa
        >>> def test_bar(...):
        >>>     ...

    Returns
    -------
    list[str]
    """
    try:
        options = os.getenv('TEST_OPTIONS').split(',')
    except (AttributeError, ValueError):
        options = []
    return options


try:
    import diveplane.nominal_substitution as _  # noqa
except ImportError:
    NOMINAL_SUBSTITUTION_AVAILABLE = False
else:
    NOMINAL_SUBSTITUTION_AVAILABLE = True
