import psycopg2
import datetime
from pandas import DataFrame
from jproperties import Properties
import paramiko
import xml.etree.ElementTree as ET
import sys,os
from pathlib import Path
import pytz
import time
path = Path(os.path.abspath(__file__))
parrent_path = path.parent.absolute()
Read_ConfigLib = os.path.dirname(parrent_path) + os.path.sep + "Read_Config";
Read_ConfigLib2 = Read_ConfigLib.replace('\\', '/')
sys.path.append(Read_ConfigLib2)

# 'C:/Users/g361355/Desktop/ROBOT_ECLIPSE/E2E-AUTO-SICONIA/Libraries/Read_Config'
# from test2 import something
# from ReadConfigFile  import ReadConfigFile as conf
import ReadConfigFile as conf
def test00():
    return True
def select_request(DB_HOST, db , database_name , db_user ,db_pass ,filter, db_name, condition):
    conn = psycopg2.connect(host=DB_HOST ,database=db, user=db_user, password=db_pass)
    cursor = conn.cursor()
    table = database_name+"."+db_name+" "
    cond= condition
    print("select "+filter+" from "+ table +"where "+ cond)
    cursor.execute("select "+filter+" from "+ table +"where "+ cond)
    output = DataFrame(cursor.fetchall())
    #print(output)
    if len(output)>0:
        output.columns =  [x.name for x in cursor.description ]
        return output[filter][0]
    else:
        return None

def check_task_in_vsdc(DB_HOST, db , database_name , db_user ,db_pass ,filter, db_name, message):

    conn = psycopg2.connect(host=DB_HOST ,database=db, user=db_user, password=db_pass)
    cursor = conn.cursor()
    table = database_name+"."+db_name+" "
    cond= "message_id='"+ message + "'"
    print("select "+filter+" from "+ table +"where "+ cond)
    cursor.execute("select "+filter+" from "+ table +"where "+ cond)
    output = DataFrame(cursor.fetchall())
    if len(output)>0:
        output.columns =  [x.name for x in cursor.description ]
        condition = "task_id='"+ output[filter][0] + "'"
        output_vsdc=select_request('172.31.12.103','vsdc_db','vsdc','postgres','postgres','task_id','vsdc_task', condition)
        return output_vsdc, True  
    else:
        return False
        
def select_request_old(DB_HOST, db , database_name , db_user ,db_pass ,filter, db_name, condition):

    conn = psycopg2.connect(host=DB_HOST ,database=db, user=db_user, password=db_pass)
    cursor = conn.cursor()
    table = database_name+"."+db_name+" "
    cond= condition
    print("select "+filter+" from "+ table +"where "+ cond)
    cursor.execute("select "+filter+" from "+ table +"where "+ cond)
    output = DataFrame(cursor.fetchall())
    print(output)
    if len(output)>0:
        output.columns =  [x.name for x in cursor.description ]
    print(output)
    return output

def select(DB_HOST, db , database_name , db_user ,db_pass ,filter, db_name, message):
    conn = psycopg2.connect(host=DB_HOST ,database=db, user=db_user, password=db_pass)
    cursor = conn.cursor()
    table = database_name+"."+db_name+" "
    cond= "message_id='"+ message + "'"
    print("select "+filter+" from "+ table +"where "+ cond)
    cursor.execute("select "+filter+" from "+ table +"where "+ cond)
    output = DataFrame(cursor.fetchall())
    #print(output)
    if len(output)>0:
        output.columns =  [x.name for x in cursor.description ]
        return output[filter][0]
    else:
        return None

def HES_Operation_Duration(message):
    end_date=select('172.31.12.103', 'metering_db' , 'metering' , 'postgres' ,'postgres' ,'end_date', 'metering_job', message)
    start_date=select('172.31.12.103', 'metering_db' , 'metering' , 'postgres' ,'postgres' ,'start_date', 'metering_job', message)
    t1 = datetime.strptime(str(end_date), "%Y-%m-%d %H:%M:%S.%f")
    t2 = datetime.strptime(str(start_date), "%Y-%m-%d %H:%M:%S.%f")
    if (int(((t1-t2).total_seconds())))==21000:
        return True
    else:
        return False

def Operation_Retry_pause(message):
    job_id=check_task_in_vsdc('172.31.12.103', 'metering_db' , 'metering' , 'postgres' ,'postgres' ,'job_id', 'metering_job', message)
    condition = "task_id='"+ job_id + "'"
    wait_recovery=select_request('172.31.12.103','vsdc_db','vsdc','postgres','postgres','wait_recovery','vsdc_task', condition)
    if (wait_recovery==1800):
        return True
    else:
        return False
# def select_request_join(DB_HOST,database_name , db_user ,db_pass ,filter, db_name, condition):
#     conn = psycopg2.connect(host=DB_HOST ,database="odm_db", user=db_user, password=db_pass)
#     cursor = conn.cursor()
#     table = database_name+"."+db_name+" "
#     cond= condition
#     cursor.execute("select "+filter+" from "+ table +"where "+ cond)
#     output = DataFrame(cursor.fetchall())
#     output.columns =  [x.name for x in cursor.description ]
#     print(output)
#     return output

def delete_request(DB_HOST,db, database_name , db_user ,db_pass, db_name, deleted_id, cond):
    conn = psycopg2.connect(host=DB_HOST ,database=db, user=db_user, password=db_pass)
    cursor = conn.cursor()
    table = database_name+"."+db_name+" "
    print("DELETE from "+ table +"where "+ cond + " = "+ str(deleted_id))
    cursor.execute("delete from "+ table +"where "+ cond + " = "+ str(deleted_id))
    conn.commit()
    cursor.close()
    conn.close()
    return True

def extract_unique_value(data):
    if len(data)>0:
        print ('data', data['id'][0])
        return data['id'][0]
    else:
        return []
def extract_meters_id(data,filter):
    print("data", data)
    if len(data)>0:

        print ('data', data[filter][0])
        return data[filter].values.tolist()
    else:
        return []

def get_meters_list(PROJECT,ssf):
    print("PROJECT : " +PROJECT)
    ssf_id= "'"+str(ssf)+"'"
    condition= "file_name="+ssf_id
    db_host= conf.ReadConfigFile.read(PROJECT,'db_host')
    odm_db_pass=conf.ReadConfigFile.read(PROJECT,'odm_db_pass')
    odm_db_user=conf.ReadConfigFile.read(PROJECT,'odm_db_user')
    ssf_idfromODM= select_request(db_host, 'odm_db', 'odm' , odm_db_user ,odm_db_pass, 'id', 'asset_shipment_file', condition)
    if len(ssf_idfromODM)>0:
        print("ssf_idfromODM",ssf_idfromODM)
        id_ssf =ssf_idfromODM['id'][0]
        print("id_ssf",id_ssf)
        condition_2 ="shipment_file_id="+str(id_ssf)
        meter_ids=select_request(db_host, 'odm_db', 'odm' , odm_db_user ,odm_db_pass, 'id, din, ldn', 'metering_meter', condition_2)
        return meter_ids
    else:
        return []

def get_meters_list_fluvius(PROJECT,ssf):
    ssf_id= "'"+str(ssf)+"'"
    condition= "file_name="+ssf_id
    db_host= conf.ReadConfigFile.read(PROJECT,'db_host')
    odm_db_pass=conf.ReadConfigFile.read(PROJECT,'odm_db_pass')
    odm_db_user=conf.ReadConfigFile.read(PROJECT,'odm_db_user')
    ssf_idfromODM= select_request(db_host, 'odm_db_2', 'odm' , odm_db_user ,odm_db_pass, 'id', 'asset_shipment_file', condition)
    if len(ssf_idfromODM)>0:
        print("ssf_idfromODM",ssf_idfromODM)
        id_ssf =ssf_idfromODM['id'][0]
        print("id_ssf",id_ssf)
        condition_2 ="shipment_file_id="+str(id_ssf)
        meter_ids=select_request(db_host, 'odm_db_2', 'odm' , odm_db_user ,odm_db_pass, 'id, din, ldn', 'metering_meter', condition_2)
        return meter_ids
    else:
        return []


def delete_SSF_meters_from_m2m_db(PROJECT,db,schema,tab):
    for i in range(len(tab)):
        meter_id= "'"+str(tab[i])+"'"
        condition= "device_id="+meter_id
        db_host= conf.ReadConfigFile.read(PROJECT,'db_host')
        m2m_db_pass=conf.ReadConfigFile.read(PROJECT,'m2m_db_pass')
        m2m_db_user=conf.ReadConfigFile.read(PROJECT,'m2m_db_user')
        meters_id= select_request(db_host, db, schema , m2m_db_user ,m2m_db_pass, 'id', 'm2m_device', condition)
        #meters_id= meters_id['id']
        print("meters_id : ",meters_id )
        delete_request(db_host, db, schema , m2m_db_user ,m2m_db_pass, 'm2m_equipment_mapping', meter_id, 'customer_id')
        delete_request(db_host, db, schema , m2m_db_user ,m2m_db_pass, 'm2m_device', meter_id, 'device_id')
        if len(meters_id)>0:
            id_meter_want_to_delete= meters_id['id'][0]
            delete_request(db_host, db, schema , m2m_db_user ,m2m_db_pass, 'm2m_device_group', id_meter_want_to_delete, 'device_id')
            delete_request(db_host, db, schema ,m2m_db_user ,m2m_db_pass, 'm2m_device_task', id_meter_want_to_delete, 'device_id')
            #delete_request(db_host, db, schema , 'postgres' ,'postgres', 'm2m_group', id_meter_want_to_delete, 'device_id')

    return True

