from kafka import KafkaConsumer
import json
from pymongo import MongoClient
from bson.objectid import ObjectId
from op_handler import OpHandler
from config import DB,MONGO_URI,TOPICS


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
    if value_payload:
        op = value_payload['op']
        key = json.loads(msg.key)
        topic = msg.topic
        collection = topic[(topic.rfind('.')+1):]
        id = None
        if op==UPDATE:
            id = json.loads(key['payload']['_id'])['_id']['$oid']
        else:
            id = key['payload']['_id']   
        return (ops[op],collection,id)
    else:
        return 'junk'



def opHandler(op_collection_userId_tuple):
    m = globals()['OpHandler']()
    func_name = "{0}_{1}".format(op_collection_userId_tuple[0].lower(),op_collection_userId_tuple[1].lower())
    func = getattr(m, func_name)
    return func(op_collection_userId_tuple[2])


def main():
    consumer = KafkaConsumer(*TOPICS,value_deserializer=lambda m: json.loads(m.decode('utf-8')))
    for msg in consumer:
        op_collection_userId_tuple = get_params_from_message(msg) 
        print(op_collection_userId_tuple)
        print('\n')
        if(op_collection_userId_tuple!='junk'):   
            opHandler(op_collection_userId_tuple)


if __name__ == "__main__":
    main() 
