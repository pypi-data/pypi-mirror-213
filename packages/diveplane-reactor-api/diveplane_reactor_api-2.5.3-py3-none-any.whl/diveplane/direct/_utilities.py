from datetime import datetime
from enum import IntEnum
from importlib import metadata
import os
from pathlib import Path
import sysconfig
from typing import Union

from diveplane import direct
from diveplane.client.exceptions import DiveplaneError
from rich import print

DIVEPLANE_EULA_ENV_VAR = "DIVEPLANE_EULA_ACCEPTED"
DIVEPLANE_EULA_ACCEPTED_FILE = "diveplane_eula_accepted.txt"


class LicenseType(IntEnum):
    COMMERCIAL = 1
    FREEWARE = 2


def model_from_dict(klass, obj):
    """
    Create OpenAPI model instance from dict.

    Parameters
    ----------
    klass : Type
        The class to instantiate.
    obj : dict or None
        The dict containing the class attributes.

    Returns
    -------
    Any
        The class instance.
    """
    if obj is None:
        return None
    if not isinstance(obj, dict):
        raise ValueError('`obj` parameter is not a dict')
    if not hasattr(klass, 'attribute_map'):
        raise ValueError("`klass` is not an OpenAPI model")
    # Only use known attributes for class instantiation
    parameters = dict()
    for key in obj.keys():
        if key in klass.attribute_map:
            dtype = klass.openapi_types[key]
            if dtype == 'datetime':
                parameters[key] = datetime.fromisoformat(obj[key])
            else:
                parameters[key] = obj[key]
    return klass(**parameters)


class DiveplaneLicenseAcceptanceException(DiveplaneError):
    """Raised when license acceptance is required, but not indicated."""


def get_file_in_distribution(file_path) -> Union[Path, None]:
    """
    Locate the LICENSE.txt file in the distribution of this package.

    Parameters
    ----------
    file_path : str
        The name/path of the desired file relative to the package distribution.

    Returns
    -------
    Path or None
        The path to the requested file or None, if not found.
    """
    purelib_path = sysconfig.get_path('purelib')
    dist = metadata.distribution('diveplane-reactor-api')
    for fp in dist.files:
        if fp.name == file_path:
            return Path(purelib_path, fp)


def get_eula_acceptance_file_path() -> Path:
    """Get the path to the special file."""
    license_accepted_path = Path(
        Path(direct.__file__).parent, "resources",
        DIVEPLANE_EULA_ACCEPTED_FILE)
    return license_accepted_path


def license_check() -> LicenseType:
    """
    Perform a commercial licence check.

    If a license acceptance is required and neither of these two artifacts
    exist, raise a DiveplaneLicenseAcceptanceException exception:
      - An ENV variable "DIVEPLANE_EULA_ACCEPTED" which is set to "True"
      - A file located in the diveplane package resources named
        "diveplane_eula_accepted.txt"

    Returns
    -------
    LicenseType
        LicenseType.COMMERCIAL if this is commercially licensed software.
        LicenseType.FREEWARE if this is subject to the Diveplane Corporation
        Free Software License Terms.

    Raises
    ------
    DiveplaneLicenseAcceptanceException
        If license acceptance is required, but not indicated.
    """
    try:
        # Diveplane Platform software is commercially licensed.
        from diveplane.platform.client import DiveplanePlatformClient  # noqa: F401
    except ImportError:
        pass
    else:
        return LicenseType.COMMERCIAL

    license_path = get_file_in_distribution("LICENSE.txt")
    license_accepted_path = get_eula_acceptance_file_path()

    if (
        os.environ.get(DIVEPLANE_EULA_ENV_VAR, '').lower() != "true"
        and not (
            license_accepted_path and license_accepted_path.exists()
        )
    ):
        # ATTN: This is formatted for an 80 column terminal. Please do not make
        # whitespace (or other) changes without careful testing!
        print(rf'''
This version of Diveplane® Reactor™ and related software is distributed under
the Diveplane Corporation Free Software License Terms which must be read and
accepted before continuing. The terms may be found here:
{license_path}''')
        print(rf'''
To indicate this acceptance, ensure there is an environment variable present
named "DIVEPLANE_EULA_ACCEPTED" with the value "True". Or, alternatively,
ensure a file exists at this location (the file contents do not matter):
{license_accepted_path}''')

        raise DiveplaneLicenseAcceptanceException(
            'The Diveplane Corporation Free Software License Terms must '
            'be accepted.')
    else:
        return LicenseType.FREEWARE
