import os
import time
from typing import List

import chromadb
import numpy as np
from chromadb import Settings
from sentence_transformers import SentenceTransformer

try: 
    from src.config import MODEL, FILE_DOCUMENTS, NAME_DOCUMENTS, SPACE, METHOD
except:
    from config import MODEL, FILE_DOCUMENTS, NAME_DOCUMENTS, SPACE, METHOD

class DocumentModel:
    """
        A class to manage document embeddings and searches using sentence transformers and ChromaDB.

        Attributes:
            model (SentenceTransformer): The sentence transformer model for encoding text.
            documents (List[str]): List of document paths.
            chroma_client (chromadb.PersistentClient): ChromaDB client for vector database operations.
            document_collection (chromadb.Collection): ChromaDB collection for storing document embeddings.
    """

    def __init__(self, documents: List[str]) -> None:
        """
            Initialize the DocumentModel with a list of documents.

            Args:
                documents (List[str]): List of document paths.
        """
        start_time = time.time()
        self.model = SentenceTransformer(MODEL)
        self.documents = documents
        self.chroma_client = chromadb.PersistentClient(FILE_DOCUMENTS, settings=Settings(allow_reset=True))
        self.chroma_client.reset()
        self.create_vector_database()
        self.add_documents_to_database()

        print("Sentence transformer model loaded")
        print('Time taken to create vector database: ', time.time() - start_time)

    def create_vector_database(self):
        """Create a new collection in ChromaDB for storing document embeddings."""
        self.document_collection = self.chroma_client.create_collection(NAME_DOCUMENTS, metadata={SPACE: METHOD})

    def read_document_content(self, file_path: str) -> str:
        """
            Read the content of a document file.

            Args:
                file_path (str): Path to the document file.

            Returns:
                str: Content of the document if it's a .txt file, empty string otherwise.
        """
        _, file_extension = os.path.splitext(file_path)
        if file_extension.lower() == '.txt':
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        else:
            return ""
        
    def add_documents_to_database(self):
        """Add all documents to the ChromaDB collection."""
        for idx, doc_path in enumerate(self.documents):
            content = self.read_document_content(doc_path)
            embedding = self.model.encode(content).tolist()
            self.document_collection.add(
                ids=[str(idx)],
                embeddings=[embedding],
                metadatas=[{"path": doc_path, "name": os.path.basename(doc_path)}],
                documents=[content]
            )
            print('Document added: ', doc_path)

    def search_document(self, search_text: str, n_results: int = 1):
        """
            Search for similar documents based on the given search text.

            Args:
                search_text (str): The text to search for.
                n_results (int, optional): Number of results to return. Defaults to 1.

            Returns:
                List[dict]: List of dictionaries containing search results.
        """
        query_embedding = self.model.encode(search_text).tolist()
        search_result = self.document_collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=["metadatas", "documents", "distances"]
        )
        results = []
        for metadata, document, distance in zip(search_result['metadatas'][0], search_result['documents'][0], search_result['distances'][0]):
            results.append({
                "name": metadata['name'],
                "path": metadata['path'],
                "content": document[:200] + "...",
                "similarity": 1 - distance
            })
        return results

