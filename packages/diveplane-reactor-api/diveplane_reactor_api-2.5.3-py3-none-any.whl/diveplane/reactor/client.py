from diveplane.client import AbstractDiveplaneClient, DiveplanePandasClient
from diveplane.client.pandas import DiveplanePandasClientMixin

__client_instance = None

__all__ = {
    'get_client',
    'use_client',
}


def get_client() -> AbstractDiveplaneClient:
    """
    Get the active Diveplane client instance.

    Returns
    -------
    DiveplanePandasClient
        The active client.
    """
    global __client_instance
    if __client_instance is None:
        __client_instance = DiveplanePandasClient()
    return __client_instance


def use_client(client: AbstractDiveplaneClient) -> None:
    """
    Set the active Diveplane client instance to use for the API.

    Parameters
    ----------
    client : AbstractDiveplaneClient
        The client instance.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        When the client is not an instance of AbstractDiveplaneClient.
    """
    global __client_instance
    if not isinstance(client, AbstractDiveplaneClient):
        raise ValueError("`client` must be a subclass of "
                         "AbstractDiveplaneClient")
    if not isinstance(client, DiveplanePandasClientMixin):
        raise ValueError("`client` must be a DiveplanePandasClient")
    __client_instance = client
