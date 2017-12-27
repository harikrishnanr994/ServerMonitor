import socketio
import eventlet
import paramiko
from contextlib import contextmanager
import const
import os
import shutil
import random
import string
from datetime import datetime
from flask import Flask, render_template
from apscheduler.schedulers.background import BackgroundScheduler
import logging
log = logging.getLogger('apscheduler.executors.default')
log.setLevel(logging.INFO)  # DEBUG

fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
h = logging.StreamHandler()
h.setFormatter(fmt)
log.addHandler(h)


sio = socketio.Server(async_mode='threading',logger=True, ping_timeout = 240 , ping_interval = 30)
app = Flask(__name__)
app.wsgi_app = socketio.Middleware(sio, app.wsgi_app)


def generate_random_string(size):
    return ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(size))

def execute_command(c,ssh):
    stdin, stdout, stderr = ssh.exec_command(c)
    return (stdout.read(),stderr.read())

def execute_command_with_input(c,ssh,g = False):
    stdin, stdout, stderr = ssh.exec_command(c,get_pty = g)
    return (stdin,stdout,stderr)

def remove_lock_file(err,ssh):
    print(err)
    if err.startswith(const.LOCK_ERR):
        op,err= execute_command('sudo rm /var/lib/apt/lists/lock',ssh)
        print op,err
        if err == '':
            print "Success"
        op,err = execute_command('sudo rm /var/cache/apt/archives/lock',ssh)
        print op,err
        if err == '':
            print "Success"
        op,err = execute_command('sudo rm /var/lib/dpkg/lock')
        print op,err
        if err == '':
            print "Success"
        return False
    return True

def write_default_values_for_ssl(inp,email):
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
    op,err = execute_command("for pid in $(ps -ef | grep 'certbot' | awk '{print $2}'); do kill -9 $pid; done",ssh)
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

def is_nginx_installed(ssh):
    op,err = execute_command('test -x /usr/sbin/nginx && echo "Nginx installed"',ssh)
    if op.startswith('Nginx installed'):
        return True
    return False

def initialize_and_update_server(ssh):
    inp,op,err= execute_command_with_input('sudo add-apt-repository ppa:certbot/certbot',ssh)
    inp.write('\n')
    inp.flush()
    print op.read()
    while True:
        op,err = execute_command('sudo apt-get update',ssh)
        print op,err
        if remove_lock_file(err,ssh):
            break
    while True:
        op,err = execute_command('sudo apt-get install python-certbot-nginx -y',ssh)
        print op,err
        if remove_lock_file(err,ssh):
            break
def add_swap_space(swap,ssh):
    op,err = execute_command('sudo fallocate -l ' + swap + ' /swapfile',ssh)
    op,err = execute_command('sudo chmod 600 /swapfile',ssh)
    print op,err
    op,err = execute_command('sudo mkswap /swapfile',ssh)
    op,err = execute_command('sudo swapon /swapfile',ssh)
    op,err = execute_command('sudo cp /etc/fstab /etc/fstab.bak',ssh)
    op,err = execute_command("echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab",ssh)
    op,err = execute_command('sudo sysctl vm.swappiness=10',ssh)
    print op,err
    with open('config_files/sysctl.conf', 'r') as myfile:
        data = myfile.read()
        ftp = ssh.open_sftp()
        ftp.put('config_files/sysctl.conf','/etc/sysctl.conf')
        ftp.close()
        op,err = execute_command('sudo cat /etc/sysctl.conf',ssh)
        print op,err
        if op == data:
            print "Swap Config written Successfully"

