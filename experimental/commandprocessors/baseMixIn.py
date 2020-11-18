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

    def do_show(self, command, *args, context=None):

        from .userViewCommandProcessor import UserViewCommandProcessor
        from .showCommandProcessor import ShowCommandProcessor

        if args.__contains__('?'):
            text = self._render('?', context=context)
            self._write(text)
        self.process(ShowCommandProcessor, 'login', 'mainloop', 'show', args=args, return_to=UserViewCommandProcessor,
                     context=context)

    def do_environment(self, command, *args, context=None):

        from .userViewCommandProcessor import UserViewCommandProcessor
        from .environmentCommandProcessor import EnvironmentCommandProcessor

        if args.__contains__('?'):
            text = self._render('?', context=context)
            self._write(text)
        self.process(EnvironmentCommandProcessor, 'login', 'mainloop', 'environment', args=args,
                     return_to=UserViewCommandProcessor, context=context)

    def do_admin(self, command, *args, context=None):

        from .userViewCommandProcessor import UserViewCommandProcessor
        from .adminCommandProcessor import AdminCommandProcessor

        if args.__contains__('?'):
            text = self._render('?', context=context)
            self._write(text)
        self.process(AdminCommandProcessor, 'login', 'mainloop', 'admin', args=args, return_to=UserViewCommandProcessor,
                     context=context)

    def do_info(self, command, *args, context=None):

        from .userViewCommandProcessor import UserViewCommandProcessor

        if command is None:
            self.process(UserViewCommandProcessor, 'login', 'mainloop', args=(), return_to=None, context=context)
        else:
            self.process(UserViewCommandProcessor, 'login', 'mainloop', args=(command,) + args, return_to=None,
                         context=context)

    def do_configure(self, command, *args, context=None):

        from .userViewCommandProcessor import UserViewCommandProcessor
        from .configureCommandProcessor import ConfigureCommandProcessor

        if args.__contains__('?'):
            text = self._render('?', context=context)
            self._write(text)
        self.process(ConfigureCommandProcessor, 'login', 'mainloop', 'configure',
                     args=args,
                     return_to=UserViewCommandProcessor, context=context)
