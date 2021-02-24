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
from .baseCommandProcessor import BaseCommandProcessor


class VlanSrvprofCommandProcessor(BaseCommandProcessor):

    def do_return(self, command, *args, context=None):

        from .enableCommandProcessor import EnableCommandProcessor

        context.pop('srvprof')
        exc = exceptions.TerminalExitError()
        exc.return_to = EnableCommandProcessor
        raise exc

    def do_quit(self, command, *args, context=None):
        context.pop('srvprof')
        raise exceptions.TerminalExitError()

    def on_unknown_command(self, command, *args, context=None):
        if self._validate(command, '?'):
            text = self._render(
                '?',
                context=context)
            self._write(text)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def get_profile(self, command, context):
        srvprofid = context['srvprof'].id
        try:
            profile = self._model.get_port_profile('id', int(srvprofid))
        except exceptions.SoftboxenError:
            raise exceptions.CommandSyntaxError(command=command)
        return profile

    def do_security(self, command, *args, context=None):
        if self._validate(args, 'anti-macspoofing', 'disable'):
            context['srvprof'].security_anti_macspoofing = 'disable'
            text = self._render('please_wait_commit', context=context)
            self._write(text)

        elif self._validate(args, 'anti-macspoofing', 'enable'):
            context['srvprof'].security_anti_macspoofing = 'enable'
            text = self._render('please_wait_commit', context=context)
            self._write(text)

        elif self._validate(args, 'anti-ipspoofing', 'disable'):
            context['srvprof'].security_anti_ipspoofing = 'disable'
            text = self._render('please_wait_commit', context=context)
            self._write(text)

        elif self._validate(args, 'anti-ipspoofing', 'enable'):
            context['srvprof'].security_anti_ipspoofing = 'enable'
            text = self._render('please_wait_commit', context=context)
            self._write(text)

        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_vmac(self, command, *args, context=None):
        if self._validate(args, 'disable'):
            context['srvprof'].vmac_ipoe = 'disable'
            context['srvprof'].vmac_pppoa = 'disable'
            context['srvprof'].vmac_pppoe = 'disable'
            text = self._render('please_wait_commit', context=context)
            self._write(text)

        elif self._validate(args, 'enable'):
            context['srvprof'].vmac_ipoe = 'enable'
            context['srvprof'].vmac_pppoa = 'enable'
            context['srvprof'].vmac_pppoe = 'enable'
            text = self._render('please_wait_commit', context=context)
            self._write(text)

        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_igmp(self, command, *args, context=None):
        if self._validate(args, 'mismatch', 'transparent'):
            context['srvprof'].igmp_mismatch = 'transparent'
            text = self._render('please_wait_commit', context=context)
            self._write(text)

        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_pitp(self, command, *args, context=None):
        if self._validate(args, 'enable'):
            self._model.set_pitp('enable')
            text = self._render('please_wait_commit', context=context)
            self._write(text)

        elif self._validate(args, 'disable'):
            self._model.set_pitp('disable')
            text = self._render('please_wait_commit', context=context)
            self._write(text)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_forwarding(self, command, *args, context=None):
        if self._validate(args, 'vlan-mac'):
            context['srvprof'].vlan_mac = 'forwarding'
            text = self._render('please_wait_commit', context=context)
            self._write(text)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_packet_policy(self, command, *args, context=None):
        if self._validate(args, 'multicast', 'forward'):
            context['srvprof'].packet_policy_multicast = 'forward'
            text = self._render(
                'please_wait_commit',
                context=context)
            self._write(text)

        elif self._validate(args, 'unicast', 'discard'):
            context['srvprof'].packet_policy_unicast = 'discard'
            text = self._render(
                'please_wait_commit',
                context=context)
            self._write(text)

        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_commit(self, command, *args, context=None):
        profile = self.get_profile(command, context)
        if len(args) == 0:
            virtprof = context['srvprof']
            profile.set('vlan_mac', virtprof.vlan_mac)
            profile.set('vmac_ipoe', virtprof.vmac_ipoe)
            profile.set('vmac_pppoa', virtprof.vmac_pppoa)
            profile.set('vmac_pppoe', virtprof.vmac_pppoe)
            profile.set('security_anti_macspoofing', virtprof.security_anti_macspoofing)
            profile.set('security_anti_ipspoofing', virtprof.security_anti_ipspoofing)
            profile.set('packet_policy_unicast', virtprof.packet_policy_unicast)
            profile.set('packet_policy_multicast', virtprof.packet_policy_multicast)
            profile.set('igmp_mismatch', virtprof.igmp_mismatch)
            profile.set('commit', True)
        else:
            raise exceptions.CommandSyntaxError(command=command)


