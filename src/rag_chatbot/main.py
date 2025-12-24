import asyncio
import logging
from typing import Dict, Any
from .agents.main_agent import MainAgent
from .agents.retrieval_agent import RetrievalAgent
from .agents.generation_agent import GenerationAgent
from .models.query_models import QueryRequest, QueryResponse
from .config.settings import settings

logger = logging.getLogger(__name__)

class RAGChatbotSystem:
    """Main class to coordinate the multi-agent RAG chatbot system"""

    def __init__(self):
        """Initialize all agents and services"""
        self.main_agent = MainAgent()
        self.retrieval_agent = RetrievalAgent()
        self.generation_agent = GenerationAgent()

        logger.info("RAGChatbotSystem initialized with all agents")

    async def process_query(self, query_request: QueryRequest) -> QueryResponse:
        """
        Process a query through the multi-agent system

        Args:
            query_request: The query request with all necessary parameters

        Returns:
            QueryResponse with the answer and metadata
        """
        logger.info(f"Processing query: {query_request.query[:50]}...")

        # Log query metadata
        logger.info(f"Query metadata - User ID: {query_request.user_id}, Session ID: {query_request.session_id}")

        # Determine if this is a complex query requiring multiple steps
        if self._is_complex_query(query_request.query):
            logger.info("Detected complex query, using multi-step processing")
            response = await self.main_agent.handle_complex_query(query_request)
        else:
            # Process as a regular query through the main agent
            response = await self.main_agent.handle_request(query_request)
            logger.info("Regular query processed successfully")

        # Log the response length and basic info
        logger.info(f"Response generated, length: {len(response.response)} characters")
        logger.info(f"Number of citations: {len(response.citations) if response.citations else 0}")
        logger.info(f"Is off-topic: {response.is_off_topic}")

        # Log additional metrics for monitoring
        if response.is_off_topic:
            logger.info(f"Off-topic query handled: {query_request.query[:50]}...")

        # Log metrics for complex query processing
        if self._is_complex_query(query_request.query):
            logger.info(f"Complex query processed: {query_request.query[:50]}...")

        return response

    def _is_complex_query(self, query: str) -> bool:
        """
        Determine if a query is complex and requires multi-step processing

        Args:
            query: The query string to analyze

        Returns:
            True if the query is complex, False otherwise
        """
        complex_indicators = [
            "compare", "contrast", "relationship between", "how do .* and .* differ",
            "multiple", "several", "various", "synthesis", "integrate", "analyze .* and .*",
            "difference between", "similarities between", "connection between"
        ]

        import re
        return any(
            re.search(indicator, query.lower()) for indicator in complex_indicators
        )

    async def health_check(self) -> Dict[str, Any]:
        """
        Perform a health check of the system

        Returns:
            Dictionary with health status of each component
        """
        logger.info("Performing health check")

        health_status = {
            "main_agent": True,
            "retrieval_agent": True,
            "generation_agent": True,
            "llm_service": True,
            "qdrant_service": True,  # This would check actual connection in real implementation
            "overall_status": True
        }

        # In a real implementation, you would check actual service connectivity
        # For now, we'll just return the status

        logger.info("Health check completed")
        return health_status

# Global instance for the system
rag_chatbot_system = RAGChatbotSystem()

# CLI interface
async def main():
    """Main entry point for the CLI interface"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m src.rag_chatbot.main \"Your query here\"")
        return

    query = " ".join(sys.argv[1:])

    try:
        # Create a query request
        query_request = QueryRequest(query=query)

        # Process the query
        response = await rag_chatbot_system.process_query(query_request)

        print(f"Response: {response.response}")

        if response.citations:
            print(f"Citations: {response.citations}")
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        print(f"Application error: {str(e)}")