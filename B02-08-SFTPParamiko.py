import paramiko
from paramiko import RSAKey

client = paramiko.SSHClient()
try:
	paramiko.util.log_to_file('paramiko.log')
	rsa_key = paramiko.RSAKey.from_private_key_file('/home/adastra/.ssh/id_rsa',password='password')
	#client.load_system_host_keys()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	#client.connect('127.0.0.1', username='adastra', password='password')
	#client.connect('127.0.0.1',key_filename='/home/adastra/.ssh/id_rsa',username='adastra',password='password')
	client.connect('127.0.0.1',pkey=rsa_key,username='adastra',password='password')
	sftp = client.open_sftp()
	dirlist = sftp.listdir('.')
	for directory in dirlist:
		print directory
	try:
		sftp.mkdir("demo")
	except IOError:
		print 'IOError, the file already exists!'
		sftp.rmdir("demo")
		sftp.mkdir("demo")		
		print "Directory recreated."
	client.close()
except Exception, e:
	print 'Exception %s' % str(e)
	try:
		client.close()
	except:
		pass