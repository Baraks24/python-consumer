import json
from pymongo import MongoClient
from bson.objectid import ObjectId
from functools import reduce

DB = "barak-db"
UPDATE = 'u'
DELETE = 'd'
CREATE = 'c'

client = MongoClient('mongodb://10.0.0.42,10.0.0.43,10.0.0.44/?replicaSet=mongo-azure')
db_input = client[DB]
tasks = db_input.tasks
users = db_input.users
projects = db_input.projects
task_archive = db_input["task_archive"]

ordertasks = db_input.ordertasks
discussions = db_input.discussions
updates = db_input.updates
update_archive = db_input["update_archive"]


"""
takes array of arrays and reduces them into a single array
"""
aoa2a = lambda aoa:list(reduce(lambda mem,a:mem+a,aoa,[]))

def match_stage(id):
    return [{"$match":{"_id":ObjectId(id)}}]

def populate_creator_stage():
    return [
        {"$lookup":{
        "from":"users",
        "localField":"creator",
        "foreignField":"_id",
        "as":"creator"}
    },
    {
        "$unwind":"$creator"
    },
    ]

def populate_assign_stage():
    return [
            {"$lookup":{
        "from":"users",
        "localField":"assign",
        "foreignField":"_id",
        "as":"assign"}
    },
    {
        "$unwind":"$assign"
    },
    ]

def get_updates_stage():
    return [
            {"$lookup":{
        "from":"updates",
        "localField":"_id",
        "foreignField":"issueId",
        "as":"updates"}
    }
    ]

def tasks_filter_stage():
    return [
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
    }
    ]

def tasks_subtasks_stage():
    return [
           {
        "$graphLookup":{
            "from": "tasks",
            "startWith": "$subTasks",
            "connectFromField": "subTasks",
            "connectToField": "_id",
            "as": "subTasksHierarchy"
        }
    }
    ]

def populate_wachers_stage():
    return [
          {
        "$lookup":{
            "from":"users",
            "localField":"watchers",
            "foreignField":"_id",
            "as":"watchers"}
    }
    ]

def populate_viewers_stage():
    return [
           {
        "$lookup":{
        "from":"users",
        "localField":"viewers.id",
        "foreignField":"_id",
        "as":"viewers"} 
    }
    ]

def populate_commenters_stage():
    return [
         {
        "$lookup":{
            "from":"users",
            "localField":"commenters.id",
            "foreignField":"_id",
            "as":"commenters"} 
    }
    ]

def populate_editors_stage():
    return [
          {
        "$lookup":{
            "from":"users",
            "localField":"editors.id",
            "foreignField":"_id",
            "as":"editors"} 
    }
    ]

def projects_filter_stage():
    return [
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
    }
    ]

def users_project_stage():
    return [
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
    }
    ]

def users_populate_stars_stage():
    return [
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
    }
    ]

def tasks_aggregation(id):
    pipeline = []
    pipeline += match_stage(id)
    pipeline += populate_creator_stage()
    pipeline += populate_assign_stage()
    pipeline += get_updates_stage()
    pipeline += tasks_filter_stage()
    pipeline += tasks_subtasks_stage()
    pipeline += populate_wachers_stage()
    pipeline += populate_viewers_stage()
    pipeline += populate_commenters_stage()
    pipeline += populate_editors_stage()
    return tasks.aggregate(pipeline=pipeline)


def projects_aggregation(id):
    pipeline = []
    pipeline += match_stage(id)
    pipeline += populate_creator_stage()
    pipeline += populate_assign_stage()
    pipeline += get_updates_stage()
    pipeline += projects_filter_stage()
    pipeline += populate_wachers_stage()
    pipeline += populate_viewers_stage()
    pipeline += populate_commenters_stage()
    pipeline += populate_editors_stage()
    return projects.aggregate(pipeline=pipeline)

"""
Aggregation for users
"""

def users_aggregation(id):
    pipeline = []
    pipeline += match_stage(id)
    pipeline += users_project_stage()
    pipeline += users_populate_stars_stage()
    return users.aggregate(pipeline=pipeline)


def discussions_aggregation(id):
    pipeline = [
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
    return discussions.aggregate(pipeline=pipeline)

