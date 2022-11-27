
import psycopg2

import sys,os
from pathlib import Path
path = Path(os.path.abspath(__file__))
parrent_path = path.parent.absolute()
Read_ConfigLib = os.path.dirname(parrent_path) + os.path.sep + "Read_Config";
Read_ConfigLib2 = Read_ConfigLib.replace('\\', '/')
sys.path.append(Read_ConfigLib2)

# sys.path.append('C:/Users/g361355/Desktop/ROBOT_ECLIPSE/E2E-AUTO-SICONIA/Libraries/Read_Config')
import ReadConfigFile as conf
from pandas import DataFrame
from jproperties import Properties
from elasticsearch import Elasticsearch
import json
import json
import datetime


def SelectElastic(PROJECT , indexstr ,param, val):
    db_host= conf.ReadConfigFile.read(PROJECT,'elk_host')
    elk_user=conf.ReadConfigFile.read(PROJECT,'elk_user')
    elk_pass=conf.ReadConfigFile.read(PROJECT,'elk_pass')
    es = Elasticsearch([{'host': db_host, 'port': 9200}],use_ssl=True,verify_certs=False,ca_certs ="C:/localhostca.crt",http_auth=(elk_user,elk_pass ))
    filter = '"' +param+'"' +":" +'"'+str(val)+'"'
    jsonvar= {'"' +param+'"' +":" +'"'+str(val)+'"'}
    blackjack_hand = (param, val)
    encoded_hand = json.dumps([['jack', 'ilena']])
    print("encoded_hand",encoded_hand)
    meter_id= str(val)
    print("our meter id : ", meter_id)
    page = es.search(
      index = indexstr ,


      body = {"query":{
    		# "match": {"meter_id":'"'+val+'"'}
            "match": {"meter_id":meter_id}
    	}
    	  }

    )
    print(page['hits']['hits'])

    return page['hits']['hits'][0]['_source']



def VerifyParamUpdateInElastic(PROJECT , indexstr ,param, val,uaaparam, uaavalue):
    mon_dictionnaire = {}
    mon_dictionnaire['CityName']='city_name'
    mon_dictionnaire['RegioGroup']='region_group_or_service_center_id'
    mon_dictionnaire['ParentInstallationPointID']='parent_installation_point_id'
    mon_dictionnaire['lifecycle_status']='lifecycle_status'

    db_host= conf.ReadConfigFile.read(PROJECT,'elk_host')
    elk_user=conf.ReadConfigFile.read(PROJECT,'elk_user')
    elk_pass=conf.ReadConfigFile.read(PROJECT,'elk_pass')
    es = Elasticsearch([{'host': db_host, 'port': 9200}],use_ssl=True,verify_certs=False,ca_certs ="C:/localhostca.crt",http_auth=(elk_user,elk_pass ))
    filter = '"' +param+'"' +":" +'"'+str(val)+'"'
    jsonvar= {'"' +param+'"' +":" +'"'+str(val)+'"'}
    blackjack_hand = (param, val)
    encoded_hand = json.dumps([['jack', 'ilena']])
    print("encoded_hand",encoded_hand)
    meter_id= str(val)
    print("our meter id : ", meter_id)
    page = es.search(
      index = indexstr ,


      body = {"query":{
    		# "match": {"meter_id":'"'+val+'"'}
            "match": {"meter_id":meter_id}
    	}
    	  }

    )
    print(page['hits']['hits'][0]['_source'])
    elasticresult=page['hits']['hits'][0]['_source']
    print(uaaparam)
    print(uaavalue)
    verified= True
    if elasticresult[mon_dictionnaire[uaaparam]] != uaavalue:
        verified= False

    # verified= True
    # for i in range(len(uaaparams[0])):
    #     param=uaaparams[0][i]
    #     print(elasticresult[mon_dictionnaire[param]], uaaparams[1][i])
    #     if elasticresult[mon_dictionnaire[param]] != uaaparams[1][i]:
    #         verified= False
    #         break

    return verified

