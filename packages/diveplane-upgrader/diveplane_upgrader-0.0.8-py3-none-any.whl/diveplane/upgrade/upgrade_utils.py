import os
from os.path import expanduser
from pathlib import Path
from typing import Optional, Union
import warnings
import yaml


DEFAULT_CONFIG_FILE = 'diveplane.yml'
DEFAULT_CONFIG_FILE_ALT = 'diveplane.yaml'
DEFAULT_CONFIG_FILE_LEGACY = 'config.yml'
DEFAULT_CONFIG_FILE_LEGACY_ALT = 'config.yaml'
CONFIG_FILE_ENV_VAR = 'DP_CONFIG'
HOME_DIR_CONFIG_PATH = '/.diveplane/'
XDG_DIR_CONFIG_PATH = '/diveplane/'
XDG_CONFIG_ENV_VAR = 'XDG_CONFIG_HOME'

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


class DiveplaneConfigurationError(Exception):
    """Custom DiveplaneConfigurationError Exception."""
    pass


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
        from diveplane import local as dp_local  # noqa: F401
    except ImportError:
        return None
    else:
        return Path(Path(dp_local.__file__).parent, "resources", file_name)


def _ask_update_config_path(filename, config_dir=''):
    """Ask the user if they want to rename the given filename to 'diveplane.yml'."""
    answer = input(f"Your Diveplane configuration file is named '{filename}' which is deprecated "
                   "(should be 'diveplane.yml'). Allow us to update? [y/n]: ")
    if answer.lower() in ['y', 'yes']:
        Path(config_dir + filename).rename(config_dir + DEFAULT_CONFIG_FILE)
        return config_dir + DEFAULT_CONFIG_FILE
    return config_dir + filename


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
            config_path = _ask_update_config_path(DEFAULT_CONFIG_FILE_LEGACY)
        # falling back to config.yaml file
        elif os.path.isfile(DEFAULT_CONFIG_FILE_LEGACY_ALT):
            config_path = _ask_update_config_path(DEFAULT_CONFIG_FILE_LEGACY_ALT)

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
            config_dir = user_dir + HOME_DIR_CONFIG_PATH
            config_path = _ask_update_config_path(DEFAULT_CONFIG_FILE_LEGACY, config_dir=config_dir)
        # falling back to config.yaml file
        elif os.path.isfile(user_dir + HOME_DIR_CONFIG_PATH + DEFAULT_CONFIG_FILE_LEGACY_ALT):  # noqa
            config_dir = user_dir + HOME_DIR_CONFIG_PATH
            config_path = _ask_update_config_path(DEFAULT_CONFIG_FILE_LEGACY_ALT, config_dir=config_dir)

        # If local is installed, use that config only if no other config was found
        if diveplane_local_installed:
            if config_path is None:
                config_path = dp_local_config
            else:  # may be deliberate, but we should warn the user
                warnings.warn('Diveplane local is installed, but a configuration file at '
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


class DiveplaneConfiguration:
    """
    Diveplane client configuration.

    Parameters
    ----------
    config_path : str
        The path to the user's diveplane.yml
    verbose : bool, default False
        Set verbose output.
    """

    def __init__(self, *args, config_path=None, verbose=False, **kwargs):
        """Initialize the configuration object."""
        super().__init__(*args, **kwargs)
        self.dp_config_path = config_path
        self.verbose = verbose

        if self.verbose:
            print(f'Using config file: {config_path}')

        try:
            with open(config_path, 'r') as config:
                self.user_config = yaml.safe_load(config)
        except yaml.YAMLError as yaml_exception:
            raise DiveplaneConfigurationError(
                'Unable to parse the configuration file located at '
                f'"{config_path}". Please verify the YAML syntax '
                'of this file and try again.'
            ) from yaml_exception
        except (IOError, OSError) as exception:
            raise DiveplaneConfigurationError(
                'Error reading the configuration file located at '
                f'"{config_path}". Check the file permissions and '
                'try again.'
            ) from exception

    def get_user_config_option(self, *args, default=None):
        """
        Retrieve a configuration option from the user's diveplane.yml settings.

        Parameters
        ----------
        args : str
            The path to the option in the configuration data.
        default : Any, default None
            The value to default to if not found.

        Returns
        -------
        Any
            The value of the option at the given path.
        """
        if len(args) == 0:
            raise AssertionError('At least one configuration option key '
                                 'is required.')
        option = self.user_config
        for arg in args:
            try:
                option = option[arg]
            except (KeyError, TypeError):
                return default
        return option

    def set_diveplane_client(self, value: str):
        """
        Set the user's 'Diveplane.client' value in the diveplane.yml file.

        Parameters
        ----------
        value: str
            The value to set. Defaults to an empty string.
        """
        self.user_config['Diveplane']['client'] = value
        with open(self.dp_config_path, 'w') as config:
            yaml.dump(self.user_config, config)
