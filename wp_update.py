import paramiko
from contextlib import contextmanager
import const
host = '139.59.15.110'
domain_name = 'mymds.xyz'
username = 'root'
password = 'fuckoffanddie'
email = 'sachingiridhar@gmail.com'
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.load_system_host_keys()

def execute_command(c):
    stdin, stdout, stderr = ssh.exec_command(c)
    return (stdout.read(),stderr.read())

def execute_command_with_input(c,g = False):
    stdin, stdout, stderr = ssh.exec_command(c,get_pty = g)
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
    inp.write(email + '\n')
    inp.flush()
    inp.write('a\n')
    inp.flush()
    inp.write('n\n')
    inp.flush()
    inp.write('2\n')
    inp.flush()

def write_default_values_for_mariadb(inp):
    inp.write('\n')
    inp.flush()
    inp.write('y\n')
    inp.flush()
    inp.write('wordpress\n')
    inp.flush()
    inp.write('wordpress\n')
    inp.flush()
    inp.write('y\n')
    inp.flush()
    inp.write('n\n')
    inp.flush()
    inp.write('y\n')
    inp.flush()
    inp.write('y\n')
    inp.flush()

def write_to_wp_config_file():
    secrets = []
    with open("temp_secret.php",'r') as fp:
        for line in fp:
            secrets.append(line)
    with open('wp-config-sample.php','r') as fin, open('wp-config.php','w') as fout:
        for i,wp_line in enumerate(fin):
            if i>=31 and i<=38:
                fout.write(secrets[i-31])
            else:
                fout.write(wp_line)

def write_commands_for_mariadb(inp):
    inp.write('CREATE DATABASE wordpress DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;\n')
    inp.flush()
    inp.write("GRANT ALL ON wordpress.* TO 'wordpressuser'@'localhost' IDENTIFIED BY 'wordpress';\n")
    inp.flush()
    inp.write('flush privileges;\n')
    inp.flush()
    inp.write('use mysql;\n')
    inp.flush()
    inp.write("update user set plugin='' WHERE User='root';\n")
    inp.flush()
    inp.write('flush privileges;\n')
    inp.flush()
    inp.write('exit;\n')
    inp.flush()

