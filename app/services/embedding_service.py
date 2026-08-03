from ollama import embed


class EmbeddingService:

    MODEL = "nomic-embed-text"

    @staticmethod
    def generate_embedding(text: str):

        response = embed(
            model=EmbeddingService.MODEL,
            input=text
        )

        return response["embeddings"][0]