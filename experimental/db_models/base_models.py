from nesi import exceptions


class BoxFunctionalities:

    def get_subrack(self, field, value):
        if not hasattr(self, 'subracks'):
            raise exceptions.SoftboxenError()
        for subrack in self.subracks:
            if getattr(subrack, field) == value:
                # print(card)
                return subrack
        else:
            raise exceptions.SoftboxenError()

    def get_card(self, field, value):
        if not hasattr(self, 'cards'):
            raise exceptions.SoftboxenError()
        for card in self.cards:
            if getattr(card, field) == value:
                # print(card)
                return card
        else:
            raise exceptions.SoftboxenError()

    def get_cards(self, field, value):
        if not hasattr(self, 'cards'):
            raise exceptions.SoftboxenError()
        component = []
        for card in self.cards:
            if getattr(card, field) == value:
                # print(card)
                component.append(card)
        else:
            return component

    def get_port(self, field, value):
        if not hasattr(self, 'ports'):
            raise exceptions.SoftboxenError()
        for port in self.ports:
            if getattr(port, field) == value:
                # print(port)
                return port
        else:
            raise exceptions.SoftboxenError()

    def get_ports(self, field, value):
        if not hasattr(self, 'ports'):
            raise exceptions.SoftboxenError()
        component = []
        for port in self.ports:
            if getattr(port, field) == value:
                # print(card)
                component.append(port)
        else:
            return component

    def get_ont(self, field, value):
        if not hasattr(self, 'onts'):
            raise exceptions.SoftboxenError()
        for ont in self.onts:
            if getattr(ont, field) == value:
                # print(card)
                return ont
        else:
            raise exceptions.SoftboxenError()

    def get_onts(self, field, value):
        if not hasattr(self, 'onts'):
            raise exceptions.SoftboxenError()
        component = []
        for ont in self.onts:
            if getattr(ont, field) == value:
                # print(card)
                component.append(ont)
        else:
            return component

    def get_ont_port(self, field, value):
        if not hasattr(self, 'ont_ports'):
            raise exceptions.SoftboxenError()
        for ont_port in self.ont_ports:
            if getattr(ont_port, field) == value:
                # print(card)
                return ont_port
        else:
            raise exceptions.SoftboxenError()

    def get_ont_ports(self, field, value):
        if not hasattr(self, 'ont_ports'):
            raise exceptions.SoftboxenError()
        component = []
        for ont_port in self.ont_ports:
            if getattr(ont_port, field) == value:
                # print(card)
                component.append(ont_port)
        else:
            return component

    def get_cpe(self, field, value):
        if not hasattr(self, 'cpes'):
            raise exceptions.SoftboxenError()
        for cpe in self.cpes:
            if getattr(cpe, field) == value:
                # print(card)
                return cpe
        else:
            raise exceptions.SoftboxenError()

    def get_cpe_port(self, field, value):
        if not hasattr(self, 'cpe_ports'):
            raise exceptions.SoftboxenError()
        for cpe_port in self.cpe_ports:
            if getattr(cpe_port, field) == value:
                # print(card)
                return cpe_port
        else:
            raise exceptions.SoftboxenError()

    def get_user(self, field, value):
        if not hasattr(self, 'users'):
            raise exceptions.SoftboxenError()
        for user in self.users:
            if getattr(user, field) == value:
                # print(card)
                return user
        else:
            raise exceptions.SoftboxenError()

    def get_users(self, field, value):
        if not hasattr(self, 'users'):
            raise exceptions.SoftboxenError()
        users = []
        for user in self.users:
            if getattr(user, field) == value:
                # print(card)
                users.append(user)
        else:
            return users

    def get_credentials(self, field, value):
        if not hasattr(self, 'credentials'):
            raise exceptions.SoftboxenError()
        for credential in self.credentials:
            if getattr(credential, field) == value:
                # print(card)
                return credential
        else:
            raise exceptions.SoftboxenError()

    def check_credentials(self, username, password):
        if not hasattr(self, 'credentials'):
            raise exceptions.SoftboxenError()
        for credential in self.credentials:
            if credential.username == username and credential.password == password:
                return True
        return False

    def get_service_port(self, field, value):
        if not hasattr(self, 'serviceports'):
            raise exceptions.SoftboxenError()
        for serviceport in self.serviceports:
            if getattr(serviceport, field) == value:
                # print(card)
                return serviceport
        else:
            raise exceptions.SoftboxenError()

    def get_service_port_by_values(self, params=None):
        if not hasattr(self, 'serviceports'):
            raise exceptions.SoftboxenError()
        for serviceport in self.serviceports:
            for (field, value) in params:
                if getattr(serviceport, field) == value:
                    # print(card)
                    return serviceport
        else:
            raise exceptions.SoftboxenError()

    def get_qos_interface(self, field, value):
        if not hasattr(self, 'qosinterfaces'):
            raise exceptions.SoftboxenError()
        for qosinterface in self.qosinterfaces:
            if getattr(qosinterface, field) == value:
                # print(card)
                return qosinterface
        else:
            raise exceptions.SoftboxenError()

    def get_port_profile(self, field, value):
        if not hasattr(self, 'port_profiles'):
            raise exceptions.SoftboxenError()
        for port_profile in self.port_profiles:
            if getattr(port_profile, field) == value:
                # print(card)
                return port_profile
        else:
            raise exceptions.SoftboxenError()

    def get_port_profiles(self, params=None):
        if not hasattr(self, 'port_profiles'):
            raise exceptions.SoftboxenError()
        component = []
        for port_profile in self.port_profiles:
            for (field, value) in params:
                if getattr(port_profile, field) == value:
                    # print(card)
                    component.append(port_profile)
        else:
            return component

    def get_service_vlan(self, field, value):
        if not hasattr(self, 'servicevlans'):
            raise exceptions.SoftboxenError()
        for servicevlan in self.servicevlans:
            if getattr(servicevlan, field) == value:
                # print(card)
                return servicevlan
        else:
            raise exceptions.SoftboxenError()

    def get_service_vlans(self, field, value):
        if not hasattr(self, 'servicevlans'):
            raise exceptions.SoftboxenError()
        component = []
        for servicevlan in self.servicevlans:
            if getattr(servicevlan, field) == value:
                # print(card)
                component.append(servicevlan)
        else:
            return component

    def get_service_vlans_by_service_port_id(self, service_port_id):
        """Get all service-vlans for a specific service-port"""
        return self.get_service_vlans('service_port_id', service_port_id)

    def get_service_vlan_by_values(self, params=None):
        if not hasattr(self, 'servicevlans'):
            raise exceptions.SoftboxenError()
        component = []
        for servicevlan in self.servicevlans:
            for (field, value) in params:
                if getattr(servicevlan, field) == value:
                    # print(card)
                    component.append(servicevlan)
        else:
            return component

    def get_vlan(self, field, value):
        if not hasattr(self, 'vlans'):
            raise exceptions.SoftboxenError()
        for vlan in self.vlans:
            if getattr(vlan, field) == value:
                # print(card)
                return vlan
        else:
            raise exceptions.SoftboxenError()

    def collect_subcomponents(self):
        if hasattr(self, 'subracks') and hasattr(self, 'cards'):
            self.cards = []
            for subrack in self.subracks:
                for card in subrack.cards:
                    self.cards.append(card)
        if hasattr(self, 'cards') and hasattr(self, 'ports'):
            self.ports = []
            for card in self.cards:
                for port in card.ports:
                    self.ports.append(port)
        if hasattr(self, 'subracks') and hasattr(self, 'mgmt_cards'):
            self.mgmt_cards = []
            for subrack in self.subracks:
                for mcart in subrack.mgmt_cards:
                    self.mgmt_cards.append(mcart)
        if hasattr(self, 'mgmt_cards') and hasattr(self, 'mgmt_ports'):
            self.mgmt_ports = []
            for card in self.mgmt_cards:
                for port in card.mgmt_ports:
                    self.mgmt_ports.append(port)
        if hasattr(self, 'credentials') and hasattr(self, 'users'):
            self.users = []
            for credential in self.credentials:
                for usr in credential.user:
                    self.users.append(usr)
