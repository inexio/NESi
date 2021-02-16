# This file is part of the NESi software.
#
# Copyright (c) 2020
# Original Software Design by Ilya Etingof <https://github.com/etingof>.
#
# Software adapted by inexio <https://github.com/inexio>.
# - Janis Groß <https://github.com/unkn0wn-user>
# - Philip Konrath <https://github.com/Connyko65>
# - Alexander Dincher <https://github.com/Dinker1996>
#
# License: https://github.com/inexio/NESi/LICENSE.rst

import argparse
import os
import sys

from nesi.devices.softbox.api import app
from nesi.devices.softbox.api import db
from nesi.devices.softbox.api.views import *  # noqa
from nesi.devices.softbox.api import config
import pydevd_pycharm
import threading

DESCRIPTION = """\
Network Equipment Simulator REST API.

Maintains network devices models in a persistent DB. Models
can be created, removed or changed by REST API.

Can be run as a WSGI application.
"""


def parse_args():
    parser = argparse.ArgumentParser(description=DESCRIPTION)

    parser.add_argument(
        '--recreate-db',
        action='store_true',
        help='DANGER! Running with this flag wipes up REST API server DB! '
             'This switch makes sense only when running this tool for the '
             'first time.')

    parser.add_argument(
        '--config', type=str,
        help='Config file path. Can also be set via environment variable '
             'NESI_CONFIG.')

    parser.add_argument(
        '--interface', type=str,
        help='IP address of the local interface for REST API'
             'server to listen on. Can also be set via config variable '
             'NESI_LISTEN_IP. Default is all local interfaces.')

    parser.add_argument(
        '--port', type=int,
        help='TCP port to bind REST API server to.  Can also be '
             'set via config variable NESI_LISTEN_PORT. '
             'Default is 5000.')

    parser.add_argument(
        '--debug', action='store_true',
        help='Run CLI instance in debug mode')

    parser.add_argument(
        '--load-model', metavar='<VENDOR>', type=str,
        help='Config file path. Can also be set via environment variable '
             'NESI_CONFIG.')

    return parser.parse_args()


def main():

    args = parse_args()

    if args.debug:
        pydevd_pycharm.settrace('localhost', port=3001, stdoutToServer=True, stderrToServer=True)

    if args.config:
        os.environ['NESI_CONFIG'] = args.config
        config_file = os.environ.get('NESI_CONFIG')
    else:
        config_file = config.DefaultConfig()

    if config_file:
        app.config.from_object(config_file)

    if args.interface:
        app.config['NESI_LISTEN_IP'] = args.interface

    if args.port:
        app.config['NESI_LISTEN_PORT'] = args.port

    if args.recreate_db:
        db.drop_all()
        db.create_all()

    if args.load_model in ('Alcatel', 'Huawei', 'Edgecore', 'Keymile', 'Pbn', 'Zhone'):
        if args.load_model == 'Alcatel':
            from nesi.bootup.conf.bootstraps.create_alcatel_7360 import create_alcatel
            p = threading.Thread(target=create_alcatel, daemon=True)
            p.start()
        elif args.load_model == 'Huawei':
            from nesi.bootup.conf.bootstraps.create_huawei_5623 import create_huawei
            p = threading.Thread(target=create_huawei, daemon=True)
            p.start()
        elif args.load_model == 'Edgecore':
            from nesi.bootup.conf.bootstraps.create_edgecore_xxxx import create_edgecore
            p = threading.Thread(target=create_edgecore, daemon=True)
            p.start()
        elif args.load_model == 'Keymile':
            from nesi.bootup.conf.bootstraps.create_keymile_MG2500 import create_keymile
            p = threading.Thread(target=create_keymile, daemon=True)
            p.start()
        elif args.load_model == 'Pbn':
            from nesi.bootup.conf.bootstraps.create_pbn_AOCM3924 import create_pbn
            p = threading.Thread(target=create_pbn, daemon=True)
            p.start()
        elif args.load_model == 'Zhone':
            from nesi.bootup.conf.bootstraps.create_zhone import create_zhone
            p = threading.Thread(target=create_zhone, daemon=True)
            p.start()
    elif args.load_model is not None:
        args.error('--load-model has invalid argument')
        return

    app.run(host=app.config.get('NESI_LISTEN_IP'), port=app.config.get('NESI_LISTEN_PORT'))



if __name__ == '__main__':
    sys.exit(main())
