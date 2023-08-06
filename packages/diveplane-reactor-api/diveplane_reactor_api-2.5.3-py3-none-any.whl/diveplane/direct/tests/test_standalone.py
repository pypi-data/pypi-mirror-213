import pytest

from amalgam.api import Amalgam
from diveplane.direct import DiveplaneDirectClient, DiveplaneCore


@pytest.fixture
def client():
    """Direct client instance using latest binaries."""
    return DiveplaneDirectClient(verbose=True, debug=True)


def test_direct_client(client):
    """Sanity check client instantiation."""
    assert isinstance(client.dp, DiveplaneCore)
    assert isinstance(client.dp.amlg, Amalgam)
    version = client.get_version()
    assert version.api is not None
    assert version.client is not None


@pytest.mark.parametrize(('filename', 'truthiness'), (
    ('./banana.txt', True),
    ('./ba\nana.txt', True),
    ('./bañän🤣a.txt', True),
))
def test_check_name_valid_for_save(client, filename, truthiness):
    """Ensure that the internal function `check_name_valid_for_save` works."""
    assert client.check_name_valid_for_save(filename, clobber=True)[0] == truthiness
