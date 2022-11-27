import pandas as pd
import json
from xml.etree import ElementTree
from lxml import etree
import datetime
import random
from robot.api import logger
import xml.etree.ElementTree as ET
import axdrDecode
import axdrTypes

import paramiko
import os
import ast
import re
from lxml import etree

import sys,os
from pathlib import Path
path = Path(os.path.abspath(__file__))
parrent_path = path.parent.absolute()

Read_ConfigLib = os.path.dirname(parrent_path) + os.path.sep + "Read_Config";
Read_ConfigLib2 = Read_ConfigLib.replace('\\', '/')
sys.path.append(Read_ConfigLib2)
import ReadConfigFile as conf

path = Path(os.path.abspath(__file__))
parrent_path = path.parent.absolute()
parrent_path = parrent_path.parent.absolute()
ODR_Reading = os.path.dirname(parrent_path) + os.path.sep + "Resources\\ODR_Reading";
ODR_Reading2 = ODR_Reading.replace('\\', '/')
sys.path.append(ODR_Reading2)

mon_dictionnaire = {}
mon_dictionnaire['1;0;32;24;0;255']='P15MIN_1-0:32.24.0.255'
mon_dictionnaire['1;0;52;24;0;255']='P15MIN_1-0:52.24.0.255'
mon_dictionnaire['1;0;72;24;0;255']='P15MIN_1-0:72.24.0.255'
mon_dictionnaire['1;0;31;24;0;255']='P15MIN_1-0:31.24.0.255'
mon_dictionnaire['1;0;51;24;0;255']='P15MIN_1-0:51.24.0.255'
mon_dictionnaire['1;0;71;24;0;255']='P15MIN_1-0:71.24.0.255'
mon_dictionnaire['1;0;3;4;0;255']='P15MIN_1-0:3.4.0.255'
mon_dictionnaire['1;0;4;4;0;255']='P15MIN_1-0:4.4.0.255'





decoder = axdrDecode.axdrDecode()
def DateTime2Date(hexString):
	year='{:04d}'.format(int(hexString[4:8],16))
	month='{:02d}'.format(int(hexString[8:10],16))
	day='{:02d}'.format(int(hexString[10:12],16))
	hour='{:02d}'.format(int(hexString[14:16],16))
	minute='{:02d}'.format(int(hexString[16:18],16))
	second='{:02d}'.format(int(hexString[18:20],16))
	return year+"-"+month+"-"+day+"T"+hour+":"+minute+":"+second




def conv_flag(flag):
    flag=int('0x'+flag,16)
    flags=''
    L=[]
    bits=0
    if len(bin(flag))==6:
        if bin(flag)[2]=='1':L.append('DST');bits=bits+2**23
        if bin(flag)[3]=='1':L.append('DATA_INVALID');bits=bits+2**30
        if bin(flag)[4]=='1':L.append('CLOCK_INVALID');bits=bits+2**20
        if bin(flag)[5]=='1':L.append('CRITICAL_ERROR');bits=bits+2**22
    elif len(bin(flag))==10:
        if bin(flag)[2]=='1':L.append('POWER_OFF');bits=bits+2**7
        if bin(flag)[4]=='1':L.append('TIME_CHANGE');bits=bits+2**13
        if bin(flag)[6]=='1':L.append('DST');bits=bits+2**23
        if bin(flag)[7]=='1':L.append('DATA_INVALID');bits=bits+2**30
        if bin(flag)[8]=='1':L.append('CLOCK_INVALID');bits=bits+2**20
        if bin(flag)[9]=='1':L.append('CRITICAL_ERROR');bits=bits+2**22
    elif len(bin(flag))==8:
        if bin(flag)[2]=='1':L.append('TIME_CHANGE');bits=bits+2**13
        if bin(flag)[4]=='1':L.append('DST');bits=bits+2**23
        if bin(flag)[5]=='1':L.append('DATA_INVALID');bits=bits+2**30
        if bin(flag)[6]=='1':L.append('CLOCK_INVALID');bits=bits+2**20
        if bin(flag)[7]=='1':L.append('CRITICAL_ERROR');bits=bits+2**22
    else:flags=''
    flags=str(bits) + ' : ' + ','.join(L)
    return flags

