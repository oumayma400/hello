import paramiko
import sys,os
from pathlib import Path
import pytz
import time
path = Path(os.path.abspath(__file__))
parrent_path = path.parent.absolute()
Read_ConfigLib = os.path.dirname(parrent_path) + os.path.sep + "Read_Config";
Read_ConfigLib2 = Read_ConfigLib.replace('\\', '/')
sys.path.append(Read_ConfigLib2)

import ReadConfigFile as conf
from lxml import etree
import lxml
import ReadConfigFile as conf
def remove_file_from_shared_folder(PROJECT, ssf_path,file_name):
	try:
		host = conf.ReadConfigFile.read(PROJECT,'odm_ip')
		#host = '172.30.13.172'
		username = conf.ReadConfigFile.read(PROJECT, 'odm_ip_user')
		password = conf.ReadConfigFile.read(PROJECT, 'odm_ip_pass')
		port = 22
		absolut_file_path = ssf_path + file_name
		command = "rm -rf "+absolut_file_path
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(host, port, username, password)
		# stdin1, stdout1, stderr1 =ssh.exec_command(command1)
		stdin, stdout, stderr = ssh.exec_command(command)
		lines = stdout.readlines()
		print(lines)
		return 200
	except Exception as e:
		return 500

def get_collect_files_by_meterid(PROJECT, collect_path,meter_id):
	try:
		host = conf.ReadConfigFile.read(PROJECT,'cim_ip')
		#host = '172.30.13.172'
		username = conf.ReadConfigFile.read(PROJECT, 'cim_ip_user')
		password = conf.ReadConfigFile.read(PROJECT, 'cim_ip_pass')
		port = 22
		absolut_file_path = collect_path
		command = "grep -l -r "+meter_id +" "+absolut_file_path
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(host, port, username, password)
		# stdin1, stdout1, stderr1 =ssh.exec_command(command1)
		stdin, stdout, stderr = ssh.exec_command(command)
		lines = stdout.readlines()
		print("result fo grep command")
		print(lines)
		ssh.close()
		return 200,lines
	except Exception as e:
		return 500, []

def remove_file_from_cim_with_complet_path(PROJECT, file_path):
	try:
		host = conf.ReadConfigFile.read(PROJECT,'cim_ip')
		#host = '172.30.13.172'
		username = conf.ReadConfigFile.read(PROJECT, 'cim_ip_user')
		password = conf.ReadConfigFile.read(PROJECT, 'cim_ip_pass')
		port = 22

		command = "rm -rf "+file_path.split("\n")[0]
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(host, port, username, password)
		# stdin1, stdout1, stderr1 =ssh.exec_command(command1)
		stdin, stdout, stderr = ssh.exec_command(command)
		lines = stdout.readlines()
		print(lines)

		ssh.close()
		return 200
	except Exception as e:
		return 500
def remove_file_from_m2m_with_complet_path(PROJECT, file_path):
	try:
		host = conf.ReadConfigFile.read(PROJECT,'m2m_ip')
		#host = '172.30.13.172'
		username = conf.ReadConfigFile.read(PROJECT, 'm2m_ip_user')
		password = conf.ReadConfigFile.read(PROJECT, 'm2m_ip_pass')
		port = 22

		command = "rm -rf "+file_path
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(host, port, username, password)
		# stdin1, stdout1, stderr1 =ssh.exec_command(command1)
		stdin, stdout, stderr = ssh.exec_command(command)
		lines = stdout.readlines()
		print(lines)
		ssh.close()
		return 200
	except Exception as e:
		return 500
def download_file(PROJECT, local_path ,remote_path):

	host = conf.ReadConfigFile.read(PROJECT,'cim_ip')
	#host = '172.30.13.172'
	username = conf.ReadConfigFile.read(PROJECT, 'cim_ip_user')
	password = conf.ReadConfigFile.read(PROJECT, 'cim_ip_pass')
	port = 22


	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(host,port,  username, password)
	# stdin1, stdout1, stderr1 =ssh.exec_command(command1)
	# localpath =local_path+"\\test.xml"
	print("localpath", local_path)
	remote_path=remote_path.split("\n")[0]
	print('"'+ remote_path+'"')
	sftp = ssh.open_sftp()

	sftp.get(remote_path, local_path)
	print("remote_path", remote_path)
	sftp.close()
	ssh.close()
	return True

def validate_collect(collect_file, xsd_file):
	xml_file = lxml.etree.parse(collect_file)
	xml_validator = lxml.etree.XMLSchema(file=xsd_file)
	is_valid = xml_validator.validate(xml_file)
	print(is_valid)
	return is_valid