def delete_SSF_meters_from_vsdc_db(PROJECT, db,schema,tab):
    for i in range(len(tab)):
        meter_id= "'"+str(tab[i])+"'"
        condition= "device_id="+meter_id
        db_host= conf.ReadConfigFile.read(PROJECT,'db_host')
        vsdc_db_pass=conf.ReadConfigFile.read(PROJECT,'vsdc_db_pass')
        vsdc_db_user=conf.ReadConfigFile.read(PROJECT,'vsdc_db_user')
        meters_id= select_request(db_host, db, schema , vsdc_db_user ,vsdc_db_pass, 'id', 'vsdc_device', condition)
        #meters_id= meters_id['id']
        print("meters_id : ",meters_id )

        #delete_request(db_host, db, schema , 'postgres' ,'postgres', 'm2m_device', meter_id, 'device_id')
        if len(meters_id)>0:
            id_meter_want_to_delete= meters_id['id'][0]
            delete_request(db_host, db, schema , vsdc_db_user ,vsdc_db_pass, 'vsdc_device_group', id_meter_want_to_delete, 'device_id')
            delete_request(db_host, db, schema , vsdc_db_user ,vsdc_db_pass, 'vsdc_device_task', id_meter_want_to_delete, 'device_id')
            delete_request(db_host, db, schema , vsdc_db_user ,vsdc_db_pass, 'vsdc_device_task_execution', id_meter_want_to_delete, 'device_id')
        delete_request(db_host, db, schema , vsdc_db_user ,vsdc_db_pass, 'vsdc_device', meter_id, 'device_id')
    return True
def delete_SSF_meters_from_kms_db(PROJECT, db,schema,tab):
    for i in range(len(tab)):
        print("inside delete_SSF_meters_from_kms_db ******************")
        meter_id= "'"+str(tab[i])+"'"
        condition= "customer_serial_number="+meter_id
        db_host= conf.ReadConfigFile.read(PROJECT,'db_host')
        kms_db_pass=conf.ReadConfigFile.read(PROJECT,'kms_db_pass')
        kms_db_user=conf.ReadConfigFile.read(PROJECT,'kms_db_user')
        meters_id= select_request(db_host, db, schema ,kms_db_user ,kms_db_pass, 'id', 'device', condition)
        #meters_id= meters_id['id']
        print("meters_id : ",meters_id )

        #delete_request(db_host, db, schema , 'postgres' ,'postgres', 'm2m_device', meter_id, 'device_id')
        if len(meters_id)>0:
            id_meter_want_to_delete= meters_id['id'][0]
            delete_request(db_host, db, schema , kms_db_user ,kms_db_pass, 'frame_counter', id_meter_want_to_delete, 'device_id')
            delete_request(db_host, db, schema , kms_db_user ,kms_db_pass, 'protected_session_key', id_meter_want_to_delete, 'unique_device_id')
            delete_request(db_host, db, schema , kms_db_user ,kms_db_pass, 'device', id_meter_want_to_delete, 'id')


    return True

def delete_SSF_from_kms_db(PROJECT, db,ssf):
    ssf_id= "'"+str(ssf)+"'"
    condition= "file_name="+ssf_id
    db_host= conf.ReadConfigFile.read(PROJECT,'db_host')
    kms_db_pass=conf.ReadConfigFile.read(PROJECT,'kms_db_pass')
    kms_db_user=conf.ReadConfigFile.read(PROJECT,'kms_db_user')
    ssf_idfromkms= select_request(db_host, db, 'kms' , kms_db_user ,kms_db_pass, 'id', 'shipment_file', condition)
    if len(ssf_idfromkms)>0:
        delete_request(db_host, db, 'kms' , kms_db_user ,kms_db_pass, 'device_revision', ssf_idfromkms['id'][0], 'shipment_file_id')
        delete_request(db_host, db, 'kms' , kms_db_user ,kms_db_pass, 'shipment_file', ssf_id, 'file_name')
    return True

def delete_meters_and_SSF_from_odm_db(PROJECT,db,ssf):
    ssf_id= "'"+str(ssf)+"'"
    condition= "file_name="+ssf_id
    db_host= conf.ReadConfigFile.read(PROJECT,'db_host')
    odm_db_pass=conf.ReadConfigFile.read(PROJECT,'odm_db_pass')
    odm_db_user=conf.ReadConfigFile.read(PROJECT,'odm_db_user')
    ssf_idfromODM= select_request(db_host, db, 'odm' , odm_db_user ,odm_db_pass, 'id', 'asset_shipment_file', condition)
    print("ssf_idfromODM",ssf_idfromODM)
    if len(ssf_idfromODM)>0:

        id_ssf =ssf_idfromODM['id'][0]
        print("id_ssf",id_ssf)
        condition_2 ="shipment_file_id="+str(id_ssf)
        meter_ids=select_request(db_host, db, 'odm' , odm_db_user ,odm_db_pass, 'id', 'metering_meter', condition_2)
        if len(meter_ids)>0:
            meter_ids=meter_ids['id']
            for i in range(len(meter_ids)):
                delete_request(db_host, db, 'odm' , odm_db_user,odm_db_pass, 'metering_meter_event', meter_ids[i], 'metering_meter_id')
                delete_request(db_host, db, 'odm' , odm_db_user,odm_db_pass, 'metering_meter_config_param_info', meter_ids[i], 'meter_metering_id')
                delete_request(db_host, db, 'odm' , odm_db_user,odm_db_pass, 'metering_meter_capa', meter_ids[i], 'meter_id')
                delete_request(db_host, db, 'odm' , odm_db_user,odm_db_pass, 'metering_firmware_program_version', meter_ids[i], 'metering_meter_id')
                delete_request(db_host, db, 'odm' , odm_db_user ,odm_db_pass, 'metering_north_com_function', meter_ids[i], 'metering_meter_id')
                delete_request(db_host, db, 'odm' , odm_db_user ,odm_db_pass, 'asset_imsi', meter_ids[i], 'meter_metering_id')
                delete_request(db_host, db, 'odm' , odm_db_user ,odm_db_pass, 'metering_meter', id_ssf, 'shipment_file_id')

    #delete_request(db_host, db, 'odm' , 'postgres' ,'postgres', 'shipment_file', ssf_id, 'file_name')
    delete_request(db_host, db, 'odm' ,odm_db_user ,odm_db_pass, 'asset_shipment_file', ssf_id, 'file_name')
    return True

def get_ssf_status(PROJECT, ssf_name):
    ssf_id= "'"+str(ssf_name)+"'"
    condition= "file_name="+ssf_id
    test= False
    test2= False
    db_host= conf.ReadConfigFile.read(PROJECT,'db_host')
    odm_db_pass=conf.ReadConfigFile.read(PROJECT,'odm_db_pass')
    odm_db_user=conf.ReadConfigFile.read(PROJECT,'odm_db_user')
    while(test== False):
        ssf_statusfromodm= select_request(db_host, 'odm_db', 'odm' , odm_db_user ,odm_db_pass, 'sf_status', 'asset_shipment_file', condition)
        if(len(ssf_statusfromodm)>0):
            current_ssf_statusfromodm=ssf_statusfromodm['sf_status'][0]
            print(current_ssf_statusfromodm)
            if(current_ssf_statusfromodm== 'PENDING_QA' or current_ssf_statusfromodm== 'TERMINATED'or current_ssf_statusfromodm =='PROVISIONED'):
                test = True
                test2 = True
                exit
            elif(current_ssf_statusfromodm== 'REJECTED'):
                test = True
                test2 = False
                exit
        exit
    return test2

def get_dc_ssf_status(PROJECT, ssf_name):
    ssf_id= "'"+str(ssf_name)+"'"
    condition= "file_name="+ssf_id
    test= False
    test2= False
    db_host= conf.ReadConfigFile.read(PROJECT,'db_host')
    oem_db_pass=conf.ReadConfigFile.read(PROJECT,'oem_db_pass')
    oem_db_user=conf.ReadConfigFile.read(PROJECT,'oem_db_user')
    while(test== False):
        ssf_statusfromoem= select_request(db_host, 'oem_db', 'oem' , oem_db_user ,oem_db_pass, 'status', 'oem_asset_shipment_file', condition)
        if(len(ssf_statusfromoem)>0):
            current_ssf_statusfromoem=ssf_statusfromoem['status'][0]
            print(current_ssf_statusfromoem)
            if(current_ssf_statusfromoem== 'PENDING_QA' or current_ssf_statusfromoem== 'TERMINATED'):
                test = True
                test2 = True
                exit
            elif(current_ssf_statusfromoem== 'REJECTED' or current_ssf_statusfromoem=='REJECTED_BY_KMS'):
                test = True
                test2 = False
                exit
        exit
    return test2

