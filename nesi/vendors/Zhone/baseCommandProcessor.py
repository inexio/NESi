# Software adapted by inexio <https://github.com/inexio>.
# - Janis Groß <https://github.com/unkn0wn-user>
# - Philip Konrath <https://github.com/Connyko65>
# - Alexander Dincher <https://github.com/Dinker1996>
# - Philipp-Noah Groß <https://github.com/pngross>
#
# License: https://github.com/inexio/NESi/LICENSE.rst

from nesi import exceptions
from nesi.devices.softbox.cli import base
import re

class BaseCommandProcessor(base.CommandProcessor):
    def do_exit(self, command, *args, context=None):
        exc = exceptions.TerminalExitError()
        exc.return_to = 'sysexit'
        raise exc

    def map_states(self, object, type):
        if object.admin_state == '0':
            if type == 'port':
                object.admin_state = 'DOWN'
        elif object.admin_state == '1':
            if type == 'port':
                object.admin_state = 'UP'
        elif object.admin_state == '2':
            if type == 'port':
                object.admin_state = 'ERR'

        if object.operational_state == '0':
            if type == 'port':
                object.operational_state = 'DOWN'
        elif object.operational_state == '1':
            if type == 'port':
                object.operational_state = 'DATA'
        elif object.operational_state == '2':
            if type == 'port':
                object.operational_state = 'HANDSHAKE'

    def create_spacers(self, positions, args):
        spacers = []
        previous_pos = 0
        i = 0
        for position in positions:
            spacer = position - (previous_pos + len(str(args[i])))
            spacers.append(spacer)
            previous_pos = position
            i += 1

        return spacers