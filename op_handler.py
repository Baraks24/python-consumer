from mongo_aggregations import projects_aggregation,users_aggregation,discussions_aggregation,tasks_aggregation
from elasticsearch_wrapper import create_doc,delete_doc,update_doc
from config import USERS_INDEX,PROJECTS_INDEX,DISCUSSIONS_INDEX,TASKS_INDEX


class OpHandler:
    @staticmethod
    def create_users(id):
        #run user aggregation pipeline and write to elastic
        #run aggregation
        agg_res = users_aggregation(id)
        res = list(agg_res)
        #write res to elastic
        create_doc(USERS_INDEX,*res) # * -spread operator
        return

    @staticmethod
    def update_users(id):
        #TODO need to find all relevant entities and rerun their aggregations
        #run aggregation
        agg_res = users_aggregation(id)
        res = list(agg_res)
        #update user
        update_doc(USERS_INDEX,*res)
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
        res = list(agg_res)
        #write aggregation to elastic
        print("res:")
        print(res)
        create_doc(TASKS_INDEX,*res)
        return

    @staticmethod
    def update_tasks(id):
        agg_res = tasks_aggregation(id)
        res = list(agg_res)
        update_doc(TASKS_INDEX,*res)
        #TODO find all relevant entities and rerun their aggregations
        return

    @staticmethod
    def delete_tasks(id):
        #TODO find all relevant entities and rerun their aggregations
        delete_doc(TASKS_INDEX,id)
        return

    @staticmethod
    def create_projects(id):
        #run aggregation
        agg_res = projects_aggregation(id)
        res = list(agg_res)
        print("res:")
        print(res)
        #write aggregation to elastic
        create_doc(PROJECTS_INDEX,*res)
        #TODO
        return

    @staticmethod
    def update_projects(id):
        #run aggregation
        agg_res = projects_aggregation(id)
        res = list(agg_res)
        print("res:")
        print(res)
        #write aggregation to elastic
        update_doc(PROJECTS_INDEX,*res)
        return

    @staticmethod
    def delete_projects(id):
        delete_doc(PROJECTS_INDEX,id)
        return

    @staticmethod
    def create_discussions(id):
        #TODO
        #run aggregation
        agg_res = discussions_aggregation(id)
        res = list(agg_res)
        print(res)
        #write aggregation to elastic
        create_doc(DISCUSSIONS_INDEX,*res)
        return

    @staticmethod
    def update_discussions(id):
        agg_res = discussions_aggregation(id)
        res = list(agg_res)
        print(res)
        update_doc(DISCUSSIONS_INDEX,*res)
        return

    @staticmethod
    def delete_discussions(id):
        delete_doc(DISCUSSIONS_INDEX,id)
        return

    @staticmethod
    def create_updates(id):
        print('Update:')
        print(id)
        #TODO: Do Something Useful
        return
