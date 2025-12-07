from typing import List, Dict, Any
from qdrant_client import QdrantClient
import openai
from uuid import UUID
import os
from ..config import settings
import tiktoken


class RAGService:
    def __init__(self):
        # Check if required environment variables are set
        if settings.QDRANT_URL and settings.QDRANT_API_KEY:
            self.client = QdrantClient(
                url=settings.QDRANT_URL,
                api_key=settings.QDRANT_API_KEY
            )
            self.collection_name = "textbook_content"
        else:
            # If Qdrant is not configured, set to None to indicate service is unavailable
            self.client = None
            self.collection_name = None

        self.tokenizer = tiktoken.get_encoding("cl100k_base")

    def _get_query_embedding(self, query: str) -> List[float]:
        """
        Get embedding for the query using OpenAI
        """
        if not settings.OPENAI_API_KEY:
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

            # Pad or truncate to 1536 dimensions (OpenAI embedding size)
            while len(embedding) < 1536:
                embedding.append(0.0)
            embedding = embedding[:1536]
            return embedding

        # In a real implementation, you'd call OpenAI's embedding API
        # Example: response = openai.Embedding.create(input=[query], model="text-embedding-ada-002")
        # return response['data'][0]['embedding']

        # For now, return a vector of the right size
        return [0.0] * 1536
    
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
                    },
                    {
                        "id": "2",
                        "content": f"Additional information related to '{query}': Humanoid robots are designed with human-like characteristics and capabilities. They feature bipedal locomotion, dexterous manipulation, and advanced perception systems for human environments.",
                        "chapter_id": "chapter-01",
                        "module_id": "foundations",
                        "title": "Chapter 1: Introduction to Physical AI & Humanoid Robotics",
                        "score": 0.8,
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
                chunk_data = {
                    "id": hit.id,
                    "content": hit.payload["content"],
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

            # Construct the prompt
            prompt = f"""
            {user_context_text}
            Context information:
            {context}

            Question: {query}

            Please provide a detailed answer to the question based on the context provided.
            If the context does not contain enough information to answer the question,
            politely explain that the information is not available in the provided context.

            Also provide citations indicating which chapters/modules this information comes from.
            """

            if settings.OPENAI_API_KEY:
                # Use OpenAI API to generate the response
                import openai

                # Set the API key
                openai.api_key = settings.OPENAI_API_KEY

                try:
                    # For newer versions of OpenAI library:
                    # response = openai.chat.completions.create(
                    #     model="gpt-3.5-turbo",  # or gpt-4 if available
                    #     messages=[
                    #         {"role": "system", "content": "You are an AI assistant for the Physical AI & Humanoid Robotics textbook. Answer questions based on the provided context and cite the relevant chapters/modules."},
                    #         {"role": "user", "content": prompt}
                    #     ],
                    #     temperature=0.3,
                    #     max_tokens=1000
                    # )
                    # return response.choices[0].message.content

                    # For compatibility with older versions:
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",  # or gpt-4 if available
                        messages=[
                            {"role": "system", "content": "You are an AI assistant for the Physical AI & Humanoid Robotics textbook. Answer questions based on the provided context and cite the relevant chapters/modules."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.3,
                        max_tokens=1000
                    )
                    return response['choices'][0]['message']['content']
                except Exception as e:
                    print(f"Error calling OpenAI API: {str(e)}")
                    # Fallback to simple response if OpenAI call fails
                    pass

            # If OpenAI API key is not configured or API call fails, create a simple response based on the context
            # This is a basic fallback that just formats the retrieved context
            response = f"Based on the textbook content:\n\n{context}\n\nFor more detailed information, please refer to the relevant chapters in the textbook."
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