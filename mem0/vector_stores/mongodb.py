from mem0.vector_stores.base import VectorStoreBase
from pymongo import MongoClient

# TODO: check here if pymongo installed and try to import it, if not - install


class MongoDB_Atlas(VectorStoreBase):
    
    def __init__(
            self,
            client: MongoClient = None,
            uri: str = None,
    ) -> None:
        if client:
            self.client = client
        else:
            params = {}
            if uri:
                params['host'] = uri
            self.client = MongoClient(**params)

    def  search(self):
        pass
        
