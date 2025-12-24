import logging
from typing import Dict, Any
from . import BaseAgent
from ..models.query_models import AgentMessage, QueryRequest, QueryResponse
from ..services.llm_service import llm_service

logger = logging.getLogger(__name__)

class GenerationAgent(BaseAgent):
    """Agent responsible for generating responses based on retrieved context"""

    def __init__(self):
        super().__init__("GenerationAgent")
        logger.info("GenerationAgent initialized")

    async def process(self, message: AgentMessage) -> AgentMessage:
        """Process messages related to response generation"""
        logger.info(f"GenerationAgent processing message: {message.content[:50]}...")

        if message.next_action == "generate_response":
            # Generate a response based on the context in the message
            response_content = await self.generate_response(message.content)

            # Create response message to send back
            response = self.create_response_message(
                content=response_content,
                receiver=message.sender,  # Usually back to the main agent or user
                next_action="return_response"
            )
        else:
            # Unknown action, return an error message
            response = self.create_response_message(
                content=f"Unknown action: {message.next_action}",
                receiver=message.sender,
                next_action="error"
            )

        logger.info(f"GenerationAgent created response for {response.receiver}")
        return response

    async def handle_request(self, query_request: QueryRequest, context: str = "", is_off_topic: bool = False) -> QueryResponse:
        """Handle a query request by generating a response"""
        logger.info(f"GenerationAgent handling request: {query_request.query[:50]}...")

        # Check if the query is a greeting
        greetings = ['hi', 'hello', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening', 'good night']
        is_greeting = query_request.query.lower().strip() in greetings

        if is_off_topic and not is_greeting:
            # Handle off-topic query appropriately (but not greetings)
            response_content = f"The query '{query_request.query}' appears to be off-topic. This system can only answer questions related to Physical AI & Humanoid Robotics based on the book content. I cannot provide answers on this topic."
        else:
            # Generate response using the LLM service
            # For greetings, we want a specific response that doesn't rely heavily on context
            if is_greeting:
                # For greetings, use minimal context or no context to avoid long responses
                response_content = await llm_service.generate_response(
                    prompt=query_request.query,
                    context=""  # Use empty context for greetings to get concise response
                )
            else:
                response_content = await llm_service.generate_response(
                    prompt=query_request.query,
                    context=context
                )

        # Create response with citations if available
        citations = []
        if query_request.include_citations and not is_off_topic and context and not is_greeting:
            # Extract source information from context if available
            citations = [{"source": "textbook_content", "page": 1}]  # This would be populated with real citations in a full implementation

        logger.info("GenerationAgent completed response generation")
        return QueryResponse(
            response=response_content,
            citations=citations,
            context_used=[{"content": context[:200] + "..." if len(context) > 200 else context, "source": "retrieved_context"}] if context and not is_off_topic and not is_greeting else [],
            is_off_topic=is_off_topic and not is_greeting  # Don't mark greetings as off-topic
        )

    async def generate_response(self, context_with_query: str) -> str:
        """Generate a response based on context and query"""
        logger.info("GenerationAgent generating response from context")

        # In a real implementation, we would extract the query and context from the message
        # For now, we'll assume the message contains both
        response = await llm_service.generate_response(
            prompt="Provide a helpful response based on the following context.",
            context=context_with_query
        )

        logger.info("Response generation completed")
        return response

    async def generate_multistep_response(self, query: str, contexts: list) -> str:
        """Generate response for complex queries requiring multiple contexts"""
        logger.info(f"GenerationAgent generating multi-step response for query: {query[:50]}...")

        # In a real implementation, we would use the LLM service to generate a response
        # that synthesizes information from multiple contexts
        # For now, we'll enhance the simulation to better reflect multi-context processing

        if len(contexts) == 0:
            return f"Could not generate a comprehensive response for the query '{query}' as no relevant contexts were found."

        # Format the contexts for the LLM to process
        formatted_contexts = "\n\n".join([
            f"Context {i+1}: {ctx}" for i, ctx in enumerate(contexts)
        ])

        # Use the LLM service to generate a response that synthesizes multiple contexts
        response = await llm_service.generate_multistep_response(query, contexts)

        logger.info("Multi-step response generation completed")
        return response

    async def format_citations(self, retrieval_results: list) -> list:
        """Format retrieval results as citations"""
        citations = []
        for result in retrieval_results:
            citations.append({
                "source": result.get("source", "Unknown"),
                "page": result.get("page_number", 1),
                "score": result.get("score", 0.0)
            })
        return citations