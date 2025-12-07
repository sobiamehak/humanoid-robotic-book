from typing import List, Dict, Any
import openai
from qdrant_client import QdrantClient
from qdrant_client.http import models
import tiktoken
from uuid import uuid4
from ..config import settings


class ContentIngestionService:
    def __init__(self):
        self.client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY
        )
        self.collection_name = "textbook_content"
        self.tokenizer = tiktoken.get_encoding("cl100k_base")  # OpenAI's tokenizer
        
        # Initialize the collection if it doesn't exist
        self._initialize_collection()
    
    def _initialize_collection(self):
        """
        Initialize the Qdrant collection with appropriate vector configuration
        """
        try:
            # Check if collection exists
            self.client.get_collection(self.collection_name)
        except:
            # Create collection if it doesn't exist
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=1536,  # Size of OpenAI's text-embedding-ada-002 vectors
                    distance=models.Distance.COSINE
                )
            )
    
    def _chunk_text(self, text: str, max_tokens: int = 800, overlap: int = 200) -> List[str]:
        """
        Chunk text into smaller pieces with overlap
        """
        tokens = self.tokenizer.encode(text)
        chunks = []
        
        start_idx = 0
        while start_idx < len(tokens):
            end_idx = start_idx + max_tokens
            
            # Make sure we don't exceed the text length
            if end_idx > len(tokens):
                end_idx = len(tokens)
                
            chunk_tokens = tokens[start_idx:end_idx]
            chunk_text = self.tokenizer.decode(chunk_tokens)
            chunks.append(chunk_text)
            
            # Move with overlap
            start_idx = end_idx - overlap
            
            # If overlap would cause us to go back, just move forward by max_tokens
            if start_idx >= end_idx:
                start_idx = end_idx
        
        return chunks
    
    def _get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Get embeddings for a list of texts using OpenAI
        """
        if not settings.OPENAI_API_KEY:
            # If OpenAI API key is not configured, return placeholder embeddings
            # This allows the system to work in development without API keys, though with reduced quality
            embeddings = []
            for text in texts:
                embedding = [0.0] * 1536  # Placeholder
                embeddings.append(embedding)
            return embeddings

        # Set the OpenAI API key
        openai.api_key = settings.OPENAI_API_KEY

        try:
            # Create embeddings using OpenAI API
            # We'll process in batches to respect API limits
            embeddings = []
            batch_size = 10  # OpenAI allows up to 2048 texts per request, but using smaller batch for safety

            for i in range(0, len(texts), batch_size):
                batch = texts[i:i+batch_size]

                # In newer versions of OpenAI library, use:
                # response = openai.embeddings.create(input=batch, model="text-embedding-ada-002")
                # embeddings.extend([item.embedding for item in response.data])

                # For compatibility with older versions:
                response = openai.Embedding.create(input=batch, model="text-embedding-ada-002")
                batch_embeddings = [item['embedding'] for item in response['data']]
                embeddings.extend(batch_embeddings)

            return embeddings
        except Exception as e:
            print(f"Error getting embeddings from OpenAI: {str(e)}")
            # Return placeholder embeddings as fallback
            embeddings = []
            for text in texts:
                embedding = [0.0] * 1536  # Placeholder
                embeddings.append(embedding)
            return embeddings
    
    def ingest_document(self, 
                       content: str, 
                       chapter_id: str, 
                       module_id: str, 
                       title: str,
                       metadata: Dict[str, Any] = None) -> bool:
        """
        Ingest a document (chapter/section) into Qdrant
        """
        try:
            # Add default metadata if not provided
            if metadata is None:
                metadata = {}
            
            # Chunk the content
            chunks = self._chunk_text(content)
            
            # Get embeddings for chunks
            embeddings = self._get_embeddings(chunks)
            
            # Prepare points for Qdrant
            points = []
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                point_id = str(uuid4())
                
                payload = {
                    "content": chunk,
                    "chapter_id": chapter_id,
                    "module_id": module_id,
                    "title": title,
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                    **metadata  # Include any additional metadata
                }
                
                points.append(
                    models.PointStruct(
                        id=point_id,
                        vector=embedding,
                        payload=payload
                    )
                )
            
            # Upload to Qdrant
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            
            return True
            
        except Exception as e:
            print(f"Error ingesting document: {str(e)}")
            return False
    
    def bulk_ingest(self, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Bulk ingest multiple documents
        """
        results = {
            "successful": 0,
            "failed": 0,
            "errors": []
        }
        
        for doc in documents:
            try:
                success = self.ingest_document(
                    content=doc.get("content", ""),
                    chapter_id=doc.get("chapter_id", ""),
                    module_id=doc.get("module_id", ""),
                    title=doc.get("title", ""),
                    metadata=doc.get("metadata", {})
                )
                
                if success:
                    results["successful"] += 1
                else:
                    results["failed"] += 1
                    
            except Exception as e:
                results["failed"] += 1
                results["errors"].append(str(e))
        
        return results