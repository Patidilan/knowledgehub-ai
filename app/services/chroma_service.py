import chromadb
from app.services.embedding_service import EmbeddingService

class ChromaService:

    COLLECTION_NAME = "knowledgehub"

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path="chroma_db"
        )

        self.collection = self.client.get_or_create_collection(
            name=self.COLLECTION_NAME
        )

    def add_document(
        self,
        chunk_id,
        text,
        embedding,
        metadata
    ):

        self.collection.add(
            ids=[chunk_id],
            documents=[text],
            embeddings=[embedding],
            metadatas=[metadata]
        )
    
    def search(self, query, n_results=5):

        query_embedding = EmbeddingService.generate_embedding(query)

        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
    )