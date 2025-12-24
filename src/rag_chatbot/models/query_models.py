from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime

class QueryRequest(BaseModel):
    """Model for incoming query requests"""
    query: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    context_window: Optional[int] = 5  # Number of context items to retrieve
    include_citations: Optional[bool] = True

class QueryResponse(BaseModel):
    """Model for query responses"""
    response: str
    query_id: str = str(uuid.uuid4())
    timestamp: datetime = datetime.now()
    citations: Optional[List[Dict[str, Any]]] = []
    context_used: Optional[List[Dict[str, Any]]] = []
    is_off_topic: Optional[bool] = False

class MultiStepQueryRequest(BaseModel):
    """Model for complex multi-step queries"""
    query: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    max_steps: Optional[int] = 3
    include_citations: Optional[bool] = True

class AgentMessage(BaseModel):
    """Model for agent-to-agent communication"""
    message_id: str = str(uuid.uuid4())
    sender: str
    receiver: str
    content: str
    timestamp: datetime = datetime.now()
    metadata: Optional[Dict[str, Any]] = {}
    next_action: Optional[str] = None  # What the receiving agent should do next

class RetrievalResult(BaseModel):
    """Model for retrieval results"""
    id: str
    content: str
    score: float
    source: str  # Chapter, section, or document identifier
    page_number: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = {}

class AgentHandoff(BaseModel):
    """Model for agent handoff requests"""
    from_agent: str
    to_agent: str
    reason: str
    context: Dict[str, Any]
    priority: int = 1  # 1-5 priority level