"""
Embedding utilities for RAG system.
"""
from typing import List, Union
import numpy as np


class EmbeddingService:
    """Service for generating embeddings."""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self._model = None
    
    def initialize(self):
        """Initialize the embedding model."""
        try:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(self.model_name)
        except ImportError:
            raise ImportError("sentence-transformers not installed. Install with: pip install sentence-transformers")
    
    def embed_text(self, text: str) -> np.ndarray:
        """Generate embedding for a single text."""
        if self._model is None:
            self.initialize()
        return self._model.encode(text)
    
    def embed_texts(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for multiple texts."""
        if self._model is None:
            self.initialize()
        return self._model.encode(texts)