def lp1(xdr):
    # tab = ['timestamp','flag','P15MIN_1-0:1.8.0.255','P15MIN_1-0:2.8.0.255']
	tab = ['timestamp','flag','P15MIN_1-0:1.8.0.255','P15MIN_1-0:2.8.0.255','P15MIN_1-0:3.8.0.255','P15MIN_1-0:4.8.0.255','P15MIN_1-0:1.8.1.255','P15MIN_1-0:1.8.2.255']
	df = pd.DataFrame(columns= tab)

	axdr = decoder.decode(xdr)
	print("decoded xdr")
	print(axdr)

	if axdr is not None:
		for entry in axdr.getValue():
			timestamp=DateTime2Date(entry.getValue()[0].getAxdr())
			flag=int('0x'+entry.getValue()[1].getAxdr()[2::],16)
			Active_energy_import=int('0x'+entry.getValue()[2].getAxdr()[2::],16)
			Active_energy_export=int('0x'+entry.getValue()[3].getAxdr()[2::],16)
			Active_energy_import_rate1=int('0x'+entry.getValue()[4].getAxdr()[2::],16)
			Active_energy_import_rate2=int('0x'+entry.getValue()[5].getAxdr()[2::],16)
			Active_energy_export_rate1=int('0x'+entry.getValue()[6].getAxdr()[2::],16)
			Active_energy_export_rate2=int('0x'+entry.getValue()[7].getAxdr()[2::],16)

			# d2= {'timestamp':timestamp,'flag' : flag,'P15MIN_1-0:1.8.0.255' :str(Active_energy_import) , 'P15MIN_1-0:2.8.0.255': str(Active_energy_export)}
			d2= {'timestamp':timestamp,'flag' : flag,'P15MIN_1-0:1.8.0.255':str(Active_energy_import),'P15MIN_1-0:2.8.0.255':str(Active_energy_export),'P15MIN_1-0:3.8.0.255':str(Active_energy_import_rate1),'P15MIN_1-0:4.8.0.255':str(Active_energy_import_rate2),'P15MIN_1-0:1.8.1.255':str(Active_energy_export_rate1),'P15MIN_1-0:1.8.2.255':str(Active_energy_export_rate2)}

			df = df.append(d2, ignore_index=True)
	return df

def lp2(xdr):
	tab = ['timestamp','flag','P15MIN_1-0:1.8.0.255','P60MIN_1-0:2.8.0.255','P60MIN_1-0:3.8.0.255','P60MIN_1-0:4.8.0.255','P60MIN_1-0:1.8.1.255','P60MIN_1-0:1.8.2.255']
	df = pd.DataFrame(columns= tab)
	axdr = decoder.decode(xdr)
	if axdr is not None:
		for entry in axdr.getValue():
			timestamp=DateTime2Date(entry.getValue()[0].getAxdr())
			flag=conv_flag(entry.getValue()[1].getAxdr()[2::])
			# print(entry.getValue()[1].getAxdr()[2::])
			print(flag)
			Active_energy_import=int('0x'+entry.getValue()[2].getAxdr()[2::],16)
			Active_energy_export=int('0x'+entry.getValue()[3].getAxdr()[2::],16)
			Active_energy_import_rate1=int('0x'+entry.getValue()[4].getAxdr()[2::],16)
			Active_energy_import_rate2=int('0x'+entry.getValue()[5].getAxdr()[2::],16)
			Active_energy_export_rate1=int('0x'+entry.getValue()[6].getAxdr()[2::],16)
			Active_energy_export_rate2=int('0x'+entry.getValue()[7].getAxdr()[2::],16)
			d2= {'timestamp':timestamp,'flag' : flag,'P60MIN_1-0:1.8.0.255':str(Active_energy_import),'P60MIN_1-0:2.8.0.255':str(Active_energy_export),'P60MIN_1-0:3.8.0.255':str(Active_energy_import_rate1),'P60MIN_1-0:4.8.0.255':str(Active_energy_import_rate2),'P60MIN_1-0:1.8.1.255':str(Active_energy_export_rate1),'P60MIN_1-0:1.8.2.255':str(Active_energy_export_rate2)}
			df = df.append(d2, ignore_index=True)
	print(df)
	return df

