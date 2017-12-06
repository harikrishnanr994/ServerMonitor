secrets = []

with open("temp_secret.php",'r') as fp:
    for line in fp:
        secrets.append(line)

with open('wp-config-sample.php','r') as fin, open('wp-config.php','w') as fout:
    for i,wp_line in enumerate(fin):

        print i,wp_line
        if i>=31 and i<=38:
            print i,wp_line
            fout.write(secrets[i-31])

        else:
            fout.write(wp_line)
