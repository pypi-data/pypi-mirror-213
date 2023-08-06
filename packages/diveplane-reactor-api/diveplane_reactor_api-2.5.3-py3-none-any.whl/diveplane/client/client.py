"""Primary Diveplane Client Class."""
from importlib import import_module
import itertools
import os
from os.path import expanduser
from pathlib import Path, PurePath
from typing import Optional, Union
import warnings

from diveplane.client.base import AbstractDiveplaneClient
from diveplane.client.exceptions import DiveplaneConfigurationError
from diveplane.utilities import UserFriendlyExit
import yaml

DEFAULT_CONFIG_FILE = 'diveplane.yml'
DEFAULT_CONFIG_FILE_ALT = 'diveplane.yaml'
DEFAULT_CONFIG_FILE_LEGACY = 'config.yml'
CONFIG_FILE_ENV_VAR = 'DP_CONFIG'
HOME_DIR_CONFIG_PATH = '/.diveplane/'
XDG_DIR_CONFIG_PATH = '/diveplane/'
XDG_CONFIG_ENV_VAR = 'XDG_CONFIG_HOME'


def _get_diveplane_local_resources_path(file_name: str) -> Union[Path, None]:
    """
    Return the Path of a file in `diveplane.local.resources`.

    Parameters
    ----------
    file_name: str
        The name of a file in the diveplane.local.resources package.

    Returns
    -------
    Path or None
        The path to the given file name in Diveplane Local resources. None is
        returned if the module isn't available in the current environment or
        the file does not exist there.
    """
    try:
        from diveplane import local as dp_local
    except ImportError:
        return None
    else:
        return Path(Path(dp_local.__file__).parent, "resources", file_name)


def _get_diveplane_community_resources_path(file_name: str) -> Union[Path, None]:
    """
    Return the Path of a file in `diveplane.community.resources`.

    Parameters
    ----------
    file_name: str
        The name of a file in the diveplane.community.resources package.

    Returns
    -------
    Path or None
        The path to the given file name in Diveplane Community resources. None is
        returned if the module isn't available in the current environment or
        the file does not exist there.
    """
    try:
        from diveplane import community as dp_community
    except ImportError:
        return None
    else:
        mypath = Path(Path(dp_community.__file__).parent, "resources", file_name)
        return Path(Path(dp_community.__file__).parent, "resources", file_name)