def run_cmd(sshClient, command):
    channel = sshClient.get_transport().open_session()
    channel.get_pty()
    channel.exec_command(command)
    out = channel.makefile().readlines()
    err = channel.makefile_stderr().read()
    returncode = channel.recv_exit_status()
    channel.close()                       # channel is closed, but not the client
    return out, err, returncode

def get_xdr_from_m2m_log(PROJECT, task_id):
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	host = conf.ReadConfigFile.read(PROJECT,'m2m_ip')
	port = 22
	username=conf.ReadConfigFile.read(PROJECT,'m2m_ip_user')
	password= conf.ReadConfigFile.read(PROJECT,'m2m_ip_pass')
	client.connect(host, port, username, password)

	print("befor grep command")
	if PROJECT=='ELLEVIO':
		print("grep command ellevio")
		out, err, rc = run_cmd(client, 'sed -n -e "/\(.*\)taskRes xmlns=\(.*\)'+task_id+'/,/taskRes>/p" /var/karaf/data/log/m2m.log | tr "\n" " "' )
	else:
		out, err, rc = run_cmd(client, 'sed -n -e "/\(.*\)taskRes xmlns=\(.*\)'+task_id+'/,/taskRes>/p" /var/log/siconia/apache-karaf/m2m.log | tr "\n" " "' )
	print("after grep command")
	client.close()
	line=str(out)
	first_result = ast.literal_eval(line)


	s= first_result[0]
	start = s.find("<taskRes")

	end = s.find("</taskRes>")

	substring = s[start:end]
	substring= '<?xml version="1.0" ?>\n'+ substring + '</taskRes>'
	print(substring)
	new_file2=open("newfile3.txt",mode="w",encoding="utf-8")
	new_file2.write(substring)
	root = etree.fromstring(substring)
	tree = etree.ElementTree(root)
	root= tree.getroot()
	print(root)
	xdr=''
	scaler={}
	for i in range(len(root[0])):
		print(root[0][i])
		transaction = root[0][i]
		if transaction[0].get('obis')=='1;0;99;14;0;255':
			print(transaction[0].text)
			xdr=transaction[0].text
		else:
			scaler[mon_dictionnaire[transaction[0].get('obis')]]=transaction[0].text

	return xdr, scaler

def get_xdr_without_scaler_from_m2m_log(PROJECT, task_id):
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	host = conf.ReadConfigFile.read(PROJECT,'m2m_ip')
	port = 22
	username=conf.ReadConfigFile.read(PROJECT,'m2m_ip_user')
	password= conf.ReadConfigFile.read(PROJECT,'m2m_ip_pass')
	client.connect(host, port, username, password)

	print("befor grep command")
	if PROJECT=='ELLEVIO':
		print("grep command ellevio")
		out, err, rc = run_cmd(client, 'sed -n -e "/\(.*\)taskRes xmlns=\(.*\)'+task_id+'/,/taskRes>/p" /var/karaf/data/log/m2m.log | tr "\n" " "' )
	else:
		out, err, rc = run_cmd(client, 'sed -n -e "/\(.*\)taskRes xmlns=\(.*\)'+task_id+'/,/taskRes>/p" /var/log/siconia/apache-karaf/m2m.log | tr "\n" " "' )
	print("after grep command")
	client.close()
	line=str(out)
	first_result = ast.literal_eval(line)


	s= first_result[0]
	start = s.find("<taskRes")

	end = s.find("</taskRes>")

	substring = s[start:end]
	substring= '<?xml version="1.0" ?>\n'+ substring + '</taskRes>'
	print(substring)
	new_file2=open("newfile3.txt",mode="w",encoding="utf-8")
	new_file2.write(substring)
	root = etree.fromstring(substring)
	tree = etree.ElementTree(root)
	root= tree.getroot()
	print(root)
	xdr=[]
	for i in range(len(root[0])):
		print(root[0][i])
		transaction = root[0][i]
		print(transaction[0].text)
		for k in range( len(transaction)):
			if len(transaction[k].text)> 4:
				xdr.append(transaction[k].text)
	return xdr