def install_nginx(host,domain,ssh):
    while True:
        op,err= execute_command('sudo apt-get install nginx -y',ssh)
        print op,err
        if remove_lock_file(err,ssh):
            break
    op,err= execute_command('curl ' + host,ssh)
    print op,err
    if op.startswith(const.CURL_OP):
        print "nginx Running Successfully"
    random = generate_random_string(16)
    if not os.path.exists('config_files/' + random):
        os.makedirs('config_files/' + random)
    with open('config_files/def', 'r') as fin,open('config_files/' + random +'/default','w') as fout:
        data = fin.read().replace('139.59.15.110',host).replace('mymds.xyz',domain)
        fout.write(data)
    op,err= execute_command('sudo mv /etc/nginx/sites-enabled/default /etc/nginx/sites-available/default.backup',ssh)
    ftp = ssh.open_sftp()
    ftp.put('config_files/'+ random + '/default','/etc/nginx/sites-enabled/default')
    ftp.close()
    op,err= execute_command('sudo cat /etc/nginx/sites-enabled/default',ssh)
    print op,err
    if op == data:
        print "nginx Config written Successfully"
    op,err = execute_command('sudo nginx -t',ssh)
    if err == const.NGINX_SUCCESS_MSG:
        print "nginx Configuation Successful...Now Restarting nginx"
    op,err= execute_command('sudo systemctl restart nginx.service',ssh)
    print op,err
    shutil.rmtree('config_files/' + random)
    op,err= execute_command('sudo service nginx stop',ssh)
    print op,err

def install_varnish(host,ssh):
    while True:
        op,err= execute_command('sudo apt-get install varnish -y',ssh)
        print op,err
        if remove_lock_file(err,ssh):
            break
    with open('config_files/varnish.service', 'r') as myfile:
        data = myfile.read()
        ftp = ssh.open_sftp()
        ftp.put('config_files/varnish.service','/lib/systemd/system/varnish.service')
        ftp.close()
        op,err= execute_command('sudo cat /lib/systemd/system/varnish.service',ssh)
        print op,err
        if op == data:
            print "Varnish Config written Successfully"
    op,err = execute_command('systemctl daemon-reload',ssh)
    op,err = execute_command('sudo service varnish restart',ssh)
    op,err = execute_command('sudo service nginx start',ssh)
    op,err = execute_command('curl ' + host,ssh)
    print op,err
    if op.startswith(const.CURL_OP):
        print "nginx with varnish Running Successfully"

def initialize_firewall(ssh):
    op,err = execute_command('sudo ufw disable',ssh)
    print op,err
    op,err = execute_command('sudo ufw default deny incoming',ssh)
    print op,err
    op,err = execute_command('sudo ufw default allow outgoing',ssh)
    print op,err
    op,err = execute_command('sudo ufw allow ssh',ssh)
    print op,err
    op,err = execute_command('sudo ufw allow www',ssh)
    print op,err
    op,err = execute_command('sudo ufw allow 8080/tcp',ssh)
    print op,err
    op,err = execute_command('sudo ufw allow ftp',ssh)
    print op,err
    op,err = execute_command("sudo ufw allow 'OpenSSH'",ssh)
    print op,err
    op,err = execute_command("sudo ufw allow 'Nginx Full'",ssh)
    print op,err
    op,err = execute_command("sudo ufw allow 'Nginx HTTP'",ssh)
    print op,err
    inp,op,err = execute_command_with_input('sudo ufw enable',ssh)
    inp.write('y\n')
    inp.flush()
    print op.read()
    op,err = execute_command('sudo ufw status',ssh)
    print op,err

def install_ssl(domain,email,ssh):
    inp,op,err = execute_command_with_input("sudo certbot --nginx -d " + domain + " -d www." + domain,ssh,True)
    for line in iter(op.readline, ""):
        if line.startswith(const.LETS_ENCRYPT_DEFAULT):
            write_default_values_for_ssl(inp,email)
        elif line.startswith(const.LETSENCRYPT_ALREADY_EXISTING):
            cancel_duplicate_ssl(inp)
        elif line.startswith(const.CERTBOT_ANOTHER_INSTANCE):
            another_instance = True
            kill_certbot_process()
            install_ssl(domain,email,ssh)
        print line



