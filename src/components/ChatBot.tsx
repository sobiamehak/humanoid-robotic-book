import React, { useState, useEffect, useRef } from 'react';
import clsx from 'clsx';
import styles from './ChatBot.module.css';

// Define TypeScript interfaces
interface SourceCitation {
  title: string;
  url: string;
}

interface ChatMessage {
  id: number;
  text: string;
  sender: 'user' | 'bot';
  sources?: SourceCitation[];
}

const ChatBot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([
    { id: 1, text: 'Hello! I\'m your AI assistant for the Physical AI & Humanoid Robotics textbook. How can I help you today?', sender: 'bot' }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value);
  };

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim() !== '' && !isLoading) {
      // Add user message
      const newUserMessage: ChatMessage = {
        id: messages.length + 1,
        text: inputValue,
        sender: 'user'
      };

      setMessages(prev => [...prev, newUserMessage]);
      setInputValue('');
      setIsLoading(true);

      try {
        // Call backend API to get response from RAG system
        const response = await fetch('http://localhost:8080/api/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            message: inputValue,
            selected_text: null,
            current_page: null
          })
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Check if the response is an SSE stream
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('text/event-stream')) {
          // Handle SSE stream
          const reader = response.body?.getReader();
          const decoder = new TextDecoder();
          let buffer = '';
          let botMessageContent = '';
          let sources = [];

          if (!reader) {
            throw new Error('No response body');
          }

          // Create a temporary bot message to update progressively
          const tempBotMessageId = messages.length + 2;
          setMessages(prev => [...prev, {
            id: tempBotMessageId,
            text: '',
            sender: 'bot'
          } as ChatMessage]);

          let hasReceivedRealContent = false;
          while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            buffer += decoder.decode(value, { stream: true });
            const lines = buffer.split('\n');
            buffer = lines.pop() || ''; // Keep last incomplete line in buffer

            for (const line of lines) {
              if (line.startsWith('data: ')) {
                try {
                  const dataStr = line.slice(6); // Remove 'data: ' prefix
                  if (dataStr.trim()) {
                    let data;
                    try {
                      // Try to parse as JSON first
                      data = JSON.parse(dataStr);
                    } catch (jsonError) {
                      // If it's not valid JSON, we need to determine if this is a sources event
                      // that couldn't be parsed due to quote format, or if it's an actual text chunk

                      // Check if this looks like a sources data string (starts with [ and contains 'title' and 'url')
                      if (dataStr.startsWith('[{') && (dataStr.includes("'title'") || dataStr.includes('"title"')) && (dataStr.includes("'url'") || dataStr.includes('"url"'))) {
                        // This appears to be sources data that couldn't be parsed as JSON due to quote format
                        // Try to handle it as sources data without adding to message content
                        try {
                          // Attempt to fix the quote format and parse
                          const fixedDataStr = dataStr.replace(/'/g, '"');
                          sources = JSON.parse(fixedDataStr);
                          // Don't add sources data to message content
                        } catch (parseError) {
                          console.error('Error parsing sources data:', parseError);
                          // Still don't add to message content as it's likely sources data
                        }
                      } else if (!dataStr.includes('Processing your request...')) {
                        // This is an actual text chunk, not sources data
                        botMessageContent += dataStr;
                        hasReceivedRealContent = true;
                        // Update the temporary bot message with new content
                        setMessages(prev =>
                          prev.map(msg =>
                            msg.id === tempBotMessageId
                              ? { ...msg, text: botMessageContent }
                              : msg
                          )
                        );
                      }
                      continue; // Skip the rest of the processing for this line
                    }

                    switch (data.event) {
                      case 'chunk':
                        // Only add the chunk if it's not the processing message or if we haven't received real content yet
                        if (!data.data.includes('Processing your request...') || !hasReceivedRealContent) {
                          if (!data.data.includes('Processing your request...')) {
                            botMessageContent += data.data;
                            hasReceivedRealContent = true;
                          } else if (!hasReceivedRealContent) {
                            // If this is the processing message and we haven't received real content yet,
                            // don't add it to the message content
                            break;
                          }
                          // Update the temporary bot message with new content
                          setMessages(prev =>
                            prev.map(msg =>
                              msg.id === tempBotMessageId
                                ? { ...msg, text: botMessageContent }
                                : msg
                            )
                          );
                        }
                        break;
                      case 'sources':
                        try {
                          sources = JSON.parse(data.data);
                          // Don't display sources in the chat message, just store them
                          // Ensure sources data is not added to botMessageContent
                        } catch (e) {
                          console.error('Error parsing sources:', e);
                        }
                        break;
                      case 'done':
                        // Update the message with final content (sources are not included in the message)
                        setMessages(prev =>
                          prev.map(msg =>
                            msg.id === tempBotMessageId
                              ? { ...msg, text: botMessageContent, sources: sources } // Add sources as a separate property
                              : msg
                          )
                        );
                        break; // Exit the while loop after completion
                    }
                  }
                } catch (e) {
                  console.error('Error parsing SSE data:', e);
                }
              }
            }
          }
        } else {
          // Handle regular JSON response as fallback
          const data = await response.json();
          // Add bot response
          const botResponse: ChatMessage = {
            id: messages.length + 2,
            text: data.response || data.answer || 'Sorry, I could not process your request.',
            sender: 'bot'
          };

          setMessages(prev => [...prev, botResponse]);
        }

        // The backend agent system already handles off-topic queries and returns appropriate responses
      } catch (error) {
        console.error('Error getting response from backend:', error);

        // Determine the type of error and provide appropriate message
        let errorMessage = "Sorry, I encountered an error while processing your request. Please try again.";

        if (error instanceof TypeError && error.message.includes('fetch')) {
          errorMessage = "Network error: Unable to connect to the AI service. Please check your internet connection and try again.";
        } else if (error.message.includes('CORS')) {
          errorMessage = "Connection error: Unable to access the AI service due to security restrictions. Please try again later.";
        } else if (error.message.includes('404') || error.message.includes('405')) {
          errorMessage = "Service error: The AI service is temporarily unavailable. Please try again later.";
        } else if (error.message.includes('NetworkError')) {
          errorMessage = "Network error: Unable to reach the AI service. Please check your connection.";
        }

        // Add error message
        const botResponse: ChatMessage = {
          id: messages.length + 2,
          text: errorMessage,
          sender: 'bot'
        };

        setMessages(prev => [...prev, botResponse]);
      } finally {
        setIsLoading(false);
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
              disabled={isLoading}
            />
            <button type="submit" className={styles.sendButton} disabled={isLoading}>
              {isLoading ? 'Sending...' : 'Send'}
            </button>
          </form>

          {/* Show loading indicator when bot is processing */}
          {isLoading && (
            <div className={styles.typingIndicator}>
              <span></span>
              <span></span>
              <span></span>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ChatBot;


