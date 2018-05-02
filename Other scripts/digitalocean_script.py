import digitalocean
from digitalocean import SSHKey


token = 'd9438060b8e14024f36044e0932c2554f40729d93179c1e75f49d5aa1912444d'

# Rememeber to uncomment this

'''
user_ssh_key = open('/home/sachin/.ssh/id_rsa.pub').read()
key = SSHKey(token=token,
             name='CadmiumKey',
             public_key=user_ssh_key)
key.create()
'''

manager = digitalocean.Manager(token=token)
keys = manager.get_all_sshkeys()
droplet = digitalocean.Droplet(token=token,
                               name='DropletWithSSHKeys',
                               region='blr1',
                               image='ubuntu-16-04-x64',
                               size_slug='1gb',
                               ssh_keys=keys,
                               backups=False)
droplet.create()
actions = droplet.get_actions()
for action in actions:
    print "Droplet in Progress"
    if action.wait():
        print "Droplet Created"
        my_droplets = manager.get_all_droplets()
        index = len(my_droplets)-1
        domain = digitalocean.Domain(name='example.in', ip_address=my_droplets[index].ip_address,token=token)
        domain.create()
        domain.create_new_domain_record(type='CNAME',name='www',data='@')
'''
my_droplets = manager.get_all_droplets()
domain = digitalocean.Domain(name='example.in', ip_address=my_droplets[1].ip_address,token=token)
print "%s,%s"% (domain.name,domain.ip_address)
domain.create()
'''
