import json
from xml.etree import ElementTree
from lxml import etree
import datetime
import random
from robot.api import logger
import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
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
namespace =   ''
mapping ={
    'noun':0
}



    
def DefaultPreparation(mrid:str,xml:str):

    root = etree.fromstring(xml)
    tree = etree.ElementTree(root)
    root= tree.getroot()
    messageID=root.find(namespace+'header/'+namespace+'noun',root.nsmap).text+'_'+str(datetime.datetime.now().isoformat())+'_'+str(random.randint(1,100001))
    print('messageID', messageID)
    root.find(namespace+'header/'+namespace+ 'messageID',root.nsmap).text = str(messageID)
    root.find(namespace+'payload/'+namespace+'meterAsset/'+namespace+'mRID',root.nsmap).text = str(mrid)
    if root.find(namespace+'payload/'+namespace+'executeStartTime',root.nsmap)==None:
        root.find(namespace+'payload/'+namespace+'activationDateTime',root.nsmap).text=datetime.datetime.now().isoformat()
    else:
        root.find(namespace+'payload/'+namespace+'executeStartTime',root.nsmap).text=datetime.datetime.now().isoformat()

    return etree.tostring(tree, pretty_print=True),messageID

def DefaultPreparationEVN(mrid:str,xml:str):
    print(xml)
    root = etree.fromstring(xml)
    tree = etree.ElementTree(root)
    root= tree.getroot()
    print('noun',root[0][1].text)
    print('messageID', root[0][5].text)
    print('mrid', root[1][1][0].text)
    #messageID=root.find(namespace+'header/'+namespace+'noun',root.nsmap).text+'_'+str(datetime.now().isoformat())+'_'+str(random.randint(1,100001))
    messageID=root[0][1].text+'_'+str(datetime.datetime.now().isoformat())+'_'+str(random.randint(1,100001))
    for header in root[0].findall('*'):
        if 'dateTime' in header.tag:
            currenttime=str(datetime.datetime.now().isoformat())
            header.text=currenttime
    print('messageID', messageID)
    root[0][5].text = str(messageID)
    root[1][1][0].text = str(mrid)
    #
    print(etree.tostring(tree, pretty_print=True))
    return etree.tostring(tree, pretty_print=True),messageID

def DefaultPreparationEVN2(mrid:str,xml:str):
    print(xml)
    root = etree.fromstring(xml)
    tree = etree.ElementTree(root)
    root= tree.getroot()
    root[1][0][0].text = str(mrid)
    noun =""
    messageID=""
    for header in root[0].findall('*'):
        if 'noun' in header.tag:
            noun=header.text
        if 'messageID' in header.tag:
            messageID=noun+str(mrid)+'_'+str(datetime.datetime.now().isoformat())+'_'+str(random.randint(1,100001))
            header.text=messageID


    print(etree.tostring(tree, pretty_print=True))
    return etree.tostring(tree, pretty_print=True),messageID_test


def UpdateValueByPath( path : str , value : str,xml:str):

    root = etree.fromstring(xml)
    tree = etree.ElementTree(root)
    root= tree.getroot()
    root.find(path,root.nsmap).text = value
    return etree.tostring(tree, pretty_print=True)


def UpdateValueByParam(xml:str,value:str,paramNamePath:str,valuePath:str,paramName:str):
    root = etree.fromstring(xml)
    tree = etree.ElementTree(root)
    root= tree.getroot()

    names=[]
    values=[]
    ValuesElement=[]

    for x in root.findall(paramNamePath,root.nsmap):
        names.append(x.text)

    for y in root.findall(valuePath,root.nsmap):
        values.append(y.text)
        ValuesElement.append(y)


    for index in range(len(names)):
        if paramName==names[index]:
            ValuesElement[index].text=value

    return etree.tostring(tree, pretty_print=True)

def UpdateXML( path : str , value : str,xml:str):

    root = etree.fromstring(xml)
    tree = etree.ElementTree(root)
    root= tree.getroot()
    root.find(path,root.nsmap).text = value
    return etree.tostring(tree, pretty_print=True)

