# Software adapted by inexio <https://github.com/inexio>.
# - Janis Groß <https://github.com/unkn0wn-user>
# - Philip Konrath <https://github.com/Connyko65>
# - Alexander Dincher <https://github.com/Dinker1996>
# - Philipp-Noah Groß <https://github.com/pngross>
#
# License: https://github.com/inexio/NESi/LICENSE.rst

from nesi import exceptions
from nesi.vendors.Zhone.baseCommandProcessor import BaseCommandProcessor

class RootCommandProcessor(BaseCommandProcessor):

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)

    def get_property(self, command, *args, context=None):
        raise exceptions.CommandExecutionError(command=command, template='invalid_property',
                                               template_scopes=('login', 'base', 'execution_errors'))

    def do_dslstat(self, command, *args, context=None):
        if self._validate(args, *()):
            self._write(self._render('dslstatEmptyArg', 'login', 'base', context=context))
        elif self._validate(args, str):
            identifier, = self._dissect(args, str)
            identifier_components = identifier.split('/')
            if len(identifier_components) != 5 or identifier_components[3] != '0' or identifier_components[4] != 'vdsl':
                context['identifier'] = identifier
                self._write(self._render('dslstatInvalidArg', 'login', 'base', context=context))
                return
            port = self._model.get_port('name', "/".join(identifier_components[:3]))

            self.map_states(port, 'port')

            context['port'] = port

            if self.daemon and self._model.network_protocol == 'ssh':
                output = self._render('dslstatTemplate', 'login', 'base', context=context).split("\n")
                pointer = 0
                buff_size = 19
                prompt_end = self.prompt_end_pos
                while True:
                    self.cursor_pos = 0
                    self._write("\n".join(output[pointer:pointer + buff_size]))
                    self._write("\n")
                    pointer += buff_size

                    if pointer >= len(output):
                        break

                    option_string = '<SPACE> for next page, <CR> for next line, A for all, Q to quit'
                    self.cursor_pos = len(option_string) + 1
                    self.prompt_end_pos = 0
                    self.updateline(option_string)

                    character = None

                    while character not in ('\r', 'a', 'q', ' '):
                        _, character = self.get()

                    self.cursor_pos = 0
                    self.updateline('')

                    if character == '\r':
                        buff_size = 1
                        continue
                    elif character == 'a':
                        buff_size = len(output) - pointer
                        continue
                    elif character == 'q':
                        break
                    elif character == ' ':
                        buff_size = 19
                        continue
                self.cursor_pos = 0
                self.prompt_end_pos = prompt_end
            else:
                output = self._render('dslstatTemplate', 'login', 'base', context=context) + "\n"
                self._write(output)
        else:
            self._write(self._render('dslstatInvalidArg', 'login', 'base', context=context))