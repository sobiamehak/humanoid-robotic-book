from typing import List, Dict, Any
from qdrant_client import QdrantClient
import openai
from uuid import UUID
import os
from ..config import settings
import tiktoken
import cohere


class RAGService:
    def __init__(self):
        # Check if required environment variables are set
        if settings.QDRANT_URL and settings.QDRANT_API_KEY:
            self.client = QdrantClient(
                url=settings.QDRANT_URL,
                api_key=settings.QDRANT_API_KEY
            )
            self.collection_name = settings.QDRANT_COLLECTION_NAME
        else:
            # If Qdrant is not configured, set to None to indicate service is unavailable
            self.client = None
            self.collection_name = None

        self.tokenizer = tiktoken.get_encoding("cl100k_base")

    def _get_query_embedding(self, query: str) -> List[float]:
        """
        Get embedding for the query using Cohere
        """
        if not settings.COHERE_API_KEY:
            # Return a basic embedding using a simple approach if API key not set
            # This is a very basic fallback that doesn't provide good embeddings
            # but at least allows the service to continue somewhat
            import hashlib
            encoded_query = query.encode('utf-8')
            hash_obj = hashlib.md5(encoded_query)
            hex_dig = hash_obj.hexdigest()

            # Convert hex digest to float vector
            embedding = []
            for i in range(0, len(hex_dig), 4):
                chunk = hex_dig[i:i+4]
                if len(chunk) == 4:
                    val = int(chunk, 16) / (16**4 - 1)  # Normalize to 0-1
                    embedding.append(val)

            # Pad or truncate to 1024 dimensions (Cohere embedding size)
            while len(embedding) < 1024:
                embedding.append(0.0)
            embedding = embedding[:1024]
            return embedding

        # Use Cohere's embedding API
        try:
            co = cohere.Client(settings.COHERE_API_KEY)
            response = co.embed(
                texts=[query],
                model="embed-english-v3.0",
                input_type="search_query"
            )
            return response.embeddings[0]
        except Exception as e:
            print(f"Error calling Cohere API: {str(e)}")
            # Return a basic fallback vector
            return [0.0] * 1024
    
    def retrieve_relevant_chunks(self,
                                query: str,
                                top_k: int = 5,
                                user_id: UUID = None) -> List[Dict[str, Any]]:
        """
        Retrieve the most relevant content chunks for a query
        """
        try:
            # Check if vector database is configured
            if self.client is None or self.collection_name is None:
                # Return mock content based on simple keyword matching
                # This is a very basic fallback for demonstration purposes
                mock_content = [
                    {
                        "id": "1",
                        "content": f"This is mock content related to your query: '{query}'. The Physical AI & Humanoid Robotics textbook covers topics such as robot operating systems (ROS 2), kinematics, dynamics, perception systems, locomotion, manipulation, machine learning for robotics, and ethical considerations.",
                        "chapter_id": "intro",
                        "module_id": "foundations",
                        "title": "Introduction to Physical AI & Humanoid Robotics",
                        "score": 0.9,
                        "metadata": {}
                    }
                ]
                return mock_content[:top_k]

            # Get embedding for the query
            query_embedding = self._get_query_embedding(query)

            # Search in Qdrant
            search_result = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=top_k,
                with_payload=True
            )

            # Format results
            relevant_chunks = []
            for hit in search_result:
                content = hit.payload["content"]
                # Limit content length to avoid overly long context
                if len(content) > 400:
                    content = content[:400] + "..."

                chunk_data = {
                    "id": hit.id,
                    "content": content,
                    "chapter_id": hit.payload["chapter_id"],
                    "module_id": hit.payload["module_id"],
                    "title": hit.payload["title"],
                    "score": hit.score,
                    "metadata": {k: v for k, v in hit.payload.items()
                                if k not in ["content", "chapter_id", "module_id", "title"]}
                }
                relevant_chunks.append(chunk_data)

            return relevant_chunks

        except Exception as e:
            print(f"Error retrieving relevant chunks: {str(e)}")
            # Return mock content as a fallback
            mock_content = [
                {
                    "id": "1",
                    "content": f"This is mock content related to your query: '{query}'. The Physical AI & Humanoid Robotics textbook covers topics such as robot operating systems (ROS 2), kinematics, dynamics, perception systems, locomotion, manipulation, machine learning for robotics, and ethical considerations.",
                    "chapter_id": "intro",
                    "module_id": "foundations",
                    "title": "Introduction to Physical AI & Humanoid Robotics",
                    "score": 0.9,
                    "metadata": {}
                }
            ]
            return mock_content
    
    def generate_response(self,
                         query: str,
                         context_chunks: List[Dict[str, Any]],
                         user_context: Dict[str, Any] = None) -> str:
        """
        Generate a response using OpenAI based on the retrieved context
        """
        try:
            # Construct the context from retrieved chunks
            context = "\n\n".join([chunk["content"] for chunk in context_chunks])

            # Include user context if provided (for personalization)
            if user_context:
                user_background = user_context.get("background_info", {})
                user_context_text = f"User background: {str(user_background)}\n\n" if user_background else ""
            else:
                user_context_text = ""

            # Special handling for greetings
            greetings = ['hi', 'hello', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening', 'good night']
            if query.lower().strip() in greetings:
                return "Hello! I'm your AI assistant for the Physical AI & Humanoid Robotics textbook. How can I help you with questions about robotics, AI, humanoid robots, or related topics from the textbook?"

            # Construct the prompt
            system_message = "You are an AI assistant for the Physical AI & Humanoid Robotics textbook. Answer questions based on the provided context. Be concise and specific to the user's question. Only use information from the provided context."

            prompt = f"""
            Context information:
            {context}

            Question: {query}

            Please provide a concise, helpful answer to the question based on the context provided. Focus specifically on answering the question asked. If the context does not contain enough information to answer the question, acknowledge this briefly. Limit your response to 2-3 sentences when possible.
            """

            if settings.OPENROUTER_API_KEY:
                # Use OpenRouter API to generate the response
                import openai

                # Set the API key and base URL for OpenRouter
                client = openai.OpenAI(
                    api_key=settings.OPENROUTER_API_KEY,
                    base_url="https://openrouter.ai/api/v1"
                )

                try:
                    response = client.chat.completions.create(
                        model="anthropic/claude-3.5-sonnet",  # Using Claude 3.5 Sonnet as requested
                        messages=[
                            {"role": "system", "content": system_message},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.3,
                        max_tokens=500  # Reduced for more concise responses
                    )
                    return response.choices[0].message.content
                except Exception as e:
                    print(f"Error calling OpenRouter API: {str(e)}")
                    # Fallback to simple response if OpenRouter call fails
                    pass

            # If OpenRouter API key is not configured or API call fails, create a simple response based on the context
            # This is a basic fallback that just formats the retrieved context
            if len(context) > 300:
                context_preview = context[:300] + "..."
            else:
                context_preview = context
            response = f"Based on the textbook content: {context_preview}\n\nFor more detailed information, please refer to the relevant chapters in the textbook."
            return response

        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return "Sorry, I encountered an error while generating a response."
    
    def query(self,
              query: str,
              user_id: UUID = None,
              top_k: int = 5,
              user_context: Dict[str, Any] = None,
              selected_text: str = None,
              context_type: str = "entire_book") -> Dict[str, Any]:
        """
        Main RAG query method that retrieves relevant chunks and generates a response
        """
        relevant_chunks = []

        # If selected text is provided and context_type is "selected_text",
        # use only the selected text as context
        if selected_text and context_type == "selected_text":
            # Create a fake chunk using the selected text
            selected_chunk = {
                "id": "selected_text",
                "content": selected_text,
                "chapter_id": "selected",
                "module_id": "selected",
                "title": "Selected Text",
                "score": 1.0,
                "metadata": {}
            }
            relevant_chunks = [selected_chunk]
        else:
            # Retrieve relevant chunks from the vector database
            relevant_chunks = self.retrieve_relevant_chunks(query, top_k, user_id)

        # Generate response based on chunks
        response = self.generate_response(query, relevant_chunks, user_context)

        # Format the result
        result = {
            "query": query,
            "response": response,
            "sources": [
                {
                    "chapter_id": chunk["chapter_id"],
                    "module_id": chunk["module_id"],
                    "title": chunk["title"],
                    "score": chunk["score"],
                    "content_snippet": chunk["content"][:200] + "..." if len(chunk["content"]) > 200 else chunk["content"]
                }
                for chunk in relevant_chunks
            ]
        }

        return result