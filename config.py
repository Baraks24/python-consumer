#For elasticsearch
ELASTICSEARCH_HOSTS = ['elasticsearch:9200'] 
USERS_INDEX = "users_test"
PROJECTS_INDEX = "projects_test"
DISCUSSIONS_INDEX = "discussions_test"
TASKS_INDEX = "tasks_test"

#Kafka
KAFKA_URL = "kafka:9092"
DB = "icu-dev"
MONGO_URI='mongodb://mongodb:27017/?replicaSet=mongo-azure'
TOPICS= [
    'barak.test.despacito',
    'barak.barak-db.users',
    'barak.icu-dev.discussions',
    'barak.icu-dev.projects',
    'barak.icu-dev.tasks',
    'barak.icu-dev.updates',
    'barak.icu-dev.users'
]