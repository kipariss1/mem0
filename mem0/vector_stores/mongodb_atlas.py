from mem0.vector_stores.base import VectorStoreBase

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from langchain.vectorstores import MongoDBAtlasVectorSearch
from pymongo.errors import CollectionInvalid

from typing import List

import logging

# TODO: Finish abstract methods with langchain, find a way to abstract the Emberdder choice for langchain vector store creaton 

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
                params['server_api'] = ServerApi(version='1') 
            self.client = MongoClient(**params)
        self.collection_name = collection_name
        self.database = self.client.get_database(database_name)
        self.collection = None
        self.create_col(embedding_model_dims)

    def create_col(self, vector_size):
        try:
            self.collection = self.database.create_collection(self.collection_name, check_exists=True)
        except CollectionInvalid:
            logger.info("Collection already exists, steps on creating collection on vectore store are skipped")
            self.collection = self.database[self.collection_name]

    def insert(self, name, vectors, payloads=None, ids=None):
        pass

    def search(self, name, query, limit=5, filters=None):
        # TODO: test after something is added to the collection
        self.collection.find(filter=query, limit=limit)
    
    def delete(self, name, vector_id):
        pass

    def update(self, name, vector_id, vector=None, payload=None):
        pass

    def get(self, name, vector_id):
        pass

    def list_cols(self) -> List[str]:
        return self.database.list_collection_names()

    def delete_col(self, name):
        self.database.drop_collection(name)

    def col_info(self, name):
        return self.database.get_collection(name)
        