def VerifyDcParamUpdateInElastic(PROJECT , indexstr , val,uaaparam, uaavalue):
    mon_dictionnaire = {}
    mon_dictionnaire['CityName']='city_name'
    mon_dictionnaire['RegioGroup']='region_group_or_service_center_id'
    mon_dictionnaire['ParentInstallationPointID']='parent_installation_point_id'
    mon_dictionnaire['lifecycle_status']='lifecycle_status'
    mon_dictionnaire['dc_id']='dc_id'

    db_host= conf.ReadConfigFile.read(PROJECT,'elk_host')
    elk_user=conf.ReadConfigFile.read(PROJECT,'elk_user')
    elk_pass=conf.ReadConfigFile.read(PROJECT,'elk_pass')
    es = Elasticsearch([{'host': db_host, 'port': 9200}],use_ssl=True,verify_certs=False,ca_certs ="C:/localhostca.crt",http_auth=(elk_user,elk_pass ))

    meter_id= str(val)
    print("our meter id : ", meter_id)
    page = es.search(
      index = indexstr ,


      body = {"query":{
    		# "match": {"meter_id":'"'+val+'"'}
            "match": {"dc_id":meter_id}
    	}
    	  }

    )
    print(page['hits']['hits'][0]['_source'])
    elasticresult=page['hits']['hits'][0]['_source']
    print(uaaparam)
    print(uaavalue)
    verified= True
    if elasticresult[mon_dictionnaire[uaaparam]] != uaavalue:
        verified= False

    # verified= True
    # for i in range(len(uaaparams[0])):
    #     param=uaaparams[0][i]
    #     print(elasticresult[mon_dictionnaire[param]], uaaparams[1][i])
    #     if elasticresult[mon_dictionnaire[param]] != uaaparams[1][i]:
    #         verified= False
    #         break

    return verified

def VerifyParamDeletedInElastic(PROJECT , indexstr ,param, val,uaaparam):
    mon_dictionnaire = {}
    mon_dictionnaire['CityName']='city_name'
    mon_dictionnaire['RegioGroup']='region_group_or_service_center_id'
    mon_dictionnaire['ParentInstallationPointID']='parent_installation_point_id'

    db_host= conf.ReadConfigFile.read(PROJECT,'elk_host')
    elk_user=conf.ReadConfigFile.read(PROJECT,'elk_user')
    elk_pass=conf.ReadConfigFile.read(PROJECT,'elk_pass')
    es = Elasticsearch([{'host': db_host, 'port': 9200}],use_ssl=True,verify_certs=False,ca_certs ="C:/localhostca.crt",http_auth=(elk_user,elk_pass ))
    filter = '"' +param+'"' +":" +'"'+str(val)+'"'
    jsonvar= {'"' +param+'"' +":" +'"'+str(val)+'"'}
    blackjack_hand = (param, val)
    encoded_hand = json.dumps([['jack', 'ilena']])
    print("encoded_hand",encoded_hand)
    meter_id= str(val)
    print("our meter id : ", meter_id)
    page = es.search(
      index = indexstr ,


      body = {"query":{
    		# "match": {"meter_id":'"'+val+'"'}
            "match": {"meter_id":meter_id}
    	}
    	  }

    )
    print(page['hits']['hits'][0]['_source'])
    elasticresult=page['hits']['hits'][0]['_source']
    print(uaaparam)

    verified= True
    if elasticresult[mon_dictionnaire[uaaparam]] != '':
        verified= False

    # verified= True
    # for i in range(len(uaaparams[0])):
    #     param=uaaparams[0][i]
    #     print(elasticresult[mon_dictionnaire[param]], uaaparams[1][i])
    #     if elasticresult[mon_dictionnaire[param]] != uaaparams[1][i]:
    #         verified= False
    #         break

    return verified



def VerifySlaDemandUpdated(PROJECT ,request_id, response_time, status):
    print("request sla demand id : ", request_id)


    db_host= conf.ReadConfigFile.read(PROJECT,'elk_host')
    elk_user=conf.ReadConfigFile.read(PROJECT,'elk_user')
    elk_pass=conf.ReadConfigFile.read(PROJECT,'elk_pass')
    es = Elasticsearch([{'host': db_host, 'port': 9200}],use_ssl=True,verify_certs=False,ca_certs ="C:/localhostca.crt",http_auth=(elk_user,elk_pass ))

    page = es.search(
      index = 'sla_demand' ,


      body = {"query":{
    		# "match": {"meter_id":'"'+val+'"'}
            "match": {"_id":request_id}
    	}
    	  }

    )
    print(page['hits']['hits'][0]['_source'])
    elasticresult=page['hits']['hits'][0]['_source']
    verified= False
    if page['hits']['hits'][0]['_source']['status']== status:
        dateTime_result=page['hits']['hits'][0]['_source']['response_timestamp']
        dateTime_result= datetime.datetime.strptime(dateTime_result[0:19], "%Y-%m-%dT%H:%M:%S")
        response_time= datetime.datetime.strptime(response_time[0:19], "%Y-%m-%dT%H:%M:%S")
        print("dateTime_result",dateTime_result )
        print("response_time" , response_time)

        shift = datetime.timedelta(minutes=3)
        past = response_time - shift
        futur = response_time + shift
        past=past.isoformat()
        futur=futur.isoformat()
        # verified= True
        if dateTime_result.isoformat() > past and dateTime_result.isoformat() < futur :
            verified= True
        # if page['hits']['hits'][0]['_source']['response_timestamp']== response_time:
        #     verified= True

    return verified



