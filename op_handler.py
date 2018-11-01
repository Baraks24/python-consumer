from mongo_aggregations import projects_aggregation,users_aggregation,discussions_aggregation,tasks_aggregation,index2collection
from elasticsearch_wrapper import create_doc,delete_doc,update_doc,search_related_docs,bulk
from config import USERS_INDEX,PROJECTS_INDEX,DISCUSSIONS_INDEX,TASKS_INDEX,UPDATABLE_INDICES



create_factory = lambda id,aggregation,index: create_doc(index,*(list(aggregation(id))))
update_factory = lambda id,aggregation,index: update_doc(index,*(list(aggregation(id))))
delete_factory = lambda id,index: delete_doc(index,id)

class OpHandler:

    @staticmethod
    def execute(op_collection):
        m = globals()['OpHandler']()
        func_name = "{0}_{1}".format(op_collection[0].lower(),op_collection[1].lower())
        func = getattr(m, func_name)
        return func


    @staticmethod
    def create_users(id):
        #run user aggregation pipeline and write to elastic
        #run aggregation
        create_factory(id,users_aggregation,USERS_INDEX)
        # agg_res = users_aggregation(id)
        # res = list(agg_res)
        # #write res to elastic
        # create_doc(USERS_INDEX,*res) # * -spread operator
        return

    @staticmethod
    def update_users(id):
        #TODO need to find all relevant entities and rerun their aggregations
        update_factory(id,users_aggregation,USERS_INDEX)
        #run aggregation
        # agg_res = users_aggregation(id)
        # res = list(agg_res)
        #update user
        # update_doc(USERS_INDEX,*res)
        #find all relevant entities
        #update all relevant entities
        return

    @staticmethod
    def delete_users(id):
        #TODO need to find all relevant entities and rerun their aggregations
        delete_factory(id,USERS_INDEX)
        #find all relevant entities
        #rerun all entities aggregations
        #update all entities
        delete_doc(USERS_INDEX,id)
        return

    @staticmethod
    def create_tasks(id):
        #run aggregation
        create_factory(id,tasks_aggregation,TASKS_INDEX)
        # agg_res = tasks_aggregation(id)
        # res = list(agg_res)
        #write aggregation to elastic
        #print("res:")
        #print(res)
        # create_doc(TASKS_INDEX,*res)
        return

    @staticmethod
    def transform_es2bulk(search_res):
        elastic_bulk_update_array=[]
        for ind in UPDATABLE_INDICES:
            ind_ids=[doc['id'] for doc in search_res if doc["index"]==ind]
            if(ind_ids and len(ind_ids)>0):
                agg_result = index2collection[ind]['bulk_aggregation'](ind_ids)
                elastic_bulk_update_array.extend([{"id":doc["_id"],"index":ind,"doc":doc} for doc in agg_result])

        bulk(elastic_bulk_update_array)
        return
        

        
        #TODO Group documents by their indices

        #TODO Bulk-aggregate each array 
        #TODO Create Action array for bulk update
        #TODO Call bulk

        print('search result/////////////////////////////')
        print(search_res)

    @staticmethod
    def update_tasks(id):
        # agg_res = tasks_aggregation(id)
        # res = list(agg_res)
        # update_doc(TASKS_INDEX,*res)
        #TODO find all relevant entities and rerun their aggregations
        #print('search result/////////////////////////////////////////////')
        #print(search_related_docs(id))
        # print("before es")
        update_factory(id,tasks_aggregation,TASKS_INDEX)
        search_res = search_related_docs(id)
        print('search result/////////////////////////////////////////////')
        print(search_related_docs(id))
        OpHandler.transform_es2bulk(search_res)

        return


    @staticmethod
    def delete_tasks(id):
        #TODO find all relevant entities and rerun their aggregations

        # delete_doc(TASKS_INDEX,id)
        delete_factory(id,TASKS_INDEX)
        return

    @staticmethod
    def create_projects(id):
        #run aggregation
        # agg_res = projects_aggregation(id)
        # res = list(agg_res)
        #print("res:")
        #print(res)
        #write aggregation to elastic
        # create_doc(PROJECTS_INDEX,*res)
        create_factory(id,projects_aggregation,PROJECTS_INDEX)
        #TODO
        return

    @staticmethod
    def update_projects(id):
        #run aggregation
        # agg_res = projects_aggregation(id)
        # res = list(agg_res)
        #print("res:")
        #print(res)
        #write aggregation to elastic
        # update_doc(PROJECTS_INDEX,*res)
        update_factory(id,projects_aggregation,PROJECTS_INDEX)
        search_res = search_related_docs(id)
        OpHandler.transform_es2bulk(search_res)
        print('search result/////////////////////////////')
        print(search_res)
        return

    @staticmethod
    def delete_projects(id):
        # delete_doc(PROJECTS_INDEX,id)
        delete_factory(id,PROJECTS_INDEX)
        return

    @staticmethod
    def create_discussions(id):
        #TODO
        #run aggregation
        # agg_res = discussions_aggregation(id)
        # res = list(agg_res)
        # print(res)
        #write aggregation to elastic
        # create_doc(DISCUSSIONS_INDEX,*res)
        create_factory(id,discussions_aggregation,DISCUSSIONS_INDEX)
        return

    @staticmethod
    def update_discussions(id):
        # agg_res = discussions_aggregation(id)
        # res = list(agg_res)
        # print(res)
        # update_doc(DISCUSSIONS_INDEX,*res)
        update_factory(id,discussions_aggregation,DISCUSSIONS_INDEX)
        search_res = search_related_docs(id)
        OpHandler.transform_es2bulk(search_res)
        print('search result/////////////////////////////')
        print(search_res)
        return

    @staticmethod
    def delete_discussions(id):
        # delete_doc(DISCUSSIONS_INDEX,id)
        delete_factory(id,DISCUSSIONS_INDEX)
        return

    @staticmethod
    def create_updates(id):
        # print('Update:')
        # print(id)
        #TODO: Do Something Useful
        return
