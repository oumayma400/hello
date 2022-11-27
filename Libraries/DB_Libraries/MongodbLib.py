from pymongo import MongoClient
import pymongo
from bson import json_util
import json

def get_database():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb://dba:dba123@127.0.0.1:27017/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass%20Community&directConnection=true&ssl=false"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    from pymongo import MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    print(client.list_database_names())
    return client['cep_db']


def ReadCepEvent(PROJECT, device_id, event_type):
    dbname = get_database()
    collection_name = dbname["cep_events"]
   # item_details = collection_name.find({"type" : "EVT_eMeter.powerResume"})
    item_details = collection_name.find({'eventObject.eventObjectMrid' : str(device_id) , "eventReference.type":event_type})
    print(item_details)
    json_docs = []
    for doc in item_details:
        json_doc = json.dumps(doc, default=json_util.default)
        json_docs.append(json_doc)
    for item in item_details:
        print(item)


    return json_docs
