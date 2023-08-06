from sentence_transformers import SentenceTransformer
import numpy as np

from clayrs.content_analyzer.embeddings.embedding_loader.embedding_loader import SentenceEmbeddingLoader


class Sbert(SentenceEmbeddingLoader):
    """
    Class that produces sentences embeddings using sbert.

    The model will be automatically downloaded if not present locally.

    Args:
        model_name_or_file_path: name of the model to download or path where the model is stored
            locally
    """

    def __init__(self, model_name_or_file_path: str = 'paraphrase-distilroberta-base-v1'):
        super().__init__(model_name_or_file_path)

    def load_model(self):
        try:
            return SentenceTransformer(self.reference)
        except (OSError, AttributeError):
            raise FileNotFoundError

    def get_vector_size(self) -> int:
        return self.model.get_sentence_embedding_dimension()

    def get_embedding(self, sentence: str) -> np.ndarray:
        return self.model.encode(sentence, show_progress_bar=False)

    def get_embedding_token(self, sentence: str) -> np.ndarray:
        raise NotImplementedError("The model chosen can't return token embeddings")

    def __str__(self):
        return "Sbert"

    def __repr__(self):
        return f"Sbert(model_name_or_file_path={self.reference})"
