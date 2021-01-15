from twisted.cred.portal import Portal
from twisted.cred import portal
from twisted.conch.ssh import factory, userauth, connection, keys, session
from twisted.conch.ssh.transport import SSHServerTransport
from twisted.conch import avatar
from twisted.cred.checkers import InMemoryUsernamePasswordDatabaseDontUse
from twisted.internet import reactor, protocol
from twisted.python import components
from zope.interface import implementer
import threading
import os
from pathlib import Path

full_path = os.path.dirname(os.path.abspath(__file__))
path = str(Path(full_path).parents[0])

SERVER_RSA_PUBLIC = path + '/conf/ssh/id_rsa.pub'
SERVER_RSA_PRIVATE = path + '/conf/ssh/id_rsa'

PRIMES = {
    2048: [(2, 24265446577633846575813468889658944748236936003103970778683933705240497295505367703330163384138799145013634794444597785054574812547990300691956176233759905976222978197624337271745471021764463536913188381724789737057413943758936963945487690939921001501857793275011598975080236860899147312097967655185795176036941141834185923290769258512343298744828216530595090471970401506268976911907264143910697166165795972459622410274890288999065530463691697692913935201628660686422182978481412651196163930383232742547281180277809475129220288755541335335798837173315854931040199943445285443708240639743407396610839820418936574217939)],
    4096: [(2, 889633836007296066695655481732069270550615298858522362356462966213994239650370532015908457586090329628589149803446849742862797136176274424808060302038380613106889959709419621954145635974564549892775660764058259799708313210328185716628794220535928019146593583870799700485371067763221569331286080322409646297706526831155237865417316423347898948704639476720848300063714856669054591377356454148165856508207919637875509861384449885655015865507939009502778968273879766962650318328175030623861285062331536562421699321671967257712201155508206384317725827233614202768771922547552398179887571989441353862786163421248709273143039795776049771538894478454203924099450796009937772259125621285287516787494652132525370682385152735699722849980820612370907638783461523042813880757771177423192559299945620284730833939896871200164312605489165789501830061187517738930123242873304901483476323853308396428713114053429620808491032573674192385488925866607192870249619437027459456991431298313382204980988971292641217854130156830941801474940667736066881036980286520892090232096545650051755799297658390763820738295370567143697617670291263734710392873823956589171067167839738896249891955689437111486748587887718882564384870583135509339695096218451174112035938859)],
}


class Avatar(avatar.ConchUser):
    def __init__(self, username, cli, model, template_root):
        avatar.ConchUser.__init__(self)
        self.username = username
        self.cli = cli
        self.model = model
        self.template_root = template_root
        self.channelLookup.update({b'session': session.SSHSession})


@implementer(portal.IRealm)
class Realm(object):
    def __init__(self, cli, model, template_root):
        self.cli = cli
        self.model = model
        self.template_root = template_root

    def requestAvatar(self, avatarId, mind, *interfaces):
        return interfaces[0], Avatar(avatarId, self.cli, self.model, self.template_root), lambda: None


class SSHProtocol(protocol.Protocol):
    char = b''

    def connectionMade(self):
        connection = self.transport.getPeer().address
        print('%s:%s connected.' % (connection.host, connection.port))

    def connectionLost(self, reason=None):
        connection = self.transport.getPeer().address
        print('%s:%s disconnected.' % (connection.host, connection.port))

    def receiveData(self):
        while self.char == b'':
            pass

        return_val = self.char
        self.char = b''
        return return_val

    def dataReceived(self, data):
        self.char = data


class ExampleSession(object):
    def __init__(self, avatar):
        self.avatar = avatar

    def getPty(self, term, windowSize, attrs):
        pass

    def execCommand(self, proto, cmd):
        raise Exception("not executing commands")

    def openShell(self, transport):
        protocol = SSHProtocol()
        protocol.makeConnection(transport)
        transport.makeConnection(session.wrapProtocol(protocol))

        command_processor = self.avatar.cli(
                    self.avatar.model, protocol, transport, (), template_root=self.avatar.template_root, daemon=True)
        command_processor.skipLogin = True
        thread = threading.Thread(target=command_processor.loop, args=())
        thread.start()

    def eofReceived(self):
        pass

    def closed(self):
        pass


class Factory(factory.SSHFactory):
    protocol = SSHServerTransport
    publicKeys = {
        b'ssh-rsa': keys.Key.fromFile(SERVER_RSA_PUBLIC)
    }
    privateKeys = {
        b'ssh-rsa': keys.Key.fromFile(SERVER_RSA_PRIVATE)
    }
    services = {
        b'ssh-userauth': userauth.SSHUserAuthServer,
        b'ssh-connection': connection.SSHConnection
    }

    def getPrimes(self):
        return PRIMES


class SshSocket:
    def __init__(self, cli, model, template_root, hostaddress, port):
        self.hostaddress = hostaddress
        self.port = port
        self.cli = cli
        self.model = model
        self.template_root = template_root

    def start(self):
        components.registerAdapter(ExampleSession, Avatar, session.ISession)

        portal = Portal(Realm(self.cli, self.model, self.template_root))
        passwdDB = InMemoryUsernamePasswordDatabaseDontUse()

        for credential in self.model.credentials:
            passwdDB.addUser(credential.username.encode('utf-8'), credential.password.encode('utf-8'))

        portal.registerChecker(passwdDB)
        Factory.portal = portal

        print("Starting ssh socket on " + self.hostaddress + ":" + str(self.port))
        reactor.listenTCP(self.port, Factory())
        reactor.run()
