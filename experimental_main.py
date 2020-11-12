# This file is part of the NESi software.
#
# Copyright (c) 2020, inexio <https://github.com/inexio>
# Janis Groß <https://github.com/unkn0wn-user>
# Philip Konrath <https://github.com/Connyko65>
# Alexander Dincher <https://github.com/Dinker1996>
#
# Ilya Etingof <etingof@gmail.com>
#
# All rights reserved.
#
# License: https://github.com/inexio/NESi/LICENSE.rst
#
import argparse
import logging
import os
import sys
from urllib.parse import urlparse
import importlib

from nesi import __version__
from nesi import exceptions
from nesi.softbox.cli import rest_client
from nesi.softbox.base_resources import root, base
from bootup.sockets.telnet import TelnetSocket
import pytest

import subprocess
from nesi.softbox.api.views import *  # noqa
import pydevd_pycharm
import time


LOG = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description='Network Equipment Simulator')

    parser.add_argument(
        '--cli', action='store_true',
        help='Run Cli')

    parser.add_argument(
        '--api', action='store_true',
        help='Run api')

    parser.add_argument(
        '--snmp', action='store_true',
        help='Run snmp')

    args = parser.parse_args()

    if args.snmp:
        return
    elif args.api:
        return
    else:
        x = input('Vendor ?\n')
        if x == 'alcatel':
            from experimental.commandprocessors import main
            alcatel = create_alcatel_db()

            template_root = 'templates/Alcatel'
            cli = main.PreLoginCommandProcessor
            stdin = os.fdopen(sys.stdin.fileno(), 'rb', 0)
            stdout = os.fdopen(sys.stdout.fileno(), 'wb', 0)

            while True:
                command_processor = cli(
                    alcatel, stdin, stdout, (), template_root=template_root, daemon=False)

                try:
                    context = dict()
                    context['login_banner'] = alcatel.get_box().login_banner
                    command_processor.history_enabled = False
                    command_processor.loop(context=context)
                except exceptions.TerminalExitError as exc:
                    if exc.return_to is not None and exc.return_to == 'sysexit':
                        break
                    elif exc.return_to is not None and exc.return_to == 'sysreboot':
                        continue
                    elif exc.return_to is not None and exc.return_to != 'sysexit':
                        raise exc
                    else:
                        return


def create_alcatel_db():
    from experimental.db_interfaces.alcatel_interface import AlcatelInterface
    alcatel = AlcatelInterface(True)
    alcatel.create_box('alcatel', '7330', ['hi', 'ho'])
    return alcatel


if __name__ == '__main__':
    sys.exit(main())
