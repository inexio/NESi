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


from .baseCommandProcessor import BaseCommandProcessor
from nesi import exceptions


class VlanCommandProcessor(BaseCommandProcessor):

    def do_vlan(self, command, *args, context=None):
        # vlan $trafficVlan name $description media ethernet
        # vlan $cpe_management_vlan name $description media ethernet
        if self._validate(args, str, 'name', str, 'media', 'ethernet'):
            number, name = self._dissect(args, str, 'name', str, 'media', 'ethernet')
            try:
                vlan = self._model.get_vlan('number', int(number))
                vlan.set('name', name)
            except exceptions.SoftboxenError:
                _ = self._model.add_vlan(number=int(number), name=name)
                vlan = self._model.get_vlan('number', int(number))
        else:
            raise exceptions.CommandSyntaxError(command=command)
