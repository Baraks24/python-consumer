from kafka import KafkaConsumer
import json
from pymongo import MongoClient
from bson.objectid import ObjectId
from op_handler import OpHandler
from config import DB,MONGO_URI,TOPICS,KAFKA_URL
import time


from elasticsearch_wrapper import create_doc,delete_doc,update_doc
from mongo_aggregations import projects_aggregation,users_aggregation,discussions_aggregation,tasks_aggregation

UPDATE = 'u'
DELETE = 'd'
CREATE = 'c'

ops={
'c':'create',
'd':'delete',
'u':'update'
}

"""
returns tuple (op,collection,Id)
"""
def get_params_from_message(msg):
    value_payload = msg.value['payload']
    # print("////////////////////msg:////////////////")
    # print(msg)
    # print("////////////////////payload:////////////////")
    # print(value_payload)
    if value_payload:
        op = value_payload['op']
        key = json.loads(msg.key)
        topic = msg.topic
        collection = topic[(topic.rfind('.')+1):]
        id = None
        if op==UPDATE:
            # print(key)
            #id = json.loads(key['payload']['_id'])['_id']['$oid']#azure version
            id = json.loads(key['payload']['id'])['$oid']
            #check if deleted/recycled by root
            op = DELETE if 'recycled' in json.loads(value_payload['patch'])['$set'].keys() else UPDATE
            # print('updated op///////////////////////////')
            # print(op)

        else:
            # print(key)
            #id = key['payload']['_id'] #azure version
            id = json.loads(key['payload']['id'])['$oid']   
        return (ops[op],collection,id)
    else:
        return 'junk'



def opHandler(op_collection_id_tuple):
    # m = globals()['OpHandler']()
    # func_name = "{0}_{1}".format(op_collection_id_tuple[0].lower(),op_collection_id_tuple[1].lower())
    # func = getattr(m, func_name)
    # return func(op_collection_id_tuple[2])
    func = OpHandler.execute((op_collection_id_tuple[0].lower(),op_collection_id_tuple[1].lower()))
    print("1////////////////////")
    print(func)
    return func(op_collection_id_tuple[2])
    


def fix(e):
    #check if kafka fell -> take last seriallized msg and run fix from mongo by querying all objects in all collections created after the timestamp from objectid
    #else just try and execute flow on last serialized msg until succesful
    #after a succesfull fix return to reading messages from kafka and executing flow
    pass

def main():
    print('Welcome!')
    consumer = KafkaConsumer(*TOPICS,value_deserializer=lambda m: json.loads(m.decode('utf-8')),bootstrap_servers=[KAFKA_URL])
    for msg in consumer:
        print("this is a message yo, read the message, ma hamazav barakos?:")
        print(msg)
        # TODO:
        #serialize message
        if msg:
            op_collection_userId_tuple = get_params_from_message(msg) 
            print(op_collection_userId_tuple)
            print('\n')
            if(op_collection_userId_tuple!='junk'):   
                opHandler(op_collection_userId_tuple)


if __name__ == "__main__":
    while True:
        try:
            main() 
        except  Exception as e:
            print("Runtime Error:")
            print(e)
            # time.sleep(5) ?
            #while true fix serialized message
            while True:
                try:
                    fix(e) #run flow with last serialized msg
                except Exception as e2:
                    print("Runtime Fix Error:")
                    print(e2)
                    continue
                break # on success return to read messages from kafka


            # while True retry last serialized message before continuing
            # need to check if we can get the creation date of the object from the mongo object id
            # and then maybe try and rerun all everything from mongo created after 1 hour before the last object
