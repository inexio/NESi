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
import threading
import time

from nesi import exceptions

from nesi.softbox.api.views import *  # noqa
import pydevd_pycharm

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

    parser.add_argument(
        '--debug', action='store_true',
        help='Run CLI instance in debug mode')

    parser.add_argument(
        '--recreate-db', action='store_true',
        help='Run CLI instance in debug mode')

    args = parser.parse_args()

    if args.debug:
        pydevd_pycharm.settrace('localhost', port=3001, stdoutToServer=True, stderrToServer=True)

    if not args.snmp and not args.api:
        args.cli = True

    if args.snmp:
        return
    elif args.api:
        create_alcatel_db(recreate_db=args.recreate_db)
        subprocess = threading.Thread(target=start_api, daemon=True)
        subprocess.start()
        if not args.cli:
            x = input('')
    if args.cli:
        time.sleep(0.5)
        x = input('Vendor ?\n')
        x = x.lower()
        stdin = os.fdopen(sys.stdin.fileno(), 'rb', 0)
        stdout = os.fdopen(sys.stdout.fileno(), 'wb', 0)
        if x == 'alcatel':
            from experimental.vendors.Alcatel.commandprocessors import main
            alcatel = create_alcatel_db(recreate_db=args.recreate_db)
            cli = main.PreLoginCommandProcessor
            command_proc_loop(cli, alcatel.get_box(), stdin, stdout, template_root='templates/Alcatel')

        elif x == 'huawei':
            from experimental.vendors.Alcatel.commandprocessors import main
            alcatel = create_alcatel_db(recreate_db=args.recreate_db)
            cli = main.PreLoginCommandProcessor
            command_proc_loop(cli, alcatel.get_box(), stdin, stdout, template_root='templates/Alcatel')
        else:
            print('Cant find Vendor', x)

    if args.api:
        print('Stopping API service.')


def create_alcatel_db(recreate_db):
    from experimental.interfaces.db_interfaces.alcatel_interface import AlcatelInterface
    alcatel = AlcatelInterface(dropall=recreate_db)
    if recreate_db:
        alcatel.create_box('alcatel', '7330')
    return alcatel


def create_huawei_db(recreate_db):
    from experimental.interfaces.db_interfaces.huawei_interface import HuaweiInterface
    huawei = HuaweiInterface(dropall=recreate_db)
    if recreate_db:
        huawei.create_box('alcatel', '7330')
    return huawei


def command_proc_loop(cli, model, stdin, stdout, template_root):
    while True:
        command_processor = cli(
            model, stdin, stdout, (), template_root=template_root, daemon=False)

        try:
            context = dict()
            context['login_banner'] = model.login_banner
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


def start_api():
    from experimental.interfaces.api_interface.views.config_views import app
    app.run(host=app.config.get('NESI_LISTEN_IP'), port=app.config.get('NESI_LISTEN_PORT'))
    return


if __name__ == '__main__':
    sys.exit(main())