def sla_dates_updated(PROJECT , meter_id):


    db_host= conf.ReadConfigFile.read(PROJECT,'elk_host')
    elk_user=conf.ReadConfigFile.read(PROJECT,'elk_user')
    elk_pass=conf.ReadConfigFile.read(PROJECT,'elk_pass')
    es = Elasticsearch([{'host': db_host, 'port': 9200}],use_ssl=True,verify_certs=False,ca_certs ="C:/localhostca.crt",http_auth=(elk_user,elk_pass ))
    meter_id = str(meter_id)
    page = es.search(
      index = 'sla_meter' ,


      body = {"query":{
    		# "match": {"meter_id":'"'+val+'"'}
            "match": {"meter_id":meter_id}
    	}
    	  }

    )
    print(page['hits']['hits'][0]['_source'])
    elasticresult=page['hits']['hits'][0]['_source']

    verified= False

    dt = datetime.datetime.now()
    shift = datetime.timedelta(minutes=10)
    past = dt - shift
    past=past.isoformat()
    futur = dt + shift
    futur=futur.isoformat()
    # print(dt.isoformat())

    if (elasticresult['activation_date'] > past) and (elasticresult['activation_date'] < futur):
        if (elasticresult['activation_pending_date'] > past) and (elasticresult['activation_pending_date'] < futur):
            if (elasticresult['reconciliation_date'] > past) and (elasticresult['reconciliation_date'] < futur):
                # if (elasticresult['installation_date'] > past) and (elasticresult['installation_date'] < futur):
                if (elasticresult['last_life_cycle_status_update'] > past) and (elasticresult['last_life_cycle_status_update'] < futur):
                    verified= True

    # verified= True
    # for i in range(len(uaaparams[0])):
    #     param=uaaparams[0][i]
    #     print(elasticresult[mon_dictionnaire[param]], uaaparams[1][i])
    #     if elasticresult[mon_dictionnaire[param]] != uaaparams[1][i]:
    #         verified= False
    #         break

    return verified


def sla_suspend_params_updated(PROJECT , meter_id):


    db_host= conf.ReadConfigFile.read(PROJECT,'elk_host')
    elk_user=conf.ReadConfigFile.read(PROJECT,'elk_user')
    elk_pass=conf.ReadConfigFile.read(PROJECT,'elk_pass')
    es = Elasticsearch([{'host': db_host, 'port': 9200}],use_ssl=True,verify_certs=False,ca_certs ="C:/localhostca.crt",http_auth=(elk_user,elk_pass ))
    meter_id = str(meter_id)
    page = es.search(
      index = 'sla_meter' ,
      body = {"query":{
    		# "match": {"meter_id":'"'+val+'"'}
            "match": {"meter_id":meter_id}
    	}
    	  }
    )
    print(page['hits']['hits'][0]['_source'])
    elasticresult=page['hits']['hits'][0]['_source']

    verified= False

    dt = datetime.datetime.now()
    shift = datetime.timedelta(minutes=5)
    past = dt - shift
    past=past.isoformat()
    futur = dt + shift
    futur=futur.isoformat()
    # print(dt.isoformat())

    if (elasticresult['suspension_update_date'] > past) and (elasticresult['suspension_update_date'] < futur):
        if (elasticresult['is_suspended'] == False):
            dateTimeObj = datetime.datetime.now()
            print('Current dateTimeObj : ', str(dateTimeObj).split(" "))
            capa_id= meter_id + str(dateTimeObj).split(" ")[0]
            page2 = es.search(
              index = 'sla_capability' ,
              body = {"query":{
            		# "match": {"meter_id":'"'+val+'"'}
                    "match": {"_id":capa_id}
            	}
            	  }
            )
            print(page2['hits']['hits'][0]['_source'])
            elasticresult2=page2['hits']['hits'][0]['_source']
            if elasticresult2['registers_delivery_status'] != False or elasticresult2['intervallen_delivery_status'] != False:
                verified= False
            else:
                verified= True

    # verified= True
    # for i in range(len(uaaparams[0])):
    #     param=uaaparams[0][i]
    #     print(elasticresult[mon_dictionnaire[param]], uaaparams[1][i])
    #     if elasticresult[mon_dictionnaire[param]] != uaaparams[1][i]:
    #         verified= False
    #         break

    return verified