def get_ssf_status_fluvius(PROJECT, ssf_name):
    ssf_id= "'"+str(ssf_name)+"'"
    condition= "file_name="+ssf_id
    test= False
    test2= False
    db_host= conf.ReadConfigFile.read(PROJECT,'db_host')
    odm_db_pass=conf.ReadConfigFile.read(PROJECT,'odm_db_pass')
    odm_db_user=conf.ReadConfigFile.read(PROJECT,'odm_db_user')
    while(test== False):
        ssf_statusfromodm= select_request(db_host, 'odm_db_2', 'odm' , odm_db_user ,odm_db_pass, 'sf_status', 'asset_shipment_file', condition)
        if(len(ssf_statusfromodm)>0):
            current_ssf_statusfromodm=ssf_statusfromodm['sf_status'][0]
            print(current_ssf_statusfromodm)
            if(current_ssf_statusfromodm== 'PENDING_QA' or current_ssf_statusfromodm== 'TERMINATED'):
                test = True
                test2 = True
                exit
            elif(current_ssf_statusfromodm== 'REJECTED'):
                test = True
                test2 = False
                exit
        exit
    return test2

def count_meters_from_db():
    db_host= conf.ReadConfigFile.read(PROJECT,'db_host')
    odm_db_pass=conf.ReadConfigFile.read(PROJECT,'odm_db_pass')
    odm_db_user=conf.ReadConfigFile.read(PROJECT,'odm_db_user')
    conn = psycopg2.connect(host=db_host ,database='odm_db', user=odm_db_user, password=odm_db_pass)
    cursor = conn.cursor()
    print("select count(*) from odm.metering_meter")
    cursor.execute("select count(*) from odm.metering_meter")
    output = DataFrame(cursor.fetchall())
    print(output)
    if len(output)>0:
        output.columns =  [x.name for x in cursor.description ]
        print(output)
        return output['count'][0]
    else:
        return 0

def verify_campaign_status(PROJECT,odm_db, table, camp_name):
    camp_status=""
    db_host= conf.ReadConfigFile.read(PROJECT,'db_host')
    odm_db_pass=conf.ReadConfigFile.read(PROJECT,'odm_db_pass')
    odm_db_user=conf.ReadConfigFile.read(PROJECT,'odm_db_user')
    conn = psycopg2.connect(host=db_host ,database=odm_db, user=odm_db_user, password=odm_db_pass)
    cursor = conn.cursor()
    condition= "name='"+str(camp_name)+"'"
    while True:
        camp_status= select_request(db_host, odm_db, 'odm' , odm_db_user ,odm_db_pass, 'status', table, condition)
        camp_status=camp_status['status'][0]
        if camp_status != 'IN_PROGRESS' :
            if camp_status== 'SUCCEEDED' or  camp_status== 'DONE' :
                output=camp_status
                break
            elif camp_status== 'FAILED' or camp_status== 'PARTIALLY FAILED' or  camp_status== "PARTIALLYFAILED":
                break
        time.sleep(60)
    return camp_status

def get_db_campaign_status(PROJECT,odm_db, table, camp_name):
    camp_status=""
    db_host= conf.ReadConfigFile.read(PROJECT,'db_host')
    odm_db_pass=conf.ReadConfigFile.read(PROJECT,'odm_db_pass')
    odm_db_user=conf.ReadConfigFile.read(PROJECT,'odm_db_user')
    conn = psycopg2.connect(host=db_host ,database=odm_db, user=odm_db_user, password=odm_db_pass)
    cursor = conn.cursor()
    condition= "name='"+str(camp_name)+"'"
    camp_status= select(PROJECT,odm_db,'odm','odm_db_user','odm_db_pass','status',table, condition )
    # camp_status= select(db_host, odm_db, 'odm' , odm_db_user ,odm_db_pass, 'status', table, condition)
    # camp_status=camp_status['status'][0]
    camp_id= select(PROJECT,odm_db,'odm','odm_db_user','odm_db_pass','id',table, condition )
    # camp_id= select(db_host, odm_db, 'odm' , odm_db_user ,odm_db_pass, 'id', table, condition)
    # camp_id=camp_id['status'][0]

    return camp_status, camp_id

def verify_delivery_param_in_odm(PROJECT,db_name, meter_id , data):
    test=True
    for i in range(len(data[0])):
        condition=  'mrid = '+"'"+ meter_id + '_'+data[0][i]+"'"
        output=select(PROJECT,db_name,'odm','odm_db_user','odm_db_pass','current_value','metering_meter_config_param_info', condition )
        if output != data[1][i]:
            test=False
            break
    return test
def verify_delivery_param_in_m2m(PROJECT, meter_id , data):
    validation=True
    test=False
    conditionFC='mrid = '+"'"+str(meter_id)+"'"
    if PROJECT=='FLUVIUS':
        meter_function_class=select(PROJECT,'odm_db_2','odm','odm_db_user','odm_db_pass','function_class','asset_meter', conditionFC )
    else:

        meter_function_class=select(PROJECT,'odm_db','odm','odm_db_user','odm_db_pass','function_class','metering_meter', conditionFC )
        print("meter_function_class :", meter_function_class)
    data_on=[]
    for i in range(len(data[0])):
        if data[1][i]=='1':
            data_on.append(data[0][i]+"_"+meter_function_class+"_SLA1")
    #condition=  'mrid = '+"'"+ meter_id + '_'+data[0][i]+"'"
    SQL= "SELECT m2m_schema.m2m_group.group_id FROM m2m_schema.m2m_device_group  join m2m_schema.m2m_group on m2m_schema.m2m_device_group.group_id =id where device_id=(select id from m2m_schema.m2m_device where device_id='"+str(meter_id) +"')"
#    SQL="select is_response_received from odm.inputs where mrid ='"+mrid+"'  and correlation_id='"+messageID+"'"
    db_host= conf.ReadConfigFile.read(PROJECT,'db_host')
    m2m_db_user=conf.ReadConfigFile.read(PROJECT,'m2m_db_user')
    m2m_db_pass=conf.ReadConfigFile.read(PROJECT,'m2m_db_pass')

    conn = psycopg2.connect(host=db_host ,database='m2m_db', user=m2m_db_user, password=m2m_db_pass)


    cursor = conn.cursor()
    cursor.execute(SQL)
    result_m2m = DataFrame(cursor.fetchall())
    #print(result_m2m)
    if len(result_m2m)>0:
        result_m2m.columns =  [x.name for x in cursor.description ]
    print(result_m2m)
    result_m2m= result_m2m['group_id']


    result_m2m_final=[]
    for i in range(len(result_m2m)):
        # if result_m2m[i] not in data.unique():
        #     test =False
        #     break
        result_m2m_final.append(result_m2m[i])
    print("result_m2m", result_m2m_final)
    print("data_on", data_on)
    for i in range(len(data_on)):
        if data[1][i] =='Off':
            for j in range(len(result_m2m_final)):
                print("check validation")
                print(result_m2m_final[j][0:len(data_on[i])])
                print(data_on[i])
                if data_on[i] == result_m2m_final[j][0:len(data_on[i])]:
                    validation = False
                    break
        else:
            if data_on[i] not in result_m2m_final:
                validation = False
                break
    return validation


def verify_delivery_param_in_VSDC_P2P(PROJECT, meter_id , data):
    test=False
    validation=True
    conditionFC='mrid = '+"'"+str(meter_id)+"'"
    meter_function_class=select(PROJECT,'odm_db','odm','odm_db_user','odm_db_pass','function_class','metering_meter', conditionFC )
    LDN=select(PROJECT,'odm_db','odm','odm_db_user','odm_db_pass','ldn','metering_meter', conditionFC )
    data_on=[]
    for i in range(len(data[0])):
        if data[1][i]=='1':
            data_on.append(data[0][i]+"_"+meter_function_class+"_SLA1")
    #condition=  'mrid = '+"'"+ meter_id + '_'+data[0][i]+"'"
    #SQL= "SELECT m2m_schema.m2m_group.group_id FROM m2m_schema.m2m_device_group  join m2m_schema.m2m_group on m2m_schema.m2m_device_group.group_id =id where device_id=(select id from m2m_schema.m2m_device where device_id='"+str(meter_id) +"')"
    SQL="SELECT vsdc_p2p.vsdc_group.group_id FROM vsdc_p2p.vsdc_device_group  join vsdc_p2p.vsdc_group on vsdc_p2p.vsdc_device_group.group_id = vsdc_p2p.vsdc_group.id where device_id=(select id from vsdc_p2p.vsdc_device where device_id='"+LDN+"')"
    db_host= conf.ReadConfigFile.read(PROJECT,'db_host')
    vsdc_p2p_db_user=conf.ReadConfigFile.read(PROJECT,'vsdc_p2p_db_user')
    vsdc_p2p_db_pass=conf.ReadConfigFile.read(PROJECT,'vsdc_p2p_db_pass')

    conn = psycopg2.connect(host=db_host ,database='vsdc_p2p_db', user=vsdc_p2p_db_user, password=vsdc_p2p_db_pass)


    cursor = conn.cursor()
    cursor.execute(SQL)
    result_vsdc_p2p = DataFrame(cursor.fetchall())
    #print(result_vsdc_p2p)
    if len(result_vsdc_p2p)>0:
        result_vsdc_p2p.columns =  [x.name for x in cursor.description ]
    print(result_vsdc_p2p)
    result_vsdc_p2p= result_vsdc_p2p['group_id']


    result_vsdc_p2p_final=[]
    for i in range(len(result_vsdc_p2p)):
        # if result_vsdc_p2p[i] not in data.unique():
        #     test =False
        #     break
        result_vsdc_p2p_final.append(result_vsdc_p2p[i])
    print("result_vsdc_p2p", result_vsdc_p2p_final)
    print("data_on", data_on)
    for i in range(len(data_on)):
        if data[1][i] =='Off':
            for j in range(len(result_vsdc_p2p_final)):
                print("check validation")
                print(result_vsdc_p2p_final[j][0:len(data_on[i])])
                print(data_on[i])
                if data_on[i] == result_vsdc_p2p_final[j][0:len(data_on[i])]:
                    validation = False
                    break
        else:
            if data_on[i] not in result_vsdc_p2p_final:
                validation = False
                break
    return validation

