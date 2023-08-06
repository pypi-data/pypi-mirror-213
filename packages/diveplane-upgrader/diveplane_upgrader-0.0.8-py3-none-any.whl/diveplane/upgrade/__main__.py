import argparse
from argparse import RawTextHelpFormatter
import json
import re
import subprocess
import sys
import os

from diveplane.upgrade.upgrade_utils import (
    diveplane_banner,
    DiveplaneConfiguration,
    get_configuration_path,
)


# Text color codes
CEND = '\33[0m'
CBLUE = '\33[34m'
CGREEN = '\33[32m'
CRED = '\33[31m'
CYELLOW = '\33[33m'

# Point at which older diveplane's need to be removed before upgrading
DIVEPLANE_REFACTOR_POINT_SEMVER = '68.0.0'

# Top-level Diveplane packages.
# NOTE: sub-dependencies should not be included here, as they will be installed
# at the correct version automatically by pip
DIVEPLANE_TOP_LEVEL_PACKAGES = [
    'diveplane',
    'diveplane-geminai',
    'diveplane-geminai-data-services',
    'diveplane-dqt-enterprise',
    'diveplane-dqt-community',
    'diveplane-upgrader',
    'diveplane-local',
    'diveplane-reactor-community',
]
# Sub-packages required by top-level packages
DIVEPLANE_SUB_PACKAGES = [
    'diveplane-reactor-api',
    'diveplane-amalgam-api',
    'diveplane-openapi-client',
    'diveplane-openapi-platform-client',
    'diveplane-local-no-telemetry',
    'diveplane-platform-openapi-client',
]
DEPRECATED_PACKAGES = [
    'diveplane-core-api',
    'diveplane-reactor',
]


def warn(msg):
    """Print a message with a yellow warning tag."""
    print(CYELLOW + '[WARNING] ' + CEND + msg)


def error(msg):
    """Print a message with a red error tag."""
    print(CRED + '[ERROR] ' + CEND + msg)


def ok(msg):
    """Print a message with a green check."""
    print(CGREEN + u'[\u2713] ' + CEND + msg)


def conf_error():
    """Raise an error about the PyPi configuration and exit the program."""
    error("'extra_index_url' not found in the 'Diveplane' "
          "section of diveplane.yml. Please set this value or specify it with the "
          "--extra-index-url argument (run 'python -m diveplane.upgrade -h' for more info).")
    exit(1)


def find_package(all_installed, package_name):
    """ Find the version of a package in the list of installed packages."""
    for installed in all_installed:
        if installed['name'] == package_name:
            return installed
    return None


def is_version_greater(version, minimum):
    """Check if the semver version is greater than or equal to the minimum version."""
    version_parts = list(map(int, version.split('.')))
    min_parts = list(map(int, minimum.split('.')))
    return version_parts > min_parts


