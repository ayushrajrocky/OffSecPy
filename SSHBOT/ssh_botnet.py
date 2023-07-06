import paramiko

class Client:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.session = self.connect()

    def connect(self):
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(
                hostname=self.host,
                port=2220,  # Set the desired port number
                username=self.user,
                password=self.password
            )
            return ssh_client
        except Exception as e:
            print(e)
            print('[-] Error Connecting')

    def send_command(self, cmd):
        stdin, stdout, stderr = self.session.exec_command(cmd)
        return stdout.read().decode()

def botnetCommand(command):
    for client in botNet:
        output = client.send_command(command)
        print('[*] Output from ' + client.host)
        print('[*] ' + output)

def addClient(host, user, password):
    client = Client(host, user, password)
    botNet.append(client)

botNet = []

# Example
# Add/connect a client to the botNet list
addClient('bandit.labs.overthewire.org', 'bandit0', 'bandit0')
# Send a command to all bots
botnetCommand('pwd')