def verify_delivery_param_in_VSDC_PLC(PROJECT, meter_id , data):
    test=False
    validation=True
    conditionFC='mrid = '+"'"+str(meter_id)+"'"
    meter_function_class=select(PROJECT,'odm_db','odm','odm_db_user','odm_db_pass','function_class','metering_meter', conditionFC )
    LDN=select(PROJECT,'odm_db','odm','odm_db_user','odm_db_pass','ldn','metering_meter', conditionFC )
    data_on=[]
    for i in range(len(data[0])):
        if data[1][i]=='1':
            data_on.append(data[0][i]+"_"+meter_function_class+"_SLA1")
    #condition=  'mrid = '+"'"+ meter_id + '_'+data[0][i]+"'"
    #SQL= "SELECT m2m_schema.m2m_group.group_id FROM m2m_schema.m2m_device_group  join m2m_schema.m2m_group on m2m_schema.m2m_device_group.group_id =id where device_id=(select id from m2m_schema.m2m_device where device_id='"+str(meter_id) +"')"
    SQL="SELECT vsdc.vsdc_group.group_id FROM vsdc.vsdc_device_group  join vsdc.vsdc_group on vsdc.vsdc_device_group.group_id = vsdc.vsdc_group.id where device_id=(select id from vsdc.vsdc_device where device_id='"+LDN+"')"
    db_host= conf.ReadConfigFile.read(PROJECT,'db_host')
    vsdc_db_user=conf.ReadConfigFile.read(PROJECT,'vsdc_db_user')
    vsdc_db_pass=conf.ReadConfigFile.read(PROJECT,'vsdc_db_pass')

    conn = psycopg2.connect(host=db_host ,database='vsdc_db', user=vsdc_db_user, password=vsdc_db_pass)


    cursor = conn.cursor()
    cursor.execute(SQL)
    result_vsdc = DataFrame(cursor.fetchall())
    #print(result_vsdc)
    if len(result_vsdc)>0:
        result_vsdc.columns =  [x.name for x in cursor.description ]
    print(result_vsdc)
    result_vsdc= result_vsdc['group_id']


    result_vsdc_final=[]
    for i in range(len(result_vsdc)):
        # if result_vsdc[i] not in data.unique():
        #     test =False
        #     break
        result_vsdc_final.append(result_vsdc[i])
    print("result_vsdc", result_vsdc_final)
    print("data_on", data_on)
    for i in range(len(data_on)):
        if data[1][i] =='Off':
            for j in range(len(result_vsdc_final)):
                print("check validation")
                print(result_vsdc_final[j][0:len(data_on[i])])
                print(data_on[i])
                if data_on[i] == result_vsdc_final[j][0:len(data_on[i])]:
                    validation = False
                    break
        else:
            if data_on[i] not in result_vsdc_final:
                validation = False
                break
    return validation

def get_meters_in_collection(PROJECT,collect_id):
    try:


        result_m2m=[]
        task_type=[]
        db_host= conf.ReadConfigFile.read(PROJECT,'db_host')
        m2m_db_pass=conf.ReadConfigFile.read(PROJECT,'m2m_db_pass')
        m2m_db_user=conf.ReadConfigFile.read(PROJECT,'m2m_db_user')

        conn = psycopg2.connect(host=db_host ,database='m2m_db', user=m2m_db_user, password=m2m_db_pass)
        cursor = conn.cursor()

        SQL1="SELECT task_type FROM m2m_schema.m2m_task where task_id ='"+ collect_id+"'"
        cursor.execute(SQL1)
        task_type = DataFrame(cursor.fetchall())
        if len(task_type)>0:
            task_type.columns =  [x.name for x in cursor.description ]
        print("task_type", task_type['task_type'][0])
        task_type=task_type['task_type'][0]
        if task_type =='COLLECT_GROUP':
            SQL="select m2m_schema.m2m_device.device_id  from(select *from (SELECT  task_id, m2m_schema.m2m_group.group_id, m2m_schema.m2m_task.destination,task_type, m2m_schema.m2m_group.id FROM m2m_schema.m2m_task join  m2m_schema.m2m_group  on m2m_schema.m2m_task.group_id = m2m_schema.m2m_group.id where task_id='"+collect_id +"') data join m2m_schema.m2m_device_group on m2m_schema.m2m_device_group.group_id= data.id )data2 join  m2m_schema.m2m_device  on m2m_schema.m2m_device.id = data2.device_id"

            cursor.execute(SQL)

            result_m2m = DataFrame(cursor.fetchall())

            if len(result_m2m)>0:
                result_m2m.columns =  [x.name for x in cursor.description ]

            cursor.close()
            conn.close()
            result_m2m=result_m2m['device_id']
            print(result_m2m)
        elif task_type =='COLLECT_DEVICES':
            SQL="select m2m_schema.m2m_device.device_id from( SELECT m2m_schema.m2m_device_task.device_id FROM m2m_schema.m2m_task join m2m_schema.m2m_device_task on m2m_schema.m2m_device_task.task_id = m2m_schema.m2m_task.id where m2m_schema.m2m_task.task_id='"+collect_id +"' )data join m2m_schema.m2m_device on m2m_schema.m2m_device.id = data.device_id"
            cursor.execute(SQL)

            result_m2m = DataFrame(cursor.fetchall())

            if len(result_m2m)>0:
                result_m2m.columns =  [x.name for x in cursor.description ]

            cursor.close()
            conn.close()
            result_m2m=result_m2m['device_id']
            print(result_m2m)
        return 200, result_m2m.values.tolist()

    except Exception as e:
        return 500,[]

def check_collect_in_m2m_by_taskid(task_id, period, initial_meters_list):


    return True


def check_exixting_tasks_in_m2m(PROJECT , meter_id):
    print("meter id : ", meter_id)
    if meter_id != None :
        test_status=200
        test_tasks =500
        reason=""
        db_host= conf.ReadConfigFile.read(PROJECT,'db_host')
        db_pass=conf.ReadConfigFile.read(PROJECT, 'm2m_db_pass')
        db_user=conf.ReadConfigFile.read(PROJECT,'m2m_db_user')

        SQL= "SELECT id,status FROM m2m_schema.m2m_device where id ="+str(meter_id)
        conn = psycopg2.connect(host=db_host ,database='m2m_db', user=db_user, password=db_pass)
        cursor = conn.cursor()
        cursor.execute(SQL)
        result_m2m = DataFrame(cursor.fetchall())
        if len(result_m2m)>0:
            result_m2m.columns =  [x.name for x in cursor.description ]
            if result_m2m['status'][0]!= 'DELETED':
                test_status =500

        if test_status ==200:
            print(meter_id)
            SQL= "SELECT id FROM m2m_schema.m2m_device_task where device_id="+str(meter_id)
            cursor = conn.cursor()
            cursor.execute(SQL)
            result_m2m_tasks = DataFrame(cursor.fetchall())
            if len(result_m2m_tasks)==0:
                SQL2= "SELECT m2m_schema.m2m_group.group_id FROM m2m_schema.m2m_device_group  join m2m_schema.m2m_group on m2m_schema.m2m_device_group.group_id =id where device_id="+str(meter_id)
                cursor2 = conn.cursor()
                cursor2.execute(SQL2)
                result_m2m_groups = DataFrame(cursor2.fetchall())
                if len(result_m2m_groups)==0:
                    test_tasks=200
                    reason ="no task related to device in m2m"
                    print( 200, "no task and groups related to device in m2m")

                else:
                    test_tasks = 500
                    reason ="there are groups related to device in m2m"

            else:
                test_tasks = 500
                reason ="there are tasks related to device in m2m"
        else:
            test_tasks = 500
            reason ="meter does not have deleted status in m2m"

        return test_tasks, reason
    else:
        return 200, "device not found in m2m"