try:
   print "Creating Connection"
   ssh.connect(host, username=username, password=password)
   print "Connected"
   inp,op,err= execute_command_with_input('sudo add-apt-repository ppa:certbot/certbot')
   inp.write('\n')
   inp.flush()
   print op.read()
   while True:
       op,err = execute_command('sudo apt-get update')
       print op,err
       if remove_lock_file(err):
           break
   while True:
       op,err = execute_command('sudo apt-get install python-certbot-nginx -y')
       print op,err
       if remove_lock_file(err):
           break
   while True:
       op,err= execute_command('sudo apt-get install nginx -y')
       print op,err
       if remove_lock_file(err):
           break

   op,err= execute_command('curl ' + host)
   print op,err
   if op.startswith(const.CURL_OP):
       print "nginx Running Successfully"
   with open('def', 'r') as fin,open('default','w') as fout:
       data = fin.read().replace('139.59.15.110',host).replace('mymds.xyz',domain_name)
       fout.write(data)
   op,err= execute_command('sudo mv /etc/nginx/sites-available/default /etc/nginx/sites-available/default.backup')
   ftp = ssh.open_sftp()
   ftp.put('default','/etc/nginx/sites-available/default')
   ftp.close()
   op,err= execute_command('sudo cat /etc/nginx/sites-available/default')
   print op,err
   if op == data:
       print "nginx Config written Successfully"
   op,err = execute_command('sudo nginx -t')
   if err == const.NGINX_SUCCESS_MSG:
       print "nginx Configuation Successful...Now Restarting nginx"
   op,err= execute_command('sudo systemctl restart nginx.service')
   op,err = execute_command('sudo ufw disable')
   print op,err
   op,err = execute_command('sudo ufw default deny incoming')
   print op,err
   op,err = execute_command('sudo ufw default allow outgoing')
   print op,err
   op,err = execute_command('sudo ufw allow ssh')
   print op,err
   op,err = execute_command('sudo ufw allow www')
   print op,err
   op,err = execute_command('sudo ufw allow ftp')
   print op,err
   op,err = execute_command("sudo ufw allow 'OpenSSH'")
   print op,err
   op,err = execute_command("sudo ufw allow 'Nginx Full'")
   print op,err
   op,err = execute_command("sudo ufw allow 'Nginx HTTP'")
   print op,err
   inp,op,err = execute_command_with_input('sudo ufw enable')
   inp.write('y\n')
   inp.flush()
   print op.read()
   op,err = execute_command('sudo ufw status')
   print op,err
   inp,op,err = execute_command_with_input("sudo certbot --nginx -d " + domain_name + " -d www." + domain_name,True)
   write_default_values_for_ssl(inp)
   for line in iter(op.readline, ""):
    print line
   while True:
       op,err= execute_command('sudo apt-get install php7.0 php7.0-fpm -y')
       print op,err
       if remove_lock_file(err):
           break

   op,err= execute_command('sudo systemctl start php7.0-fpm')
   op,err= execute_command('sudo systemctl status php7.0-fpm')
   if const.PHP_RUNNING_MSG in op:
       print "PHP Successfully Running"
   with open('index.php', 'r') as myfile:
       data = myfile.read()
       ftp = ssh.open_sftp()
       ftp.put('index.php','/var/www/html/index.php')
       ftp.close()
       op,err= execute_command('sudo cat /var/www/html/index.php')
       print op,err
       if op == data:
           print "PHP Index written Successfully"
   while True:
       op,err= execute_command('sudo apt-get install mariadb-server mariadb-client php7.0-mysql -y')
       print op,err
       if remove_lock_file(err):
           break
   op,err= execute_command('sudo systemctl status php7.0-fpm')
   inp,op,err= execute_command_with_input('sudo mysql_secure_installation')
   write_default_values_for_mariadb(inp)
   print "MariaDB Installed"
   inp,op,err= execute_command_with_input('sudo mysql -u root -pwordpress',True)
   write_commands_for_mariadb(inp)
   print "MariaDB Commands Successfully Executed"
   while True:
       op,err= execute_command('sudo apt-get install php-curl php-gd php-mbstring php-mcrypt php-xml php-xmlrpc -y')
       print op,err
       if remove_lock_file(err):
           break
   op,err= execute_command('sudo systemctl restart php7.0-fpm')
   print op,err
   op,err= execute_command('sudo cd /tmp')
   print "Downloading Wordpress"
   op,err= execute_command('curl -O https://wordpress.org/latest.tar.gz')
   print op,err
   op,err= execute_command('tar xzvf latest.tar.gz')
   print op,err
   print "Wordpress Downloaded"
   op,err= execute_command('cp wordpress/wp-config-sample.php wordpress/wp-config.php')
   print op,err
   op,err= execute_command('mkdir wordpress/wp-content/upgrade')
   op,err= execute_command('sudo cp -a wordpress/. /var/www/html')
   print op,err
   op,err= execute_command('sudo chown -R root:www-data /var/www/html')
   print op,err
   op,err= execute_command('sudo find /var/www/html -type d -exec chmod g+s {} \;')
   print op,err
   op,err= execute_command('sudo chmod g+w /var/www/html/wp-content')
   print op,err
   op,err= execute_command('sudo chmod -R g+w /var/www/html/wp-content/themes')
   print op,err
   op,err= execute_command('sudo chmod -R g+w /var/www/html/wp-content/plugins')
   print op,err
   op,err= execute_command('curl -s https://api.wordpress.org/secret-key/1.1/salt/')
   print op,err
   with open('temp_secret.php', 'w') as myfile:
       myfile.write(op)
   write_to_wp_config_file()
   ftp = ssh.open_sftp()
   ftp.put('wp-config.php','/var/www/html/wp-config.php')
   ftp.close()
   temp_secret = op
   op,err= execute_command('sudo cat /var/www/html/wp-config.php')
   print op,err
   print "Wordpress Configuration File Created"
   op,err= execute_command('curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar')
   print op,err
   op,err= execute_command('chmod +x wp-cli.phar')
   print op,err
   op,err= execute_command('sudo mv wp-cli.phar /usr/local/bin/wp')
   print op,err
   op,err= execute_command('sudo wp cli version --allow-root')
   print op,err
   op,err= execute_command('sudo wp core install --url="' +  domain_name + '"  --title="Your Blog Title" --admin_user="' + username + '" --admin_password="' +  password + '" --admin_email="' + email + '" --path="/var/www/html/" --allow-root')
   print op,err
   op,err= execute_command("sudo wp search-replace 'http://" + domain_name + "' 'https://" + domain_name + "' --skip-columns=guid --allow-root --path='/var/www/html/'")
   print op,err
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
