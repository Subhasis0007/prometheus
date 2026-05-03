import chromadb
from chromadb.config import Settings
import uuid
from datetime import datetime

class AdvancedMemory:
    def __init__(self, persist_directory="./prometheus_db"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Short-term memory (recent conversation)
        self.short_term = []
        self.max_short_term = 10
        
        # Long-term memory (semantic search)
        try:
            self.long_term = self.client.get_collection("prometheus_long_term")
        except:
            self.long_term = self.client.create_collection("prometheus_long_term")
    
    def add(self, text, metadata=None):
        if metadata is None:
            metadata = {}
        
        # Add to short-term
        self.short_term.append({
            "text": text,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata
        })
        
        # Keep only recent
        if len(self.short_term) > self.max_short_term:
            self.short_term.pop(0)
        
        # Add to long-term with embedding
        self.long_term.add(
            documents=[text],
            metadatas=[metadata],
            ids=[str(uuid.uuid4())]
        )
    
    def search(self, query, n_results=5):
        # Search long-term memory
        results = self.long_term.query(
            query_texts=[query],
            n_results=n_results
        )
        
        # Combine with short-term
        short_term_texts = [item["text"] for item in self.short_term]
        
        # Return combined context
        context = short_term_texts + results["documents"][0] if results["documents"] else short_term_texts
        return context[:n_results]
    
    def get_recent(self, n=5):
        return [item["text"] for item in self.short_term[-n:]]