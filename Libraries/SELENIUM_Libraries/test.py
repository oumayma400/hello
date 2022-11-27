import paramiko
import os

host = '172.30.13.165'
port = 22
username='root'
password= 'Sa<#Xu!-q]8IodY'
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh.connect(host, port, username, password)


apath = '/var/log/siconia/apache-karaf/'
apattern = '"*.log"'
rawcommand = 'find {path} -name {pattern}'
command = rawcommand.format(path=apath, pattern=apattern)
stdin, stdout, stderr = ssh.exec_command(command)
filelist = stdout.read().splitlines()

ftp = ssh.open_sftp()
for afile in filelist:
    (head, filename) = os.path.split(afile)
    print(filename)
    ftp.get(afile, './'+filename)
ftp.close()
ssh.close()
