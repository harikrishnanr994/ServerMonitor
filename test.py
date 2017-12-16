#!/usr/bin/python
import re
import subprocess

line = subprocess.call("echo Hello World", shell=True)
print line
matchObj = re.match( r'ssh-keygen', line, re.M|re.I)

if matchObj:
   print "matchObj.group() : ", matchObj.group()
   print "matchObj.group(1) : ", matchObj.group(1)
   print "matchObj.group(2) : ", matchObj.group(2)
else:
   print "No match!!"