def main():  # noqa: C901
    """Upgrade Diveplane software installed to the current Python environment.
    Also remove any deprecated packages if they exist."""
    # Parse for the --force flag to execute the pip command to upgrade all Diveplane packages
    upgrader_help = (diveplane_banner +
                     "\nDiveplane client upgrade utility.\n"
                     "Run without parameters in most use cases.\n\n")
    parser = argparse.ArgumentParser(description=upgrader_help,
                                     formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        '-f', '--force', dest='force', required=False, default=False,
        action='store_true',
        help=('Upgrade Diveplane client without prompting for confirmation. ')
    )

    # Remove all diveplane packages and reinstall
    parser.add_argument(
        '--reset', dest='reset', required=False, default=False,
        action='store_true', help='Remove all diveplane packages and reinstall.'
    )

    # Check for a manually specified --dry-run
    parser.add_argument(
        '--dryrun', dest='dryrun', required=False, default=False,
        action='store_true',
        help=('Show upgrade commands, but do not execute them. ')
    )

    # Check for a manually specified --extra-index-url
    parser.add_argument(
        '--extra-index-url', dest='index', required=False, default='',
        help=('Specify an alternate PyPi repository. This will take '
              'precedence over the value stored in diveplane.yml, if any.')
    )
    # Check for a manually specified --pip-cache directory
    parser.add_argument(
        '-a', '--pip-archive', dest='piparchive', required=False, default='',
        help=('Specify a local pip archive directory to resolve packages from.')
    )

    args = parser.parse_args()
    print(diveplane_banner)

    # Diveplane configuration
    configuration = DiveplaneConfiguration(
        config_path=get_configuration_path(), verbose=False
    )

    # Pip resolving logic:
    # We need to deal with the following scenarios:
    # 1. User has a Diveplane Platform to resolve packages from (using an extra-index-url in diveplane.yml or --extra-index-url)
    # 2. User has a Diveplane Local install using a pip archive
    # For now the upgrader does not support using both at the same time.
    #   - Fail if both are specified via cmd line.
    #   - Warn if extra-index-url is specified diveplane.yml, but pip-archive is also specified via cmd line
    #     (the diveplane.yml value will be ignored in this case).

    # if an archive is specified, check it is a valid directory
    if args.piparchive:
        if not os.path.isdir(args.piparchive):
            print("Error: --pip-archive must be a valid directory.")
            sys.exit(1)

    # Fail if both --extra-index-url and --pip-archive are specified
    if args.index and args.piparchive:
        print("Error: --extra-index-url and --pip-archive cannot be used together.")
        sys.exit(1)

    # Determine the PyPi index URL
    url_in_conf = False
    if args.index:
        # If the command-line index was specified, use it
        extra_index_url = args.index
    else:
        # Check Diveplane.yml for 'extra_index_url'
        extra_index_url = configuration.get_user_config_option(
            'Diveplane',
            'extra_index_url'
        )
        # If the user has a pip archive, use that instead
        if args.piparchive:
            if extra_index_url:
                warn("extra_index_url found in diveplane.yml, but --pip-archive was also specified. "
                     "The extra_index_url will be ignored.")
                extra_index_url = ''
        else:
            if not extra_index_url:
                pip_cmd = f'{sys.executable} -m pip config get global.extra-index-url'
                conf = subprocess.getoutput(pip_cmd).split('[notice]')[0]
                if 'ERROR' in conf:
                    conf_error()
                print(f"The following extra-index-url was found in your pip config: {conf}")
                if not args.force:
                    answer = input("Is this the PyPi repository you wish to install Diveplane software "
                                   "from? [y/n]: ")
                    if answer.lower() in ['y', 'yes']:
                        extra_index_url = conf
                        url_in_conf = True
                    else:
                        conf_error()
                else:
                    # Fail as we don't want to force an upgrade, without confirming the PyPi repo
                    error("Cannot force upgrade without specifying an extra index url.")
                    exit(1)

    if not args.piparchive:
        # Parse out trusted-host
        match = re.search(
            r"^(?:https?:\/\/)?(?:[^@\n]+@)?([^:\/\n?]+)",
            extra_index_url,
            re.IGNORECASE,
        )
        if match is None:
            error('extra-index-url has invalid PyPi repository format.')
            exit(1)
        trusted_host = match.group(1)

    # Check the 'Diveplane.client' property in diveplane.yml
    client = configuration.get_user_config_option(
        'Diveplane',
        'client'
    )
    if client == 'diveplaned.client.DirectDiveplaneClient':
        warn('The Diveplane.client value in your diveplane.yml is out-of-date (should be '
             'diveplane.direct.DiveplaneDirectClient).')
        answer = input('Do you allow us to make the recommended change to your diveplane.yml? '
                       '[y/n] ')
        if answer.lower() in ['y', 'yes']:
            configuration.set_diveplane_client('diveplane.direct.DiveplaneDirectClient')
            ok('Successfully updated diveplane.yml')
        else:
            warn('Diveplane software may not work properly with a deprecated client value in your '
                 'diveplane.yml.')

    # Get installed packages by running 'pip list'
    pip_cmd = f'{sys.executable} -m pip list --format json --disable-pip-version-check'
    all_installed = json.loads(
        subprocess.getoutput(pip_cmd).split('[notice]')[0]
    )

    # Detect installed Diveplane packages (and any that should be removed)
    dp_installed = []
    dp_installed_deps = []
    to_remove = []
    for pkg in all_installed:
        if pkg['name'] in DIVEPLANE_TOP_LEVEL_PACKAGES:
            dp_installed.append(pkg['name'])
        elif pkg['name'] in DIVEPLANE_SUB_PACKAGES:
            dp_installed_deps.append(pkg['name'])
        elif pkg['name'] in DEPRECATED_PACKAGES:
            to_remove.append(pkg['name'])

    # Upgrading diveplane through the version at DIVEPLANE_REFACTOR_POINT_SEMVER refactor point
    # (where diveplane was split into diveplane, diveplane-reactor-api, etc) requires diveplane
    # to be removed first.  Otherwise the diveplane/client directory that is added by reactor
    # is removed again when diveplane is uninstalled.
    if 'diveplane' in dp_installed:
        # Check the version of diveplane installed is past the refactor point
        if not is_version_greater(find_package(all_installed, 'diveplane')['version'],
                                  DIVEPLANE_REFACTOR_POINT_SEMVER):
            # ... remove diveplane, so it is removed before reactor is installed
            to_remove.append('diveplane')
            # with this diveplane version, reactor shouldn't be there, but remove if it is.
            if 'diveplane-reactor-api' in dp_installed_deps:
                to_remove.append('diveplane-reactor-api')
        else:
            # If a customer has updated past the refactor point, but without uninstalling
            # they will have a recent diveplane, but may have overwritten the diveplane/client
            # sitepackages directory during that install.
            # if to_remove is not empty, then add diveplane and reactor to remove list
            # (they will be reinstalled later)
            # if to_remove container 'diveplane-core-api' then ..
            if find_package(all_installed, 'diveplane-core-api'):
                to_remove.extend(['diveplane', 'diveplane-reactor-api'])

    if not dp_installed:
        error('Did not discover any Diveplane software installed. Exiting.')
        exit(1)
    else:
        ok('Discovered Diveplane packages: ' + CBLUE + ", ".join(dp_installed) + CEND)

    # if reset, then add all diveplane installed packages to remove list
    if args.reset:
        to_remove.extend(dp_installed)
        to_remove.extend(dp_installed_deps)

    # Check if we should remove any deprecated software before upgrading
    pip_rm_cmd = None
    if to_remove:
        warn('Packages slated for uninstall: '
             f'{CYELLOW + ", ".join(to_remove) + CEND}')
        pip_rm_cmd = f'pip uninstall -y {" ".join(to_remove)}'
        if args.dryrun:
            ok('To remove packages slated for uninstall, run the following command: ')
            print()
            print(f'{CGREEN + pip_rm_cmd + CEND}\n')

    # Craft the 'pip install' command
    if args.piparchive:
        pip_cmd = f'pip install -U --no-index --find-links {args.piparchive} {" ".join(dp_installed)}'
    else:
        if url_in_conf:
            pip_cmd = (f'pip install -U --trusted-host {trusted_host} '
                       f'{" ".join(dp_installed)}')
        else:
            pip_cmd = (f'pip install -U --trusted-host {trusted_host} '
                       f'--extra-index-url {extra_index_url} {" ".join(dp_installed)}')

    # Run or simply print the pip command(s) that will upgrade all installed
    # Diveplane packages at once.
    if not args.dryrun:
        ok('Installing Diveplane software...')
        if not args.force:
            print('The following pip command(s) will be run:\n')
            if pip_rm_cmd:
                print(f'    > {CGREEN + pip_rm_cmd + CEND}')
            print(f'    > {CGREEN + pip_cmd + CEND}')
            print()
            answer = input("Continue with installation of Diveplane software? [y/n]: ")
            if not answer.lower() in ['y', 'yes']:
                print(f'{CYELLOW}Installation cancelled.{CEND}')
                exit(1)

        try:
            # Remove deprecated packages first
            if pip_rm_cmd:
                pip_rm_cmd = [sys.executable, '-m'] + pip_rm_cmd.split(' ')
                subprocess.check_call(pip_rm_cmd)
            # Install and upgrade packages
            pip_cmd = [sys.executable, '-m'] + pip_cmd.split(' ')
            subprocess.check_call(pip_cmd)
            ok('Your Diveplane software have been successfully upgraded!')
        except subprocess.CalledProcessError:
            error('There was a problem installing the Diveplane packages. '
                  'Please contact Diveplane support.')
    else:
        ok('To upgrade installed Diveplane packages, '
           'please run the following:\n')
        print(f'{CGREEN + pip_cmd + CEND}\n')


if __name__ == '__main__':
    main()