def configure_nginx_for_ssl(host,domain,ssh):
    random = generate_random_string(16)
    if not os.path.exists('config_files/' + random):
        os.makedirs('config_files/' + random)
    with open('config_files/def_ssl', 'r') as fin,open('config_files/' +  random +'/default','w') as fout:
        data = fin.read().replace('139.59.15.110',host).replace('mymds.xyz',domain)
        fout.write(data)
    op,err= execute_command('sudo mv /etc/nginx/sites-enabled/default /etc/nginx/sites-available/default.backup',ssh)
    ftp = ssh.open_sftp()
    ftp.put('config_files/' +  random +'/default','/etc/nginx/sites-enabled/default')
    ftp.close()
    op,err= execute_command('sudo cat /etc/nginx/sites-enabled/default',ssh)
    print op,err
    if op == data:
        print "nginx Config written Successfully"
    op,err = execute_command('sudo nginx -t',ssh)
    if err == const.NGINX_SUCCESS_MSG:
        print "nginx Configuation Successful...Now Restarting nginx"
    op,err= execute_command('sudo systemctl restart nginx.service',ssh)
    print op,err
    shutil.rmtree('config_files/' + random)

def install_php(ssh):
    while True:
        op,err= execute_command('sudo apt-get install php7.0 php7.0-fpm -y',ssh)
        print op,err
        if remove_lock_file(err,ssh):
            break

    op,err= execute_command('sudo systemctl start php7.0-fpm',ssh)
    op,err= execute_command('sudo systemctl status php7.0-fpm',ssh)
    if const.PHP_RUNNING_MSG in op:
        print "PHP Successfully Running"
    with open('config_files/index.php', 'r') as myfile:
        data = myfile.read()
        ftp = ssh.open_sftp()
        ftp.put('config_files/index.php','/var/www/html/index.php')
        ftp.close()
        op,err= execute_command('sudo cat /var/www/html/index.php',ssh)
        print op,err
        if op == data:
            print "PHP Index written Successfully"

def install_mariadb(ssh):
    while True:
        op,err= execute_command('sudo apt-get install mariadb-server mariadb-client php7.0-mysql -y',ssh)
        print op,err
        if remove_lock_file(err,ssh):
            break
    op,err= execute_command('sudo systemctl status php7.0-fpm',ssh)
    inp,op,err= execute_command_with_input('sudo mysql_secure_installation',ssh)
    write_default_values_for_mariadb(inp)
    print "MariaDB Installed"
    inp,op,err= execute_command_with_input('sudo mysql -u root -pwordpress',ssh,True)
    write_commands_for_mariadb(inp)
    print "MariaDB Commands Successfully Executed"
    while True:
        op,err= execute_command('sudo apt-get install php-curl php-gd php-mbstring php-mcrypt php-xml php-xmlrpc -y',ssh)
        print op,err
        if remove_lock_file(err,ssh):
            break
    op,err= execute_command('sudo systemctl restart php7.0-fpm',ssh)
    print op,err

def install_wordpress(email,password,domain,username,ssh):
    print "Downloading Wordpress"
    op,err= execute_command('curl -O https://wordpress.org/latest.tar.gz',ssh)
    print op,err
    op,err= execute_command('tar xzvf latest.tar.gz',ssh)
    print op,err
    print "Wordpress Downloaded"
    op,err= execute_command('cp wordpress/wp-config-sample.php wordpress/wp-config.php',ssh)
    print op,err
    op,err= execute_command('mkdir wordpress/wp-content/upgrade',ssh)
    op,err= execute_command('sudo cp -a wordpress/. /var/www/html',ssh)
    print op,err
    op,err= execute_command('sudo chown -R root:www-data /var/www/html',ssh)
    print op,err
    op,err= execute_command('sudo find /var/www/html -type d -exec chmod g+s {} \;',ssh)
    print op,err
    op,err= execute_command('sudo chmod g+w /var/www/html/wp-content',ssh)
    print op,err
    op,err= execute_command('sudo chmod -R g+w /var/www/html/wp-content/themes',ssh)
    print op,err
    op,err= execute_command('sudo chmod -R g+w /var/www/html/wp-content/plugins',ssh)
    print op,err
    op,err= execute_command('curl -s https://api.wordpress.org/secret-key/1.1/salt/',ssh)
    print op,err
    with open('config_files/temp_secret.php', 'w') as myfile:
        myfile.write(op)
    write_to_wp_config_file()
    ftp = ssh.open_sftp()
    ftp.put('config_files/wp-config.php','/var/www/html/wp-config.php')
    ftp.close()
    temp_secret = op
    op,err= execute_command('sudo cat /var/www/html/wp-config.php',ssh)
    print op,err
    print "Wordpress Configuration File Created"
    op,err= execute_command('curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar',ssh)
    print op,err
    op,err= execute_command('chmod +x wp-cli.phar',ssh)
    print op,err
    op,err= execute_command('sudo mv wp-cli.phar /usr/local/bin/wp',ssh)
    print op,err
    op,err= execute_command('sudo wp cli version --allow-root',ssh)
    print op,err
    op,err= execute_command('sudo wp core install --url="' +  domain + '"  --title="Your Blog Title" --admin_user="' + username + '" --admin_password="' +  password + '" --admin_email="' + email + '" --path="/var/www/html/" --allow-root',ssh)
    print op,err
    op,err= execute_command("sudo wp search-replace 'http://" + domain + "' 'https://" + domain + "' --skip-columns=guid --allow-root --path='/var/www/html/'",ssh)
    print op,err


