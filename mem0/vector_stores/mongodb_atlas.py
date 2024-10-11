from mem0.vector_stores.base import VectorStoreBase

from pymongo import MongoClient
from langchain.vectorstores import MongoDBAtlasVectorSearch

import logging

# TODO: check here if pymongo installed and try to import it, if not - install

logger = logging.getLogger(__name__)

class MongoDBAtlas(VectorStoreBase):
    
    def __init__(
            self,
            collection_name: str,
            embedding_model_dims: int,
            client: MongoClient = None,
            uri: str = None,
            database_name: str = None
    ) -> None:
        if client:
            self.client = client
        else:
            params = {}
            if uri:
                params['host'] = uri
            self.client = MongoClient(**params)
        try:
            self.database = self.client.get_database(database_name)
            self.collection = self.database.get_collection(collection_name)
        except:
            logger.error("The MongoDB Atlas database couldn't connect to database")
            self.database = None
            self.collection = None
        self.create_col(collection_name, embedding_model_dims)

    def create_col(self, name, vector_size, distance):
        # TODO: implement it with checking if collection exists already
        pass

    def insert(self, name, vectors, payloads=None, ids=None):
        pass

    def search(self, name, query, limit=5, filters=None):
        pass
    
    def delete(self, name, vector_id):
        pass

    def update(self, name, vector_id, vector=None, payload=None):
        pass

    def get(self, name, vector_id):
        pass

    def list_cols(self):
        pass

    def delete_col(self, name):
        pass

    def col_info(self, name):
        pass
        