def check_exixting_tasks_in_vsdc(PROJECT , meter_id):
    print("meter id : ", meter_id)
    if meter_id != None:
        test_status=200
        test_tasks =500
        reason=""

        db_host= conf.ReadConfigFile.read(PROJECT,'db_host')
        db_pass=conf.ReadConfigFile.read(PROJECT, 'vsdc_db_pass')
        db_user=conf.ReadConfigFile.read(PROJECT,'vsdc_db_user')

        SQL= "SELECT id,administrative_state FROM vsdc.vsdc_device where id ="+str(meter_id)
        conn = psycopg2.connect(host=db_host ,database='vsdc_db', user=db_user, password=db_pass)
        cursor = conn.cursor()
        cursor.execute(SQL)
        result_vsdc = DataFrame(cursor.fetchall())
        if len(result_vsdc)>0:
            result_vsdc.columns =  [x.name for x in cursor.description ]
            if result_vsdc['administrative_state'][0]!= 4:
                test_status =500

        if test_status ==200:
            print(meter_id)
            SQL= "SELECT id FROM vsdc.vsdc_device_task where device_id="+str(meter_id)
            cursor = conn.cursor()
            cursor.execute(SQL)
            result_vsdc_tasks = DataFrame(cursor.fetchall())
            if len(result_vsdc_tasks)==0:
                SQL2= "SELECT vsdc.vsdc_group.group_id FROM vsdc.vsdc_device_group  join vsdc.vsdc_group on vsdc.vsdc_device_group.group_id =id where device_id="+str(meter_id)
                cursor2 = conn.cursor()
                cursor2.execute(SQL2)
                result_vsdc_groups = DataFrame(cursor2.fetchall())
                if len(result_vsdc_groups)==0:
                    test_tasks=200
                    reason ="no task related to device in vsdc"
                    print( 200, "no task and groups related to device in vsdc")

                else:
                    test_tasks = 500
                    reason ="there are groups related to device in vsdc"

            else:
                test_tasks = 500
                reason ="there are tasks related to device in vsdc"
        else:
            test_tasks = 500
            reason ="meter does not have deleted status in vsdc"

        return test_tasks, reason
    else:
        return 200, "device not found in vsdc"


def get_mbus_channel(PROJECT , meter_id):

    db_host= conf.ReadConfigFile.read(PROJECT,'db_host')
    db_pass=conf.ReadConfigFile.read(PROJECT, 'odm_db_pass')
    db_user=conf.ReadConfigFile.read(PROJECT,'odm_db_user')
    SQL="SELECT amr_router,  mbus_meter_channel, energy_type FROM odm.metering_north_com_function where metering_meter_id= (select id from odm.metering_meter where din='"+str(meter_id)+"')"

    conn = psycopg2.connect(host=db_host ,database='odm_db_2', user=db_user, password=db_pass)
    cursor = conn.cursor()
    cursor.execute(SQL)
    result = DataFrame(cursor.fetchall())
    print(result)
    if len(result)>0:
        print(result)
        result.columns =  [x.name for x in cursor.description ]
        return 200, result['amr_router'][0], result['mbus_meter_channel'][0],result['energy_type'][0]
    else:
        return 500, '','',''

def check_task_mbus_in_m2m(PROJECT , amr_router , channel, energy_type):
    if amr_router != None:
        db_host= conf.ReadConfigFile.read(PROJECT,'db_host')
        db_pass=conf.ReadConfigFile.read(PROJECT, 'm2m_db_pass')
        db_user=conf.ReadConfigFile.read(PROJECT,'m2m_db_user')
        validation =True
        # SQL= "SELECT id FROM m2m.m2m_device where device_id='"+str(amr_router)+"'"
        conn = psycopg2.connect(host=db_host ,database='m2m_db', user=db_user, password=db_pass)
        # cursor = conn.cursor()
        # cursor.execute(SQL)
        # result_m2m_device_technical_id = DataFrame(cursor.fetchall())
        # if len(result_m2m_device_technical_id)==0:
        SQL= "SELECT m2m_schema.m2m_group.group_id FROM m2m_schema.m2m_device_group join m2m_schema.m2m_group on m2m_schema.m2m_device_group.group_id =id where device_id=(select id from m2m_schema.m2m_device where device_id='"+str(amr_router)+"')"
        cursor = conn.cursor()
        cursor.execute(SQL)
        result_m2m_tasks = DataFrame(cursor.fetchall())
        if len(result_m2m_tasks)==0:
            return 200, validation, "no tasks found on parent device"
        else:
            for i in range(len(result_m2m_tasks)):
                print("hello")
                print(result_m2m_tasks[0][i])
                print(result_m2m_tasks[0][i][0:7])
                if result_m2m_tasks[0][i][0:7] == energy_type+"_CH"+str(channel):
                    print(result_m2m_tasks[0][i][0:7])
                    validation = False
                    break
            return 200, validation, "there are tasks but not on current channel"
    else:
        return 200, True, "device not associated to elec meter"
    # else:
    #     return 500, "device found in m2m"



def check_task_mbus_in_vsdc(PROJECT , amr_router , channel, energy_type):

    if amr_router != None:
        db_host= conf.ReadConfigFile.read(PROJECT,'db_host')
        odm_db_pass=conf.ReadConfigFile.read(PROJECT, 'odm_db_pass')
        odm_db_user=conf.ReadConfigFile.read(PROJECT,'odm_db_user')

        vsdc_db_pass=conf.ReadConfigFile.read(PROJECT, 'vsdc_db_pass')
        vsdc_db_user=conf.ReadConfigFile.read(PROJECT,'vsdc_db_user')
        validation =True
        odm_sql= "SELECT ldn FROM odm.metering_meter where din='"+str(amr_router)+"'"
        conn = psycopg2.connect(host=db_host ,database='odm_db_2', user=odm_db_user, password=odm_db_pass)
        cursor = conn.cursor()
        cursor.execute(odm_sql)
        result_odm = DataFrame(cursor.fetchall())
        amr_router_ldn=result_odm[0][0]
        cursor.close()
        conn.close()

        conn = psycopg2.connect(host=db_host ,database='vsdc_db', user=vsdc_db_user, password=vsdc_db_pass)
        # cursor = conn.cursor()
        # cursor.execute(SQL)
        # result_m2m_device_technical_id = DataFrame(cursor.fetchall())
        # if len(result_m2m_device_technical_id)==0:

        SQL= "SELECT vsdc.vsdc_group.group_id FROM vsdc.vsdc_device_group  join vsdc.vsdc_group on vsdc.vsdc_device_group.group_id = vsdc.vsdc_group.id where device_id=(select id from vsdc.vsdc_device where device_id='"+str(amr_router_ldn)+"')"
        cursor = conn.cursor()
        cursor.execute(SQL)
        result_m2m_tasks = DataFrame(cursor.fetchall())
        cursor.close()
        conn.close()
        if len(result_m2m_tasks)==0:
            return 200, validation, "no tasks found on parent device"
        else:
            for i in range(len(result_m2m_tasks)):
                print("hello")
                print(result_m2m_tasks[0][i])
                print(result_m2m_tasks[0][i][0:7])
                if result_m2m_tasks[0][i][0:7] == energy_type+"_CH"+str(channel):
                    print(result_m2m_tasks[0][i][0:7])
                    validation = False
                    break
            return 200, validation, "there are tasks but not on current channel"
    else:
        return 200, True, "device not associated to elec meter"
    # else:
    #     return 500, "device found in m2m"




def verify_delivery_param_in_m2mFLUVIES(PROJECT, meter_id , data, prefix ):
    validation=True
    data_on=[]
    for i in range(len(data[0])):
        if data[1][i]!= 'Off':
            data_on.append(prefix+data[0][i]+"_SLA"+str(data[1][i]))
        else:
            data_on.append(prefix+data[0][i])
    #condition=  'mrid = '+"'"+ meter_id + '_'+data[0][i]+"'"
    SQL= "SELECT m2m_schema.m2m_group.group_id FROM m2m_schema.m2m_device_group  join m2m_schema.m2m_group on m2m_schema.m2m_device_group.group_id =id where device_id=(select id from m2m_schema.m2m_device where device_id='"+str(meter_id) +"')"