def get_configuration_path(config_path: Optional[str] = None,  # noqa: C901
                           verbose: bool = False):
    """
    Determine where the configuration is stored, if anywhere.

    If no config found, will exit with a friendly error message.

    Parameters
    ----------
    config_path : str or None
        The given config_path.
    verbose : bool
        If True provides more verbose messaging. Default is false.

    Returns
    -------
    The found config_path
    """
    if config_path is None:
        # Check DP_CONFIG env variable
        user_dir = str(expanduser("~"))
        xdg_config_home_not_abs_msg = (
            'The path set in the XDG_CONFIG_HOME environment variable'
            'is not absolute: "{0}". The specification for XDG_CONFIG_HOME '
            'variables requires the value to be an absolute path.'.format(
                os.environ.get(XDG_CONFIG_ENV_VAR)
            ))
        # Calculate if diveplane-local is installed
        dp_local_config = _get_diveplane_local_resources_path(DEFAULT_CONFIG_FILE)
        # Boolean to check if diveplane-local is installed
        diveplane_local_installed = False
        if isinstance(dp_local_config, Path) and dp_local_config.is_file():
            diveplane_local_installed = True

        # Calculate if diveplane-community is installed
        dp_community_config = _get_diveplane_community_resources_path(DEFAULT_CONFIG_FILE)
        # Boolean to check if diveplane-community is installed
        diveplane_community_installed = False
        if isinstance(dp_community_config, Path) and dp_community_config.is_file():
            diveplane_community_installed = True
        
        # Check if DP_CONFIG env variable is set
        if os.environ.get(CONFIG_FILE_ENV_VAR) is not None:
            config_path = os.environ[CONFIG_FILE_ENV_VAR]
            if not os.path.isfile(config_path):
                raise DiveplaneConfigurationError(
                    'The environment variable "{0}" was found, but it does '
                    'not point to Diveplane configuration '
                    'file.'.format(CONFIG_FILE_ENV_VAR))
            elif verbose:
                print(CONFIG_FILE_ENV_VAR + ' set to ' + config_path)
        # Check current working directory for diveplane.yml file
        elif os.path.isfile(DEFAULT_CONFIG_FILE):
            config_path = DEFAULT_CONFIG_FILE
        # falling back to diveplane.yaml file
        elif os.path.isfile(DEFAULT_CONFIG_FILE_ALT):
            config_path = DEFAULT_CONFIG_FILE_ALT
        # falling back to config.yml file
        elif os.path.isfile(DEFAULT_CONFIG_FILE_LEGACY):
            config_path = DEFAULT_CONFIG_FILE_LEGACY
            warnings.warn(
                'Deprecated use of diveplane "config.yml" file. '
                'rename to diveplane.yml')

        # Check for .yml config file in XDG_CONFIG_HOME directory, if configured
        elif (
            os.environ.get(XDG_CONFIG_ENV_VAR) is not None and
            os.path.isfile(os.environ[XDG_CONFIG_ENV_VAR] + XDG_DIR_CONFIG_PATH + DEFAULT_CONFIG_FILE)):  # noqa
            # Check if XDG_CONFIG_HOME is an absolute path.
            if not os.path.isabs(os.path.expandvars(os.environ.get(XDG_CONFIG_ENV_VAR))):
                raise DiveplaneConfigurationError(xdg_config_home_not_abs_msg)
            config_path = os.environ[XDG_CONFIG_ENV_VAR] + XDG_DIR_CONFIG_PATH + DEFAULT_CONFIG_FILE
        # Check for .yaml config file in XDG_CONFIG_HOME directory, if configured
        elif (
            os.environ.get(XDG_CONFIG_ENV_VAR) is not None and
            os.path.isfile(os.environ[XDG_CONFIG_ENV_VAR] + XDG_DIR_CONFIG_PATH + DEFAULT_CONFIG_FILE_ALT)):  # noqa
            # Check if XDG_CONFIG_HOME is an absolute path.
            if not os.path.isabs(os.path.expandvars(os.environ.get(XDG_CONFIG_ENV_VAR))):
                raise DiveplaneConfigurationError(xdg_config_home_not_abs_msg)
            config_path = os.environ[XDG_CONFIG_ENV_VAR] + XDG_DIR_CONFIG_PATH + DEFAULT_CONFIG_FILE_ALT
        # Check default home directory for config file
        elif os.path.isfile(user_dir + HOME_DIR_CONFIG_PATH + DEFAULT_CONFIG_FILE):  # noqa
            config_path = user_dir + HOME_DIR_CONFIG_PATH + DEFAULT_CONFIG_FILE
        # falling back to diveplane.yaml file
        elif os.path.isfile(user_dir + HOME_DIR_CONFIG_PATH + DEFAULT_CONFIG_FILE_ALT):  # noqa
            config_path = user_dir + HOME_DIR_CONFIG_PATH + DEFAULT_CONFIG_FILE_ALT
        # falling back to config.yml file
        elif os.path.isfile(user_dir + HOME_DIR_CONFIG_PATH + DEFAULT_CONFIG_FILE_LEGACY):  # noqa
            config_path = user_dir + HOME_DIR_CONFIG_PATH + DEFAULT_CONFIG_FILE_LEGACY
            warnings.warn(
                'Deprecated use of diveplane "config.yml" file. '
                'rename to diveplane.yml')

        # If local is installed, use that config only if no other config was found
        if diveplane_local_installed:
            if config_path is None:
                config_path = dp_local_config
            else:  # may be deliberate, but we should warn the user
                warnings.warn('Diveplane local is installed, but a configuration file at '
                              f'{config_path} was found that will take precendence.')
        elif diveplane_community_installed: # only use community if local is not installed
            if config_path is None:
                config_path = dp_community_config
            else:
                warnings.warn('Diveplane community is installed, but a configuration file at '
                              f'{config_path} was found that will take precendence.')


        if config_path is None:
            raise DiveplaneConfigurationError(
                'No configuration file found. Specify configuration with the '
                '"{0}" environment variable, config parameter or place a '
                'diveplane.yml file in {1}{2} or your current working '
                'directory.'.format(
                    CONFIG_FILE_ENV_VAR, user_dir, HOME_DIR_CONFIG_PATH))

    # Verify file in config_path parameter exists
    elif not os.path.isfile(config_path):
        raise DiveplaneConfigurationError(
            "Specified configuration file was not found. Verify that the "
            "location of your configuration file matches the config parameter "
            "used when instantiating the client.")
    if verbose:
        print(f'Using configuration at path: {config_path}')
    return config_path


def get_extras_path(directory: Union[str, PurePath]):
    """
    Look for a file `extras.yml` or similar in the given path.

    If found, return the path to the file, else, None.

    Parameters
    ----------
    directory : str or Path
        The directory to look within. This is given as the directory containing
        the `diveplane.yml` et al file.

    Returns
    -------
    Path or None
        The file path to the extras.yml file, or None, if none found.
    """
    extras_stems = ['extras', 'Extras', 'EXTRAS']
    extras_exts = ['yml', 'yaml', 'YML', 'YAML']
    for stem, ext in itertools.product(extras_stems, extras_exts):
        extras_path = Path(directory, f"{stem}.{ext}")
        if extras_path.exists():
            return extras_path
    return None