def MeterUpdateparams(xml, param, val):
    root = etree.fromstring(xml)
    tree = etree.ElementTree(root)
    root= tree.getroot()
    for movie in root[1].findall('*'):
        for xx in movie.findall('*'):
            if 'parameter' in xx.tag:
                for params in xx.findall('*'):
                    print(params.text)
                    if 'name' in params.tag:
                        params.text = param
                    if 'value' in params.tag:
                        params.text = val
					# result =  params.text

    return etree.tostring(tree, pretty_print=True)

def MeterUpdateparamName(xml,param, val):
    root = etree.fromstring(xml)
    tree = etree.ElementTree(root)
    root= tree.getroot()
    for movie in root[1].findall('*'):
        for xx in movie.findall('*'):
            if 'parameter' in xx.tag:
                print(xx[0])
                if xx[0].text.find(param)!=-1:
                    xx[0].text = val

                """ for params in xx.findall('*'):
                    print(params.text)
                    if 'name' in params.tag:
                        params.text = param
                    if 'value' in params.tag:
                        params.text = val """
					# result =  params.text

    return etree.tostring(tree, pretty_print=True)

#don't work for ADM
def MeterUpdateparamsByParamName(xml, param, val):
    root = etree.fromstring(xml)
    tree = etree.ElementTree(root)
    root= tree.getroot()
    for movie in root[1].findall('*'):
        for xx in movie.findall('*'):
            if 'parameter' in xx.tag:
                print(xx[0])
                if xx[0].text==param:
                    xx[1].text = val

                """ for params in xx.findall('*'):
                    print(params.text)
                    if 'name' in params.tag:
                        params.text = param
                    if 'value' in params.tag:
                        params.text = val """
					# result =  params.text

    return etree.tostring(tree, pretty_print=True)



def MeterAddparamsByParamName(project, xml, param, val):
    ET.register_namespace('xmlns:ami','http://www.emeter.com/energyip/amiinterface')
    root = etree.fromstring(xml)
    tree = etree.ElementTree(root)
    root= tree.getroot()[1][0]
    if project =='FLUVIUS' or project =='ELLEVIO':
        parameter = etree.SubElement(root,"{http://www.emeter.com/energyip/amiinterface}parameter")
        name = etree.SubElement(parameter,"{http://www.emeter.com/energyip/amiinterface}name")
        value = etree.SubElement(parameter,"{http://www.emeter.com/energyip/amiinterface}value")
        name.text = param
        value.text = val
        root.insert(3, parameter)
        print(etree.tostring(tree, pretty_print=True))
        return etree.tostring(tree, pretty_print=True)
    else:
        parameter = etree.SubElement(root,"parameter")
        name = etree.SubElement(parameter,"name")
        value = etree.SubElement(parameter,"value")
        name.text = param
        value.text = val
        root.insert(2, parameter)
        print(etree.tostring(tree, pretty_print=True))
        return etree.tostring(tree, pretty_print=True)

def MeterDeleteparamsByParamName(xml, param):
    root = etree.fromstring(xml)
    tree = etree.ElementTree(root)
    root= tree.getroot()[1][0]
    parameter = etree.SubElement(root,"parameter")
    name = etree.SubElement(parameter,"name")
    value = etree.SubElement(parameter,"value")
    name.text = param
    value.text = ""
    root.insert(2, parameter)
    print(etree.tostring(tree, pretty_print=True))
    return etree.tostring(tree, pretty_print=True)





def Update_Xml_Request(xml, param, val):
    if param !='None':
        print("i'm in None case")
        root = etree.fromstring(xml)
        tree = etree.ElementTree(root)
        root= tree.getroot()
        namespaces = {'xmlns': 'http://www.emeter.com/energyip/amiinterface'}
        root[1].findall('xmlns:'+param, namespaces)[0].text=val


        return etree.tostring(tree, pretty_print=True)
    else:
        return xml
def Update_Xml_Request_Empty_Param(xml, param):
    if param !='None':
        print("i'm in None case")
        root = etree.fromstring(xml)
        tree = etree.ElementTree(root)
        root= tree.getroot()
        namespaces = {'xmlns': 'http://www.emeter.com/energyip/amiinterface'}
        root[1].findall('xmlns:'+param, namespaces)[0].text=""


        return etree.tostring(tree, pretty_print=True)
    else:
        return xml
