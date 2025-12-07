import React, { useState, useRef, useEffect } from 'react';

const ChatbotButton = () => {
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [messages, setMessages] = useState([
    { id: 1, text: "Hello! I'm your AI assistant for the Physical AI & Humanoid Robotics textbook. How can I help you today?", sender: 'bot' }
  ]);
  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef(null);

  const toggleChat = () => {
    setIsChatOpen(!isChatOpen);
  };

  const closeChat = () => {
    setIsChatOpen(false);
  };

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  };

  const handleSendMessage = () => {
    if (inputValue.trim() === '') return;

    // Add user message
    const newUserMessage = {
      id: messages.length + 1,
      text: inputValue,
      sender: 'user'
    };

    setMessages(prev => [...prev, newUserMessage]);
    setInputValue('');

    // Call backend API to get real response
    fetch('http://localhost:8000/chatbot/query', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query: inputValue,
        context_type: 'entire_book'  // Default to entire book context
      })
    })
    .then(response => response.json())
    .then(data => {
      const botResponse = {
        id: messages.length + 2,
        text: data.response || "Sorry, I couldn't process your request.",
        sender: 'bot'
      };
      setMessages(prev => [...prev, botResponse]);
    })
    .catch(error => {
      console.error('Error:', error);
      const botResponse = {
        id: messages.length + 2,
        text: "Sorry, I'm having trouble connecting to the backend. Please try again later.",
        sender: 'bot'
      };
      setMessages(prev => [...prev, botResponse]);
    });
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSendMessage();
    }
  };

  // Scroll to bottom of messages when they change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <>
      <button
        className="chatbot-button"
        onClick={toggleChat}
        aria-label="Open chatbot"
      >
        🤖
      </button>

      {isChatOpen && (
        <div className="chatbot-popup">
          <div className="chatbot-container">
            <div className="chatbot-header">
              <h3>AI Assistant</h3>
              <button className="chatbot-close" onClick={closeChat} aria-label="Close chat">×</button>
            </div>
            <div className="chatbot-messages">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`message ${message.sender}-message`}
                >
                  {message.text}
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>
            <div className="chatbot-input-area">
              <input
                type="text"
                className="chatbot-input"
                placeholder="Ask a question..."
                value={inputValue}
                onChange={handleInputChange}
                onKeyPress={handleKeyPress}
              />
              <button
                className="chatbot-send"
                onClick={handleSendMessage}
                aria-label="Send message"
              >
                Send
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default ChatbotButton;