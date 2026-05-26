"""
Vector store implementation using LanceDB.
"""
from typing import List, Dict, Any, Optional
import os


class VectorStore:
    """LanceDB vector store for RAG system."""
    
    def __init__(self, db_path: str = "./data/lancedb"):
        self.db_path = db_path
        self.db = None
        self.table = None
    
    def initialize(self, table_name: str = "resumes"):
        """Initialize LanceDB connection."""
        try:
            import lancedb
            os.makedirs(self.db_path, exist_ok=True)
            self.db = lancedb.connect(self.db_path)
            self.table_name = table_name
        except ImportError:
            raise ImportError("lancedb not installed. Install with: pip install lancedb")
    
    def create_table(self, data: List[Dict[str, Any]]):
        """Create a new table with data."""
        if self.db is None:
            self.initialize()
        self.table = self.db.create_table(self.table_name, data, mode="overwrite")
    
    def add_documents(self, documents: List[Dict[str, Any]]):
        """Add documents to the vector store."""
        if self.table is None:
            self.create_table(documents)
        else:
            self.table.add(documents)
    
    def search(self, query_vector: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """Search for similar documents."""
        if self.table is None:
            raise ValueError("Table not initialized. Call initialize() or add_documents() first.")
        
        results = self.table.search(query_vector).limit(limit).to_list()
        return results
    
    def delete_table(self):
        """Delete the current table."""
        if self.db and self.table:
            self.db.drop_table(self.table_name)