def pq(PROJECT,xdr, meter_type):
    # tmp = open(str(time.time())[:10]+'.csv', 'a')
	if meter_type =='ELEC_MONO':
		df = pd.read_csv(ODR_Reading2+'/'+PROJECT+'/'+'PQ_OBIS_ORDER_MONO.csv', sep=';')
		print(len(df))
		print(df.iloc[0]['obis'])
		print(df.iloc[0]['order'])
		tab = ['timestamp','flag']
		for i in range(len(df)):
			tab.append(str(df.iloc[i]['obis']))
		df_out = pd.DataFrame(columns= tab)
		# tmp = open(str(meter)+'.csv', 'a')
		# tmp.write("meter;timestamp;P15MIN_1-0:32.24.0.255;P15MIN_1-0:31.24.0.255;code\n")
		# print("meter;timestamp;code")
		axdr = decoder.decode(xdr)
		if axdr is not None:
			for entry in axdr.getValue():
				# print("entry.getValue()")
				# print(entry.getValue())
				values=[]
				# values.append(meter)
				timestamp=DateTime2Date(entry.getValue()[0].getAxdr())
				# values.append(timestamp)
				flag='0x'+entry.getValue()[1].getAxdr()[2::]
				flag=int(flag,16)
				# values.append(str(code))
				d2= {'timestamp':str(timestamp),'flag' : flag}
				for k in range(len(df)):
					print(entry.getValue()[df.iloc[k]['order']].getAxdr()[2::])
					# if(entry.getValue()[df.iloc[k]['order']].getAxdr()[2::]=='00000000'):
					# 	print("helooooooooo")
					# 	d2[str(df.iloc[k]['obis'])] ='0'
					# else:
					pq_value='0x'+entry.getValue()[df.iloc[k]['order']].getAxdr()[2::]
					pq_value=int(pq_value,df.iloc[k]['size'])
					d2[str(df.iloc[k]['obis'])] =pq_value

				df_out = df_out.append(d2, ignore_index=True)

	elif meter_type =='ELEC_TRI':
		df = pd.read_csv(ODR_Reading2+'/'+PROJECT+'/'+'PQ_OBIS_ORDER_TRI.csv', sep=';')
		print(len(df))
		print(df.iloc[0]['obis'])
		print(df.iloc[0]['order'])
		tab = ['timestamp','flag']
		for i in range(len(df)):
			tab.append(str(df.iloc[i]['obis']))
		df_out = pd.DataFrame(columns= tab)
		# tmp = open(str(meter)+'.csv', 'a')
		# tmp.write("meter;timestamp;P15MIN_1-0:32.24.0.255;P15MIN_1-0:31.24.0.255;code\n")
		# print("meter;timestamp;code")
		axdr = decoder.decode(xdr)
		if axdr is not None:
			for entry in axdr.getValue():
				# print("entry.getValue()")
				# print(entry.getValue())
				values=[]
				# values.append(meter)
				timestamp=DateTime2Date(entry.getValue()[0].getAxdr())
				# values.append(timestamp)
				flag='0x'+entry.getValue()[1].getAxdr()[2::]
				flag=int(flag,16)
				# values.append(str(code))
				d2= {'timestamp':str(timestamp),'flag' : flag}
				for k in range(len(df)):
					print(entry.getValue()[df.iloc[k]['order']].getAxdr()[2::])
					# if(entry.getValue()[df.iloc[k]['order']].getAxdr()[2::]=='00000000'):
					# 	print("helooooooooo")
					# 	d2[str(df.iloc[k]['obis'])] ='0'
					# else:
					pq_value='0x'+entry.getValue()[df.iloc[k]['order']].getAxdr()[2::]
					pq_value=int(pq_value,df.iloc[k]['size'])
					d2[str(df.iloc[k]['obis'])] =pq_value

				df_out = df_out.append(d2, ignore_index=True)
	df_out.to_csv(r'./parsing.csv', index = False, header=True)
	return df_out

