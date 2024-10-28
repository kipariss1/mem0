from mem0.vector_stores.base import VectorStoreBase

from pymongo.mongo_client import MongoClient
from pymongo.operations import SearchIndexModel
from pymongo.server_api import ServerApi
from pymongo.errors import CollectionInvalid

from typing import List, Dict, Any

import logging

# TODO: Finish abstract methods with langchain, find a way to abstract the Emberdder choice for langchain vector store creaton 

logger = logging.getLogger(__name__)

class MongoDBAtlas(VectorStoreBase):
    
    def __init__(
            self,
            collection_name: str,
            embedding_model_dims: int,
            vector_field: str,
            similarity: str,
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
        self._embeding_model_dims = embedding_model_dims
        self._similarity = similarity
        self._index_name = "vector-search-index"
        self.collection_name = collection_name
        self.vector_field = vector_field
        self.database = self.client.get_database(database_name)
        self.collection = None
        self.create_col()

    def _create_index(self):
        idxs = [idx['name'] for idx in self.collection.list_search_indexes().to_list()]
        if self._index_name in idxs:
            return
        search_index_model = SearchIndexModel(
            definition={
                "fields": [
                    {
                        "type": "vector",
                        "numDimensions": self._embeding_model_dims,
                        "path": self.vector_field,
                        "similarity": self._similarity
                    }
                ]
            },
            name=self._index_name,
            type="vectorSearch"
        )
        self.collection.create_search_index(model=search_index_model)

    def _update_index(self, filters: Dict[str, Any]):
        # TODO: get indexed fields from search index and check that all filters are present in the indexed fields
        pass

    def create_col(self):
        try:
            self.collection = self.database.create_collection(self.collection_name, check_exists=True)
        except CollectionInvalid:
            logger.info("Collection already exists, steps on creating collection on vectore store are skipped")
            self.collection = self.database[self.collection_name]
        self._create_index()

    def insert(self, vectors, payloads=None, ids=None):
        documents = []
        for idx, vector in enumerate(vectors):
            document = {
                self.vector_field: vector,
                "_id": ids[idx]
            }
            document.update(payloads[idx])
            documents.append(document)
        self.collection.insert_many(documents)


    def _construct_search_query(self, query, limit, filters):
        return [{
            "$vectorSearch": {
                "index": self._index_name,
                "path": self.vector_field,
                "queryVector": query,
                "filter": filters,
                "limit": limit,
                "numCandidates": limit
            }
        }]

    def search(self, query, limit=5, filters={}) -> list:
        # TODO: fix error with indexing filters for search index
        self._update_index(filters)
        result = self.collection.aggregate(self._construct_search_query(query, limit, filters))
        return result.to_list()
    
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
        
