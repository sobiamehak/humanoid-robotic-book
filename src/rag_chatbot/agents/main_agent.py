import logging
from typing import Dict, Any, List
from . import BaseAgent
from ..models.query_models import AgentMessage, QueryRequest, QueryResponse, AgentHandoff
from ..services.llm_service import llm_service
from .retrieval_agent import RetrievalAgent
from .generation_agent import GenerationAgent

logger = logging.getLogger(__name__)

class MainAgent(BaseAgent):
    """Main agent that coordinates between retrieval and generation agents"""

    def __init__(self):
        super().__init__("MainAgent")
        self.retrieval_agent = "RetrievalAgent"
        self.generation_agent = "GenerationAgent"
        logger.info("MainAgent initialized")

    async def process(self, message: AgentMessage) -> AgentMessage:
        """Process incoming messages and coordinate with other agents"""
        logger.info(f"MainAgent processing message from {message.sender}: {message.content[:50]}...")

        # Determine the next action based on the message content and metadata
        if message.next_action == "retrieval":
            # Forward to retrieval agent
            response = self.create_response_message(
                content=message.content,
                receiver=self.retrieval_agent,
                next_action="retrieve_context"
            )
        elif message.next_action == "generation":
            # Forward to generation agent with context
            response = self.create_response_message(
                content=message.content,
                receiver=self.generation_agent,
                next_action="generate_response"
            )
        elif message.next_action == "check_relevance":
            # Check if query is off-topic
            is_relevant = await llm_service.check_query_relevance(message.content)
            if not is_relevant:
                # Handle off-topic query
                response = self.create_response_message(
                    content=f"The query '{message.content}' appears to be off-topic. This system can only answer questions related to Physical AI & Humanoid Robotics based on the book content.",
                    receiver=message.sender,
                    next_action="return_response"
                )
            else:
                # Query is relevant, proceed with retrieval
                response = self.create_response_message(
                    content=message.content,
                    receiver=self.retrieval_agent,
                    next_action="retrieve_context"
                )
        else:
            # Default behavior - check relevance first
            response = self.create_response_message(
                content=message.content,
                receiver=message.sender,
                next_action="check_relevance"
            )

        logger.info(f"MainAgent created response for {response.receiver}")
        return response

    async def handle_request(self, query_request: QueryRequest) -> QueryResponse:
        """Handle a query request end-to-end"""
        logger.info(f"MainAgent handling request: {query_request.query[:50]}...")

        # First, check if the query is relevant to the book topic
        is_relevant = await llm_service.check_query_relevance(query_request.query)

        if not is_relevant and "off-topic" not in query_request.query.lower():
            # Return off-topic response
            logger.info(f"Query identified as off-topic: {query_request.query[:50]}...")
            # Use the generation agent to create an appropriate off-topic response
            generation_agent = GenerationAgent()
            return await generation_agent.handle_request(query_request, context="", is_off_topic=True)

        # Use the retrieval agent to get relevant context
        retrieval_agent = RetrievalAgent()
        retrieval_results = await retrieval_agent.handle_request(query_request)

        # Format the context from retrieval results
        # Only include content that is not empty
        valid_contents = [result.content for result in retrieval_results if result.content.strip()]
        context_str = "\n\n".join(valid_contents) if valid_contents else ""

        # Use the generation agent to create the final response
        generation_agent = GenerationAgent()
        response = await generation_agent.handle_request(
            query_request,
            context=context_str,
            is_off_topic=False
        )

        # Add citations from retrieval results
        citations = []
        for result in retrieval_results:
            citations.append({
                "source": result.source,
                "page": result.page_number or 1,
                "score": result.score
            })

        # Update the response with citations and context used
        response.citations = citations
        response.context_used = [
            {
                "content": result.content,
                "source": result.source,
                "score": result.score
            }
            for result in retrieval_results
        ]

        logger.info("MainAgent completed request processing")
        return response

    async def handle_complex_query(self, query_request: QueryRequest) -> QueryResponse:
        """Handle complex queries that may require multiple steps"""
        logger.info(f"MainAgent handling complex query: {query_request.query[:50]}...")

        # First, check if the query is relevant to the book topic
        is_relevant = await llm_service.check_query_relevance(query_request.query)

        if not is_relevant and "off-topic" not in query_request.query.lower():
            # Return off-topic response
            logger.info(f"Complex query identified as off-topic: {query_request.query[:50]}...")
            # Use the generation agent to create an appropriate off-topic response
            generation_agent = GenerationAgent()
            return await generation_agent.handle_request(query_request, context="", is_off_topic=True)

        # For complex queries, we need to retrieve from multiple sections of the book
        # and then synthesize the information
        retrieval_agent = RetrievalAgent()
        generation_agent = GenerationAgent()

        # Get broader context by using different query formulations
        sub_queries = await self.generate_sub_queries(query_request.query)
        all_contexts = []
        all_retrieval_results = []

        for sub_query in sub_queries:
            logger.info(f"Processing sub-query: {sub_query[:30]}...")
            sub_results = await retrieval_agent.handle_request(
                QueryRequest(query=sub_query, context_window=query_request.context_window)
            )
            # Only add non-empty content
            for result in sub_results:
                if result.content.strip():
                    all_contexts.append(result.content)
            all_retrieval_results.extend(sub_results)

        # Pass these contexts to the generation agent for synthesis
        context_str = "\n\n".join(all_contexts)
        response = await generation_agent.generate_multistep_response(query_request.query, all_contexts)

        # Create citations from all retrieval results
        citations = []
        for result in all_retrieval_results:
            citations.append({
                "source": result.source,
                "page": result.page_number or 1,
                "score": result.score
            })

        logger.info("MainAgent completed complex query processing")
        return QueryResponse(
            response=response,
            citations=citations,
            context_used=[
                {
                    "content": result.content,
                    "source": result.source,
                    "score": result.score
                }
                for result in all_retrieval_results
            ]
        )

    async def generate_sub_queries(self, original_query: str) -> List[str]:
        """Generate sub-queries for complex queries"""
        # In a real implementation, this would use an LLM to break down the complex query
        # For now, we'll use a simple heuristic approach

        import re

        # Identify entities or topics to query separately
        # This is a simplified approach - real implementation would be more sophisticated
        sub_queries = [original_query]  # Start with the original query

        # Look for comparison patterns: "A vs B", "A and B", "A or B"
        comparison_pattern = r'(.+?)\s+(?:and|vs\.?|versus|or|compared to|versus)\s+(.+)'
        match = re.search(comparison_pattern, original_query, re.IGNORECASE)

        if match:
            part1, part2 = match.groups()
            sub_queries.extend([part1.strip(), part2.strip()])

        # Look for multi-topic patterns: "A, B, and C"
        multi_topic_pattern = r'(\w+)\s*,\s*(\w+)\s*(?:and|,)\s*(\w+)'
        match = re.search(multi_topic_pattern, original_query, re.IGNORECASE)

        if match:
            topics = list(match.groups())
            sub_queries.extend([f"{original_query.split(':')[0]}: {topic}" for topic in topics])

        # Remove duplicates while preserving order
        unique_queries = []
        for query in sub_queries:
            if query not in unique_queries and query.strip():
                unique_queries.append(query.strip())

        logger.info(f"Generated {len(unique_queries)} sub-queries from: {original_query[:30]}...")
        return unique_queries