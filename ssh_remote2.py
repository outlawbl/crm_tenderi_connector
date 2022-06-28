import os
import time
from paramiko import SSHClient, AutoAddPolicy, Transport
from regex import E
from scp import SCPClient
from contextlib import closing
import pprint

host = "23.88.46.218"
port = 22
transport = Transport((host, port))
username = "root"
password="banjaluka2018"

while(True):
    print("Connecting...")

    ssh = SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    ssh.connect(host, port, username, password)

    scp = SCPClient(ssh.get_transport())

    sftp = ssh.open_sftp()

    print("Connected.")

    remoteFolder = '/home/copy_uploaded_crm_files/uploads_from_remote_server/'
    localFolder = '/var/www/crm/data/upload/'


    try:
        remoteFiles = sftp.listdir(path=remoteFolder)
        for file in remoteFiles:
            scp.get(remoteFolder+file, localFolder+file, recursive=True)
            sftp.remove(remoteFolder+file)

    except Exception as e:
        print('Greska:' ,e)
        pass

    scp.close()
    ssh.close()
    print("Closed connection.")
    time.sleep(300)