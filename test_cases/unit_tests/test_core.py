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

import os, sys
from nesi import exceptions
from os import listdir
from os.path import isfile, join
from urllib.parse import urlparse
import importlib
from nesi.softbox import rest_client
from nesi.softbox import root, base
import pytest


class TestCore:

    def prep_cli(self):
        self.prep_model()
        main = importlib.import_module('vendors.' + self.model.vendor + '.' + self.model.model + '.' + self.model.vendor + '_' + self.model.model + '.main')
        cli = main.PreLoginCommandProcessor
        self.cli = cli
        return cli

    def prep_model(self):
        service_root = 'http://127.0.0.1:5000/nesi/v1'
        insecure = False
        service_root = urlparse(service_root)
        prefix = os.path.dirname(service_root.path)
        filename = os.path.basename(service_root.path)

        conn = rest_client.RestClient(
            '%s://%s%s/' % (service_root.scheme, service_root.netloc, prefix),
            verify=not insecure,
        )

        root_resource = root.Root(conn, path=filename)

        for model in root_resource.boxen():
            break

        try:
            model = root_resource.get_box(base.get_member_identity(model.json), model.vendor)
        except exceptions.ExtensionNotFoundError as exc:
            return

        self.model = model
        return model

    @pytest.fixture(autouse=True)
    def setUp(self):
        self.prep_cli()
        yield

    def run(self, inpath, outpath):
        flags = os.O_WRONLY | os.O_CREAT
        fd = os.open(outpath, flags=flags)
        stdout1 = os.fdopen(fd, 'wb', 0)
        fd1 = os.open(inpath, os.O_RDONLY)
        stdin1 = os.fdopen(fd1, 'rb', 0)

        while True:
            command_processor = self.cli(self.model, stdin1, stdout1, (), template_root='templates/', daemon=True)
            try:
                context = dict()
                context['login_banner'] = self.model.login_banner
                command_processor.history_enabled = False
                command_processor.loop(context=context)
            except exceptions.TerminalExitError as exc:
                if exc.return_to is not None and exc.return_to == 'sysexit':
                    break
                elif exc.return_to is not None and exc.return_to == 'sysreboot':
                    continue
                else:
                    pass

        stdin1.close()
        stdout1.close()
        del stdin1
        del stdout1


    def get_path(self):
        print(self.model.vendor)
        if self.model.vendor == 'Alcatel':
            path = 'test_cases/unit_tests/alcatel/'
        elif self.model.vendor == 'Huawei':
            path = 'test_cases/unit_tests/huawei/'
        else:
            path = 'broke'
        return path