def sla_delivery_params_updated(PROJECT , meter_id, delivery_list:list):


    db_host= conf.ReadConfigFile.read(PROJECT,'elk_host')
    elk_user=conf.ReadConfigFile.read(PROJECT,'elk_user')
    elk_pass=conf.ReadConfigFile.read(PROJECT,'elk_pass')
    es = Elasticsearch([{'host': db_host, 'port': 9200}],use_ssl=True,verify_certs=False,ca_certs ="C:/localhostca.crt",http_auth=(elk_user,elk_pass ))
    meter_id = str(meter_id)
    page = es.search(
      index = 'sla_meter' ,
      body = {"query":{
    		# "match": {"meter_id":'"'+val+'"'}
            "match": {"meter_id":meter_id}
    	}
    	  }
    )
    print(page['hits']['hits'][0]['_source'])
    elasticresult=page['hits']['hits'][0]['_source']

    verified= True

    for i in range(len(delivery_list)):
        param=(delivery_list[0][i]).lower()+'_sla'
        param_capa=(delivery_list[0][i]).lower()+'_status'
        if delivery_list[1][i] =='Off':
            if (elasticresult[param]!=""):
                verified=False
                break
            elif (elasticresult[param_capa]!=False):
                verified=False
                break
        else:
            if (elasticresult[param]!=str(delivery_list[1][i])):
                verified=False
                break
            elif (elasticresult[param_capa]!=True):
                verified=False
                break
    return verified


def verify_meters_status_in_sla(PROJECT, params):
    validation= True
    for i in range(len(params)):
        meter_id= params[i]['Serial_number']
        validation = VerifyParamUpdateInElastic(PROJECT , 'sla_meter' ,'lifecycle_status', str(meter_id) ,'lifecycle_status', "PROVISIONED")
        if validation == False:
            break
    return validation
def verify_dcs_status_in_sla(PROJECT, params):
    validation= True
    for i in range(len(params)):
        meter_id= params[i]['Serial_number']
        validation = VerifyDcParamUpdateInElastic(PROJECT , 'sla_dc' , str(meter_id) ,'dc_id', str(meter_id))
        if validation == False:
            break
    return validation


def get_cep_events(PROJECT , meter_id,event_type, delta ):

    verified= False
    event_id = ''
    db_host= conf.ReadConfigFile.read(PROJECT,'elk_host')
    elk_user=conf.ReadConfigFile.read(PROJECT,'elk_user')
    elk_pass=conf.ReadConfigFile.read(PROJECT,'elk_pass')
    es = Elasticsearch([{'host': db_host, 'port': 9200}],use_ssl=True,verify_certs=False,ca_certs ="C:/localhostca.crt",http_auth=(elk_user,elk_pass ))
    meter_id = str(meter_id)

    dt = datetime.datetime.now()
    shift = datetime.timedelta(minutes=int(delta))
    past = dt - shift
    # past=past.isoformat()
    print("past")
    print(past)
    dte =past.strftime('%Y-%m-%dT%H:%M:%S')+".000+01:00"
    print(dte)
    now = datetime.datetime.now()
    year=str(now.year)
    month =str(now.month)
    if now.month <10:
        month = '0'+month

    page = es.search(
      index = 'cep_events_'+year +'-'+month ,
      body = {

     "query": {
       "bool": {
         "must": [
           {
             "range": {
               "eventManagement.registeredDateTime": {
                 # "gte":"2022-01-05T13:00:59.994+01:00"
                 "gte": dte
               }
             }
           },
           {
             "match": {
              "eventObject.eventObjectMrid" : meter_id
             },
             "match": {
              "eventReference.type" : event_type
             }

           }
         ]
       }
     }





    	  }
    )
    if len(page['hits']['hits'])>0:

        print(page['hits']['hits'][0]['_source'])
        elasticresult=page['hits']['hits'][0]['_source']
        event_id=page['hits']['hits'][0]['_id']
        verified= True


    return verified, event_id
