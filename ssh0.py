import paramiko
from contextlib import contextmanager
import const
host = '139.59.15.110'
username = 'root'
password = 'fuckoffanddie'
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.load_system_host_keys()

def execute_command(c):
    stdin, stdout, stderr = ssh.exec_command(c)
    return (stdout.read(),stderr.read())

def execute_command_with_input(c):
    stdin, stdout, stderr = ssh.exec_command(c)
    return (stdin,stdout,stderr)

def remove_lock_file(err):
    print(err)
    if err.startswith(const.LOCK_ERR):
        op,err= execute_command('sudo rm /var/lib/apt/lists/lock')
        print op,err
        if err == '':
            print "Success"
        op,err = execute_command('sudo rm /var/cache/apt/archives/lock')
        print op,err
        if err == '':
            print "Success"
        op,err = execute_command('sudo rm /var/lib/dpkg/lock')
        print op,err
        if err == '':
            print "Success"
        return False
    return True

def write_default_values_for_ssl(inp):
    inp.write('.\n')
    inp.flush()
    inp.write('.\n')
    inp.flush()
    inp.write('.\n')
    inp.flush()
    inp.write('.\n')
    inp.flush()
    inp.write('.\n')
    inp.flush()
    inp.write('GD\n')
    inp.flush()
    inp.write('sachingiridhar@gmail.com\n')
    inp.flush()

try:
   print "Creating Connection"
   ssh.connect(host, username=username, password=password)
   print "Connected"

   while True:
       op,err = execute_command('sudo apt-get update')
       print op,err
       if remove_lock_file(err):
           break
   while True:
       op,err= execute_command('sudo apt-get install nginx -y')
       print op,err
       if remove_lock_file(err):
           break

   op,err= execute_command('curl ' + host)
   if op.startswith(const.CURL_OP):
       print "nginx Running Successfully"
   with open('default', 'r') as myfile:
       data = myfile.read()
       op,err= execute_command('sudo mv /etc/nginx/sites-available/default /etc/nginx/sites-available/default.backup')
       ftp = ssh.open_sftp()
       ftp.put('default','/etc/nginx/sites-available/default')
       ftp.close()
       op,err= execute_command('sudo cat /etc/nginx/sites-available/default')
       if op == data:
           print "nginx Config written Successfully"
   op,err= execute_command('sudo mkdir /etc/nginx/ssl')
   inp,op,err= execute_command_with_input('sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/nginx/ssl/nginx.key -out /etc/nginx/ssl/nginx.crt')
   write_default_values_for_ssl(inp)
   print "SSL Certificate Created"
   op,err= execute_command('ls /etc/nginx/ssl/')
   print op,err
   print "Creating Diffie Hellman Key...Please wait this is going to take a long time"
   op,err= execute_command('sudo openssl dhparam -out /etc/nginx/ssl/dhparam.pem 2048')
   if err.startswith(const.DIFFIE_HELMAN_OP):
       print "Diffie Helman Key Exchange Done"
   op,err= execute_command('sudo nginx -t')
   if err == const.NGINX_SUCCESS_MSG:
       print "nginx Configuation Successful...Now Restarting nginx"
   op,err= execute_command('sudo systemctl restart nginx.service')
   while True:
       op,err= execute_command('sudo apt-get install php7.0 php7.0-fpm -y')
       print op,err
       if remove_lock_file(err):
           break
   op,err= execute_command('sudo systemctl start php7.0-fpm')
   op,err= execute_command('sudo systemctl status php7.0-fpm')
   if const.PHP_RUNNING_MSG in op:
       print "PHP Successfully Running"
   with open('default', 'r') as myfile:
       data = myfile.read()
       ftp = ssh.open_sftp()
       ftp.put('default','/etc/nginx/sites-available/default')
       ftp.close()
       op,err= execute_command('sudo cat /etc/nginx/sites-available/default')
       print op,err
       if op == data:
           print "PHP Config written Successfully"
   '''
   if op.startswith(const.UFW_ERR):
        print 'Yooo'
        inp,op,err= execute_command_with_input("sudo ufw enable")
        inp.write('y\n')
        inp.flush()
        print op.read(),err.read()
        op,err= execute_command("sudo ufw status")
        print op,err'''
finally:
   print "Closing connection"
   ssh.close()
   print "Closed"
