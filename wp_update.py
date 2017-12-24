import paramiko
from contextlib import contextmanager
import const
import os
import shutil
import random
import string

host = '139.59.41.122'
domain_name = 'mymds.xyz'
username = 'root'
password = 'fuckoffanddie'
email = 'sachingiridhar@gmail.com'
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.load_system_host_keys()

def generate_random_string(size):
    return ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(size))

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

def cancel_duplicate_ssl(inp):
    inp.write('1\n')
    inp.flush()
    inp.write('2\n')
    inp.flush()

def kill_certbot_process():
    op,err = execute_command("for pid in $(ps -ef | grep 'certbot' | awk '{print $2}'); do kill -9 $pid; done")
    print op,err


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
    with open("config_files/temp_secret.php",'r') as fp:
        for line in fp:
            secrets.append(line)
    with open('config_files/wp-config-sample.php','r') as fin, open('config_files/wp-config.php','w') as fout:
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

def initialize_and_update_server():
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
def add_swap_space(swap):
    op,err = execute_command('sudo fallocate -l ' + swap + ' /swapfile')
    op,err = execute_command('sudo chmod 600 /swapfile')
    print op,err
    op,err = execute_command('sudo mkswap /swapfile')
    op,err = execute_command('sudo swapon /swapfile')
    op,err = execute_command('sudo cp /etc/fstab /etc/fstab.bak')
    op,err = execute_command("echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab")
    op,err = execute_command('sudo sysctl vm.swappiness=10')
    print op,err
    with open('config_files/sysctl.conf', 'r') as myfile:
        data = myfile.read()
        ftp = ssh.open_sftp()
        ftp.put('config_files/sysctl.conf','/etc/sysctl.conf')
        ftp.close()
        op,err = execute_command('sudo cat /etc/sysctl.conf')
        print op,err
        if op == data:
            print "Swap Config written Successfully"

def install_nginx():
    while True:
        op,err= execute_command('sudo apt-get install nginx -y')
        print op,err
        if remove_lock_file(err):
            break
    op,err= execute_command('curl ' + host)
    print op,err
    if op.startswith(const.CURL_OP):
        print "nginx Running Successfully"
    random = generate_random_string(16)
    if not os.path.exists('config_files/' + random):
        os.makedirs('config_files/' + random)
    with open('config_files/def', 'r') as fin,open('config_files/' + random +'/default','w') as fout:
        data = fin.read().replace('139.59.15.110',host).replace('mymds.xyz',domain_name)
        fout.write(data)
    op,err= execute_command('sudo mv /etc/nginx/sites-enabled/default /etc/nginx/sites-available/default.backup')
    ftp = ssh.open_sftp()
    ftp.put('config_files/'+ random + '/default','/etc/nginx/sites-enabled/default')
    ftp.close()
    op,err= execute_command('sudo cat /etc/nginx/sites-enabled/default')
    print op,err
    if op == data:
        print "nginx Config written Successfully"
    op,err = execute_command('sudo nginx -t')
    if err == const.NGINX_SUCCESS_MSG:
        print "nginx Configuation Successful...Now Restarting nginx"
    op,err= execute_command('sudo systemctl restart nginx.service')
    print op,err
    shutil.rmtree('config_files/' + random)
    op,err= execute_command('sudo service nginx stop')
    print op,err

def install_varnish():
    while True:
        op,err= execute_command('sudo apt-get install varnish -y')
        print op,err
        if remove_lock_file(err):
            break
    with open('config_files/varnish.service', 'r') as myfile:
        data = myfile.read()
        ftp = ssh.open_sftp()
        ftp.put('config_files/varnish.service','/lib/systemd/system/varnish.service')
        ftp.close()
        op,err= execute_command('sudo cat /lib/systemd/system/varnish.service')
        print op,err
        if op == data:
            print "Varnish Config written Successfully"
    op,err = execute_command('systemctl daemon-reload')
    op,err = execute_command('sudo service varnish restart')
    op,err = execute_command('sudo service nginx start')
    op,err = execute_command('curl ' + host)
    print op,err
    if op.startswith(const.CURL_OP):
        print "nginx with varnish Running Successfully"

def initialize_firewall():
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
    op,err = execute_command('sudo ufw allow 8080/tcp')
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

def install_ssl():
    inp,op,err = execute_command_with_input("sudo certbot --nginx -d " + domain_name + " -d www." + domain_name,True)
    for line in iter(op.readline, ""):
        if line.startswith(const.LETS_ENCRYPT_DEFAULT):
            write_default_values_for_ssl(inp)
        elif line.startswith(const.LETSENCRYPT_ALREADY_EXISTING):
            cancel_duplicate_ssl(inp)
        elif line.startswith(const.CERTBOT_ANOTHER_INSTANCE):
            another_instance = True
            kill_certbot_process()
            install_ssl()
        print line



def configure_nginx_for_ssl():
    random = generate_random_string(16)
    if not os.path.exists('config_files/' + random):
        os.makedirs('config_files/' + random)
    with open('config_files/def_ssl', 'r') as fin,open('config_files/' +  random +'/default','w') as fout:
        data = fin.read().replace('139.59.15.110',host).replace('mymds.xyz',domain_name)
        fout.write(data)
    op,err= execute_command('sudo mv /etc/nginx/sites-enabled/default /etc/nginx/sites-available/default.backup')
    ftp = ssh.open_sftp()
    ftp.put('config_files/' +  random +'/default','/etc/nginx/sites-enabled/default')
    ftp.close()
    op,err= execute_command('sudo cat /etc/nginx/sites-enabled/default')
    print op,err
    if op == data:
        print "nginx Config written Successfully"
    op,err = execute_command('sudo nginx -t')
    if err == const.NGINX_SUCCESS_MSG:
        print "nginx Configuation Successful...Now Restarting nginx"
    op,err= execute_command('sudo systemctl restart nginx.service')
    print op,err
    #shutil.rmtree('config_files/' + random)

def install_php():
    while True:
        op,err= execute_command('sudo apt-get install php7.0 php7.0-fpm -y')
        print op,err
        if remove_lock_file(err):
            break

    op,err= execute_command('sudo systemctl start php7.0-fpm')
    op,err= execute_command('sudo systemctl status php7.0-fpm')
    if const.PHP_RUNNING_MSG in op:
        print "PHP Successfully Running"
    with open('config_files/index.php', 'r') as myfile:
        data = myfile.read()
        ftp = ssh.open_sftp()
        ftp.put('config_files/index.php','/var/www/html/index.php')
        ftp.close()
        op,err= execute_command('sudo cat /var/www/html/index.php')
        print op,err
        if op == data:
            print "PHP Index written Successfully"

def install_mariadb():
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

def install_wordpress():
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
    with open('config_files/temp_secret.php', 'w') as myfile:
        myfile.write(op)
    write_to_wp_config_file()
    ftp = ssh.open_sftp()
    ftp.put('config_files/wp-config.php','/var/www/html/wp-config.php')
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
try:
   print "Creating Connection"
   k = paramiko.RSAKey.from_private_key_file("/home/sachin/.ssh/id_rsa" , password=password)
   ssh.connect(host, username=username, pkey=k)
   print "Connected"
   initialize_and_update_server()
   add_swap_space('4G')
   install_nginx()
   install_varnish()
   initialize_firewall()
   install_ssl()
   configure_nginx_for_ssl()
   install_php()
   install_mariadb()
   install_wordpress()
except paramiko.BadHostKeyException:
    os.system('ssh-keygen -f "/home/sachin/.ssh/known_hosts" -R ' + host)
finally:
   print "Closing connection"
   ssh.close()
   print "Closed"