def event(PROJECT, xdr):
	tab = ['timestamp','name']
	df_out = pd.DataFrame(columns= tab)
	axdr = decoder.decode(xdr)
	json_file=open(ODR_Reading2+'/'+PROJECT+'/'+'event.txt','r')
	ev = json.load(json_file)
	if axdr is not None:
		for entry in axdr.getValue():
			print("entry.getValue()")
			print(entry.getValue())
			timestamp=DateTime2Date(entry.getValue()[0].getAxdr())
			code='0x'+entry.getValue()[1].getAxdr()[2::]
			code=int(code,16)
			d2= {'timestamp':str(timestamp),'name' : ev[str(code)]}
			df_out = df_out.append(d2, ignore_index=True)
	df_out.to_csv(r'./parsing_events.csv', index = False, header=True)
	return df_out


# def validate_cim_output(PROJECT, task_id):
# 	# task_id= 'JOB_ODR_1637758534550_I491607'
# 	xdr, scaler = get_xdr_from_m2m_log(PROJECT, task_id)
# 	print("scaler *********************", scaler)
# 	df = lp1(xdr)
# 	# df = pq(xdr,'ELEC_MONO')
#
#     # print(df[['timestamp', 'Active_energy_import']])
# 	imp = df[['timestamp','P15MIN_1-0:1.8.0.255', 'P15MIN_1-0:2.8.0.255']]
# 	print(imp.iloc[[2]]['timestamp'].values[0])
# 	print(imp[imp['timestamp']=='2021-11-21T02:45:00'])
# 	tree = ET.parse('C:/Users/g361355/Desktop/test_python/reads_20211122144252_ID-cim-adapter-tucana-urd3-local-1636641000709-2-295533.xml')
# 	root = tree.getroot()
# 	i=0
# 	x=len(root[1][0])-1
# 	mon_dictionnaire = {}
# 	mon_dictionnaire['CityName']='city_name'
# 	validation= True
# 	for payload in root[1].findall('*'):
#
# 		meter_id= payload.findall('{http://www.emeter.com/energyip/amiinterface}Meter')
# 		meter_id=meter_id[0][0].text
# 		print(meter_id)
# 		for MeterReading in payload.findall('{http://www.emeter.com/energyip/amiinterface}IntervalBlock'):
# 			print(MeterReading)
# 			IntervalBlock = MeterReading.findall("{http://www.emeter.com/energyip/amiinterface}IReading")
# 			readingTypeId= MeterReading.findall('*')
# 			readingTypeId=readingTypeId[0].text
# 			print("readingTypeId", readingTypeId)
# 			# for k in range( len(IntervalBlock)):
# 			for IReading in IntervalBlock:
#                 # print(IReading)
# 				endtime= IReading.findall("{http://www.emeter.com/energyip/amiinterface}endTime")
# 				endtime=endtime[0].text
# 				value= IReading.findall("{http://www.emeter.com/energyip/amiinterface}value")
# 				value=value[0].text
# 				print('hello')
# 				print(imp[imp['timestamp']==endtime[0:19]])
# 				out= imp[imp['timestamp']==endtime[0:19]][readingTypeId].values[0]
# 				print("out", out)
# 				print(int(out)*0.001)
# 				print(imp[imp['timestamp']==endtime[0:19]][readingTypeId].values[0])
# 				print(value)
# 				if (imp[imp['timestamp']==endtime[0:19]][readingTypeId].values[0] != out):
# 					validation = False
# 					break
# 				flags= IReading.findall("{http://www.emeter.com/energyip/amiinterface}flags")
# 				flags=flags[0].text
#
# 			if validation == False:
# 				break
# 			i+=1
# 			if i==x:
# 				i=0
# 				break
#
# 	print(validation)
# 	return validation

def scalerunit(xdr):
    axdr = decoder.decode(xdr)
    print(axdr.getValue()[0].getValue())
    return axdr.getValue()[0].getValue()


