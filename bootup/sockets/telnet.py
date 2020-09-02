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
import socket
import threading
from nesi import exceptions


class TelnetSocket:
    def __init__(self, cli, model, template_root, hostaddress, port):
        self.hostaddress = hostaddress
        self.port = port
        self.cli = cli
        self.model = model
        self.template_root = template_root
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((hostaddress, port))
        self.s.listen(4)

        self.clients = []
        self.lock = threading.Lock()

    class Socket(threading.Thread):
        def __init__(self, socket, address, telnet):

            threading.Thread.__init__(self)
            self.socket = socket
            self.address = address
            self.telnet = telnet

        def run(self):
            self.telnet.lock.acquire()
            self.telnet.clients.append(self)
            self.telnet.lock.release()
            print('%s:%s connected.' % self.address)

            command_processor = self.telnet.cli(
                self.telnet.model, self, self, (),
                template_root=self.telnet.template_root, daemon=True)

            try:
                context = dict()
                context['login_banner'] = self.telnet.model.login_banner
                command_processor.loop(context=context)

            except exceptions.TerminalExitError:
                self.socket.close()
                print('%s:%s disconnected.' % self.address)
                self.telnet.lock.acquire()
                self.telnet.clients.remove(self)
                self.telnet.lock.release()

        def readline(self):
            return self.socket.recv(1024)

        def write(self, data):
            return self.socket.sendall(data)

    def start(self):
        print("Starting telnet socket on " + self.hostaddress + ":" + str(self.port))
        while True:
            sock, address = self.s.accept()
            self.Socket(sock, address, self).start()
