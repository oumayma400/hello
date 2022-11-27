import json
from lxml import etree
from datetime import datetime
import random
from robot.api import logger
import time
import sys,os
from pathlib import Path
import xml.etree.ElementTree as ET
import pandas as pd
import sys,os
from pathlib import Path
import pytz
import time
import re
path = Path(os.path.abspath(__file__))
parrent_path = path.parent.absolute()
parrent_path = parrent_path.parent.absolute()
ODR_Reading = os.path.dirname(parrent_path) + os.path.sep + "Resources\\ODR_Reading";
ODR_Reading2 = ODR_Reading.replace('\\', '/')
sys.path.append(ODR_Reading2)



def GetValueByPath( path : str,xml:str):

        root = etree.fromstring(xml)
        tree = etree.ElementTree(root)
        root= tree.getroot()
        value=root.find(path,root.nsmap).text
        logger.info(value)
        return str(value)

def VerifyCapa(capaName:list,xml:str, expected_values: list , expected_availibility: list) -> str:

        print("capaName")
        print(capaName)
        i=0
        H=''
        Value=[]
        Availibility=[]

        CapaFound=False
        root = etree.fromstring(str.encode(xml))
        tree = etree.ElementTree(root)
        root= tree.getroot()
        validation =True
        for capabilities in root.findall('{http://www.fluvius.be/hpc/capabilityUpdate}capabilities'):
            for capaN in capaName:
                for capability in capabilities.findall('{http://www.fluvius.be/hpc/capabilityUpdate}capability'):

                    code = capability.find('{http://www.fluvius.be/hpc/capabilityUpdate}code').text

                    if code == capaN:

                        Value.append(capability.find('{http://www.fluvius.be/hpc/capabilityUpdate}value').text)

                        Availibility.append(capability.find('{http://www.fluvius.be/hpc/capabilityUpdate}available').text)
                        CapaFound=True
                        break

        if CapaFound==True:
            print(Value, expected_values)
            print(Availibility, expected_availibility)
            if expected_values !=Value:
                validation= False
            if expected_availibility !=Availibility:
                validation= False
            return "200",validation
        else:
            return "408", 'None'



flag_list=[1073741824, 8388608,4194304, 1048576,8192,128 ]
def check_flags(flag, k=0, end=len(flag_list)):
    if k <= end:
        if flag >0:
            if flag>=flag_list[k]:
                flag= flag -flag_list[k]
                k=k+1
                return check_flags(flag,k,end)
            else:
                k=k+1
                return check_flags(flag,k, end)
        elif flag ==0:
            print(flag)
            return str(flag)
        else:
            print(flag)
            return str(flag)
    else:
        print(flag)
        return str(flag)


def validate_flag(xml):
    root = etree.fromstring(str.encode(xml))
    tree = etree.ElementTree(root)
    root= tree.getroot()
    flag =root.find('payload/MeterReading/IntervalBlock/IReading/flags',root.nsmap).text
    print("flag" , flag)
    output=""
    output = check_flags(int(flag), 0,len(flag_list) )
    time.sleep(20)
    return output