#    SQL="select is_response_received from odm.inputs where mrid ='"+mrid+"'  and correlation_id='"+messageID+"'"
    db_host= conf.ReadConfigFile.read(PROJECT,'db_host')
    m2m_db_user=conf.ReadConfigFile.read(PROJECT,'m2m_db_user')
    m2m_db_pass=conf.ReadConfigFile.read(PROJECT,'m2m_db_pass')

    conn = psycopg2.connect(host=db_host ,database='m2m_db', user=m2m_db_user, password=m2m_db_pass)


    cursor = conn.cursor()
    cursor.execute(SQL)
    result_m2m = DataFrame(cursor.fetchall())
    #print(result_m2m)
    if len(result_m2m)>0:
        result_m2m.columns =  [x.name for x in cursor.description ]
        print(result_m2m)
        result_m2m= result_m2m['group_id']


    result_m2m_final=[]
    for i in range(len(result_m2m)):
        # if result_m2m[i] not in data.unique():
        #     test =False
        #     break
        result_m2m_final.append(result_m2m[i])
    print("result_m2m", result_m2m_final)
    print("data_on", data_on)

    for i in range(len(data_on)):
        if data[1][i] =='Off':
            for j in range(len(result_m2m_final)):
                print("check validation")
                print(result_m2m_final[j][0:len(data_on[i])])
                print(data_on[i])
                if data_on[i] == result_m2m_final[j][0:len(data_on[i])]:
                    validation = False
                    break
        else:
            if data_on[i] not in result_m2m_final:
                validation = False
                break
    return validation



def verify_delivery_param_in_vsdcFLUVIES(PROJECT, meter_id , data,prefix):
    validation=True
    conditionFC='mrid = '+"'"+str(meter_id)+"'"
    db_host= conf.ReadConfigFile.read(PROJECT,'db_host')
    odm_db_pass=conf.ReadConfigFile.read(PROJECT, 'odm_db_pass')
    odm_db_user=conf.ReadConfigFile.read(PROJECT,'odm_db_user')
    odm_sql= "SELECT ldn FROM odm.metering_meter where din='"+str(meter_id)+"'"
    if PROJECT=='FLUVIUS':
        conn = psycopg2.connect(host=db_host ,database='odm_db_2', user=odm_db_user, password=odm_db_pass)
    else:
        conn = psycopg2.connect(host=db_host ,database='odm_db', user=odm_db_user, password=odm_db_pass)
    cursor = conn.cursor()
    cursor.execute(odm_sql)
    result_odm = DataFrame(cursor.fetchall())
    meter_ldn=result_odm[0][0]
    data_on=[]
    for i in range(len(data[0])):
        if data[1][i]!= 'Off':
            data_on.append(prefix+data[0][i]+"_SLA"+str(data[1][i]))
        else:
            data_on.append(prefix+data[0][i])
    #condition=  'mrid = '+"'"+ meter_id + '_'+data[0][i]+"'"
    # SQL= "SELECT vsdc.vsdc_group.group_id FROM vsdc.vsdc_device_group  join vsdc.vsdc_group on vsdc.vsdc_device_group.group_id = id where device_id=(select id from vsdc.vsdc_device where device_id='"+str(meter_id) +"')"
    SQL="SELECT vsdc.vsdc_group.group_id FROM vsdc.vsdc_device_group  join vsdc.vsdc_group on vsdc.vsdc_device_group.group_id = vsdc.vsdc_group.id where device_id=(select id from vsdc.vsdc_device where device_id='"+meter_ldn+"')"

#    SQL="select is_response_received from odm.inputs where mrid ='"+mrid+"'  and correlation_id='"+messageID+"'"
    db_host= conf.ReadConfigFile.read(PROJECT,'db_host')
    vsdc_db_user=conf.ReadConfigFile.read(PROJECT,'vsdc_db_user')
    vsdc_db_pass=conf.ReadConfigFile.read(PROJECT,'vsdc_db_pass')

    conn = psycopg2.connect(host=db_host ,database='vsdc_db', user=vsdc_db_user, password=vsdc_db_pass)


    cursor = conn.cursor()
    cursor.execute(SQL)
    result_vsdc = DataFrame(cursor.fetchall())
    #print(result_vsdc)
    if len(result_vsdc)>0:
        result_vsdc.columns =  [x.name for x in cursor.description ]
    print(result_vsdc)
    result_vsdc= result_vsdc['group_id']


    result_vsdc_final=[]
    for i in range(len(result_vsdc)):
        # if result_vsdc[i] not in data.unique():
        #     test =False
        #     break
        result_vsdc_final.append(result_vsdc[i])
    print("result_vsdc", result_vsdc_final)
    print("data_on", data_on)

    for i in range(len(data_on)):
        if data[1][i] =='Off':
            for j in range(len(result_vsdc_final)):
                print("check validation")
                print(result_vsdc_final[j][0:len(data_on[i])])
                print(data_on[i])
                if data_on[i] == result_vsdc_final[j][0:len(data_on[i])]:
                    validation = False
                    break
        else:
            if data_on[i] not in result_vsdc_final:
                validation = False
                break
    return validation


def check_rlc(PROJECT , meter_id, db_name):

    db_host= conf.ReadConfigFile.read(PROJECT,'db_host')
    db_pass=conf.ReadConfigFile.read(PROJECT, 'odm_db_pass')
    db_user=conf.ReadConfigFile.read(PROJECT,'odm_db_user')
    SQL="SELECT is_response_received, reception_timestamp FROM odm.inputs where mrid ='"+ str(meter_id)+ "' and input_type= 'READ_LOCAL_CONFIG' order by id"


    conn = psycopg2.connect(host=db_host ,database=db_name, user=db_user, password=db_pass)
    cursor = conn.cursor()
    cursor.execute(SQL)
    result = DataFrame(cursor.fetchall())
    print(result)
    if len(result)>0:
        print(result)
        result.columns =  [x.name for x in cursor.description ]
        last_rlc_status = result['is_response_received'][len(result['is_response_received'])-1]
        last_rlc_date = result['reception_timestamp'][len(result['reception_timestamp'])-1]
        # date_time_obj = datetime.datetime.strptime(last_rlc_date.isoformat(), '%Y-%m-%d %H:%M:%S')
        dt = datetime.datetime.now()
        shift = datetime.timedelta(minutes=3)
        past = dt - shift
        past=past.isoformat()
        futur = dt + shift
        futur=futur.isoformat()
        if last_rlc_date.isoformat() > past and last_rlc_date.isoformat() < futur:
            validation= True
        else:
            validation= False
    else:
        validation= False
    return validation
def check_activation(PROJECT , meter_id, db_name):

    db_host= conf.ReadConfigFile.read(PROJECT,'db_host')
    db_pass=conf.ReadConfigFile.read(PROJECT, 'odm_db_pass')
    db_user=conf.ReadConfigFile.read(PROJECT,'odm_db_user')
    SQL="SELECT is_response_received, reception_timestamp FROM odm.inputs where mrid ='"+ str(meter_id)+ "' and input_type= 'ACTIVATION' order by id"


    conn = psycopg2.connect(host=db_host ,database=db_name, user=db_user, password=db_pass)
    cursor = conn.cursor()
    cursor.execute(SQL)
    result = DataFrame(cursor.fetchall())
    print(result)
    if len(result)>0:
        print(result)
        result.columns =  [x.name for x in cursor.description ]
        last_rlc_status = result['is_response_received'][len(result['is_response_received'])-1]
        last_rlc_date = result['reception_timestamp'][len(result['reception_timestamp'])-1]
        # date_time_obj = datetime.datetime.strptime(last_rlc_date.isoformat(), '%Y-%m-%d %H:%M:%S')
        dt = datetime.datetime.now()
        shift = datetime.timedelta(minutes=3)
        past = dt - shift
        past=past.isoformat()
        futur = dt + shift
        futur=futur.isoformat()
        if last_rlc_date.isoformat() > past and last_rlc_date.isoformat() < futur:
            validation= True
        else:
            validation= False
    else:
        validation= False
    return validation


def DB_Param_Validation(PROJECT,db_name ,  meter_id: str, param_name: list, param_value: list):
    test=True
    for i in range(len(param_name)):
        condition = "mrid='" +str(meter_id) +"_"+param_name[i]+"'"
        output=select(PROJECT,db_name,'odm','odm_db_user','odm_db_pass','current_value','metering_meter_config_param_info', condition )
        print("output db : " , output)
        if output != param_value[i]:
            test =False
            break
    return test
def change_meter_status(PROJECT ,db_name, meter_id, status):
    try:
        db_host= conf.ReadConfigFile.read(PROJECT,'db_host')
        db_pass=conf.ReadConfigFile.read(PROJECT, 'odm_db_pass')
        db_user=conf.ReadConfigFile.read(PROJECT,'odm_db_user')
        SQL="UPDATE odm.metering_meter SET status ='"+status+"' WHERE din='"+str(meter_id)+ "'"
        # SQL ="UPDATE odm.metering_meter SET status ='DISCOVERED' WHERE din='1SAG3100009615'"
        conn = psycopg2.connect(host=db_host ,database=db_name, user=db_user, password=db_pass)
        cursor = conn.cursor()
        cursor.execute(SQL)
        conn.commit()
        cursor.close()
        conn.close()
        return 200
    except Exception as e:
        raise Exception(e)
        return 500
