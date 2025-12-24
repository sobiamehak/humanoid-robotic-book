from abc import ABC, abstractmethod
from typing import Any, Dict
from ..models.query_models import AgentMessage, QueryRequest, QueryResponse

class BaseAgent(ABC):
    """Abstract base class for all agents in the system"""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    async def process(self, message: AgentMessage) -> AgentMessage:
        """Process an incoming message and return a response"""
        pass

    @abstractmethod
    async def handle_request(self, query_request: QueryRequest) -> QueryResponse:
        """Handle a query request and return a response"""
        pass

    def create_response_message(self, content: str, receiver: str, next_action: str = None) -> AgentMessage:
        """Helper method to create a standard response message"""
        return AgentMessage(
            sender=self.name,
            receiver=receiver,
            content=content,
            next_action=next_action
        )

# Import all agent types to make them available at package level
from .main_agent import MainAgent
from .retrieval_agent import RetrievalAgent
from .generation_agent import GenerationAgent

__all__ = ["BaseAgent", "MainAgent", "RetrievalAgent", "GenerationAgent"]