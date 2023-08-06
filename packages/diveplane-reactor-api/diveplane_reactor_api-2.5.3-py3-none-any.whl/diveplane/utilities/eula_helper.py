import os
from pathlib import Path

from diveplane.direct import DiveplaneDirectClient
from diveplane.client.client import get_diveplane_client_class
from diveplane.direct._utilities import (
    DIVEPLANE_EULA_ENV_VAR,
    DiveplaneLicenseAcceptanceException,
    get_eula_acceptance_file_path,
    license_check,
    LicenseType,
)
from rich import print

DIVEPLANE_EULA_FILE = "LICENSE.TXT"


def eula_not_accepted():
    """Walk end-user through accepting (or not) the license."""
    # ATTN: This is formatted for an 80 column terminal. Please do not make
    # whitespace (or other) changes without careful testing!
    eula_file = get_eula_acceptance_file_path()

    response = input(r'''
In order to continue, this agreement must be accepted. If you have read and
accept the terms and conditions presented in this document, enter "I ACCEPT".
> ''')
    if response.lower() == "i accept":
        try:
            eula_file.parent.mkdir(parents=True, exist_ok=True)
            eula_file.touch(exist_ok=True)
        except Exception:  # noqa: Deliberately broad
            """Something went wrong, advise the alternative ENV VAR method."""
            print(rf'''
This utilitiy unsuccessfully tried to create a file at "{eula_file}"
to indicate that the Diveplane Corporation Free Software License Terms was
accepted.

An alternative method of indicating acceptance of the license is to set an
environment variable "{DIVEPLANE_EULA_ENV_VAR}" to "True" before running
the Diveplane software.
''')
        else:
            print(rf'''
This utility successfully created a file at:
{eula_file}
which indicates that the Diveplane Corporation Free Software License Terms was
read and accepted. The software should now run without interruption.
''')


def eula_already_accepted():
    """Show the end-user which artifact indicates the EULA was accepted."""
    env_var_value = os.environ.get(DIVEPLANE_EULA_ENV_VAR, '')
    env_var = env_var_value.lower() == 'true'
    eula_file = get_eula_acceptance_file_path()

    print('The Diveplane End User License Agreement was read and accepted as '
          'indicated by ', end='')

    if env_var:
        print(f'the\nenvironment variable "{DIVEPLANE_EULA_ENV_VAR}" set to '
              f'"{env_var_value}".')
    else:
        print(f'the existance of the file:\n{eula_file}')

    print('\nThe software should run without interruption.')


def main():
    """
    Primary entry point.

    Attempt to create a client, if the DiveplaneLicenseAcceptanceException is
    raised, then help the user.
    """
    klass, _ = get_diveplane_client_class()
    if issubclass(klass, DiveplaneDirectClient):
        try:
            license_type = license_check()
        except DiveplaneLicenseAcceptanceException:
            eula_not_accepted()
        else:
            if license_type == LicenseType.COMMERCIAL:
                print('This software appears to be commercially licensed.')
            else:
                eula_already_accepted()
                print(r'''
If you would like to commercially license Diveplane software, please visit
https://diveplane.com/licensing/.
''')
    else:
        print('This software appears to be commercially licensed.')


if __name__ == "__main__":
    main()
