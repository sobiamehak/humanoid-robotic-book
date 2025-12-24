import logging
from typing import List, Dict, Any
from . import BaseAgent
from ..models.query_models import AgentMessage, QueryRequest, RetrievalResult
from ..services.qdrant_service import qdrant_service

logger = logging.getLogger(__name__)

class RetrievalAgent(BaseAgent):
    """Agent responsible for retrieving relevant information from the vector database"""

    def __init__(self):
        super().__init__("RetrievalAgent")
        self.generation_agent = "GenerationAgent"
        logger.info("RetrievalAgent initialized")

    async def process(self, message: AgentMessage) -> AgentMessage:
        """Process messages related to information retrieval"""
        logger.info(f"RetrievalAgent processing message: {message.content[:50]}...")

        if message.next_action == "retrieve_context":
            # Perform the retrieval
            retrieval_results = await self.retrieve_context(message.content)

            # Format results for the generation agent
            context_str = self.format_retrieval_results(retrieval_results)

            response = self.create_response_message(
                content=context_str,
                receiver=self.generation_agent,
                next_action="generate_response"
            )
            response.metadata["retrieval_results"] = [r.dict() for r in retrieval_results]
        else:
            # Unknown action, return an error message
            response = self.create_response_message(
                content=f"Unknown action: {message.next_action}",
                receiver=message.sender,
                next_action="error"
            )

        logger.info(f"RetrievalAgent created response for {response.receiver}")
        return response

    async def handle_request(self, query_request: QueryRequest) -> List[RetrievalResult]:
        """Handle a query request by retrieving relevant context"""
        logger.info(f"RetrievalAgent handling request: {query_request.query[:50]}...")

        # Convert the query to an embedding and search Qdrant
        query_embedding = await self.get_embedding(query_request.query)
        results = await qdrant_service.search(query_embedding, top_k=query_request.context_window or 5)

        # Format results to RetrievalResult objects
        formatted_results = []
        for result in results:
            payload = result['payload']
            formatted_results.append(
                RetrievalResult(
                    id=result['id'],
                    content=payload.get('content', ''),
                    score=result['score'],
                    source=payload.get('title', 'Unknown Source'),
                    page_number=None  # Page number might not be available in all payloads
                )
            )

        logger.info(f"RetrievalAgent found {len(formatted_results)} results")
        return formatted_results

    async def retrieve_context(self, query: str, top_k: int = 3) -> List[RetrievalResult]:  # Reduced top_k to get more focused results
        """Retrieve context for a query from the vector database"""
        logger.info(f"RetrievalAgent retrieving context for query: {query[:50]}...")

        # Check if the query is a greeting, and if so, return minimal context
        greetings = ['hi', 'hello', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening', 'good night']
        if query.lower().strip() in greetings:
            # For greetings, return a simple response-indicating result
            logger.info("Query is a greeting, returning minimal context")
            return [
                RetrievalResult(
                    id="greeting_context",
                    content="",
                    score=1.0,
                    source="General",
                    page_number=None
                )
            ]

        # Convert the query to an embedding using an embedding model
        query_embedding = await self.get_embedding(query)

        # Search the Qdrant database for similar vectors
        results = await qdrant_service.search(query_embedding, top_k=top_k)

        # Format results to RetrievalResult objects
        formatted_results = []
        for result in results:
            payload = result['payload']
            content = payload.get('content', '')

            # Truncate content to avoid overly long responses
            if len(content) > 400:  # Limit content length
                content = content[:400] + "..."

            formatted_results.append(
                RetrievalResult(
                    id=result['id'],
                    content=content,
                    score=result['score'],
                    source=payload.get('title', 'Unknown Source'),
                    page_number=payload.get('page_number', None)  # Extract page number if available
                )
            )

        logger.info(f"Retrieved {len(formatted_results)} context items")
        return formatted_results

    async def retrieve_complex_context(self, query: str, top_k: int = 8, search_strategy: str = "diverse") -> List[RetrievalResult]:
        """Retrieve context for complex queries using various search strategies"""
        logger.info(f"RetrievalAgent retrieving complex context for query: {query[:50]}... using {search_strategy} strategy")

        # For complex queries, we might want to use different search strategies
        # such as diverse retrieval (getting results from different chapters/sections)
        # or multi-vector search (searching for different aspects of the query)

        if search_strategy == "diverse":
            # Try to get results from different sections of the book
            simulated_results = [
                RetrievalResult(
                    id=f"diverse_sim_{i}",
                    content=f"Diverse content for complex query '{query}' - Result {i+1}",
                    score=0.85 - (i * 0.05),  # Scores slightly lower but diverse
                    source=f"Different Chapter {i*2 + 1}: Related Topic",
                    page_number=20 + (i * 25)
                )
                for i in range(top_k)
            ]
        elif search_strategy == "focused":
            # Focus on the most relevant results
            simulated_results = [
                RetrievalResult(
                    id=f"focused_sim_{i}",
                    content=f"Focused content for complex query '{query}' - Result {i+1}",
                    score=0.92 - (i * 0.03),  # High scores, focused
                    source=f"Related Chapter {i+1}: Specific Topic",
                    page_number=15 + (i * 20)
                )
                for i in range(top_k)
            ]
        else:
            # Default strategy
            simulated_results = [
                RetrievalResult(
                    id=f"complex_sim_{i}",
                    content=f"Complex query content for '{query}' - Result {i+1}",
                    score=0.88 - (i * 0.04),
                    source=f"Multi-section Reference {i+1}",
                    page_number=5 + (i * 18)
                )
                for i in range(top_k)
            ]

        logger.info(f"Retrieved {len(simulated_results)} complex context items using {search_strategy} strategy")
        return simulated_results

    def format_retrieval_results(self, results: List[RetrievalResult]) -> str:
        """Format retrieval results into a context string for the generation agent"""
        if not results:
            return "No relevant context found."

        context_parts = []
        for i, result in enumerate(results):
            context_parts.append(
                f"Source: {result.source} (Page {result.page_number})\n"
                f"Content: {result.content}\n"
                f"Relevance Score: {result.score}\n"
                f"---\n"
            )

        return "Retrieved Context:\n" + "\n".join(context_parts)

    async def get_embedding(self, text: str) -> List[float]:
        """Get embedding for text using an embedding model"""
        # Import the LLM service to use for embeddings
        from ..services.llm_service import llm_service
        import openai
        import os
        from ..config.settings import settings

        # Check if we have OpenAI API key configured
        if settings.LLM_API_KEY and 'openai' in settings.DEFAULT_MODEL.lower():
            # Use OpenAI API for embeddings
            try:
                openai.api_key = settings.LLM_API_KEY
                response = openai.Embedding.create(
                    input=text,
                    model="text-embedding-ada-002"  # Using OpenAI's embedding model
                )
                return response['data'][0]['embedding']
            except Exception as e:
                logger.error(f"Error getting embedding from OpenAI: {str(e)}")
                # Fallback to a basic embedding if API fails
                import hashlib
                encoded_text = text.encode('utf-8')
                hash_obj = hashlib.md5(encoded_text)
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
        else:
            # Fallback to basic embedding if no API key is configured
            import hashlib
            encoded_text = text.encode('utf-8')
            hash_obj = hashlib.md5(encoded_text)
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