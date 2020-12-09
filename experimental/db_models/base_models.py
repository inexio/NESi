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

    def get_port(self, field, value):
        if not hasattr(self, 'ports'):
            raise exceptions.SoftboxenError()
        for port in self.ports:
            if getattr(port, field) == value:
                # print(port)
                return port
        else:
            raise exceptions.SoftboxenError()

    def get_ont(self, field, value):
        if not hasattr(self, 'onts'):
            raise exceptions.SoftboxenError()
        for ont in self.onts:
            if getattr(ont, field) == value:
                # print(card)
                return ont
        else:
            raise exceptions.SoftboxenError()

    def get_ont_port(self, field, value):
        if not hasattr(self, 'ont_ports'):
            raise exceptions.SoftboxenError()
        for ont_port in self.ont_ports:
            if getattr(ont_port, field) == value:
                # print(card)
                return ont_port
        else:
            raise exceptions.SoftboxenError()

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

    def check_credentials(self, username, password):
        if not hasattr(self, 'credentials'):
            raise exceptions.SoftboxenError()
        for credential in self.credentials:
            if credential.username == username and credential.password == password:
                return True
        return False

    def collect_subcomponents(self):
        if hasattr(self, 'subracks') and hasattr(self, 'cards'):
            for subrack in self.subracks:
                for card in subrack.cards:
                    self.cards.append(card)
        if hasattr(self, 'cards') and hasattr(self, 'ports'):
            for card in self.cards:
                for port in card.ports:
                    self.ports.append(port)
