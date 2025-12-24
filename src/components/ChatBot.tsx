import React, { useState, useEffect, useRef } from 'react';
import clsx from 'clsx';
import styles from './ChatBot.module.css';

const ChatBot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { id: 1, text: 'Hello! How can I help you today?', sender: 'bot' }
  ]);
  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value);
  };

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim() !== '') {
      // Add user message
      const newUserMessage = {
        id: messages.length + 1,
        text: inputValue,
        sender: 'user'
      };

      setMessages(prev => [...prev, newUserMessage]);
      setInputValue('');

      try {
        // Call backend API to get response from RAG system
        const response = await fetch('https://mehaksobi-my-book.hf.space/api/ask', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            query: inputValue
          })
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        // Add bot response
        const botResponse = {
          id: messages.length + 2,
          text: data.response,
          sender: 'bot'
        };

        setMessages(prev => [...prev, botResponse]);

        // The backend agent system already handles off-topic queries and returns appropriate responses
      } catch (error) {
        console.error('Error getting response from backend:', error);

        // Add error message
        const botResponse = {
          id: messages.length + 2,
          text: "Sorry, I encountered an error while processing your request. Please try again.",
          sender: 'bot'
        };

        setMessages(prev => [...prev, botResponse]);
      }
    }
  };

  // Scroll to bottom of messages when they change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className={styles.chatContainer}>
      {/* Chatbot button */}
      <button 
        className={clsx(styles.chatButton, { [styles.open]: isOpen })}
        onClick={toggleChat}
        aria-label={isOpen ? 'Close chat' : 'Open chat'}
      >
        💬
      </button>

      {/* Chat window */}
      {isOpen && (
        <div className={styles.chatWindow}>
          <div className={styles.chatHeader}>
            <h3>AI Assistant</h3>
            <button 
              className={styles.closeButton}
              onClick={toggleChat}
              aria-label="Close chat"
            >
              ×
            </button>
          </div>
          
          <div className={styles.chatMessages}>
            {messages.map((message) => (
              <div 
                key={message.id} 
                className={clsx(
                  styles.message, 
                  { [styles.userMessage]: message.sender === 'user' },
                  { [styles.botMessage]: message.sender === 'bot' }
                )}
              >
                <div className={styles.messageText}>
                  {message.text}
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>
          
          <form onSubmit={handleSendMessage} className={styles.chatInputForm}>
            <input
              type="text"
              value={inputValue}
              onChange={handleInputChange}
              placeholder="Type your message..."
              className={styles.chatInput}
            />
            <button type="submit" className={styles.sendButton}>
              Send
            </button>
          </form>
        </div>
      )}
    </div>
  );
};

export default ChatBot;