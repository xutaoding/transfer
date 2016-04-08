"""
This module is suitable for the transfer files between Linux machine,
mainly use the SCP command to operate, But this operation method is a bit awkward
"""
import pexpect as transfer


class Base(object):
    @property
    def host(self):
        return '192.168.250.207'

    @property
    def pwd(self):
        return 'chinascope'


class GoosyTransfer(Base):
    def __init__(self, host=None, password=None):
        super(GoosyTransfer, self).__init__()
        self._host = host or self.host
        self._password = password or self.pwd

    def ssh_command(self, cmd):
        ssh = transfer.spawn('ssh root@%s "%s"' % (self._host, cmd), echo=False)

        try:
            i = ssh.expect(['password:', 'continue connecting(yes/no)?'], timeout=5)
            if i == 0:
                ssh.sendline(self._password)
            elif i == 1:
                ssh.sendline('yes')
                ssh.expect('password:')
                ssh.sendline(self._password)
            ssh.sendline(cmd)
            r = ssh.read()
            ret = 0
        except transfer.EOF:
            ret = -1
        except transfer.TIMEOUT:
            ret = -2
        finally:
            ssh.close()
        return ret

    def put(self, local, remote):
        """
        Make local file push remote path
        :param local: local machine absolutely file path
        :param remote: remote machine absolutely directory path
        """
        self.ssh_command('mkdir -p %s' % remote)
        child = transfer.spawn('scp -q %s root@%s:%s' % (local, self._host,  remote), echo=False)

        try:
            while True:
                index = child.expect(["root@%s's password:" % self._host, transfer.TIMEOUT], timeout=None)

                if index == 0:
                    child.sendline('%s' % self._password)
                    break
                elif index == 1:
                    pass
        except (transfer.EOF, transfer.TIMEOUT):
            pass
        finally:
            child.interact()
            child.close()