def validate_cim_odr_output(PROJECT, task_id, meter_type, profilename, xml):
	# task_id= 'JOB_ODR_1637837735026_I491705'

	# xdr= get_xdr_from_m2m_log(task_id)
	xdr, scaler = get_xdr_from_m2m_log(PROJECT, task_id)
	print("scaler*****************--", scaler)
	# df = lp1(xdr)
	df = pq(PROJECT, xdr,'ELEC_'+meter_type)
	print("m2m df after parsing")
	print(df)
    # print(df[['timestamp', 'Active_energy_import']])
	# print(ODR_Reading2+'/'+PROJECT+'/'+ODR_TRI+'.csv')
	df_pq_obis = pd.read_csv(ODR_Reading2+'/'+PROJECT+'/'+'ODR_'+meter_type+'.csv', sep=';')
	obistab= df_pq_obis[df_pq_obis['profile']==profilename]['obis']
	print("obistab",obistab)
	res= obistab.values
	res= res[0].split(',')
	print("res+++++++++++++")
	print(res)
	list= ['timestamp']
	for j in range(len(res)):
		list.append(res[j])
	imp = df[list]
	print(imp)
	print(imp.iloc[[2]]['timestamp'].values[0])
	print(imp[imp['timestamp']=='2021-11-21T02:45:00'])
	root = etree.fromstring(xml)
	tree = etree.ElementTree(root)
	root= tree.getroot()

	# tree = ET.parse(message)
	# root = tree.getroot()
	i=0
	x=len(root[1][0])-1
	validation= True
	for payload in root[1].findall('*'):

		meter_id= payload.findall('{http://www.emeter.com/energyip/amiinterface}Meter')
		meter_id=meter_id[0][0].text
		print(meter_id)
		for MeterReading in payload.findall('{http://www.emeter.com/energyip/amiinterface}IntervalBlock'):
			print(MeterReading)
			IntervalBlock = MeterReading.findall("{http://www.emeter.com/energyip/amiinterface}IReading")
			readingTypeId= MeterReading.findall('*')
			readingTypeId=readingTypeId[0].text
			print("readingTypeId", readingTypeId)
			# for k in range( len(IntervalBlock)):
			for IReading in IntervalBlock:
                # print(IReading)
				endtime= IReading.findall("{http://www.emeter.com/energyip/amiinterface}endTime")
				endtime=endtime[0].text
				value= IReading.findall("{http://www.emeter.com/energyip/amiinterface}value")
				value=value[0].text
				print('hello')
				# print(imp[imp['timestamp']==endtime[0:19]])
				out= imp[imp['timestamp']==endtime[0:19]][readingTypeId].values[0]
				# print("out", out)
				# print(int(out)*0.1)
				# print(imp[imp['timestamp']==endtime[0:19]][readingTypeId].values[0])
				output_cim= float(value)
				if readingTypeId in ['P15MIN_1-0:32.24.0.255', 'P15MIN_1-0:52.24.0.255','P15MIN_1-0:72.24.0.255']:
					output_m2m= float(out)*(10**scalerunit(scaler['P15MIN_1-0:32.24.0.255']))
				elif readingTypeId in ['P15MIN_1-0:31.24.0.255', 'P15MIN_1-0:51.24.0.255','P15MIN_1-0:71.24.0.255']:
					output_m2m= float(out)*(10**scalerunit(scaler['P15MIN_1-0:31.24.0.255']))
				else:
					output_m2m= float(out)*(0.001)

				print("output cim :",output_cim)
				print("output m2m :",round(output_m2m, 3) )
				if output_cim != round(output_m2m, 2) :
					validation = False
					break
				flags= IReading.findall("{http://www.emeter.com/energyip/amiinterface}flags")
				flags=flags[0].text

			if validation == False:
				break
			i+=1
			if i==x:
				i=0
				break
		if validation == False:
			break

	print(validation)
	return validation


