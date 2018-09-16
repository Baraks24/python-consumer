from elasticsearch import Elasticsearch
es = Elasticsearch()#(['localhost', 'otherhost'],http_auth=('user', 'secret'),scheme="https",port=443,)

USERS_INDEX = "users"
PROJECTS_INDEX = "projects"
DISCUSSIONS_INDEX = "discussions"
TASKS_INDEX = "tasks"

#TODO: actually write something useful

def create_doc(index,doc):
    id = doc["_id"]
    doc.pop("_id")
    es.create(index=index,id=id,body=doc,doc_type=index)
    return

def update_doc(index,doc):
    return

def delete_doc(index,id):
    return

create_doc(index=TASKS_INDEX,doc={"_id":"456","foo":"foo"})

#create indices
# es.indices.create(index=USERS_INDEX)
# es.indices.create(index=PROJECTS_INDEX)
# es.indices.create(index=DISCUSSIONS_INDEX)
# es.indices.create(index=TASKS_INDEX)