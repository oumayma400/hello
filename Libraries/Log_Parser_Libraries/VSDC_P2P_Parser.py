import paramiko
import ast
import datetime
import time
import xml.etree.ElementTree as ET
import sys,os
from pathlib import Path
path = Path(os.path.abspath(__file__))
parrent_path = path.parent.absolute()

Read_ConfigLib = os.path.dirname(parrent_path) + os.path.sep + "Read_Config";
Read_ConfigLib2 = Read_ConfigLib.replace('\\', '/')
sys.path.append(Read_ConfigLib2)
import ReadConfigFile as conf


def run_cmd(sshClient, command):
    channel = sshClient.get_transport().open_session()
    channel.get_pty()
    channel.exec_command(command)
    out = channel.makefile().readlines()
    err = channel.makefile_stderr().read()
    returncode = channel.recv_exit_status()
    channel.close()                       # channel is closed, but not the client
    return out, err, returncode

def vsdc_push_on_connectivity(PROJECT, currentdate, meter_id, tm):
    push_found= False
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    host = conf.ReadConfigFile.read(PROJECT,'vsdc_ip')
    port = 22
    username=conf.ReadConfigFile.read(PROJECT,'vsdc_ip_user')
    password= conf.ReadConfigFile.read(PROJECT,'vsdc_ip_pass')

    timeout =0
    while push_found == False and timeout <= int(tm):
        timeout =timeout +1
        time.sleep(60)
        client.connect(host, port, username, password)
        out, err, rc = run_cmd(client, 'sed -n -e "/\(.*\)RESULT exection Push on connectivity:/,/taskRes>/p" /var/log/siconia/vsdc-p2p-fe/vsdc-p2p-fe.log | tr "\n" " "' )
        # print(out)
        client.close()
        line=str(out)
        first_result = ast.literal_eval(line)


        s= first_result[0]
        start = s.find("<taskRes")

        end = s.find("</taskRes>")

        substring = s[start:end]
        substring= '<?xml version="1.0" ?>\n'+ substring + '</taskRes>'
        # print(substring)
        new_file2=open("vsdcextractedlog.log",mode="w",encoding="utf-8")
        new_file2.write(s)

        f = open("C:/Users/g361355/Desktop/ROBOT_ECLIPSE/E2E-AUTO-SICONIA/Test_Suite/vsdcextractedlog.log", "r")
        n = sum(1 for line in open("C:/Users/g361355/Desktop/ROBOT_ECLIPSE/E2E-AUTO-SICONIA/Test_Suite/vsdcextractedlog.log"))
        print(n)
        i = 0
        while i < n:
            x = f.readline()
            i += 1
            # if "connection failed for device" in x:
            #     meter = [x[135:-2]]
            #     # print(meter)
            #     time = x[:19]
            #     # print(time)
            #     while "HAZELCAST : task TODO Task" not in x and i < n and "error accured when creating task" not in x:
            #         x = f.readline()
            #         i += 1
            #         if "connection failed for device" in x:
            #             meter.append(x[135:-2])
            #     # print(x)
            #     if "HAZELCAST : task TODO Task" in x:
            #         s = "execS"
            #         for i in range(0, len(x)):
            #             if s in x[0:i]:
            #                 break
            #         task = x[140:i - 7]
            #         execStart = x[i + 9:i + 28]
            #         # print(task)
            #         for m in range(0, len(meter)):
            #             if "COLLECT" in task:
            #                 writerCollect.writerow((time, meter[m], task, execStart, "", "", "failed", "Wakeup failed", ""))
            #             else:
            #                 if "ALARM" not in task:
            #                     writerUnitary.writerow(
            #                         (time, meter[m], task, execStart, "", "", "failed", "Wakeup failed", ""))
            #     else:
            #         for m in range(0, len(meter)):
            #             writerCollect.writerow((time, meter[m], "No task", "", "", "", "failed", "Wakeup failed", ""))
            response = ""
            # if 'RESULT exection Task DLMS: <?xml version="1.0" encoding="UTF-8" ?>' in x:
            #     time = x[:19]
            #     # print(time)
            #     x = f.readline()
            #     i += 1
            #     response = response + x
            #     while '</taskRes>' not in x and i < n:
            #         x = f.readline()
            #         i += 1
            #         response = response + x
            #     # print(response)
            #     if '</taskRes>' in x:
            #         response = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><root>" + response + "</root>"
            #         tree = ET.fromstring(response)
            #         reason = ""
            #         for taskNode in tree:
            #             taskId = taskNode.attrib["taskId"]
            #             execStart = taskNode.attrib["taskExec"]
            #             # print(taskId)
            #             meter = taskNode[0].attrib['id']
            #             retry = taskNode[0][0].attrib['retry']
            #             start = taskNode[0][0].attrib['start']
            #             stop = taskNode[0][0].attrib['stop']
            #             # print(meter)
            #             # print(len(taskNode[0]))
            #             # print(taskNode[0][7][0].attrib['reason'])
            #             status = 'done'
            #             for i in range(0, len(taskNode[0])):
            #                 # print(i)
            #                 # print(taskNode[0][i].attrib['status'])
            #                 if taskNode[0][i].attrib['status'] == "failed":
            #                     status = "failed"
            #                     if taskNode[0][i][0].attrib['status'] == "failed":
            #                         reason = taskNode[0][i][0].attrib['reason']
            #                     else:
            #                         reason = "Unknown"
            #                     # print(status)
            #                     # print(reason)
            #                     break
            #                 elif taskNode[0][i].attrib['status'] == "canceled":
            #                     status = "canceled"
            #                     reason = taskNode[0][i][0].attrib['reason']
            #                     # print(status)
            #                     # print(reason)
            #                     break
            #
            #         if "COLLECT" in taskId:
            #             if status == 'done':
            #                 value = taskNode[0][0][len(taskNode[0][0]) - 1].text
            #             else:
            #                 value = ''
            #             writerCollect.writerow((time, meter, taskId, execStart, start, stop, status, reason, retry, value))
            #         else:
            #             writerUnitary.writerow((time, meter, taskId, execStart, start, stop, status, reason, retry))
            #     else:
            #         print(" no completed task result")
            # if 'RESULT exection Task FIRMWARE: <?xml version="1.0" encoding="UTF-8" ?>' in x:
            #     time = x[:19]
            #     # print(time)
            #     x = f.readline()
            #     i += 1
            #     response = response + x
            #     while '</taskRes>' not in x and i < n:
            #         x = f.readline()
            #         i += 1
            #         response = response + x
            #     # print(response)
            #     if '</taskRes>' in x:
            #         response = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><root>" + response + "</root>"
            #         tree = ET.fromstring(response)
            #         reason = ""
            #         for taskNode in tree:
            #             taskId = taskNode.attrib["taskId"]
            #             meter = taskNode[0].attrib['id']
            #             execStart = execStart = taskNode.attrib["taskExec"]
            #             retry = taskNode[0][0].attrib['retry']
            #             start = taskNode[0][0].attrib['start']
            #             stop = taskNode[0][0].attrib['stop']
            #             status = 'done'
            #             for i in range(0, len(taskNode[0])):
            #                 # print(i)
            #                 # print(taskNode[0][i].attrib['status'])
            #                 if taskNode[0][0].attrib['status'] == "failed":
            #                     status = "failed"
            #                     reason = taskNode[0][0].attrib['reason']
            #                     # print(status)
            #                     # print(reason)
            #                     break
            #                 elif taskNode[0][0].attrib['status'] == "canceled":
            #                     status = "canceled"
            #                     reason = taskNode[0][0].attrib['reason']
            #                     # print(status)
            #                     # print(reason)
            #                     break
            #         if "COLLECT" in taskId:
            #             writerCollect.writerow((time, meter, taskId, execStart, start, stop, status, reason, retry))
            #         else:
            #             writerUnitary.writerow((time, meter, taskId, execStart, start, stop, status, reason, retry))
            #     else:
            #         print("we have a no completed task")
            if 'RESULT exection Push on connectivity: <?xml version="1.0" encoding="UTF-8" ?>' in x:
                if x[0]==" ":
                    receptiontime = x[1:20]
                else:
                    receptiontime = x[:19]
                # print(time)
                x = f.readline()
                i += 1
                response = response + x
                while '</taskRes>' not in x and i < n:
                    x = f.readline()
                    i += 1
                    response = response + x
                # print(response)
                if '</taskRes>' in x:
                    response = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><root>" + response + "</root>"
                    tree = ET.fromstring(response)
                    reason = ""
                    for taskNode in tree:
                        taskId = taskNode.attrib["taskId"]
                        meter = taskNode[0].attrib['id']
                        start = taskNode[0][0].attrib['start']
                        stop = taskNode[0][0].attrib['stop']
                        status = 'done'
                        a = len(taskNode[0][0])
                        value = taskNode[0][0][a - 1].text
                    # writerPushs.writerow((time, meter, taskId, start, stop, status, value))
                    print(receptiontime, meter, taskId, start, stop, status, value)
                    print(receptiontime > currentdate)
                    if receptiontime > currentdate and meter== meter_id:
                        print("push on connectivity for the meter "+ meter_id + " found in vsdc log")
                        print(receptiontime, meter, taskId, start, stop, status, value)
                        push_found = True
                        break
                else:
                    print("we have a no completed task")

        # root = etree.fromstring(substring)
        # tree = etree.ElementTree(root)
        # root= tree.getroot()
        # # print(root)
        #
        # return etree.tostring(tree, pretty_print=True)
        if push_found == True :
            break
    return  push_found

