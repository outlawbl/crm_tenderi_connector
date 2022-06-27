import paramiko
class remote_operations:
    def __init__(self):
          pass

    def connect(self, hostname, username, password):
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.connect(hostname, username=username, password=password)
        return client

    def open_remote_file(self, ssh_client, filename):
        sftp_client = ssh_client.open_sftp()
        file = sftp_client.open(filename)
        return file

    def download_remote_file(self, ssh_client, remotepath, localpath):
        sftp_client = ssh_client.open_sftp()
        sftp_client.get(remotepath, localpath)

    def list_dirs(self, ssh_client, remotepath):
        sftp_client = ssh_client.open_sftp()
        sftp_client.list_dir(remotepath)

# connect('23.88.46.218', 'root', 'banjaluka2018')

test = remote_operations()
client = test.connect('23.88.46.218', 'root', 'banjaluka2018')
# file = test.open_remote_file(client, "/home/sandro/test.txt")
# test.download_remote_file(client, "/home/sandro/test.txt", '/home/downloads')
test.list_dirs(client, '/home/sandro/')

# for line in file:
#      print(line)
# file.close()
# client.close()