def get_ssf_parameters(PROJECT, ssf_name, meter_type):

    output=[]
    path = Path(os.path.abspath(__file__))
    parrent_path = path.parent.absolute()
    parrent_path = parrent_path.parent.absolute()
    ssf_path = os.path.dirname(parrent_path) + os.path.sep + "Resources"
    ssf_path= ssf_path +'\\SSF_Files\\'+ PROJECT +'\\'+ ssf_name
    tree = ET.parse(ssf_path)
    root = tree.getroot()
    print( root[1][0][1][1].text)
    Device_type = root[1][0][1][1].text
    Configuration_version= root[1][0][1][2].text
    Supplier= root[1][0][0][1].text
    print("Supplier ", Supplier)
    print("Device_type ", Device_type)
    print("Configuration_version ", Configuration_version)
    Box_id = root[1][0][2][1]
    print(len(Box_id))
    print(Box_id)
    if meter_type =='ELEC':
        for i in range(1, len(Box_id)):
            Serial_number= Box_id[i][0][0].text
            Year_of_manufactory=Box_id[i][0][8].text
            Communication_method=Box_id[i][0][7].text
            Hardware_version=Box_id[i][0][9].text
            Module_active_firmware_version=Box_id[i][0][10].text
            Core_active_firmware_version=Box_id[i][0][11].text
            IMSI= Box_id[i][1][1][0].text
            IMEI = Box_id[i][1][2][0].text
            Communication_module_id=Box_id[i][1][2][1].text
        	# print("Serial_number ", Serial_number)
        	# print("Year_of_manufactory ", Year_of_manufactory)
        	# print("Communication_method ", Communication_method)
        	# print("Hardware_version ", Hardware_version)
        	# print("Module_active_firmware_version ", Module_active_firmware_version)
        	# print("Core_active_firmware_version ", Core_active_firmware_version)
        	# print("IMSI ", IMSI)
        	# print("IMEI ", IMEI)
            # print("Communication_module_id ", Communication_module_id)
            result = {"Serial_number":Serial_number , "Year_of_manufactory": Year_of_manufactory, "Communication_method": Communication_method, "Hardware_version": Hardware_version,"Module_active_firmware_version": Module_active_firmware_version, "Core_active_firmware_version": Core_active_firmware_version, "IMSI": IMSI,"IMEI":IMEI , "Communication_module_id": Communication_module_id, "Device_type": Device_type, "Configuration_version":Configuration_version, "Supplier": Supplier}
            output.append(result)
        return output

    elif meter_type == 'MBUS':
        for i in range(1, len(Box_id)):
            Serial_number= Box_id[i][0][0].text
            Year_of_manufactory=Box_id[i][0][8].text
            Communication_method=Box_id[i][0][7].text
            Hardware_version=Box_id[i][0][9].text
            # Module_active_firmware_version=Box_id[i][0][10].text
            Core_active_firmware_version=Box_id[i][0][10].text
            result = {"Serial_number":Serial_number , "Year_of_manufactory": Year_of_manufactory, "Communication_method": Communication_method, "Hardware_version": Hardware_version, "Core_active_firmware_version": Core_active_firmware_version,"Device_type": Device_type, "Configuration_version":Configuration_version, "Supplier": Supplier}
            output.append(result)
        return output

def get_dc_ssf_parameters(PROJECT, ssf_name):

    output=[]
    path = Path(os.path.abspath(__file__))
    parrent_path = path.parent.absolute()
    parrent_path = parrent_path.parent.absolute()
    ssf_path = os.path.dirname(parrent_path) + os.path.sep + "Resources"
    ssf_path= ssf_path +'\\SSF_Files\\'+ PROJECT +'\\'+ ssf_name
    tree = ET.parse(ssf_path)
    root = tree.getroot()
    print( root[1][0][1][1].text)
    Device_type = root[1][0][1][1].text
    Configuration_version= root[1][0][1][3].text
    Supplier= root[1][0][0][1].text
    print("Supplier ", Supplier)
    print("Device_type ", Device_type)
    print("Configuration_version ", Configuration_version)
    Box_id = root[1][0][2][1]
    print(len(Box_id))
    print(Box_id)

    for i in range(1, len(Box_id)):
        Serial_number= Box_id[i][0][0].text
        Equipment_identifier=Box_id[i][0][1].text
        Customer_Article_Number=Box_id[i][0][2].text
        Year_of_manufactory=Box_id[i][0][4].text
        Hardware_version=Box_id[i][0][5].text
        APPLICATIVE_FW=Box_id[i][0][6][1].text
        PLC_G3_Mac_Address= Box_id[i][0][10].text
        WAN_Mac_Address = Box_id[i][0][11].text

        result = {"Serial_number":Serial_number , "Year_of_manufactory": Year_of_manufactory, "Hardware_version": Hardware_version, "Equipment_identifier": Equipment_identifier,"Customer_Article_Number": Customer_Article_Number, "APPLICATIVE_FW": APPLICATIVE_FW, "PLC_G3_Mac_Address": PLC_G3_Mac_Address,"WAN_Mac_Address":WAN_Mac_Address , "Device_type": Device_type, "Configuration_version":Configuration_version, "Supplier": Supplier}
        output.append(result)
    return output


def namespace(element):
    m = re.match(r'\{.*\}', element.tag)
    return m.group(0) if m else ''


