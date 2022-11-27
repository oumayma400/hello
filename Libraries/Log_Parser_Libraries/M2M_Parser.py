
import paramiko
import pandas as pd
import ast
import re
from lxml import etree
import sys,os
from pathlib import Path
path = Path(os.path.abspath(__file__))
parrent_path = path.parent.absolute()

DB_Libraries = os.path.dirname(parrent_path) + os.path.sep + "DB_Libraries";
DB_Libraries2 = DB_Libraries.replace('\\', '/')
sys.path.append(DB_Libraries2)
import AccessDB as accessdb

Read_ConfigLib = os.path.dirname(parrent_path) + os.path.sep + "Read_Config";
Read_ConfigLib2 = Read_ConfigLib.replace('\\', '/')
sys.path.append(Read_ConfigLib2)
import ReadConfigFile as conf

currentpath = os.path.dirname(parrent_path) + os.path.sep + "Log_Parser_Libraries";
currentpath2 = currentpath.replace('\\', '/')
sys.path.append(currentpath2)


def run_cmd(sshClient, command):
    channel = sshClient.get_transport().open_session()
    channel.get_pty()
    channel.exec_command(command)
    out = channel.makefile().readlines()
    err = channel.makefile_stderr().read()
    returncode = channel.recv_exit_status()
    channel.close()                       # channel is closed, but not the client
    return out, err, returncode

def m2m_task(PROJECT, task_id):
    job_id= accessdb.get_job_id_from_cim(PROJECT,task_id)
    print(job_id)
    if job_id != '':
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        host = conf.ReadConfigFile.read(PROJECT,'m2m_ip')
        port = 22
        username=conf.ReadConfigFile.read(PROJECT,'m2m_ip_user')
        password= conf.ReadConfigFile.read(PROJECT,'m2m_ip_pass')
        client.connect(host, port, username, password)


        out, err, rc = run_cmd(client, 'sed -n -e "/\(.*\)taskRes xmlns=\(.*\)'+job_id+'/,/taskRes>/p" /var/log/siconia/apache-karaf/m2m.log | tr "\n" " "' )
        print(out)
        client.close()
        line=str(out)
        first_result = ast.literal_eval(line)


        s= first_result[1]
        start = s.find("<taskRes")

        end = s.find("</taskRes>")

        substring = s[start:end]
        substring= '<?xml version="1.0" ?>\n'+ substring + '</taskRes>'
        print(substring)
        # new_file2=open("newfile3.txt",mode="w",encoding="utf-8")
        # new_file2.write(substring)
        root = etree.fromstring(substring)
        tree = etree.ElementTree(root)
        root= tree.getroot()
        print(root)

        return etree.tostring(tree, pretty_print=True)

def m2m_message(PROJECT, device_id, message_type):

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    host = conf.ReadConfigFile.read(PROJECT,'m2m_ip')
    port = 22
    username=conf.ReadConfigFile.read(PROJECT,'m2m_ip_user')
    password= conf.ReadConfigFile.read(PROJECT,'m2m_ip_pass')
    client.connect(host, port, username, password)


    out, err, rc = run_cmd(client, 'sed -n -e "/\(.*\)devdisc xmlns=\(.*\)/,/devdisc>/p" /var/log/siconia/apache-karaf/m2m.log | tr "\n" " "' )
    print(out)
    final_out=''
    client.close()
    line=str(out)
    first_result = ast.literal_eval(line)

    new_file2=open("newfile3.txt",mode="w",encoding="utf-8")


    s= first_result[1]
    new_file2.write(first_result[1])
    # start = s.find("<devdisc")
    start = s.rfind("<devdisc")
    print("start: ",start)
    # end = s.find("</devdisc>")
    end = s.rfind("</devdisc>")
    print("end: ",end)
    substring = s[start:end]
    substring= '<?xml version="1.0" ?>\n'+ substring + '</devdisc>'
    print(substring)
    # new_file2=open("newfile3.txt",mode="w",encoding="utf-8")
    # new_file2.write(substring)
    root = etree.fromstring(substring)
    tree = etree.ElementTree(root)
    root= tree.getroot()
    print(root)
    df = pd.read_csv(currentpath2+'/patterns.csv', sep=';')
    print(df[df['message_type']== message_type])
    start_pattern= df[df['message_type']== message_type]['start_pattern']
    end_pattern= df[df['message_type']== message_type]['end_pattern']
    starts = re.finditer(start_pattern[0], s)
    ends = re.finditer(end_pattern[0], s)
    startslist=[]
    endslist=[]
    for m in starts:
        startslist.append(m.start())
    for n in ends:
        endslist.append(n.end())
    # for i in range(len(startslist)):
    #     print(s[startslist[i]:endslist[i]])

    for i in range(len(startslist)-1, -1, -1):
        print(s[startslist[i]:endslist[i]])
        xml_message=s[startslist[i]:endslist[i]]
        position = xml_message.rfind(device_id)
        if(position != -1):
            xml_message= '<?xml version="1.0" ?>\n'+ xml_message
            root = etree.fromstring(xml_message)
            tree = etree.ElementTree(root)
            root= tree.getroot()
            final_out=etree.tostring(tree, pretty_print=True)
            break

    return final_out
