from pydantic import BaseModel, Field
from typing import ClassVar, Optional, Literal


class MongoDBAtlassConfig(BaseModel):
    from pymongo import MongoClient

    MongoClient: ClassVar[type] = MongoClient
    
    collection_name: str = Field("mem0", description="Name of the collection")
    embedding_model_dims: Optional[int] = Field(1536, description="Dimensions of the embedding model")
    uri: str = Field(None, description="uri string to connect to MongoDB Atlass")
    database_name: Optional[str] = Field("mem0_db", description="name of the database in MongoDB Atlass")
    vector_field: Optional[str] = Field("vector_embedding", description="Path to the vector field in your documents")
    similarity: Literal[
        'euclidian', 'cosine', 'dotProduct'
        ] = Field('cosine', description='way to find evaluate similarity of two vectors')
