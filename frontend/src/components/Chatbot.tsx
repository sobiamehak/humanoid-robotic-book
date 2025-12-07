import React, { useState, useRef, useEffect } from 'react';
import { Container, Row, Col, Form, Button, Card, ListGroup } from 'react-bootstrap';

interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: Date;
  sources?: Array<{
    chapter_id: string;
    module_id: string;
    title: string;
    content_snippet: string;
  }>;
}

interface ChatbotProps {
  // Any props needed for the chatbot
}

const Chatbot: React.FC<ChatbotProps> = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  // Scroll to bottom of messages when new message is added
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async () => {
    if (!inputText.trim() || isLoading) return;

    // Add user message to the chat
    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputText,
      role: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsLoading(true);

    try {
      // In a real implementation, this would call the backend API
      // For now, using a mock response
      const response = await mockChatbotAPI(inputText);
      
      // Add assistant response to the chat
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: response.response,
        role: 'assistant',
        timestamp: new Date(),
        sources: response.sources
      };
      
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error getting chatbot response:', error);
      
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: 'Sorry, I encountered an error processing your request.',
        role: 'assistant',
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // Mock API call - in a real implementation, this would call the backend
  const mockChatbotAPI = async (query: string): Promise<{ response: string; sources: any[] }> => {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // This is just a mock response - in a real implementation, 
    // you would call the backend API: /api/chatbot/query
    return {
      response: `This is a simulated response to your query: "${query}". In a real implementation, this would come from the RAG chatbot connected to your textbook knowledge base.`,
      sources: [
        {
          chapter_id: 'chapter-01',
          module_id: 'module-1',
          title: 'Introduction to Physical AI',
          content_snippet: 'Physical AI combines robotics...'
        }
      ]
    };
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <Container fluid className="chatbot-container">
      <Row>
        <Col>
          <Card>
            <Card.Header>
              <h5>Textbook RAG Chatbot</h5>
              <p className="text-muted">Ask questions about the textbook content</p>
            </Card.Header>
            <Card.Body className="chat-history" style={{ height: '400px', overflowY: 'auto' }}>
              {messages.length === 0 ? (
                <div className="text-center text-muted mt-5">
                  <p>Ask me anything about the textbook content!</p>
                  <p>Try asking: "Explain locomotion in humanoid robots" or "What are the key principles of perception systems?"</p>
                </div>
              ) : (
                <div>
                  {messages.map((message) => (
                    <div 
                      key={message.id} 
                      className={`d-flex mb-3 ${message.role === 'user' ? 'justify-content-end' : 'justify-content-start'}`}
                    >
                      <div 
                        className={`p-3 rounded ${message.role === 'user' ? 'bg-primary text-white' : 'bg-light'}`} 
                        style={{ maxWidth: '80%' }}
                      >
                        <div className="fw-bold mb-1">
                          {message.role === 'user' ? 'You' : 'Textbook Assistant'}
                        </div>
                        <div>{message.content}</div>
                        
                        {/* Show sources if available */}
                        {message.sources && message.sources.length > 0 && (
                          <ListGroup variant="flush" className="mt-2">
                            <ListGroup.Item className="p-1">
                              <small className="text-muted">Sources:</small>
                              {message.sources.map((source, idx) => (
                                <div key={idx} className="text-muted small">
                                  - {source.title} ({source.chapter_id})
                                </div>
                              ))}
                            </ListGroup.Item>
                          </ListGroup>
                        )}
                      </div>
                    </div>
                  ))}
                  <div ref={messagesEndRef} />
                </div>
              )}
            </Card.Body>
            <Card.Footer>
              <Form onSubmit={(e) => { e.preventDefault(); handleSendMessage(); }}>
                <div className="d-flex">
                  <Form.Control
                    as="textarea"
                    rows={1}
                    value={inputText}
                    onChange={(e) => setInputText(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Ask a question about the textbook..."
                    disabled={isLoading}
                    style={{ resize: 'none' }}
                  />
                  <Button 
                    variant="primary" 
                    onClick={handleSendMessage} 
                    disabled={isLoading || !inputText.trim()}
                    className="ms-2"
                  >
                    {isLoading ? 'Sending...' : 'Send'}
                  </Button>
                </div>
              </Form>
            </Card.Footer>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default Chatbot;