def vsdc_push_on_interval(PROJECT, currentdate, meter_id, tm):
    push_found= False
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    host = conf.ReadConfigFile.read(PROJECT,'vsdc_ip')
    port = 22
    username=conf.ReadConfigFile.read(PROJECT,'vsdc_ip_user')
    password= conf.ReadConfigFile.read(PROJECT,'vsdc_ip_pass')

    timeout =0
    while push_found == False and timeout < int(tm):
        timeout =timeout +1
        time.sleep(60)
        client.connect(host, port, username, password)
        out, err, rc = run_cmd(client, 'sed -n -e "/\(.*\)RESULT exection push interval:/,/taskRes>/p" /var/log/siconia/vsdc-p2p-fe/vsdc-p2p-fe.log | tr "\n" " "' )
        # print(out)
        client.close()
        line=str(out)
        first_result = ast.literal_eval(line)


        s= first_result[0]
        start = s.find("<taskRes")

        end = s.find("</taskRes>")

        substring = s[start:end]
        substring= '<?xml version="1.0" ?>\n'+ substring + '</taskRes>'
        # print(substring)
        new_file2=open("vsdcextractedlog.log",mode="w",encoding="utf-8")
        new_file2.write(s)

        f = open("C:/Users/g361355/Desktop/ROBOT_ECLIPSE/E2E-AUTO-SICONIA/Test_Suite/vsdcextractedlog.log", "r")
        n = sum(1 for line in open("C:/Users/g361355/Desktop/ROBOT_ECLIPSE/E2E-AUTO-SICONIA/Test_Suite/vsdcextractedlog.log"))
        print(n)
        i = 0
        while i < n:
            x = f.readline()
            i += 1
            response = ""
            if 'RESULT exection push interval: <?xml version="1.0" encoding="UTF-8" ?>' in x:
                receptiontime = x[:19]
                # print(time)
                x = f.readline()
                i += 1
                response = response + x
                while '</taskRes>' not in x and i < n:
                    x = f.readline()
                    i += 1
                    response = response + x
                # print(response)
                if '</taskRes>' in x:
                    response = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><root>" + response + "</root>"
                    tree = ET.fromstring(response)
                    reason = ""
                    for taskNode in tree:
                        taskId = taskNode.attrib["taskId"]
                        meter = taskNode[0].attrib['id']
                        start = taskNode[0][0].attrib['start']
                        stop = taskNode[0][0].attrib['stop']
                        status = 'done'
                        a = len(taskNode[0][0])
                        value = taskNode[0][0][a - 1].text
                    # writerPushs.writerow((time, meter, taskId, start, stop, status, value))
                    print(receptiontime, meter, taskId, start, stop, status, value)
                    print(receptiontime > currentdate)
                    if receptiontime > currentdate and meter== meter_id:
                        print("push on connectivity for the meter "+ meter_id + " found in vsdc log")
                        print(receptiontime, meter, taskId, start, stop, status, value)
                        push_found = True
                        break
                else:
                    print("we have a no completed task")
        if push_found == True :
            break
    return  push_found