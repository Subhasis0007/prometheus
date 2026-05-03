import chromadb
from chromadb.config import Settings
import uuid
from datetime import datetime
from src.utils.logger import logger

class LongTermMemory:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="./prometheus_db", settings=Settings(anonymized_telemetry=False))
        self.collection = self.client.get_or_create_collection(name="eternal_mind", metadata={"hnsw:space": "cosine"})
        logger.info("Hierarchical memory initialized")

    def add(self, text: str, metadata: dict = None):
        if metadata is None:
            metadata = {}
        metadata["timestamp"] = datetime.now().isoformat()
        self.collection.add(documents=[text], metadatas=[metadata], ids=[str(uuid.uuid4())])
        logger.info(f"Memory stored: {text[:80]}...")

    def search(self, query: str, n_results: int = 6):
        results = self.collection.query(query_texts=[query], n_results=n_results)
        return results["documents"][0] if results["documents"] else []