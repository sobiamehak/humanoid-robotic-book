"""
Local response generation service that works with the book content directly.
This provides a fallback when external AI services are not available.
"""
import re
from typing import List, Dict, Any
from .rag import retrieve, build_context


class LocalResponseService:
    """
    Service class for generating responses based on retrieved content from the book.
    This works as a fallback when external AI services are unavailable.
    """

    def __init__(self):
        pass

    def generate_response(self, prompt: str, context: str = None) -> str:
        """
        Generate a response based on the prompt and context from the book.

        Args:
            prompt: The user's question/query
            context: Retrieved context from the book

        Returns:
            Generated response string
        """
        # Check if the question is related to the book topic
        book_related_keywords = ['humanoid', 'robotics', 'physical ai', 'ai', 'robot', 'artificial intelligence', 'machine learning', 'perception', 'navigation', 'manipulation', 'control', 'locomotion', 'embodied', 'cognition', 'robotic', 'sensors', 'actuators', 'locomotion', 'bipedal', 'gait', 'balance', 'human-robot', 'interaction', 'embodiment', 'grounded', 'cognition']

        is_related = any(keyword in prompt.lower() for keyword in book_related_keywords)

        if not is_related and not context:
            return "I can only answer questions about the Physical AI & Humanoid Robotics textbook. Please ask questions related to the book content."

        if not context:
            # If no context is provided, try to retrieve relevant content
            hits = retrieve(prompt, top_k=3)
            context, _ = build_context(hits)

        if not context.strip() and not is_related:
            return "I can only answer questions about the Physical AI & Humanoid Robotics textbook. Please ask questions related to the book content."
        elif not context.strip():
            return "I couldn't find relevant information in the book to answer your question."

        # Simple response generation based on the context
        # This finds relevant sentences in the context that match the query
        query_keywords = self._extract_keywords(prompt.lower())
        relevant_sentences = self._find_relevant_sentences(context, query_keywords)

        if relevant_sentences:
            response = "Based on the book content:\n\n" + "\n".join(relevant_sentences[:3])  # Limit to 3 sentences
            return response
        else:
            return f"Based on the book content: {context[:500]}..." if len(context) > 500 else f"Based on the book content: {context}"

    def _extract_keywords(self, text: str) -> List[str]:
        """
        Extract keywords from the text for matching.

        Args:
            text: Input text to extract keywords from

        Returns:
            List of keywords
        """
        # Remove common stop words and extract meaningful keywords
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those'}
        words = re.findall(r'\b\w+\b', text)
        return [word for word in words if word not in stop_words and len(word) > 2]

    def _find_relevant_sentences(self, context: str, keywords: List[str]) -> List[str]:
        """
        Find sentences in the context that contain the keywords.

        Args:
            context: The context text to search in
            keywords: List of keywords to match

        Returns:
            List of relevant sentences
        """
        # Split context into sentences
        sentences = re.split(r'[.!?]+', context)
        relevant_sentences = []

        for sentence in sentences:
            sentence_lower = sentence.lower()
            # Count how many keywords match in this sentence
            matches = sum(1 for keyword in keywords if keyword in sentence_lower)
            if matches > 0:
                # Add sentence if it contains at least one keyword
                clean_sentence = sentence.strip()
                if clean_sentence:
                    relevant_sentences.append(clean_sentence)

        # Sort by number of keyword matches (descending)
        relevant_sentences.sort(key=lambda s: sum(1 for keyword in keywords if keyword in s.lower()), reverse=True)

        return relevant_sentences


# Global instance for easy access
local_response_service = LocalResponseService()


def generate_response(prompt: str, context: str = None) -> str:
    """
    Generate response using the local response service.

    Args:
        prompt: The user's question/query
        context: Retrieved context from the book

    Returns:
        Generated response string
    """
    return local_response_service.generate_response(prompt, context)