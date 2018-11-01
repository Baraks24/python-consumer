#For elasticsearch
# ELASTICSEARCH_HOSTS = ['localhost:9200'] 
ELASTICSEARCH_HOSTS = ['elasticsearch:9200'] 
#ELASTICSEARCH_HOSTS=['10.100.11.104:9200']
USERS_INDEX = "users_test"
PROJECTS_INDEX = "projects_test"
DISCUSSIONS_INDEX = "discussions_test"
TASKS_INDEX = "tasks_test"
UPDATABLE_INDICES=[USERS_INDEX,PROJECTS_INDEX,DISCUSSIONS_INDEX,TASKS_INDEX]

es2mongo = {}
mongo2es = {}

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

#Testing
TESTS_INDEX = "tests"