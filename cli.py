# This file is part of the NESi software.
#
# Copyright (c) 2020, inexio <https://github.com/inexio>
# - Janis Groß <https://github.com/unkn0wn-user>
# - Philip Konrath <https://github.com/Connyko65>
# - Alexander Dincher <https://github.com/Dinker1996>
# - Philipp-Noah Groß <https://github.com/pngross>
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
from nesi.devices.softbox.cli import rest_client
from nesi.devices.softbox.base_resources import root, base
from nesi.bootup.sockets.telnet import TelnetSocket
from nesi.bootup.sockets.ssh import SshSocket
import pytest

import subprocess
from nesi.devices.softbox.api.views import *  # noqa
import pydevd_pycharm
import time


LOG = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description='Network Equipment Simulator')

    parser.add_argument(
        '-v', '--version', action='version',
        version='%(prog)s ' + __version__)

    parser.add_argument(
        '--service-root', metavar='<URL>', type=str, default='http://127.0.0.1:5000/nesi/v1',
        help='URL of NESi REST API service root. '
             'Example: https://example.com/nesi/v1/root.json')

    parser.add_argument(
        '--list-boxen', action='store_true',
        help='Discover and print out existing box models')

    parser.add_argument(
        '--box-uuid', metavar='<UUID>', type=str,
        help='Run CLI instance using specified box instance as a '
             'backend model')

    parser.add_argument(
        '--daemon', action='store_true',
        help='Run CLI instance in network daemon mode')

    parser.add_argument(
        '--ip-address', metavar='<IPADDR>', type=str,
        help='IP-Address for socket mode')

    parser.add_argument(
        '--port', metavar='<PORT>', type=str,
        help='Port for socket mode')

    parser.add_argument(
        '--debug', action='store_true',
        help='Run CLI instance in debug mode')

    parser.add_argument(
        '--test', metavar='<VENDOR>', type=str,
        help='Run CLI instance with test cases')

    parser.add_argument(
        '--standalone', metavar='<VENDOR>', type=str,
        help='Run Cli without starting api')

    args = parser.parse_args()

    try:
        if args.debug:
            pydevd_pycharm.settrace('localhost', port=3001, stdoutToServer=True, stderrToServer=True)

        if args.standalone in ('Alcatel', 'Huawei', 'Edgecore', 'Keymile', 'Pbn', 'Zhone'):
            p = start_api_with_vendor(args.standalone)
        elif args.standalone is not None:
            parser.error('--standalone has invalid argument')
            return

        if args.test in ('Alcatel', 'Huawei', 'Edgecore', 'Keymile', 'Pbn', 'Zhone'):
            p = start_api_with_vendor(args.test)
            if args.test == 'Alcatel':
                pytest.main(['--pyargs', 'test_cases.unit_tests.alcatel', '-rA', '--disable-warnings'])
                return
            elif args.test == 'Huawei':
                pytest.main(['--pyargs', 'test_cases.unit_tests.huawei', '-rA', '--disable-warnings'])
                return
            elif args.test == 'Edgecore':
                pytest.main(['--pyargs', 'test_cases.unit_tests.edgecore', '-rA', '--disable-warnings'])
                return
            elif args.test == 'Keymile':
                pytest.main(['--pyargs', 'test_cases.unit_tests.keymile', '-rA', '--disable-warnings'])
                return
            elif args.test == 'Pbn':
                pytest.main(['--pyargs', 'test_cases.unit_tests.pbn', '-rA', '--disable-warnings'])
                return
            elif args.test == 'Zhone':
                pytest.main(['--pyargs', 'test_cases.unit_tests.zhone', '-rA', '--disable-warnings'])
                return
        elif args.test is not None:
            parser.error('--test has invalid argument')
            return

        service_root = urlparse(args.service_root)
        prefix = os.path.dirname(service_root.path)
        filename = os.path.basename(service_root.path)
        conn = rest_client.RestClient('%s://%s%s/' % (service_root.scheme, service_root.netloc, prefix))
        root_resource = root.Root(conn, path=filename)

        if args.list_boxen:
            for model in root_resource.boxen():
                print('Vendor %s, model %s, version %s, uuid %s' % (
                    model.vendor, model.model, model.version, model.uuid))
            return 0

        if not args.box_uuid:
            parser.error('--box-uuid is required')
            return

        for model in root_resource.boxen():
            if model.uuid == args.box_uuid:
                LOG.debug('Found requested box with UUID %s', model.uuid)
                break
        else:
            parser.error('Requested box with UUID %s not found' % args.box_uuid)
            return

        try:
            model = root_resource.get_box(base.get_member_identity(model.json), model.vendor)
            main = importlib.import_module('nesi.vendors.' + model.vendor + '.main')
            cli = main.PreLoginCommandProcessor
            os.chdir(os.path.dirname(os.path.realpath(__file__)))
            template_root = 'nesi/templates/' + str(model.vendor)

        except exceptions.ExtensionNotFoundError as exc:
            parser.error(exc)
            return

        if args.daemon:
            if model.network_address is not None:
                ip_address = model.network_address
            else:
                ip_address = args.ip_address

            if model.network_port is not None:
                port = model.network_port
            else:
                port = args.port

            if port is None or ip_address is None:
                parser.error('ip-address and port are required')
                return

            if model.network_protocol == 'telnet':
                telnet = TelnetSocket(cli, model, template_root, ip_address, int(port))
                telnet.start()
            elif model.network_protocol == 'ssh':
                cli = main.PostLoginCommandProcessor
                ssh = SshSocket(cli, model, template_root, ip_address, int(port))
                ssh.start()

        else:
            stdin = os.fdopen(sys.stdin.fileno(), 'rb', 0)
            stdout = os.fdopen(sys.stdout.fileno(), 'wb', 0)

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
    finally:
        if (args.standalone or args.test) and p is not None:
            p.terminate()
            p.kill()


def start_api_with_vendor(vendor):
    p = subprocess.Popen(['python3', 'api.py', '--recreate-db', '--load-model', vendor])
    time.sleep(10)
    return p


if __name__ == '__main__':
    sys.exit(main())