def StandardDefaultPreparation(mrid:str,xml:str, tag:str):
    print(xml)
    namespaces = {'xmlns': 'http://www.emeter.com/energyip/amiinterface'}
    root = etree.fromstring(xml)
    tree = etree.ElementTree(root)
    root= tree.getroot()
    metertag=root[1].findall('xmlns:'+tag, namespaces)
    print(metertag)
    metertag[0].findall('xmlns:mRID', namespaces)[0].text = str(mrid)
    # mrid[0].text = str(mrid)
    noun =""
    messageID=""
    for header in root[0].findall('*'):
        if 'noun' in header.tag:
            noun=header.text
        if 'messageID' in header.tag:
            messageID=noun+str(mrid)+'_'+str(datetime.datetime.now().isoformat())+'_'+str(random.randint(1,100001))
            header.text=messageID
        if 'dateTime' in header.tag:
            currenttime=str(datetime.datetime.now().isoformat())
            header.text=currenttime
    for payload in root[1].findall('*'):
        if 'executeStartTime' in payload.tag:
            currenttime=str(datetime.datetime.now().isoformat())
            payload.text=currenttime

    print(etree.tostring(tree, pretty_print=True))
    return etree.tostring(tree, pretty_print=True),messageID

def StandardDefaultPreparationPastDateTime(mrid:str,xml:str, tag:str, timeparam, shift_value):
    print(xml)
    namespaces = {'xmlns': 'http://www.emeter.com/energyip/amiinterface'}
    root = etree.fromstring(xml)
    tree = etree.ElementTree(root)
    root= tree.getroot()
    metertag=root[1].findall('xmlns:'+tag, namespaces)
    print(metertag)
    metertag[0].findall('xmlns:mRID', namespaces)[0].text = str(mrid)
    # mrid[0].text = str(mrid)
    noun =""
    messageID=""
    for header in root[0].findall('*'):
        if 'noun' in header.tag:
            noun=header.text
        if 'messageID' in header.tag:
            messageID=noun+str(mrid)+'_'+str(datetime.datetime.now().isoformat())+'_'+str(random.randint(1,100001))
            header.text=messageID
        if 'dateTime' in header.tag:
            dt = datetime.datetime.now()
            if timeparam =='dateTime':
                shift = datetime.timedelta(minutes=int(shift_value))
                past = dt - shift
                header.text=past.isoformat()
            else:
                header.text=str(dt.isoformat())
    for payload in root[1].findall('*'):
        if 'executeStartTime' in payload.tag:
            dt = datetime.datetime.now()
            if timeparam =='executeStartTime':
                shift = datetime.timedelta(minutes=int(shift_value))
                past = dt - shift
                payload.text=past.isoformat()
            else:
                payload.text=str(dt.isoformat())

    print(etree.tostring(tree, pretty_print=True))
    return etree.tostring(tree, pretty_print=True),messageID


def UpdateTextMessage(value:str,xml:str, tag:str):
    print(xml)
    namespaces = {'xmlns': 'http://www.emeter.com/energyip/amiinterface'}
    root = etree.fromstring(xml)
    tree = etree.ElementTree(root)
    root= tree.getroot()
    metertag=root[1].findall('xmlns:'+tag, namespaces)[0].text =str(value)



    print(etree.tostring(tree, pretty_print=True))
    return etree.tostring(tree, pretty_print=True)

#ADDED FOR ESO
def UpdateMeter(mrid:str,xml:str, tag:str):
    print(xml)
    namespaces = {'xmlns': 'http://www.emeter.com/energyip/amiinterface'}
    root = etree.fromstring(xml)
    tree = etree.ElementTree(root)
    root= tree.getroot()
    metertag=root[1].findall('xmlns:'+tag, namespaces)
    print(metertag)
    metertag[0].findall('xmlns:mRID', namespaces)[0].text = str(mrid)
    # mrid[0].text = str(mrid)

    for header in root[0].findall('*'):

        if 'messageID' in header.tag:
            messageID=header.text

        if 'dateTime' in header.tag:
            currenttime=str(datetime.datetime.now().isoformat())
            header.text=currenttime
    for payload in root[1].findall('*'):
        if 'executeStartTime' in payload.tag:
            currenttime=str(datetime.datetime.now().isoformat())
            payload.text=currenttime
        if 'executeExpireTime' in payload.tag:
            executetime=str((datetime.datetime.now() + datetime.timedelta(hours=1)).isoformat() )
            #executetime=datetime.strftime(datetime.now() - timedelta(1), "%Y-%m-%dT%H-%M-%S")
            payload.text=executetime



    print(etree.tostring(tree, pretty_print=True))
    return etree.tostring(tree, pretty_print=True),messageID

