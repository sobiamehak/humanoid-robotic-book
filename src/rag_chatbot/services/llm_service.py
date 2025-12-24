import logging
import asyncio
from typing import List, Dict, Any, Optional
from ..config.settings import settings

logger = logging.getLogger(__name__)

class LLMService:
    """Service class for handling LLM operations via OpenRouter API"""

    def __init__(self):
        """Initialize LLM service with configuration from settings"""
        self.api_key = settings.LLM_API_KEY
        self.default_model = settings.DEFAULT_MODEL
        logger.info(f"LLMService initialized with model: {self.default_model}")

    async def generate_response(self, prompt: str, context: str = "") -> str:
        """
        Generate a response using the LLM with the given prompt and context

        Args:
            prompt: The user's query or prompt
            context: Context retrieved from the vector database

        Returns:
            Generated response string
        """
        try:
            # Format the prompt with context
            system_message = "You are an AI assistant for the Physical AI & Humanoid Robotics textbook. Answer questions based on the provided context. Be concise and specific to the user's question. Only use information from the provided context. If the question is about 'hi' or greetings, respond with a brief greeting and offer help with textbook-related questions."

            # Special handling for greetings
            if prompt.lower().strip() in ['hi', 'hello', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening']:
                return "Hello! I'm your AI assistant for the Physical AI & Humanoid Robotics textbook. How can I help you with questions about robotics, AI, humanoid robots, or related topics from the textbook?"

            full_prompt = f"Context:\n{context}\n\nQuestion: {prompt}\n\nPlease provide a concise, helpful response based on the context provided. Focus specifically on answering the question asked. If the context doesn't contain enough information to answer the question, acknowledge this briefly."

            # Make an API call to the LLM provider
            import openai
            from ..config.settings import settings

            # Check if we have an API key configured
            if settings.LLM_API_KEY:
                openai.api_key = settings.LLM_API_KEY

                try:
                    # For compatibility with older versions:
                    response = openai.ChatCompletion.create(
                        model=settings.DEFAULT_MODEL.replace("openai/", ""),
                        messages=[
                            {"role": "system", "content": system_message},
                            {"role": "user", "content": full_prompt}
                        ],
                        temperature=0.3,
                        max_tokens=500  # Reduced to get more concise responses
                    )
                    return response['choices'][0]['message']['content']
                except Exception as e:
                    logger.error(f"Error calling LLM API: {str(e)}")
                    # Fallback to simple response if API call fails
            else:
                logger.warning("LLM API key not configured, using fallback response")

            # Fallback response if API key is not configured or API call fails
            # Extract the most relevant part of the context for the query
            if context and len(context) > 300:
                # Truncate context to most relevant part
                truncated_context = context[:300] + "..."
            else:
                truncated_context = context

            fallback_response = f"Based on the context provided: {truncated_context}\n\nFor your query '{prompt}', please refer to the relevant chapters in the textbook for detailed information."
            logger.info("Using fallback response generation")
            return fallback_response
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise

    async def check_query_relevance(self, query: str, book_topic: str = "Physical AI & Humanoid Robotics") -> bool:
        """
        Check if a query is relevant to the book topic

        Args:
            query: The user's query
            book_topic: The topic of the book

        Returns:
            True if the query is relevant, False otherwise
        """
        try:
            # First, check if it's a greeting - these should be handled specially
            greetings = ['hi', 'hello', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening', 'good night']
            if query.lower().strip() in greetings:
                # Greetings are considered relevant as they're the start of a conversation
                logger.info(f"Query relevance check: '{query[:30]}...' -> True (greeting)")
                return True

            # For non-greetings, check for book-related content
            query_lower = query.lower()
            relevant_keywords = [
                'robotics', 'ai', 'artificial intelligence', 'physical ai', 'humanoid',
                'locomotion', 'manipulation', 'perception', 'learning', 'nvidia',
                'isaac', 'gazebo', 'ros', 'simulation', 'ethics', 'safety', 'kinematics',
                'dynamics', 'cognition', 'applications', 'future', 'platforms', 'chapter',
                'textbook', 'book', 'robot', 'motion', 'control', 'algorithm', 'sensor',
                'actuator', 'navigation', 'planning', 'control', 'dynamics', 'kinematics'
            ]

            # If it contains obvious relevant keywords, it's likely relevant
            has_relevant_keywords = any(keyword in query_lower for keyword in relevant_keywords)

            if has_relevant_keywords:
                logger.info(f"Query relevance check: '{query[:30]}...' -> True (contains relevant keywords)")
                return True

            # For more nuanced checking, we can use the LLM
            # Create a prompt to determine relevance
            relevance_prompt = f"""
            Determine if the following query is related to {book_topic}:
            Query: {query}

            Respond with "RELEVANT" if the query is about {book_topic} or related topics like robotics, AI,
            humanoid robots, physical AI, locomotion, manipulation, perception, etc.
            Respond with "IRRELEVANT" if the query is about completely unrelated topics like cooking,
            gardening, sports, etc.

            Only respond with either "RELEVANT" or "IRRELEVANT".
            """

            # Use the LLM to determine relevance
            import openai
            from ..config.settings import settings

            if settings.LLM_API_KEY:
                openai.api_key = settings.LLM_API_KEY

                try:
                    response = openai.ChatCompletion.create(
                        model=settings.DEFAULT_MODEL.replace("openai/", ""),
                        messages=[
                            {"role": "system", "content": "You are an AI assistant that determines if queries are relevant to a specific topic. Only respond with 'RELEVANT' or 'IRRELEVANT'."},
                            {"role": "user", "content": relevance_prompt}
                        ],
                        temperature=0.1,  # Low temperature for consistent results
                        max_tokens=10
                    )

                    result = response['choices'][0]['message']['content'].strip().upper()
                    is_relevant = "RELEVANT" in result

                    logger.info(f"Query relevance check: '{query[:30]}...' -> {is_relevant} (LLM decision: {result})")
                    return is_relevant
                except Exception as e:
                    logger.error(f"Error calling LLM for relevance check: {str(e)}")
                    # Fall back to keyword matching if LLM fails
            else:
                logger.warning("LLM API key not configured for relevance check, using keyword matching")

            # Fallback to keyword-based check if LLM is not available
            # Apply a more lenient keyword check
            broader_keywords = [
                'robot', 'machine', 'intelligent', 'automated', 'system', 'control',
                'algorithm', 'computer', 'technology', 'engineering', 'science',
                'data', 'learning', 'neural', 'sensor', 'actuator', 'motion'
            ]

            is_relevant = any(keyword in query_lower for keyword in broader_keywords) or has_relevant_keywords

            logger.info(f"Query relevance check: '{query[:30]}...' -> {is_relevant} (keyword-based)")
            return is_relevant

        except Exception as e:
            logger.error(f"Error checking query relevance: {str(e)}")
            return True  # Default to relevant if there's an error

    async def generate_multistep_response(self, query: str, contexts: List[str]) -> str:
        """
        Generate a response for complex queries requiring multiple contexts

        Args:
            query: The user's complex query
            contexts: List of contexts from different parts of the book

        Returns:
            Generated response string synthesizing information from multiple contexts
        """
        try:
            logger.info(f"Generating multi-step response for complex query: {query[:50]}...")

            # Combine all contexts
            combined_context = "\n\n".join([f"Section {i+1}: {ctx}" for i, ctx in enumerate(contexts)])

            system_message = "You are an AI assistant for the Physical AI & Humanoid Robotics textbook. Synthesize information from multiple contexts to answer complex queries. Be comprehensive but concise, and cite the relevant chapters/modules."

            full_prompt = f"Multiple Contexts: {combined_context}\n\nQuestion: {query}\n\nPlease provide a comprehensive response that synthesizes information from the multiple contexts provided. Focus specifically on answering the question asked."

            # Make an API call to the LLM provider
            import openai
            from ..config.settings import settings

            # Check if we have an API key configured
            if settings.LLM_API_KEY:
                openai.api_key = settings.LLM_API_KEY

                try:
                    # For compatibility with older versions:
                    response = openai.ChatCompletion.create(
                        model=settings.DEFAULT_MODEL.replace("openai/", ""),
                        messages=[
                            {"role": "system", "content": system_message},
                            {"role": "user", "content": full_prompt}
                        ],
                        temperature=0.3,
                        max_tokens=800  # Reduced to get more concise responses
                    )
                    return response['choices'][0]['message']['content']
                except Exception as e:
                    logger.error(f"Error calling LLM API for multistep response: {str(e)}")
                    # Fallback to simple response if API call fails
            else:
                logger.warning("LLM API key not configured for multistep response, using fallback")

            # Fallback response if API key is not configured or API call fails
            # Truncate contexts to avoid too much text
            if combined_context and len(combined_context) > 500:
                truncated_context = combined_context[:500] + "..."
            else:
                truncated_context = combined_context

            fallback_response = f"Based on multiple sections of the book: {truncated_context}\n\nFor your complex query '{query}', please refer to the relevant chapters in the textbook for detailed information."
            logger.info("Using fallback multistep response generation")
            return fallback_response
        except Exception as e:
            logger.error(f"Error generating multi-step response: {str(e)}")
            raise

# Global instance for use in other modules
llm_service = LLMService()