def validate_cim_odr_event_output(PROJECT, task_id, profilename, xml):
	validation = True
	xdr = get_xdr_without_scaler_from_m2m_log(PROJECT, task_id)
	tab = ['timestamp','name']
	df_out_cim = pd.DataFrame(columns= tab)

	root = etree.fromstring(xml)
	tree = etree.ElementTree(root)
	root= tree.getroot()
	i=0
	x=len(root[1][0])-1
	validation= True
	for payload in root[1].findall('*'):

		meter_id= payload.findall('{http://www.emeter.com/energyip/amiinterface}Meter')
		meter_id=meter_id[0][0].text
		print(meter_id)
		for event_tag in payload.findall('{http://www.emeter.com/energyip/amiinterface}Event'):
			# print(event)
			endtime= event_tag.findall("{http://www.emeter.com/energyip/amiinterface}timestamp")
			endtime=str(endtime[0].text)
			name= event_tag.findall("{http://www.emeter.com/energyip/amiinterface}name")
			name=name[0].text
			# print("endtime :", endtime ,"name :", name)
			# out= imp[imp['timestamp']==endtime[0:19]][readingTypeId].values[0]
			d2= {'timestamp':endtime[0:19],'name' : name}
			df_out_cim = df_out_cim.append(d2, ignore_index=True)
	print("cim_event_value")
	print(df_out_cim)
	for i in range(len(xdr)):
		out= event(PROJECT, xdr[i])
		print("m2m xdr : ", xdr[i])
		print("formated xdr " , out)
		# validation = out in df_out_cim
		validation = (out == df_out_cim).all(1).any()
		if validation == False:
			print(xdr[i] , "is not correctly mapped in cim" )
			break
		# for k in range(len(out)):
		# 	print("hellooooooooooo11111111111")
		# 	print("helloooooooooooe" , out["timestamp"][k])
		# 	cim_event_value = df_out_cim[df_out_cim['timestamp']== out['timestamp'][k]]['name']
		# 	print("cim_event_value : ", cim_event_value[0])
		# 	print("m2m_event_value : " , out['name'][k])
		# 	if(str(cim_event_value[0]) != str(out['name'][k])):
		# 		validation = False
		# 		break
		# if validation == False:
		# 	print(xdr[i] , "is not correctly mapped in cim" )
		# 	break

	return validation

def validate_cim_odr_LP2_output(PROJECT, task_id, meter_type, profilename, xml):
	# task_id= 'JOB_ODR_1637837735026_I491705'

	# xdr= get_xdr_from_m2m_log(task_id)
	xdr = get_xdr_without_scaler_from_m2m_log(PROJECT, task_id)
	print(" m2m xdr :")
	print(xdr)

	df = lp2(xdr[0])
	# df = lp1(PROJECT, xdr,'ELEC_'+meter_type)
	print("m2m df after parsing")
	print(df)
    # print(df[['timestamp', 'Active_energy_import']])
	# print(ODR_Reading2+'/'+PROJECT+'/'+ODR_TRI+'.csv')
	df_pq_obis = pd.read_csv(ODR_Reading2+'/'+PROJECT+'/'+'ODR_'+meter_type+'.csv', sep=';')
	obistab= df_pq_obis[df_pq_obis['profile']==profilename]['obis']
	print("obistab",obistab)
	res= obistab.values
	res= res[0].split(',')
	print("res+++++++++++++")
	print(res)
	list= ['timestamp']
	for j in range(len(res)):
		list.append(res[j])
	imp = df[list]
	print(imp)
	print(imp.iloc[[2]]['timestamp'].values[0])
	print(imp[imp['timestamp']=='2021-11-21T02:45:00'])
	root = etree.fromstring(xml)
	tree = etree.ElementTree(root)
	root= tree.getroot()

	# tree = ET.parse(message)
	# root = tree.getroot()
	i=0
	x=len(root[1][0])-1
	validation= True
	for payload in root[1].findall('*'):

		meter_id= payload.findall('{http://www.emeter.com/energyip/amiinterface}Meter')
		meter_id=meter_id[0][0].text
		print(meter_id)
		for MeterReading in payload.findall('{http://www.emeter.com/energyip/amiinterface}IntervalBlock'):
			print(MeterReading)
			IntervalBlock = MeterReading.findall("{http://www.emeter.com/energyip/amiinterface}IReading")
			readingTypeId= MeterReading.findall('*')
			readingTypeId=readingTypeId[0].text
			print("readingTypeId", readingTypeId)
			# for k in range( len(IntervalBlock)):
			for IReading in IntervalBlock:
                # print(IReading)
				endtime= IReading.findall("{http://www.emeter.com/energyip/amiinterface}endTime")
				endtime=endtime[0].text
				value= IReading.findall("{http://www.emeter.com/energyip/amiinterface}value")
				value=value[0].text
				print('hello')
				# print(imp[imp['timestamp']==endtime[0:19]])
				out= imp[imp['timestamp']==endtime[0:19]][readingTypeId].values[0]
				# print("out", out)
				# print(int(out)*0.1)
				# print(imp[imp['timestamp']==endtime[0:19]][readingTypeId].values[0])
				output_cim= float(value)
				output_m2m= float(out)*(0.001)

				print("output cim :",output_cim)
				print("output m2m :",round(output_m2m, 3) )
				if output_cim != round(output_m2m, 3) :
					validation = False
					break
				flags= IReading.findall("{http://www.emeter.com/energyip/amiinterface}flags")
				flags=flags[0].text

			if validation == False:
				break
			i+=1
			if i==x:
				i=0
				break
		if validation == False:
			break

	print(validation)
	return validation