def get_meters_din_ldn_from_ssf(PROJECT, ssf_name):
    output=[]
    path = Path(os.path.abspath(__file__))
    parrent_path = path.parent.absolute()
    parrent_path = parrent_path.parent.absolute()
    ssf_path = os.path.dirname(parrent_path) + os.path.sep + "Resources"
    ssf_path= ssf_path +'\\SSF_Files\\'+ PROJECT +'\\'+ ssf_name
    tree = ET.parse(ssf_path)
    root = tree.getroot()
    Box_id = root[1][0][2][1]
    print(len(Box_id))
    print(Box_id)
    Serial_number=[]
    ldn=[]
    print(root.tag)
    print(namespace(root))
    Device_attributes=Box_id.findall(namespace(root)+'Device_attributes')
    # print(Device_attributes)
    for Device_attribute in Device_attributes:
        General = Device_attribute.findall(namespace(root)+'General')
        Serial_numberxml= General[0].findall(namespace(root)+'Serial_number')
        Serial_number.append(Serial_numberxml[0].text)
        sag = Device_attribute.findall(namespace(root)+'DLMSAttributes')
        sag2= sag[0].findall(namespace(root)+'Equipment_identifier')
        print(sag2[0].text)
        ldn.append(sag2[0].text)
    return Serial_number, ldn

def get_DCs_din_ldn_from_ssf(PROJECT, ssf_name):
    output=[]
    path = Path(os.path.abspath(__file__))
    parrent_path = path.parent.absolute()
    parrent_path = parrent_path.parent.absolute()
    ssf_path = os.path.dirname(parrent_path) + os.path.sep + "Resources"
    ssf_path= ssf_path +'\\SSF_Files\\'+ PROJECT +'\\'+ ssf_name
    tree = ET.parse(ssf_path)
    root = tree.getroot()
    Box_id = root[1][0][2][1]
    print(len(Box_id))
    print(Box_id)
    Serial_number=[]
    ldn=[]
    print(root.tag)
    print(namespace(root))
    Device_attributes=Box_id.findall(namespace(root)+'Device_attributes')
    # print(Device_attributes)
    for Device_attribute in Device_attributes:
        General = Device_attribute.findall(namespace(root)+'General')
        Serial_numberxml= General[0].findall(namespace(root)+'Serial_number')
        Serial_number.append(Serial_numberxml[0].text)
        print(Serial_number)
        # sag = Device_attribute.findall(namespace(root)+'DLMSAttributes')
        sag2= General[0].findall(namespace(root)+'Equipment_identifier')
        print(sag2[0].text)
        ldn.append(sag2[0].text)
    return Serial_number, ldn





def validODR(Project  ,ODR_TRI , xml,profilename):
    # with open(pathname+profilename+'.xml', 'r') as f:
    L=[]
    print(Project  ,ODR_TRI , xml,profilename)

    namespaces = {'xmlns': 'http://www.emeter.com/energyip/amiinterface'}
    root = etree.fromstring(str.encode(xml))
    tree = etree.ElementTree(root)
    root= tree.getroot()

    # root = etree.fromstring(data)
    # tree = etree.ElementTree(root)
    # root= tree.getroot()

    i=0
    x=len(root[1][0])-1
    metertag=root[1].findall('xmlns:'+'meterAsset', namespaces)
    for payload in root[1].findall('*'):
        for MeterReading in root[1][0].findall('*'):
            i+=1
            IntervalBlock = root[1][0][i].findall('*')[0]
            if 'readingTypeId' in IntervalBlock.tag:

                L.append(IntervalBlock.text)
            if i==x:
                break
    print(L)
    print(ODR_Reading2+'/'+Project+'/'+ODR_TRI+'.csv')
    df = pd.read_csv(ODR_Reading2+'/'+Project+'/'+ODR_TRI+'.csv', sep=';')
    obistab= df[df['profile']==profilename]['obis']
    print(type(obistab))
    res= obistab.values
    res= res[0].split(',')
    print("list of readingtypeid from the csv template")
    print(res)
    print("list from extracted CIM")
    print(L)
    print("validation :")
    print(res == L)
    return sorted(res) == sorted(L)





def ValidCSV(file, profilename):
    C=[]
    df = pd.read_csv(file, sep=';')
    obistab= df[df['profile']=='PQ1']['obis']
    print(type(obistab))
    res= obistab.values
    res= res[0].split(',')

    for i in range (len(df.index)):
        #print(df.loc[i, 'Instant_U_PerPhase'])
        C.append(df.loc[i, profilename])
        CN = [str(x) for x in C]
        new = [x for x in CN if x != 'nan']
    return new


def valid(L,C):
    r=[]
    print(L)

    for i in L:
        res = [ele for ele in C if(ele in i)]

        r.append(bool(res))

    if sum(r) == len(r):
       return True