def Get(xml:str, tag:str, status):
    print(xml)
    namespaces = {'xmlns': 'http://www.emeter.com/energyip/amiinterface'}
    root = etree.fromstring(str.encode(xml))
    tree = etree.ElementTree(root)
    root= tree.getroot()
    metertag=root[1].findall('xmlns:'+tag, namespaces)
    print(metertag)


    for payload in root[1].findall('*'):
        if 'additionalInfo' in payload.tag:

            additionalInfo=payload.text
            x=json.loads(additionalInfo)

    return x[status]


def compare(start,end):
    x=random_dates(start,end)

    t1=pd.to_datetime(x[0].strftime("%Y-%m-%dT%H:%M:%S"))
    t2=pd.to_datetime(x[1].strftime("%Y-%m-%dT%H:%M:%S"))
    print(t1)
    print(t2)
    if t1>t2:
        print('t2 older then t1')
        s=t2
        e=t1
    elif t1<t2:
        print("t1 older then t2")
        s=t1
        e=t2
    else:
        s=e=t1
    return s.strftime("%Y-%m-%dT%H:%M:%S"),e.strftime("%Y-%m-%dT%H:%M:%S")



def updateXmlFileWithIntervall(mrid:str,xml:str, tag:str,startTime,endTime):
    print(xml)
    namespaces = {'xmlns': 'http://www.emeter.com/energyip/amiinterface'}
    root = etree.fromstring(xml)
    tree = etree.ElementTree(root)
    root= tree.getroot()
    metertag=root[1].findall('xmlns:'+tag, namespaces)
    print(metertag)
    metertag[0].findall('xmlns:mRID', namespaces)[0].text = str(mrid)
    # mrid[0].text = str(mrid)
    noun =""
    messageID=""
    for header in root[0].findall('*'):
        if 'noun' in header.tag:
            noun=header.text
        if 'messageID' in header.tag:
            messageID=noun+str(mrid)+'_'+str(datetime.datetime.now().isoformat())+'_'+str(random.randint(1,100001))
            header.text=messageID
        if 'dateTime' in header.tag:
            currenttime=str(datetime.datetime.now().isoformat())
            header.text=currenttime
    for payload in root[1].findall('*'):
        if 'startTime' in payload.tag:


            payload.text=startTime


        if 'endTime' in payload.tag:

            payload.text=endTime

        if 'executeStartTime' in payload.tag:
            currenttime=str(datetime.datetime.now().isoformat())
            payload.text=currenttime
        if 'executeExpireTime' in payload.tag:
            executetime=str((datetime.datetime.now() + datetime.timedelta(hours=1)).isoformat() )
            payload.text=executetime



    print(etree.tostring(tree, pretty_print=True))
    return etree.tostring(tree, pretty_print=True),messageID


def getDates(start,end):
    x=random_dates(start,end)

    t1=pd.to_datetime(x[0].strftime("%Y-%m-%dT%H:%M:%S"))
    t2=t1+ datetime.timedelta(days=1)

    return t1.strftime("%Y-%m-%dT%H:%M:%S"),t2.strftime("%Y-%m-%dT%H:%M:%S")
def getData(Project,j:int,column):
    df = pd.read_csv(ODR_Reading2+'/'+Project+'/'+'DCT_Profiles'+'.csv', sep=';')
    print("(df.loc[j, column])")
    print(df.loc[j, column])
    return str(df.loc[j, column])


def floatToInteger(x):
    if pd.isna(float(x))==False:
        x=int(float(x))

    return  str(x)

def getIndex(Project, DCT_Profiles):
    df = pd.read_csv(ODR_Reading2+'/'+Project+'/'+DCT_Profiles+'.csv', sep=';')

    return len(df.index)

def random_dates(start, end, n=2):
    s=pd.to_datetime(start)
    e=pd.to_datetime(end)

    start_u = s.value//10**9
    end_u = e.value//10**9
    return pd.to_datetime(np.random.randint(start_u, end_u, n), unit='s')
