import logging
import re
from typing import List, Dict, Any
from ..config.settings import settings

logger = logging.getLogger(__name__)

class QueryRelevanceService:
    """Service for determining query relevance to book content"""

    def __init__(self):
        """Initialize the query relevance service"""
        self.topic_keywords = [
            # Physical AI & Robotics
            'robot', 'robotics', 'robotic', 'physical ai', 'embodied ai',
            'ai', 'artificial intelligence', 'machine learning', 'ml',

            # Humanoid-specific
            'humanoid', 'bipedal', 'locomotion', 'balance', 'walking',
            'gait', 'posture', 'humanoid robot', 'bipedal locomotion',

            # Technical components
            'perception', 'navigation', 'manipulation', 'control',
            'sensor', 'actuator', 'kinematics', 'dynamics', 'inverse dynamics',

            # Platforms & tools
            'ros', 'ros2', 'gazebo', 'unity', 'nvidia', 'isaac', 'isaac sim',
            'simulation', 'digital twin', 'gazebo simulation',

            # Specific topics from the textbook
            'chapter', 'textbook', 'learning from demonstration', 'reinforcement learning',
            'rl', 'imitation learning', 'sim-to-real', 'transfer learning',
            'computer vision', 'vision', 'language', 'vlm', 'vqa',
            'ethics', 'safety', 'social robotics', 'conversational',

            # Book-specific terminology
            'physical ai', 'humanoid robotics', 'humanoid robot',
            'robotic nervous system', 'digital twin', 'ai-robot brain',
            'vision-language-action', 'vla', 'kinematics', 'dexterous manipulation'
        ]

        self.off_topic_keywords = [
            # General off-topic indicators
            'weather', 'joke', 'recipe', 'movie', 'tv', 'celebrity', 'sport',
            'politics', 'stock', 'finance', 'cryptocurrency', 'news',
            'unrelated', 'random', 'nonsense', 'garbage', 'spam'
        ]

        logger.info("QueryRelevanceService initialized with keyword lists")

    async def is_query_relevant(self, query: str, book_topic: str = "Physical AI & Humanoid Robotics") -> bool:
        """
        Determine if a query is relevant to the book topic

        Args:
            query: The user's query
            book_topic: The topic of the book

        Returns:
            True if the query is relevant, False otherwise
        """
        query_lower = query.lower().strip()

        logger.info(f"Checking relevance for query: {query_lower[:50]}...")

        # Check for obvious off-topic keywords first
        for off_topic_word in self.off_topic_keywords:
            if off_topic_word in query_lower:
                logger.info(f"Query contains off-topic keyword: {off_topic_word}")
                return False

        # Check for topic keywords
        topic_matches = []
        for keyword in self.topic_keywords:
            if keyword in query_lower:
                topic_matches.append(keyword)

        if topic_matches:
            logger.info(f"Query contains topic keywords: {topic_matches}")
            return True

        # Use a more sophisticated approach for longer queries
        # Check if query contains technical terms related to robotics
        technical_indicators = [
            r'\b(robot|robotic)\b',  # robot/robotic as whole words
            r'\b(ai|ml|dl)\b',  # AI, ML, DL
            r'\b(ros|gazebo|isaac)\b',  # specific tools
            r'(kinematic|dynamic|locomotion|manipulation|perception)',  # technical terms
        ]

        for pattern in technical_indicators:
            if re.search(pattern, query_lower):
                logger.info(f"Query contains technical indicator: {pattern}")
                return True

        # If no clear matches found, assume it's not relevant
        # (This is a conservative approach - better to mark uncertain queries as not relevant)
        logger.info("No topic matches found, marking as not relevant")
        return False

    async def get_relevance_score(self, query: str) -> float:
        """
        Get a relevance score between 0 and 1 for the query

        Args:
            query: The user's query

        Returns:
            Relevance score (0.0 to 1.0)
        """
        query_lower = query.lower().strip()

        # Start with base score
        score = 0.0

        # Add points for topic keywords
        for keyword in self.topic_keywords:
            if keyword in query_lower:
                score += 0.1  # Each topic keyword adds 0.1 to the score

        # Subtract points for off-topic keywords
        for off_topic_word in self.off_topic_keywords:
            if off_topic_word in query_lower:
                score -= 0.3  # Each off-topic keyword subtracts 0.3

        # Apply technical indicators
        technical_indicators = [
            r'\b(robot|robotic)\b',
            r'\b(ai|ml|dl)\b',
            r'\b(ros|gazebo|isaac)\b',
            r'(kinematic|dynamic|locomotion|manipulation|perception)',
        ]

        for pattern in technical_indicators:
            if re.search(pattern, query_lower):
                score += 0.15

        # Normalize score to 0-1 range
        score = max(0.0, min(1.0, score))

        logger.info(f"Relevance score for query: {score:.2f}")
        return score

    async def suggest_related_topics(self, query: str) -> List[str]:
        """
        Suggest related topics from the book that might be relevant to the query

        Args:
            query: The user's query

        Returns:
            List of related topics from the book
        """
        query_lower = query.lower().strip()
        related_topics = []

        # Map common query patterns to book topics
        topic_mappings = {
            r'(walk|walki|gait|balance|posture)': [
                "Bipedal Locomotion and Balance",
                "Humanoid Kinematics and Dynamics"
            ],
            r'(manipulat|hand|grasp|pick|place)': [
                "Dexterous Manipulation",
                "Humanoid Kinematics and Dynamics"
            ],
            r'(learn|demo|imitat|reinforc)': [
                "Learning from Demonstration and RL",
                "Sim-to-Real Transfer"
            ],
            r'(vision|percept|sensor|see)': [
                "Perception for Humanoids",
                "Vision-Language-Action (VLA) Models"
            ],
            r'(ethic|safe|social)': [
                "Ethics, Safety, and Societal Impact",
                "Conversational and Social Robotics"
            ],
            r'(sim|gazebo|unity|isaac)': [
                "Digital Twin - Gazebo and Unity",
                "NVIDIA Isaac Platform"
            ],
            r'(ros|nervous)': [
                "The Robotic Nervous System - ROS 2"
            ]
        }

        for pattern, topics in topic_mappings.items():
            if re.search(pattern, query_lower):
                related_topics.extend(topics)

        # Remove duplicates while preserving order
        unique_topics = []
        for topic in related_topics:
            if topic not in unique_topics:
                unique_topics.append(topic)

        logger.info(f"Suggested related topics: {unique_topics}")
        return unique_topics

# Global instance for use in other modules
query_relevance_service = QueryRelevanceService()