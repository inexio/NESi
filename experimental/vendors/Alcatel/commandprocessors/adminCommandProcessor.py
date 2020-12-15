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

import os
import threading
from time import sleep
from nesi import exceptions
from .baseCommandProcessor import BaseCommandProcessor
from .baseMixIn import BaseMixIn
from experimental.interfaces.db_interfaces.alcatel_interface import AlcatelInterface


class AdminCommandProcessor(BaseCommandProcessor, BaseMixIn):

    def on_unknown_command(self, command, *args, context=None):
        if self._validate(command, '?'):
            text = self._render('?', context=context)
            self._write(text)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_software_mngt(self, command, *args, context=None):
        if self._validate(args, 'shub', 'database', 'save'):
            return

        elif self._validate(args, 'database', 'upload', str):
            target_file, = self._dissect(args, 'database', 'upload', str)

            if target_file.startswith('actual-active:') and target_file.endswith('.tar'):
                interface = AlcatelInterface(box_id=self._model.id)
                box = interface.get_box()
                box.upload_progress = 'upload-ongoing'
                interface.store(box)
                interface.close_session()

                subprocess = threading.Thread(target=self.simulate_upload, args=(self._model.id,))
                subprocess.start()

            else:
                raise exceptions.CommandSyntaxError(command=command)

        elif self._validate(args, 'oswp', '2', 'download', str):
            path, = self._dissect(args, 'oswp', '2', 'download', str)
            if path.count('/') > 0:
                path_pieces = path.split('/')
                try:
                    assert path_pieces[0] == 'firmware'
                    assert path_pieces[1] == 'isam'
                    sleep(5)
                    pass
                except (exceptions.SoftboxenError, AssertionError):
                    raise exceptions.CommandSyntaxError(command=command)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def simulate_upload(self, id):
        sleep(30)
        interface = AlcatelInterface(box_id=id)
        box = interface.get_box()
        box.upload_progress = 'upload-success'
        interface.store(box)
        interface.close_session()
        return
