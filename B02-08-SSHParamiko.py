'''
For public key authentication:
Generate the keys:
				ssh-keygen -t rsa
Copy the keys to the server:
				ssh-copy-id user@host
'''

import paramiko

paramiko.util.log_to_file('paramiko.log')
client = paramiko.SSHClient()
rsa_key = paramiko.RSAKey.from_private_key_file('/home/adastra/.ssh/id_rsa', password='password')
#client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#client.connect('127.0.0.1', username='adastra', password='password')
#client.connect('127.0.0.1', key_filename='/home/hacker/.ssh/id_rsa', username='adastra', password='password')
client.connect('127.0.0.1', pkey=rsa_key, username='adastra', password='password')
stdin, stdout, stderr = client.exec_command('uname -a;id')
for line in stdout.readlines():
	print line
client.close()