from pydantic import BaseModel, Field, model_validator
from typing import ClassVar, Optional, Dict, Any


class MongoDBAtlassConfig(BaseModel):
    from pymongo import MongoClient

    MongoClient: ClassVar[type] = MongoClient
    
    collection_name: str = Field("mem0", description="Name of the collection")
    embedding_model_dims: Optional[int] = Field(1536, description="Dimensions of the embedding model")
    uri: str = Field(None, description="uri string to connect to MongoDB Atlass")
    database_name: Optional[str] = Field("mem0_db", description="name of the database in MongoDB Atlass")
