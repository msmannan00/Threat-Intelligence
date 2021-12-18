# Local Imports
import pymongo

from crawler_services.native_services.mongo_manager.mongo_enums import MONGODB_KEYS, MANAGE_USER_MESSAGES, MONGO_CRUD
from crawler_services.native_services.mongo_manager.mongo_request_generator import mongo_request_generator
from crawler_services.shared_model.request_handler import request_handler
from native_services.constants.constant import CRAWL_SETTINGS_CONSTANTS
from native_services.log_manager.log_manager import log


class mongo_controller(request_handler):
    __instance = None
    __m_connection = None
    __m_mongo_request_generator = None

    # Initializations
    @staticmethod
    def get_instance():
        if mongo_controller.__instance is None:
            mongo_controller()
        return mongo_controller.__instance

    def __init__(self):
        mongo_controller.__instance = self
        self.__m_mongo_request_generator = mongo_request_generator()
        self.__link_connection()

    def __link_connection(self):
        self.__m_connection = pymongo.MongoClient(CRAWL_SETTINGS_CONSTANTS.S_DATABASE_IP, CRAWL_SETTINGS_CONSTANTS.S_DATABASE_PORT)[CRAWL_SETTINGS_CONSTANTS.S_DATABASE_NAME]

    def __create(self, p_data):
        try:
            self.__m_connection[p_data[MONGODB_KEYS.S_DOCUMENT]].insert(p_data[MONGODB_KEYS.S_VALUE])
            return True, MANAGE_USER_MESSAGES.S_INSERT_SUCCESS
        except Exception as ex:
            log.g().e("E1 : " + MANAGE_USER_MESSAGES.S_INSERT_FAILURE + " : " + str(ex))
            return False, str(ex)

    def __read(self, p_data, p_limit):
        try:
            if p_limit is not None:
                documents = self.__m_connection[p_data[MONGODB_KEYS.S_DOCUMENT]].find(p_data[MONGODB_KEYS.S_FILTER]).limit(p_limit)
            else:
                documents = self.__m_connection[p_data[MONGODB_KEYS.S_DOCUMENT]].find(p_data[MONGODB_KEYS.S_FILTER])
            return documents
        except Exception as ex:
            log.g().e("E3 : " + MANAGE_USER_MESSAGES.S_READ_FAILURE)
            return str(ex)

    def __update(self, p_data, p_upsert):
        try:
            self.__m_connection[p_data[MONGODB_KEYS.S_DOCUMENT]].update_many(p_data[MONGODB_KEYS.S_FILTER],p_data[MONGODB_KEYS.S_VALUE], upsert=p_upsert)
            return True, MANAGE_USER_MESSAGES.S_UPDATE_SUCCESS

        except Exception as ex:
            log.g().e("E4 : " + MANAGE_USER_MESSAGES.S_UPDATE_FAILURE)
            return False, str(ex)

    def __delete(self, p_data):
        try:
            documents = self.__m_connection[p_data[MONGODB_KEYS.S_DOCUMENT]].remove(p_data[MONGODB_KEYS.S_FILTER])
            return documents, MANAGE_USER_MESSAGES.S_DELETE_SUCCESS
        except Exception as ex:
            log.g().e("E2 : " + MANAGE_USER_MESSAGES.S_DELETE_FAILURE)
            return False, str(ex)

    def invoke_trigger(self, p_commands, p_data=None):
        m_request = self.__m_mongo_request_generator.invoke_trigger(p_data[0], p_data[1:])
        if p_commands == MONGO_CRUD.S_CREATE:
            return self.__create(m_request)
        elif p_commands == MONGO_CRUD.S_READ:
            return self.__read(m_request, p_data[1])
        elif p_commands == MONGO_CRUD.S_UPDATE:
            return self.__update(m_request, p_data[1])
        elif p_commands == MONGO_CRUD.S_DELETE:
            return self.__delete(m_request)
