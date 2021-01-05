# Software adapted by inexio <https://github.com/inexio>.
# - Janis Groß <https://github.com/unkn0wn-user>
# - Philip Konrath <https://github.com/Connyko65>
# - Alexander Dincher <https://github.com/Dinker1996>
# - Philipp-Noah Groß <https://github.com/pngross>
#
# License: https://github.com/inexio/NESi/LICENSE.rst

from nesi import exceptions
from vendors.Zhone.baseCommandProcessor import BaseCommandProcessor

class RootCommandProcessor(BaseCommandProcessor):

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)

    def get_property(self, command, *args, context=None):
        raise exceptions.CommandExecutionError(command=command, template='invalid_property',
                                               template_scopes=('login', 'base', 'execution_errors'))

    def do_dslstat(self, command, *args, context=None):

        if self._validate(args, *()):
            self._write(self._render('dslstatEmptyArg', 'login', 'base', context=context))
        elif self._validate(args, "1/1/1/0/vdsl"):

            port = self._model.get_port('name', '1/1/1/0')

            context['port'] = port

            self._write(self._render('dslstatTemplate', 'login', 'base', context=context))
        else:
            self._write(self._render('dslstatInvalidArg', 'login', 'base', context=context))