def connect_to_ssh(host,domain,email,username,password,sid):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.load_system_host_keys()
        step = {}
        print "Creating Connection"
        k = paramiko.RSAKey.from_private_key_file("/home/sachin/.ssh/id_rsa" , password='fuckoffanddie')
        ssh.connect(host, username='root', pkey=k)
        print "Connected"
        sio.emit('ssh_connected', 'SSH Connected',room=sid)
        step['name'] = 'Updating Packages'
        step['percent'] = '5%'
        sio.emit('step', step,room=sid)
        initialize_and_update_server(ssh)
        add_swap_space('4G',ssh)
        if is_nginx_installed(ssh):
            step['name'] = 'Installing nginx'
            step['percent'] = '20%'
            sio.emit('step', step,room=sid)
            install_nginx(host,domain,ssh)

        step['name'] = 'Installing Varnish'
        step['percent'] = '30%'
        sio.emit('step', step,room=sid)
        install_varnish(host,ssh)
        step['name'] = 'Configuring Firewall for Extra Security'
        step['percent'] = '40%'
        sio.emit('step', step,room=sid)
        initialize_firewall(ssh)
        step['name'] = 'Installing SSL for ' + domain
        step['percent'] = '50%'
        sio.emit('step', step,room=sid)
        install_ssl(domain,email,ssh)
        step['name'] = 'Configuring nginx for SSL'
        step['percent'] = '65%'
        sio.emit('step', step,room=sid)
        configure_nginx_for_ssl(host,domain,ssh)
        step['name'] = 'Installing PHP'
        step['percent'] = '70%'
        sio.emit('step', step,room=sid)
        install_php(ssh)
        step['name'] = 'Installing MariaDB'
        step['percent'] = '80%'
        sio.emit('step', step,room=sid)
        install_mariadb(ssh)
        step['name'] =  'Installing Wordpress'
        step['percent'] = '90%'
        sio.emit('step', step,room=sid)
        install_wordpress(email,password,domain,username,ssh)
        step['name'] =  'Completed'
        step['percent'] = '100%'
        sio.emit('step', step,room=sid)

    except paramiko.BadHostKeyException:
        os.system('ssh-keygen -f "/home/sachin/.ssh/known_hosts" -R ' + host)
        connect_to_ssh(host,domain,email,username,password)
    finally:
       print "Closing connection"
       ssh.close()
       sio.leave_room(sid,sid)
       print "Closed"

@sio.on('connect')
def connect(sid, environ):
    print('connect ', sid , environ)
    sio.enter_room(sid,sid)
    sio.emit('socket_connected', "Socket Connected",room=sid)


@sio.on('send_details')
def send_details(sid, data):
    print ('message ', data)
    host = data['host']
    domain = data['domain']
    email = data['email']
    username = data['username']
    password = data['password']
    connect_to_ssh(host,domain,email,username,password,sid)




@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)



if __name__ == '__main__':
    # wrap Flask application with socketio's middleware
    # deploy as an eventlet WSGI server
    app.run(threaded=True,port=5000)
