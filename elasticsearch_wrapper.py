from elasticsearch import Elasticsearch
from config import ELASTICSEARCH_HOSTS,USERS_INDEX,PROJECTS_INDEX,DISCUSSIONS_INDEX,TASKS_INDEX
from JSONSerializer import JSONSerializer

es = Elasticsearch(ELASTICSEARCH_HOSTS,serializer = JSONSerializer())

#TODO: actually write something useful

def create_doc(index,doc):
    id = doc["_id"]
    doc.pop("_id")
    es.create(index=index,id=id,body=doc,doc_type=index,ignore=[400, 404,409])
    return

def update_doc(index,doc):
    id = doc["_id"]
    doc.pop("_id")
    #doc["foo"] = "despacito 2"
    es.update(index=index,id=id,body={"doc":doc},doc_type=index,ignore=[400, 404,409])
    return

def delete_doc(index,id):
    es.delete(index=index,id=id,doc_type=index,ignore=[400, 404,409])
    return

#create_doc(index=TASKS_INDEX,doc={"_id":"456","foo":"foo"})
#update_doc(index=TASKS_INDEX,doc={"_id":"456","foo":"foo2"})
#delete_doc(index=TASKS_INDEX,id=456)

#create indices
# es.indices.create(index=USERS_INDEX)
# es.indices.create(index=PROJECTS_INDEX)
# es.indices.create(index=DISCUSSIONS_INDEX)
# es.indices.create(index=TASKS_INDEX)