def delete_meter_from_metering_meter_db(PROJECT ,db_name, meter_id):
    try:
        db_host= conf.ReadConfigFile.read(PROJECT,'db_host')
        db_pass=conf.ReadConfigFile.read(PROJECT, 'odm_db_pass')
        db_user=conf.ReadConfigFile.read(PROJECT,'odm_db_user')
        SQL="DELETE from odm.metering_meter WHERE din='"+str(meter_id)+ "'"
        # SQL ="UPDATE odm.metering_meter SET status ='DISCOVERED' WHERE din='1SAG3100009615'"
        conn = psycopg2.connect(host=db_host ,database=db_name, user=db_user, password=db_pass)
        cursor = conn.cursor()
        cursor.execute(SQL)
        conn.commit()
        cursor.close()
        conn.close()
        return 200
    except Exception as e:
        raise Exception(e)
        return 500

def date_by_adding_business_daysold(from_date, add_days):
    utc = pytz.timezone("UTC")
    europetz = pytz.timezone('Europe/Paris')
    from_date_uts_time= from_date.astimezone(utc)
    from_date_local_time = from_date.astimezone(europetz)
    from_date_uts_timestr = datetime.datetime.strftime(from_date_uts_time, "%Y-%m-%dT%H:%M:%S")
    from_date_uts_timeobj = datetime.datetime.strptime(from_date_uts_timestr, "%Y-%m-%dT%H:%M:%S")
    from_date_local_timestr = datetime.datetime.strftime(from_date_local_time, "%Y-%m-%dT%H:%M:%S")
    from_date_local_timeobj = datetime.datetime.strptime(from_date_local_timestr, "%Y-%m-%dT%H:%M:%S")
    out_shift_start=from_date_local_timeobj- from_date_uts_timeobj
    out_shift_start=out_shift_start.total_seconds() / 3600

    business_days_to_add = add_days
    current_date = from_date
    while business_days_to_add > 0:
        current_date += datetime.timedelta(days=1)
        weekday = current_date.weekday()
        # if weekday >= 5: # sunday = 6
        #     continue
        business_days_to_add -= 1
    current_date_uts_time= current_date.astimezone(utc)
    current_date_local_time = current_date.astimezone(europetz)
    current_date_uts_timestr = datetime.datetime.strftime(current_date_uts_time, "%Y-%m-%dT%H:%M:%S")
    current_date_uts_timeobj = datetime.datetime.strptime(current_date_uts_timestr, "%Y-%m-%dT%H:%M:%S")
    current_date_local_timestr = datetime.datetime.strftime(current_date_local_time, "%Y-%m-%dT%H:%M:%S")
    current_date_local_timeobj = datetime.datetime.strptime(current_date_local_timestr, "%Y-%m-%dT%H:%M:%S")
    out_shift_end=current_date_local_timeobj- current_date_uts_timeobj
    out_shift_end=out_shift_end.total_seconds() / 3600
    output_shift_end_start = out_shift_end -out_shift_start

    shift =datetime.timedelta(hours=output_shift_end_start)
    current_date=current_date +shift
    return current_date
def date_by_adding_business_days(from_date, add_days):
    utc = pytz.timezone("UTC")
    europetz = pytz.timezone('Europe/Paris')
    from_date_uts_time= from_date.astimezone(utc)
    from_date_local_time = from_date.astimezone(europetz)
    from_date_uts_timestr = datetime.datetime.strftime(from_date_uts_time, "%Y-%m-%dT%H:%M:%S")
    from_date_uts_timeobj = datetime.datetime.strptime(from_date_uts_timestr, "%Y-%m-%dT%H:%M:%S")
    from_date_local_timestr = datetime.datetime.strftime(from_date_local_time, "%Y-%m-%dT%H:%M:%S")
    from_date_local_timeobj = datetime.datetime.strptime(from_date_local_timestr, "%Y-%m-%dT%H:%M:%S")
    out_shift_start=from_date_local_timeobj- from_date_uts_timeobj
    out_shift_start=out_shift_start.total_seconds() / 3600

    business_days_to_add = add_days
    current_date = from_date
    while business_days_to_add > 0:
        current_date += datetime.timedelta(days=1)
        weekday = current_date.weekday()
        if weekday >= 5: # sunday = 6
            continue
        business_days_to_add -= 1
    current_date_uts_time= current_date.astimezone(utc)
    current_date_local_time = current_date.astimezone(europetz)
    current_date_uts_timestr = datetime.datetime.strftime(current_date_uts_time, "%Y-%m-%dT%H:%M:%S")
    current_date_uts_timeobj = datetime.datetime.strptime(current_date_uts_timestr, "%Y-%m-%dT%H:%M:%S")
    current_date_local_timestr = datetime.datetime.strftime(current_date_local_time, "%Y-%m-%dT%H:%M:%S")
    current_date_local_timeobj = datetime.datetime.strptime(current_date_local_timestr, "%Y-%m-%dT%H:%M:%S")
    out_shift_end=current_date_local_timeobj- current_date_uts_timeobj
    out_shift_end=out_shift_end.total_seconds() / 3600
    output_shift_end_start = out_shift_end -out_shift_start

    shift =datetime.timedelta(hours=output_shift_end_start)
    current_date=current_date +shift
    return current_date


def get_job_id_from_cim(PROJECT, task_id):
    condition= "message_id='"+ task_id + "'"
    job_id = select(PROJECT,'metering_db','metering','metering_db_user','metering_db_pass','job_id','metering_job', condition )
    return job_id



def validate_execPriority_and_reqenddate(PROJECT, request_type,task_id, expected_execPriority, expected_recovery_execPriority, shift ):
    validation = True
    condition= "message_id='"+ task_id + "'"
    job_id = select(PROJECT,'metering_db','metering','metering_db_user','metering_db_pass','job_id','metering_job', condition )
    print(job_id)
    req_path = conf.ReadConfigFile.read(PROJECT,'m2m_task_resp_path')
    local_path = conf.ReadConfigFile.read(PROJECT,'project_local_path')
    host = conf.ReadConfigFile.read(PROJECT,'m2m_ip')
    username = conf.ReadConfigFile.read(PROJECT, 'm2m_ip_user')
    password = conf.ReadConfigFile.read(PROJECT, 'm2m_ip_pass')
    port = 22
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, password)

    sftp = ssh.open_sftp()
    sftp.get(req_path + job_id +".xml", local_path +"/"+ job_id +".xml")

    tree = ET.parse(local_path+"/"+ job_id +".xml")
    root = tree.getroot()
    print("execPriority", root.get('execPriority'))
    print("recovery execPriority", root[2][2].get('execPriority'))
    print("start", root[1][0].text)
    print("stop", root[1][1].text)
    execPriority= root.get('execPriority')
    recovery_execPriority=root[2][2].get('execPriority')
    start= root[1][0].text
    stop = root[1][1].text
    if execPriority != expected_execPriority:
        validation= False
    if recovery_execPriority != expected_recovery_execPriority:
        validation= False
    if (float(shift) <24 or request_type =='ODR'):
        print("request with type ODR")
        start_time_obj = datetime.datetime.strptime(start[0:19], "%Y-%m-%dT%H:%M:%S")
        stop_time_obj = datetime.datetime.strptime(stop[0:19], "%Y-%m-%dT%H:%M:%S")
        if float(shift) <24:
            print(stop_time_obj- start_time_obj)
            out_shift = stop_time_obj- start_time_obj
            result=out_shift.total_seconds() / 3600
            print(result, shift)
            print( float(result) != float(shift))
            if float(result) != float(shift):
                validation= False
        else:
            expected_stop_date= date_by_adding_business_daysold(start_time_obj,float(shift)/24)
            out_shift = expected_stop_date- stop_time_obj
            print(out_shift)
            result=out_shift.total_seconds() / 3600
            print("result",result)
            print( float(result) != float(0))
            if float(result) != float(0):
                validation= False
    else:
        print("request with type NOT ODR")
        start_time_obj = datetime.datetime.strptime(start[0:19], "%Y-%m-%dT%H:%M:%S")
        stop_time_obj = datetime.datetime.strptime(stop[0:19], "%Y-%m-%dT%H:%M:%S")
        expected_stop_date= date_by_adding_business_days(start_time_obj,float(shift)/24)
        out_shift = expected_stop_date- stop_time_obj
        print(out_shift)
        result=out_shift.total_seconds() / 3600
        print("result",result)
        print( float(result) != float(0))
        if float(result) != float(0):
            validation= False
    return validation

def check_meter_status(PROJECT ,db_name, meter_id, target_status, timeout):
    status='NOT_ACTIVATED'
    wait=0
    while status != target_status and  wait< int(timeout):

        try:
            db_host= conf.ReadConfigFile.read(PROJECT,'db_host')
            db_pass=conf.ReadConfigFile.read(PROJECT, 'odm_db_pass')
            db_user=conf.ReadConfigFile.read(PROJECT,'odm_db_user')
            SQL="select status from odm.metering_meter WHERE din='"+str(meter_id)+ "'"
            # SQL ="UPDATE odm.metering_meter SET status ='DISCOVERED' WHERE din='1SAG3100009615'"
            conn = psycopg2.connect(host=db_host ,database=db_name, user=db_user, password=db_pass)
            cursor = conn.cursor()
            cursor.execute(SQL)
            output = DataFrame(cursor.fetchall())
            print(output)
            if len(output)>0:
                output.columns =  [x.name for x in cursor.description ]
                status=output['status'][0]

        except Exception as e:
            raise Exception(e)
            return 500
        time.sleep(10)
        wait = wait +1
    conn.close()
    cursor.close()
    if status==target_status:
        return True
    else:
        return False


