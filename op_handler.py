from mongo_aggregations import projects_aggregation,users_aggregation,discussions_aggregation,tasks_aggregation
from elasticsearch_wrapper import create_doc,delete_doc,update_doc

USERS_INDEX = "users"
PROJECTS_INDEX = "projects"
DISCUSSIONS_INDEX = "discussions"
TASKS_INDEX = "tasks"


class OpHandler:
    @staticmethod
    def create_users(id):
        #TODO run user aggregation pipeline and write to elastic
        #run aggregation
        agg_res = users_aggregation(id)
        print(agg_res)
        #write res to elastic
        create_doc(USERS_INDEX,*agg_res) # * -spread operator
        return

    @staticmethod
    def update_users(id):
        #TODO need to find all relevant entities and rerun their aggregations
        #run aggregation
        agg_res = users_aggregation(id)
        #update user
        update_doc(USERS_INDEX,*agg_res)
        #find all relevant entities
        #update all relevant entities
        return

    @staticmethod
    def delete_users(id):
        #TODO need to find all relevant entities and rerun their aggregations
        #find all relevant entities
        #rerun all entities aggregations
        #update all entities
        delete_doc(USERS_INDEX,id)
        return

    @staticmethod
    def create_tasks(id):
        #run aggregation
        agg_res = tasks_aggregation(id)
        #write aggregation to elastic
        create_doc(TASKS_INDEX,*agg_res)
        #TODO simply run aggregation and write to elastic
        return

    @staticmethod
    def update_tasks(id):
        #TODO find all relevant entities and rerun their aggregations
        return

    @staticmethod
    def delete_tasks(id):
        #TODO find all relevant antities and rerun their aggregations
        return

    @staticmethod
    def create_projects(id):
        #run aggregation
        agg_res = projects_aggregation(id)
        #write aggregation to elastic
        create_doc(PROJECTS_INDEX,*agg_res)
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
        #run aggregation
        agg_res = discussions_aggregation(id)
        #write aggregation to elastic
        create_doc(DISCUSSIONS_INDEX,*agg_res)
        return

    @staticmethod
    def update_discussions(id):
        #TODO
        return

    @staticmethod
    def delete_discussions(id):
        #TODO
        return
