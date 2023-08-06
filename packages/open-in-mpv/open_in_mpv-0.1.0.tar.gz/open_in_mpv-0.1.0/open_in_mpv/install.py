# SPDX-License-Identifier: MIT
from copy import deepcopy
from pathlib import Path
import json
import os
import platform
from typing import Any, Sequence

from loguru import logger
from whichcraft import which
import click
import xdg.BaseDirectory

IS_MAC = bool(platform.mac_ver()[0])
IS_WIN = bool(platform.win32_ver()[0])
IS_LINUX = not IS_MAC and not IS_WIN

JSON_FILENAME = 'sh.tat.open_in_mpv.json'
HOME = os.environ.get('HOME', '')

USER_CHROME_HOSTS_REG_PATH_WIN = 'HKCU:\\Software\\Google\\Chrome\\NativeMessagingHosts'

MAC_HOSTS_DIRS = (f'{HOME}/Library/Application Support/Google/Chrome Beta/NativeMessagingHosts',
                  f'{HOME}/Library/Application Support/Google/Chrome Canary/NativeMessagingHosts',
                  f'{HOME}/Library/Application Support/Google/Chrome/NativeMessagingHosts',
                  f'{HOME}/Library/Application Support/Chromium/NativeMessagingHosts')

SYSTEM_HOSTS_DIRS = ('/etc/chromium/native-messaging-hosts',
                     '/etc/opt/chrome/native-messaging-hosts',
                     '/etc/opt/edge/native-messaging-hosts')
USER_HOSTS_DIRS = (
    f'{xdg.BaseDirectory.xdg_config_home}/google-chrome/NativeMessagingHosts',
    f'{xdg.BaseDirectory.xdg_config_home}/google-chrome-beta/NativeMessagingHosts',
    f'{xdg.BaseDirectory.xdg_config_home}/google-chrome-canary/NativeMessagingHosts',
    f'{xdg.BaseDirectory.xdg_config_home}/chromium/NativeMessagingHosts',
    f'{xdg.BaseDirectory.xdg_config_home}/BraveSoftware/Brave-Browser/NativeMessagingHosts')

COMMON_HOST_DATA = {
    'description': 'Opens a URL in mpv (for use with extension).',
    'path': None,
    'type': 'stdio'
}
HOST_DATA = {
    **COMMON_HOST_DATA,
    # cspell:disable-next-line
    'allowed_origins': ['chrome-extension://ggijpepdpiehgbiknmfpfbhcalffjlbj/'],
    'name': 'sh.tat.open_in_mpv',
}
HOST_DATA_FIREFOX = {
    **COMMON_HOST_DATA,
    'allowed_extensions': ['{43e6f3ef-84a0-55f4-b9dd-d879106a24a9}'],
    'name': 'sh.tat.open-in-mpv',
}


def write_json(host_data: Any, directory: str) -> None:
    with open(Path(directory) / JSON_FILENAME) as f:
        logger.debug(f'Writing to {f.name}')
        json.dump(host_data, f)
        f.write('\n')


def write_json_files(host_data: Any, directories: Sequence[str], force: bool = False) -> None:
    for directory in directories:
        if os.path.exists(directory):
            write_json(host_data, directory)
        elif force:
            os.makedirs(directory, exist_ok=True)
            write_json(host_data, directory)


@click.command()
@click.option('-f', '--force', is_flag=True)
@click.option('-s', '--system', is_flag=True)
@click.option('-u', '--user', is_flag=True)
def main(system: bool = False, user: bool = False, force: bool = False) -> None:
    if not system and not user:
        click.echo('Need an action.', err=True)
        raise click.Abort()
    host_data = deepcopy(HOST_DATA)
    full_path = which('open-in-mpv')
    if not full_path:
        click.echo('open-in-mpv not found in PATH.', err=True)
        raise click.Abort()
    host_data['path'] = full_path
    if IS_LINUX and system and os.geteuid() != 0:
        click.echo('Run this as root.', err=True)
        raise click.Abort()
    if IS_LINUX:
        if system:
            for directory in SYSTEM_HOSTS_DIRS:
                os.makedirs(directory, exist_ok=True)
                write_json(host_data, directory)
        if user:
            write_json_files(host_data, USER_HOSTS_DIRS, force)
    if IS_MAC:
        write_json_files(host_data, MAC_HOSTS_DIRS, force)
