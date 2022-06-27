import os
from paramiko import SSHClient, AutoAddPolicy, Transport
# import paramiko
from regex import E
from scp import SCPClient
from contextlib import closing
import pprint

host = "23.88.46.218"
port = 22
transport = Transport((host, port))
username = "root"
password="banjaluka2018"

print("Connecting...")

ssh = SSHClient()
ssh.set_missing_host_key_policy(AutoAddPolicy())
ssh.connect(host, port, username, password)

scp = SCPClient(ssh.get_transport())

print("Connected.")



try:
    scp.get('/home/sandro/test.txt', '/home/sandro/Dev/crm_tenderi_connector/uploads_from_remote_server')
except Exception as e:
    print('Greska:' ,e)
    pass

scp.close()
ssh.close()
print("Closed connection.")