def check_ssf_exist(PROJECT, odm_db_name , ssf_name):
    condition= "file_name='"+ssf_name+"'"
    ssf_id = select(PROJECT,odm_db_name,'odm','odm_db_user','odm_db_pass','id','asset_shipment_file', condition )
    print(ssf_id)
    if ssf_id==None :
        return True
    else:
        return False
def check_dc_ssf_exist(PROJECT , ssf_name):
    condition= "file_name='"+ssf_name+"'"
    ssf_id = select(PROJECT,'oem_db','oem','oem_db_user','oem_db_pass','id','oem_asset_shipment_file', condition )
    print(ssf_id)
    if ssf_id==None :
        return True
    else:
        return False

def check_vsdc_mapping(PROJECT , din, ldn):
    condition= "din='"+din+"' and ldn = '"+str(ldn)+ "'"
    ldn = select(PROJECT,'vsdc_db','vsdc','vsdc_db_user','vsdc_db_pass','ldn','vsdc_din_mapping', condition )
    print(ldn)
    if ldn==None:
        return False
    else:
        return True

def check_m2m_dc_mapping(PROJECT , din, ldn):
    condition= "customer_id='"+din+"' and ldn = '"+str(ldn)+ "'"
    ldn = select(PROJECT,'m2m_db','m2m_schema','m2m_db_user','m2m_db_pass','ldn','m2m_equipment_mapping', condition )
    print(ldn)
    if ldn==None :
        return False
    else:
        return True


def verify_dc_update_campaign_status(PROJECT, table, camp_name):
    camp_status=""
    db_host= conf.ReadConfigFile.read(PROJECT,'db_host')
    oem_db_pass=conf.ReadConfigFile.read(PROJECT,'oem_db_pass')
    oem_db_user=conf.ReadConfigFile.read(PROJECT,'oem_db_user')
    conn = psycopg2.connect(host=db_host ,database='oem_db', user=oem_db_user, password=oem_db_pass)
    cursor = conn.cursor()
    condition= "name='"+str(camp_name)+"'"
    while True:
        camp_status= select_request(db_host, 'oem_db', 'oem' , oem_db_user ,oem_db_pass, 'status', table, condition)
        camp_status=camp_status['status'][0]
        if camp_status != 'IN_PROGRESS' :
            if camp_status== 'SUCCEEDED' or  camp_status== 'DONE' :
                output=camp_status
                break
            elif camp_status== 'FAILED' or camp_status== 'PARTIALLY FAILED' or  camp_status== "PARTIALLYFAILED" or camp_status =='CANCELLED':
                break
        time.sleep(30)
    return camp_status


def verify_config_upload_status(PROJECT, config_id ):
    time.sleep(30)
    condition=  'config_id = ' "'" +config_id+"'"
    output=select(PROJECT,'oem_db','oem','oem_db_user','oem_db_pass','status','oem_config_file', condition )
    return output

def verify_config_uploaded_in_scape_prod(PROJECT, config_id ):
    time.sleep(10)
    condition=  'name = '+"'" +config_id+"'"
    output=select(PROJECT,'scape','fwk_user','scape_db_user','scape_db_pass','name','gateway_config_set', condition )
    if output==None :
        return False
    else:
        return True

def verify_config_uploaded_in_scape_qa(PROJECT, config_id ):
    time.sleep(10)
    condition=  'name = '+"'" +config_id+"'"
    output=select(PROJECT,'scape_qa','fwk_user','scape_db_user','scape_db_pass','name','gateway_config_set', condition )
    if output==None :
        return False
    else:
        return True

def verify_firmware_uploaded_in_scape_prod(PROJECT, config_id ):
    time.sleep(10)
    condition=  'name = '+"'" +config_id+"'"
    output=select(PROJECT,'scape','fwk_user','scape_db_user','scape_db_pass','name','gateway_bundle_set', condition )
    if output==None :
        return False
    else:
        return True
def verify_firmware_uploaded_in_scape_qa(PROJECT, config_id ):
    time.sleep(10)
    condition=  'name = '+"'" +config_id+"'"
    output=select(PROJECT,'scape_qa','fwk_user','scape_db_user','scape_db_pass','name','gateway_bundle_set', condition )
    if output==None:
        return False
    else:
        return True

def verify_firmware_upload_status(PROJECT, firmware_name ):
    time.sleep(30)
    condition=  'firmware_id = ' "'" +firmware_name+"'"
    output=select(PROJECT,'oem_db','oem','oem_db_user','oem_db_pass','status','oem_fw_bundleset', condition )
    return output

def get_p2p_meter_connectivity(PROJECT, meter_ldn):
    condition = "device_id='"+str(meter_ldn)+"'"
    last_contact_date = select(PROJECT,'vsdc_db','vsdc','vsdc_db_user','vsdc_db_pass','last_contact_date','vsdc_device', condition )
    print(last_contact_date)
    shift = datetime.timedelta(minutes=1)
    now  = datetime.datetime.now()
    past = now -shift
    futur= now+shift
    print(past <last_contact_date < futur)
    return past <last_contact_date < futur
def wait_meter_to_be_communicating(PROJECT, meter_id, timeout):
    condition = "customer_id='"+str(meter_id)+"'"
    ldn = select(PROJECT,'m2m_db','m2m_schema','m2m_db_user','m2m_db_pass','ldn','m2m_equipment_mapping', condition )
    test= False
    t=0
    while test == False and t<int(timeout):
        t=t+1
        out = get_p2p_meter_connectivity(PROJECT, ldn)
        test = out
        print("test :", test)
        time.sleep(1)
    return test


def validate_execPriority_and_reqenddate_per_minute(PROJECT, request_type,task_id, expected_execPriority, expected_recovery_execPriority, shift ):
    validation = True
    condition= "message_id='"+ task_id + "'"
    timeout=0
    job_id=None 
    while job_id == None and timeout <2:
        job_id = select(PROJECT,'metering_db','metering','metering_db_user','metering_db_pass','job_id','metering_job', condition )
        print(job_id)
        time.sleep(5)
        timeout =timeout +1
    if job_id != None:
        req_path = conf.ReadConfigFile.read(PROJECT,'m2m_task_resp_path')
        local_path = conf.ReadConfigFile.read(PROJECT,'project_local_path')
        host = conf.ReadConfigFile.read(PROJECT,'m2m_ip')
        username = conf.ReadConfigFile.read(PROJECT, 'm2m_ip_user')
        password = conf.ReadConfigFile.read(PROJECT, 'm2m_ip_pass')
        port = 22
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, username, password)

        sftp = ssh.open_sftp()
        sftp.get(req_path + job_id +".xml", local_path +"/"+ job_id +".xml")

        tree = ET.parse(local_path+"/"+ job_id +".xml")
        root = tree.getroot()
        print("execPriority", root.get('execPriority'))
        print("recovery execPriority", root[2][2].get('execPriority'))
        print("start", root[1][0].text)
        print("stop", root[1][1].text)
        execPriority= root.get('execPriority')
        recovery_execPriority=root[2][2].get('execPriority')
        start= root[1][0].text
        stop = root[1][1].text
        if execPriority != expected_execPriority:
            validation= False
        if recovery_execPriority != expected_recovery_execPriority:
            validation= False
        if (float(shift) <1440 or request_type =='ODR'):
            print("request with type ODR")
            start_time_obj = datetime.datetime.strptime(start[0:19], "%Y-%m-%dT%H:%M:%S")
            stop_time_obj = datetime.datetime.strptime(stop[0:19], "%Y-%m-%dT%H:%M:%S")
            if float(shift) <24:
                print(stop_time_obj- start_time_obj)
                out_shift = stop_time_obj- start_time_obj
                result=out_shift.total_seconds() / 60
                print(result, shift)
                print( float(result) != float(shift))
                if float(result) != float(shift):
                    validation= False
            else:
                expected_stop_date= date_by_adding_business_daysold(start_time_obj,float(shift)/24)
                out_shift = expected_stop_date- stop_time_obj
                print(out_shift)
                result=out_shift.total_seconds() / 60
                print("result",result)
                print( float(result) != float(0))
                if float(result) != float(0):
                    validation= False
        else:
            print("request with type NOT ODR")
            start_time_obj = datetime.datetime.strptime(start[0:19], "%Y-%m-%dT%H:%M:%S")
            stop_time_obj = datetime.datetime.strptime(stop[0:19], "%Y-%m-%dT%H:%M:%S")
            expected_stop_date= date_by_adding_business_days(start_time_obj,float(shift)/1440)
            out_shift = expected_stop_date- stop_time_obj
            print(out_shift)
            result=out_shift.total_seconds() / 60
            print("result",result)
            print( float(result) != float(0))
            if float(result) != float(0):
                validation= False
    return validation
