#For elasticsearch
ELASTICSEARCH_HOSTS = ['10.0.0.31'] 
USERS_INDEX = "users_test"
PROJECTS_INDEX = "projects_test"
DISCUSSIONS_INDEX = "discussions_test"
TASKS_INDEX = "tasks_test"

#Kafka
DB = "icu-dev"
MONGO_URI='mongodb://10.0.0.42,10.0.0.43,10.0.0.44/?replicaSet=mongo-azure'
TOPICS= [
    'barak.barak-db.users',
    'barak.icu-dev.discussions',
    'barak.icu-dev.projects',
    'barak.icu-dev.tasks',
    'barak.icu-dev.updates',
    'barak.icu-dev.users'
]