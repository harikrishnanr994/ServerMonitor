import paramiko
import os
import firebase_admin
import json
from firebase_admin import credentials,db
cred = credentials.Certificate('cadmium75_admin.json')
firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://cadmium75-5deb5.firebaseio.com/' }
)
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.load_system_host_keys()
mRef = db.reference()
local_username =  os.popen("whoami").read().replace('\n', '')

def execute_command(c,ssh):
    stdin, stdout, stderr = ssh.exec_command(c)
    return (stdout.read(),stderr.read())

def execute_command_with_input(c,ssh,g = False):
    stdin, stdout, stderr = ssh.exec_command(c,get_pty = g)
    return (stdin,stdout,stderr)

server_list = mRef.child('Servers').get()
for server in server_list:
        server = server.replace('-','.')
        k = paramiko.RSAKey.from_private_key_file("/home/" + local_username + "/.ssh/id_rsa" , password='fuckoffanddie')
        ssh.connect(server, username='root', pkey=k)
        print "Connected"
        op,err = execute_command("sudo wp plugin update --all --allow-root --path='/var/www/html/'",ssh)
        print op,err
        op,err = execute_command("sudo wp theme update --all --allow-root --path='/var/www/html/'",ssh)
        print op,err
        op,err = execute_command("sudo wp core update --path='/var/www/html/' --allow-root",ssh)
        print op,err

