from elasticsearch import Elasticsearch,helpers
from config import ELASTICSEARCH_HOSTS,USERS_INDEX,PROJECTS_INDEX,DISCUSSIONS_INDEX,TASKS_INDEX,UPDATABLE_INDICES
from JSONSerializer import JSONSerializer
import json

es = Elasticsearch(ELASTICSEARCH_HOSTS,serializer = JSONSerializer())

#TODO: actually write something useful

def filter_relevant(search_results):
    return [doc for doc in search_results if doc['index'] in UPDATABLE_INDICES]

def create_doc(index,doc):
    id = doc["_id"]
    doc.pop("_id")
    doc["id"] = id
    es.create(index=index,id=id,body=doc,doc_type=index,ignore=[400, 404,409])
    return

def update_doc(index,doc):
    id = doc["_id"]
    doc.pop("_id")
    doc["id"] = id
    #doc["foo"] = "despacito 2"
    es.update(index=index,id=id,body={"doc":doc},doc_type=index,ignore=[400, 404,409])
    return

def delete_doc(index,id):
    es.delete(index=index,id=id,doc_type=index,ignore=[400, 404,409])
    return

def search_related_docs(id):
    body = {
        "query":{
            "multi_match":{
                "query":id
            }
        }
    }
    res = es.search(index='_all',body=body)
    print("elastic res")
    print(res)
    # hits = [hit['_id'] for hit in res['hits']['hits']]
    # index = [hit['_index'] for hit in res['hits']['hits']]
    ret = [{"id":hit['_id'],"index":hit['_index']} for hit in res['hits']['hits']]
    relevant_projects = [{"id":hit['_source']['project'],"index":PROJECTS_INDEX} for hit in res['hits']['hits'] if "project" in hit['_source']]
    print('relevant projects//////////////////////////////')
    print(relevant_projects)

    ret.extend(relevant_projects)
    ret = filter_relevant(ret)
    return ret

"""
assums docs are from elastic , i.e. they have _id and id
docs-an array of {index,id,doc} to update
"""
def bulk(docs):
    for doc in docs:
        if("_id" in doc['doc']):
            id = doc['doc']['_id']
            doc['doc'].pop('_id')
            doc['doc']['id'] = id
        else:
            id = doc['id']
            doc['doc']['id'] = id
    bulk_actions = [{"_id":doc['id'],"_index":doc['index'],"_type":doc['index'],"_source":{'doc':doc['doc']},"_op_type":"update"} for doc in docs]
    try:
        helpers.bulk(es,bulk_actions,ignore=["400"])
    except Exception as inst:
        print(inst)



#create_doc(index=TASKS_INDEX,doc={"_id":"abc","id":"abc","foo":"foo"})
#update_doc(index=TASKS_INDEX,doc={"_id":"456","foo":"foo2"})
#delete_doc(index=TASKS_INDEX,id=456)

# actions_arr =[{"_id":"abc","index":TASKS_INDEX,"doc":{"id":"abc","foo":"despacito5"}}]
# try:
    # bulk(actions_arr)
# except Exception as inst:
    # print(inst)

#create indices
# es.indices.create(index=USERS_INDEX)
# es.indices.create(index=PROJECTS_INDEX)
# es.indices.create(index=DISCUSSIONS_INDEX)
# es.indices.create(index=TASKS_INDEX)