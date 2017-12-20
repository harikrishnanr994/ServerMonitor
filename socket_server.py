import socketio
import eventlet
import paramiko
from contextlib import contextmanager
import const
import os
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

scheduler = BackgroundScheduler()

sio = socketio.Server(async_mode='threading',logger=True, ping_timeout = 120 , ping_interval = 30)
app = Flask(__name__)
app.wsgi_app = socketio.Middleware(sio, app.wsgi_app)

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

def write_default_values_for_ssl(inp,email):
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
    with open('sysctl.conf', 'r') as myfile:
        data = myfile.read()
        ftp = ssh.open_sftp()
        ftp.put('sysctl.conf','/etc/sysctl.conf')
        ftp.close()
        op,err = execute_command('sudo cat /etc/sysctl.conf')
        print op,err
        if op == data:
            print "Swap Config written Successfully"

def install_nginx(host,domain_name):
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
    print op,err
    op,err= execute_command('sudo service nginx stop')
    print op,err

def install_varnish(host):
    while True:
        op,err= execute_command('sudo apt-get install varnish -y')
        print op,err
        if remove_lock_file(err):
            break
    with open('varnish.service', 'r') as myfile:
        data = myfile.read()
        ftp = ssh.open_sftp()
        ftp.put('varnish.service','/lib/systemd/system/varnish.service')
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

def install_ssl(domain_name,email):
    inp,op,err = execute_command_with_input("sudo certbot --nginx -d " + domain_name + " -d www." + domain_name,True)
    write_default_values_for_ssl(inp,email)
    for line in iter(op.readline, ""):
        print line

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
    with open('index.php', 'r') as myfile:
        data = myfile.read()
        ftp = ssh.open_sftp()
        ftp.put('index.php','/var/www/html/index.php')
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

def install_wordpress(email,password,domain_name,username):
    print "Downloading Wordpress"
    op,err= execute_command('curl -O https://wordpress.org/latest.tar.gz')
    print op,err
    op,err= execute_command('tar xzvf latest.tar.gz')
    print op,err
    '''step['name'] =  'Wordpress Downloaded'
    step['percent'] = '95%'
    sio.emit('step', step)'''
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

def sio_heartbeat():
    sio.emit('heartbeat','heartbeat')

def connect_to_ssh(host,domain,email,username,password):
    try:
        scheduler.add_job(sio_heartbeat, 'interval', seconds=10)
        scheduler.start()
        step = {}
        print "Creating Connection"
        k = paramiko.RSAKey.from_private_key_file("/home/sachin/.ssh/id_rsa" , password='fuckoffanddie')
        ssh.connect(host, username='root', pkey=k)
        print "Connected"
        sio.emit('ssh_connected', 'SSH Connected')
        initialize_and_update_server()
        add_swap_space('4G')
        step['name'] = 'Updating Packages'
        step['percent'] = '20%'
        sio.emit('step', step)
        install_nginx(host,domain)
        step['name'] = 'nginx Installed'
        step['percent'] = '35%'
        sio.emit('step', step)
        install_varnish(host)
        step['name'] = 'Varnish Installed'
        step['percent'] = '50%'
        sio.emit('step', step)
        initialize_firewall()
        step['name'] = 'Firewall Configured for Extra Security'
        step['percent'] = '60%'
        sio.emit('step', step)
        install_ssl(domain,email)
        step['name'] = 'Installed SSL for ' + domain
        step['percent'] = '70%'
        sio.emit('step', step)
        install_php()
        step['name'] = 'PHP Installed'
        step['percent'] = '80%'
        sio.emit('step', step)
        install_mariadb()
        step['name'] = 'MariaDB Installed'
        step['percent'] = '90%'
        sio.emit('step', step)
        install_wordpress(email,password,domain,username)
        step['name'] =  'Wordpress Installed'
        step['percent'] = '100%'
        sio.emit('step', step)
    except paramiko.BadHostKeyException:
        os.system('ssh-keygen -f "/home/sachin/.ssh/known_hosts" -R ' + host)
        connect_to_ssh(host)
    finally:
       print "Closing connection"
       ssh.close()
       scheduler.shutdown()
       print "Closed"

@sio.on('connect')
def connect(sid, environ):
    print('connect ', sid , environ)
    sio.emit('socket_connected', "Socket Connected")


@sio.on('send_details')
def send_details(sid, data):
    print ('message ', data)
    host = data['host']
    domain = data['domain']
    email = data['email']
    username = data['username']
    password = data['password']
    connect_to_ssh(host,domain,email,username,password)




@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)



if __name__ == '__main__':
    # wrap Flask application with socketio's middleware
    # deploy as an eventlet WSGI server
    app.run(threaded=True,port=5000)
