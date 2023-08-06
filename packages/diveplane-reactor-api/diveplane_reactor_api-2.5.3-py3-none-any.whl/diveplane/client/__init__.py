"""
The Python API for the Diveplane Client.

The Diveplane Python Client API has two major components,

- client module:
    A basic client that implements the Diveplane REST API.
- scikit module:
    Implements a scikit-learn Estimator which uses the Diveplane
    cloud service to make predictions off of fit data.


Additional submodules are included in the package but are for internal client/scikit operations and thus are omitted
from the documentation.

Examples implementations are included in the diveplane/examples directory.
"""

from .base import AbstractDiveplaneClient  # noqa: F401
from .client import (  # noqa: F401
    CONFIG_FILE_ENV_VAR,
    DEFAULT_CONFIG_FILE,
    DEFAULT_CONFIG_FILE_ALT,
    DiveplaneClient,
    get_configuration_path,
    get_diveplane_client
)
from .pandas.client import (  # noqa: F401
    DiveplanePandasClient,
)

diveplane_banner = """
                      ,▄▀▀▀▀█▄                 (R)
             ..⌐══ⁿ▀▀▀▀▀▀▀▀▀ ▀▌▀'
                ,▄▄▄ææAP▀▀▀▀▀▀▀███████▄▄▄,
▄▄▄    ,.═^"'                          '▀▀███▄
  |                                         ▀██
                                             █
                                            ▀
  _____  _                 _
 |  __ \\(_)               | |
 | |  | |___   _____ _ __ | | __ _ _ __   ___  (R)
 | |  | | \\ \\ / / _ \\ '_ \\| |/ _` | '_ \\ / _ \\
 | |__| | |\\ V /  __/ |_) | | (_| | | | |  __/
 |_____/|_| \\_/ \\___| .__/|_|\\__,_|_| |_|\\___|
                    | |
                    |_|

Understandable AI (R)
"""

__all__ = [
    "AbstractDiveplaneClient",
    "diveplane_banner",
    "CONFIG_FILE_ENV_VAR",
    "DEFAULT_CONFIG_FILE",
    "DEFAULT_CONFIG_FILE_ALT",
    "get_configuration_path",
    "DiveplaneClient",
    "DiveplanePandasClient",
    "get_diveplane_client",
    "__version__",
]


# The version number is automatically incremented by the pipeline
# It should not be manually changed.
# To change the major/minor number change the number in azure-pipelines.yml

__version__ = "2.5.3"