def get_diveplane_client_class(**kwargs):  # noqa: C901
    """
    Return the appropriate AbstractDiveplaneClient subclass based on config.

    This is a "factory function" that, based on the given parameters, will
    decide which AbstractDiveplaneClient derivative to return.

    Parameters
    ----------
    kwargs : dict
        config_path: str or None
            The path to a valid configuration file, or None
        verbose : bool
            If True provides more verbose messaging. Default is false.
        Any other kwargs. These will be passed to the client constructor along
        with `config_path` and `verbose`.

    Returns
    -------
    AbstractDiveplaneClient
        A resolved subclass of AbstractDiveplaneClient.
    dict
        Client extra kwargs.
    """
    config_path = kwargs.get('config_path', None)
    verbose = kwargs.get('verbose', False)

    kind_exit = UserFriendlyExit(verbose=verbose)

    # Attempt to load and parse config.yaml.
    config_path = get_configuration_path(config_path, verbose)
    try:
        with open(config_path, 'r') as config:
            config_data = yaml.safe_load(config)
    except yaml.YAMLError as yaml_exception:
        kind_exit('Unable to parse the configuration file located at "{0}". '
                  'Please verify the YAML syntax of this file and '
                  'try again.'.format(config_path), exception=yaml_exception)
    except (IOError, OSError) as exception:
        kind_exit('Error reading the configuration file located at "{0}". '
                  'Check the file permissions and try '
                  'again.'.format(config_path), exception=exception)

    client_class = None

    # Check if the configuration file `config.yaml` contains the item
    # 'client' that is a valid, dotted-path to another sub-class of
    # AbstractDiveplaneClient. If so, instantiate that one and return it. This
    # provides an opportunity for customer-specific functionality and/or
    # authentication schemes, etc.
    try:
        custom_client = config_data['Diveplane']['client']
        # Split the dotted-path into "module" and the specific "class". For
        # example. `my_package.my_module.MyClass' would become
        # `custom_module_path` of `my_package.my_module` and
        # `custom_class_name` becomes `MyClass`.
        custom_module_path, custom_class_name = custom_client.rsplit('.', 1)
        # Attempt to load the module itself.
        custom_module = import_module(custom_module_path)
        # Set `client_class` to the actual class provided at the end of the
        # dotted-path.
        client_class = getattr(custom_module, custom_class_name)
        # Ensure that the `client_class` is a subclass of
        # AbstractDiveplaneClient.
        if not issubclass(client_class, AbstractDiveplaneClient):
            raise DiveplaneConfigurationError(
                'The provided client_class must be a subclass '
                'of AbstractDiveplaneClient.')
    except KeyError:
        # Looks like no attempt was made to override the default client class.
        # By passing here, we'll determine a default class to return
        pass
    except (AttributeError, ImportError, ModuleNotFoundError, ValueError) as exception:
        # User attempted to override the default client class, but there was
        # an error.
        kind_exit('The configuration at Diveplane -> client, if provided, '
                  'should contain a valid dotted-path to a '
                  'subclass of AbstractDiveplaneClient.', exception=exception)
    except DiveplaneConfigurationError as exception:
        # User provided a dotted-path to a class, but it's not a subclass of
        # the AbstractDiveplaneClient
        kind_exit('The client configured in Diveplane -> client is not a '
                  'valid subclass of AbstractDiveplaneClient.',
                  exception=exception)

    # Determine default client if one is not set by the config
    if client_class is None:
        try:
            # If the platform client found, give precedence to this client
            from diveplane.platform import DiveplanePlatformClient
            client_class = DiveplanePlatformClient
        except ImportError:
            # Otherwise use the direct client
            from diveplane.direct import DiveplaneDirectClient
            client_class = DiveplaneDirectClient

    # customer-specific functionality and/or authentication schemes, etc.
    try:
        client_extra_params = config_data['Diveplane']['client_extra_params']
    except KeyError:
        # No extra params set - that is ok - let's move on
        client_extra_params = dict()

    if client_extra_params is None:
        client_extra_params = dict()
    elif not isinstance(client_extra_params, dict):
        kind_exit('The configuration at Diveplane -> client_extra_params '
                  'should be defined as a dictionary.')

    # Add extras
    if not isinstance(config_path, PurePath):
        config_path = Path(config_path)
    extras_path = get_extras_path(config_path.parent)
    if extras_path:
        try:
            with open(extras_path, 'r') as extra_config:
                extra_data = yaml.safe_load(extra_config)
                client_extra_params.update(extra_data['Diveplane'])
        except Exception:  # noqa: deliberately broad
            pass

    if verbose:
        print("Instantiating %r" % client_class)

    return client_class, client_extra_params


def get_diveplane_client(**kwargs):
    """
    Return the appropriate AbstractDiveplaneClient subclass based on config.

    This is a "factory function" that, based on the given parameters, will
    decide which AbstractDiveplaneClient derivative to instantiate and return.

    Parameters
    ----------
    config_path: str or None, optional
        The path to a valid configuration file, or None
    verbose : bool, optional
        If True provides more verbose messaging. Default is false.
    kwargs : dict
        Additional client arguments. These will be passed to the client
        constructor along with `config_path` and `verbose`.

    Returns
    -------
    AbstractDiveplaneClient
        An instantiated subclass of AbstractDiveplaneClient.
    """
    client_class, client_params = get_diveplane_client_class(**kwargs)
    client_params.update(kwargs)
    return client_class(**client_params)


# For backwards compatibility, let this factory function assume the default
# client class name.
DiveplaneClient = get_diveplane_client
