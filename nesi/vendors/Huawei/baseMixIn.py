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

from nesi import exceptions


class BaseMixIn:

    def process(self, commandprocessor, *envvars, args, return_to, context=None):
        subprocessor = self._create_subprocessor(commandprocessor, *envvars)

        command = None
        if args != ():
            command = ''
            for arg in args:
                command = command + arg
                command = command + ' '

        subprocessor.loop(context=context, return_to=return_to, command=command)

    def do_config(self, command, *args, context=None):

        from .enableCommandProcessor import EnableCommandProcessor
        from .configCommandProcessor import ConfigCommandProcessor


        try:
            admin = self._model.get_user('status', 'online')
            assert admin.level != 'User'
        except (exceptions.SoftboxenError, AssertionError):
            raise exceptions.CommandSyntaxError(command=command)

        if args.__contains__('?'):
            text = self._render('?', context=context)
            self._write(text)
        self.process(ConfigCommandProcessor, 'login', 'mainloop', 'enable', 'config', args=args,
                     return_to=EnableCommandProcessor, context=context)

    def do_diagnose(self, command, *args, context=None):

        from .enableCommandProcessor import EnableCommandProcessor
        from .diagnoseCommandProcessor import DiagnoseCommandProcessor

        if args.__contains__('?'):
            text = self._render('?', context=context)
            self._write(text)
        self.process(DiagnoseCommandProcessor, 'login', 'mainloop', 'enable', 'diagnose', args=args,
                     return_to=EnableCommandProcessor, context=context)