def validate_cim_odr_LP1_output(PROJECT, task_id, meter_type, profilename, xml):
	# task_id= 'JOB_ODR_1637837735026_I491705'

	# xdr= get_xdr_from_m2m_log(task_id)
	xdr = get_xdr_without_scaler_from_m2m_log(PROJECT, task_id)
	print(" m2m xdr :")
	print(xdr)

	df = lp1(xdr[0])
	# df = lp1(PROJECT, xdr,'ELEC_'+meter_type)
	print("m2m df after parsing")
	print(df)
    # print(df[['timestamp', 'Active_energy_import']])
	# print(ODR_Reading2+'/'+PROJECT+'/'+ODR_TRI+'.csv')
	df_pq_obis = pd.read_csv(ODR_Reading2+'/'+PROJECT+'/'+'ODR_'+meter_type+'.csv', sep=';')
	obistab= df_pq_obis[df_pq_obis['profile']==profilename]['obis']
	print("obistab",obistab)
	res= obistab.values
	res= res[0].split(',')
	print("res+++++++++++++")
	print(res)
	list= ['timestamp']
	for j in range(len(res)):
		list.append(res[j])
	imp = df[list]
	print(imp)
	print(imp.iloc[[2]]['timestamp'].values[0])
	print(imp[imp['timestamp']=='2021-11-21T02:45:00'])
	root = etree.fromstring(xml)
	tree = etree.ElementTree(root)
	root= tree.getroot()

	# tree = ET.parse(message)
	# root = tree.getroot()
	i=0
	x=len(root[1][0])-1
	validation= True
	for payload in root[1].findall('*'):

		meter_id= payload.findall('{http://www.emeter.com/energyip/amiinterface}Meter')
		meter_id=meter_id[0][0].text
		print(meter_id)
		for MeterReading in payload.findall('{http://www.emeter.com/energyip/amiinterface}IntervalBlock'):
			print(MeterReading)
			IntervalBlock = MeterReading.findall("{http://www.emeter.com/energyip/amiinterface}IReading")
			readingTypeId= MeterReading.findall('*')
			readingTypeId=readingTypeId[0].text
			print("readingTypeId", readingTypeId)
			# for k in range( len(IntervalBlock)):
			for IReading in IntervalBlock:
                # print(IReading)
				endtime= IReading.findall("{http://www.emeter.com/energyip/amiinterface}endTime")
				endtime=endtime[0].text
				value= IReading.findall("{http://www.emeter.com/energyip/amiinterface}value")
				value=value[0].text
				print('hello')
				# print(imp[imp['timestamp']==endtime[0:19]])
				out= imp[imp['timestamp']==endtime[0:19]][readingTypeId].values[0]
				# print("out", out)
				# print(int(out)*0.1)
				# print(imp[imp['timestamp']==endtime[0:19]][readingTypeId].values[0])
				output_cim= float(value)
				output_m2m= float(out)*(0.001)

				print("output cim :",output_cim)
				print("output m2m :",round(output_m2m, 3) )
				if output_cim != round(output_m2m, 3) :
					validation = False
					break
				flags= IReading.findall("{http://www.emeter.com/energyip/amiinterface}flags")
				flags=flags[0].text

			if validation == False:
				break
			i+=1
			if i==x:
				i=0
				break
		if validation == False:
			break

	print(validation)
	return validation
