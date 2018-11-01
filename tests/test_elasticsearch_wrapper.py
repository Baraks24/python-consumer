import pytest

#make elasticsearch importable
import sys
sys.path.append('../')


from elasticsearch import Elasticsearch
es = Elasticsearch()
from elasticsearch_wrapper import  bulk,create_doc,delete_doc,update_doc,filter_relevant,search_related_docs
from config import TESTS_INDEX



def print_assert(condition, str_fail, str_pass):
    assert condition, str_fail
    print(str_pass)

@pytest.fixture(scope="function")
def mocks():
    yield lambda:[
            {"id":"1234","index":TESTS_INDEX,"doc":{"_id":"1234","a":"a","b":"b"}},
            {"id":"2345","index":TESTS_INDEX,"doc":{"_id":"2345","a":"b","b":"c"}}
        ]
    

@pytest.fixture(scope="function")
def mock_doc():
    yield lambda:{"_id":"1234","a":"a","b":"b"}

@pytest.fixture(scope="function")
def mock_docs_for_search_related_docs():
    yield lambda:[
            {"_id":"1234","id":"1234","a":"a","b":"b"},
            {"_id":"2345","a":"b","b":"c","despasito":"1234"}
        ]

@pytest.fixture(scope="function",autouse=True)
def each():
    print("before each") #execute code before each test
    yield "someValue" #pass value to each test expecting the fixture function name as input, aka DI
    print("after each") #execute code after each test, can see print from cli with -v -s but doesnt appear in html.
    es.indices.delete(TESTS_INDEX,ignore=[400, 404])

#'result': 'created'
def test_bulk(mocks):
    print("try to update existing documents")
    docs = mocks()
    create_doc(TESTS_INDEX,docs[0]['doc'])
    create_doc(TESTS_INDEX,docs[1]['doc'])
    docs=mocks()
    docs[0]['doc']['despacito']="despacito"
    docs[1]['doc']['despacito']="despacito"
    res = bulk(docs)
    assert res[0]==2

    print("try to update non existing documents")
    docs=mocks()
    docs[0]['doc']['_id']="despacito"
    docs[1]['id']="despacito"
    docs[1]['doc']['_id']="despacito2"
    docs[0]['id']="despacito2"
    res = {}
    res = bulk(docs)
    assert len(res.errors) == 2, "updated non existing documents (;-_-)" #num of errors



#TODO: create doc changes the input doc maybe make it pure so getDoc\lambda wont be necessary
def test_create_doc(mock_doc):

    print("try to create a none existing document")
    res = create_doc(TESTS_INDEX,mock_doc())
    assert res['result']=='created' , "Document creation Failed"

    print("try to create an existing document")
    res = create_doc(TESTS_INDEX,mock_doc())
    assert 'error' in res , "Created an existing document (;-_-)"

def test_delete_doc(mock_doc):
    print("try to delete a non existing document")
    res = delete_doc(TESTS_INDEX,mock_doc()["_id"])
    assert 'error' in res, "Deleted a none existing document (;-_-)"

    print("create a document and try to delete it")
    create_doc(TESTS_INDEX,mock_doc())
    res = delete_doc(TESTS_INDEX,mock_doc()["_id"])
    assert res['result']=='deleted' , "Document creation Failed"

def test_update_doc(mock_doc):
    print("try to update a none existing document")
    res = update_doc(TESTS_INDEX,mock_doc())
    assert 'error' in res, "Updated a none existing document (;-_-)"

    print("create a document and try to update it")
    create_doc(TESTS_INDEX,mock_doc())
    modified_doc = mock_doc()
    modified_doc["c"] = "c"
    res = update_doc(TESTS_INDEX,modified_doc)
    assert res['result']=='updated' , "Document creation Failed"

def test_search_related_docs(mock_docs_for_search_related_docs):
    print("try to get relevant documents by id")
    docs = mock_docs_for_search_related_docs()
    create_doc(TESTS_INDEX,docs[0])
    create_doc(TESTS_INDEX,docs[1])
    print(docs[0]['id'])
    #TODO refactor to recieve filter index
    res = search_related_docs(docs[0]['id'])
    print(res)
    assert True


def test_filter_relevant():
    assert True
