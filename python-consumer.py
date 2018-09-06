from kafka import KafkaConsumer
import json
from pymongo import MongoClient
from bson.objectid import ObjectId

DB = "barak-db"
UPDATE = 'u'
DELETE = 'd'
CREATE = 'c'

client = MongoClient('mongodb://10.0.0.42,10.0.0.43,10.0.0.44/?replicaSet=mongo-azure')
db_input = client[DB]
users = db_input.users


class OpHandler:

    @staticmethod
    def tasks_aggregation(id):
        return [{
            "$match":{"_id":ObjectId(id)}
        },
        #populate creator
        {"$lookup":{
            "from":"users",
            "localField":"creator",
            "foreignField":"_id",
            "as":"creator"}
        },
        {
            "$unwind":"$creator"
        },
        #populate assign
        {"$lookup":{
            "from":"users",
            "localField":"assign",
            "foreignField":"_id",
            "as":"assign"}
        },
        {
            "$unwind":"$assign"
        },
        #get all updates
        {"$lookup":{
            "from":"updates",
            "localField":"_id",
            "foreignField":"issueId",
            "as":"updates"}
        },
        #filter only comments status and assignee changes
        {
            "$project":{
                '_id':1,
                'title':1,
                'updated':1,
                'creator':1,
                'subTasks':1,
                'sources':1,
                'discussions':1,
                #'permissions':1,
                'watchers':1,
                'status':1,
                'tags':1,
                'created':1,
                '__v':1,
                'circles':1,
                'assign':1, 
                'description':1,
                'due':1,
                "comments":{
                    "$filter":{
                    "input":"$updates",
                    "as":"update",
                    "cond":{"$eq":["$$update.type","comment"]}
                    }
                },
                "statusUpdates":{
                    "$filter":{
                        "input":"$updates",
                        "as":"update",
                        "cond":{"$eq":["$$update.type","updateStatus"]}
                    }
                },
                "assignUpdates":{   
                    "$filter":{
                        "input":"$updates",
                        "as":"update",
                        "cond":{"$or":[
                            {"$eq":["$$update.type","assignNew"]},
                            {"$eq":["$$update.type","assign"]},
                            ]
                        }
                    } 
                },
                #permissions unpopulated
                "editors":{
                    "$filter":{
                        "input":"$permissions",
                        "as":"permission",
                        "cond":{"$eq":["$$permission.level","editor"]}
                    }
                },
                "commenters":{
                    "$filter":{
                        "input":"$permissions",
                        "as":"permission",
                        "cond":{"$eq":["$$permission.level","commenter"]}
                    }
                },
                "viewers":{
                    "$filter":{
                        "input":"$permissions",
                        "as":"permission",
                        "cond":{"$eq":["$$permission.level","viewer"]}
                    }
                },
            }
        },
        #subtasks
        {
            "$graphLookup":{
                "from": "tasks",
                "startWith": "$subTasks",
                "connectFromField": "subTasks",
                "connectToField": "_id",
                "as": "subTasksHierarchy"
            }
        },
        #watchers
        {
            "$lookup":{
                "from":"users",
                "localField":"watchers",
                "foreignField":"_id",
                "as":"watchers"}
        },
        #premissions populate/lookup -viewers
        {
            "$lookup":{
            "from":"users",
            "localField":"viewers.id",
            "foreignField":"_id",
            "as":"viewers"} 
        },
        #premissions populate/lookup -commenters
        {
            "$lookup":{
                "from":"users",
                "localField":"commenters.id",
                "foreignField":"_id",
                "as":"commenters"} 
        },
        #premissions populate/lookup -editors
        {
            "$lookup":{
                "from":"users",
                "localField":"editors.id",
                "foreignField":"_id",
                "as":"editors"} 
        }, 
        ]

    @staticmethod
    def projects_aggregation(id):
        return [{
            "$match":{"_id":ObjectId(id)}
        },
        #populate creator
        {"$lookup":{
            "from":"users",
            "localField":"creator",
            "foreignField":"_id",
            "as":"creator"}
        }, 
        {
            "$unwind":"$creator"
        },
        #populate assign
        {"$lookup":{
            "from":"users",
            "localField":"assign",
            "foreignField":"_id",
            "as":"assign"}
        },
        {
            "$unwind":"$assign"
        },
        #get all updates
        {"$lookup":{
            "from":"updates",
            "localField":"_id",
            "foreignField":"issueId",
            "as":"updates"}
        },
        #filter only comments status and assignee changes
        {
            "$project":{
                '_id':1,
                'title':1,
                'location':1,
                'updated':1,
                'creator':1,
                #'subTasks':1, ? relevant
                #'sources':1, ?relevant
                'discussions':1,
                #'permissions':1,
                'watchers':1,
                'status':1,
                'tags':1,
                'created':1,
                '__v':1,
                #'circles':1, ? relevant
                'assign':1, 
                'description':1,
                'due':1,
                "comments":{
                    "$filter":{
                        "input":"$updates",
                        "as":"update",
                        "cond":{"$eq":["$$update.type","comment"]}
                    }
                },
                "statusUpdates":{
                    "$filter":{
                        "input":"$updates",
                        "as":"update",
                        "cond":{"$eq":["$$update.type","updateStatus"]}
                    }
                },
                "assignUpdates":{   
                    "$filter":{
                        "input":"$updates",
                        "as":"update",
                        "cond":{"$or":[
                            {"$eq":["$$update.type","assignNew"]},
                            {"$eq":["$$update.type","assign"]},
                            ]
                        }
                    } 
                },
                #permissions unpopulated
                "editors":{
                    "$filter":{
                        "input":"$permissions",
                        "as":"permission",
                        "cond":{"$eq":["$$permission.level","editor"]}
                    }
                },
                "commenters":{
                    "$filter":{
                        "input":"$permissions",
                        "as":"permission",
                        "cond":{"$eq":["$$permission.level","commenter"]}
                    }
                },
                "viewers":{
                    "$filter":{
                        "input":"$permissions",
                        "as":"permission",
                        "cond":{"$eq":["$$permission.level","viewer"]}
                    }
                },
            }
        },
        #     #subtasks - change to subProjects if its necessary
        #     {
        #         "$graphLookup":{
        #               "from": "tasks",
        #          "startWith": "$subTasks",
        #          "connectFromField": "subTasks",
        #          "connectToField": "_id",
        #          "as": "subTasksHierarchy"
        #         }
        #     },
        #watchers
        {
            "$lookup":{
            "from":"users",
            "localField":"watchers",
            "foreignField":"_id",
            "as":"watchers"}
        },
        #premissions populate/lookup -viewers
        {
            "$lookup":{
                "from":"users",
                "localField":"viewers.id",
                "foreignField":"_id",
                "as":"viewers"} 
        },
        #premissions populate/lookup -commenters
        {
            "$lookup":{
                "from":"users",
                "localField":"commenters.id",
                "foreignField":"_id",
                "as":"commenters"} 
        },
        #premissions populate/lookup -editors
        {
            "$lookup":{
                "from":"users",
                "localField":"editors.id",
                "foreignField":"_id",
                "as":"editors"} 
        },   
        ]



    """
    Aggregation for users
    """
    @staticmethod
    def users_aggregation(id):
        return [
        {
            "$match":{"_id":ObjectId(id)}
        },
        {
            "$project":{
                "_id":1,
                "uid": 1,
                'id':1,
                'name': 1,
                'email': 1,
                'username':1,
                #'hashed_password':1,
                #'salt': 1,
                #'GetMailEveryDayAboutMyTasks': 1,
                #'GetMailEveryWeekAboutGivenTasks': 1,
                #'GetMailEveryWeekAboutMyTasks': 1,
                #'provider': 1,
                #'roles': 1,
                #'__v': 1,
                #'profile':1,
                'starredTasks':{
                    "$map":{
                        "input":"$profile.starredTasks",
                        "as":"star",
                        "in":{"$convert": { "input": "$$star", "to": "objectId" }}
                    }
                },
                'starredProjects':{
                    "$map":{
                        "input":"$profile.starredProjects",
                        "as":"star",
                        "in":{"$convert": { "input": "$$star", "to": "objectId" }}
                    }
                },
                'starredDiscussions':{
                    "$map":{
                        "input":"$profile.starredDiscussions",
                        "as":"star",
                        "in":{"$convert": { "input": "$$star", "to": "objectId" }}
                    }
                }
            }
        },
        #populate stars
        {
            "$lookup":{
            "from":"tasks",
            "localField":"starredTasks",
            "foreignField":"_id",
            "as":"starredTasks"} 
        },
        {
            "$lookup":{
            "from":"projects",
            "localField":"starredProjects",
            "foreignField":"_id",
            "as":"starredProjects"} 
        },
        {
            "$lookup":{
            "from":"discussions",
            "localField":"starredDiscussions",
            "foreignField":"_id",
            "as":"starredDiscussions"} 
        },
        ]

    @staticmethod
    def discussions_aggregation(id):
        return [
        #populate creator
            {"$lookup":{
                "from":"users",
                "localField":"creator",
                "foreignField":"_id",
                "as":"creator"}
            }, 
            {
                "$unwind":"$creator"
            },
        #populate assign
            {"$lookup":{
                "from":"users",
                "localField":"assign",
                "foreignField":"_id",
                "as":"assign"}
            },
            {
                "$unwind":"$assign"
            },
        #get all updates
            {"$lookup":{
                "from":"updates",
                "localField":"_id",
                "foreignField":"issueId",
                "as":"updates"}
            },
        #filter only comments status and assignee changes
            {
                "$project":{
                    '_id':1,
                    'title':1,
                    'location':1,
                    'updated':1,
                    'creator':1,
                    #'subTasks':1, ? relevant
                    #'sources':1, ?relevant
                    'discussions':1,
                    #'permissions':1,
                    'watchers':1,
                    'status':1,
                    'tags':1,
                    'created':1,
                    '__v':1,
                    #'circles':1, ? relevant
                    'assign':1, 
                    'description':1,
                    'due':1,
                    "comments":{
                        "$filter":{
                            "input":"$updates",
                            "as":"update",
                            "cond":{"$eq":["$$update.type","comment"]}
                        }
                    },
                    "statusUpdates":{
                        "$filter":{
                            "input":"$updates",
                            "as":"update",
                            "cond":{"$eq":["$$update.type","updateStatus"]}
                        }
                    },
                "assignUpdates":{   
                    "$filter":{
                        "input":"$updates",
                        "as":"update",
                        "cond":{"$or":[
                            {"$eq":["$$update.type","assignNew"]},
                            {"$eq":["$$update.type","assign"]},
                        ]
                        }
                    } 
                },
                #permissions unpopulated
                "editors":{
                    "$filter":{
                        "input":"$permissions",
                        "as":"permission",
                        "cond":{"$eq":["$$permission.level","editor"]}
                    }
                },
                "commenters":{
                    "$filter":{
                        "input":"$permissions",
                        "as":"permission",
                        "cond":{"$eq":["$$permission.level","commenter"]}
                    }
                },
                "viewers":{
                    "$filter":{
                        "input":"$permissions",
                        "as":"permission",
                        "cond":{"$eq":["$$permission.level","viewer"]}
                    }
                },
                }
            },
            #     #subtasks - subDiscussions exist?
            #     {
            #         "$graphLookup":{
            #               "from": "tasks",
            #          "startWith": "$subTasks",
            #          "connectFromField": "subTasks",
            #          "connectToField": "_id",
            #          "as": "subTasksHierarchy"
            #         }
            #     },
            #watchers
            {
                "$lookup":{
                    "from":"users",
                    "localField":"watchers",
                    "foreignField":"_id",
                    "as":"watchers"}
            },
            #premissions populate/lookup -viewers
            {
                "$lookup":{
                    "from":"users",
                    "localField":"viewers.id",
                    "foreignField":"_id",
                    "as":"viewers"} 
            },
            #premissions populate/lookup -commenters
            {
                "$lookup":{
                    "from":"users",
                    "localField":"commenters.id",
                    "foreignField":"_id",
                    "as":"commenters"} 
            },
            #premissions populate/lookup -editors
            {
            "$lookup":{
                "from":"users",
                "localField":"editors.id",
                "foreignField":"_id",
                "as":"editors"} 
            },  
        ]


    @staticmethod
    def create_users(id):
        #TODO
        return

    @staticmethod
    def update_users(id):
        #TODO
        return

    @staticmethod
    def delete_users(id):
        #TODO
        return

    @staticmethod
    def create_tasks(id):
        #TODO
        return

    @staticmethod
    def update_tasks(id):
        #TODO
        return

    @staticmethod
    def delete_tasks(id):
        #TODO
        return

    @staticmethod
    def create_projects(id):
        #TODO
        return

    @staticmethod
    def update_projects(id):
        #TODO
        return

    @staticmethod
    def delete_projects(id):
        #TODO
        return

    @staticmethod
    def create_discussions(id):
        #TODO
        return

    @staticmethod
    def update_discussions(id):
        #TODO
        return

    @staticmethod
    def delete_discussions(id):
        #TODO
        return

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
        return (op,collection,id)
    else:
        return 'Junk message'



def opHandler(op_collection_userId_tuple):
    m = globals()['OpHandler']()
    func_name = "{0}_{1}".format(op_collection_userId_tuple[0].lower(),op_collection_userId_tuple[1].lower())
    func = getattr(m, func_name)
    return func(op_collection_userId_tuple[2])


def main():
    consumer = KafkaConsumer('barak.barak-db.users',value_deserializer=lambda m: json.loads(m.decode('utf-8')))
    for msg in consumer:
        op_collection_userId_tuple = get_params_from_message(msg) 
        print(op_collection_userId_tuple)
        print('\n')
        #print(opHandler(op_collection_userId_tuple))


if __name__ == "__main__":
    main() 
