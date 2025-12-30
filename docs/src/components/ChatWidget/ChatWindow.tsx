import React, { useState, useRef, useEffect } from 'react';
import clsx from 'clsx';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import styles from './ChatWidget.module.css';

// Define TypeScript interfaces
interface SourceCitation {
  title: string;
  url: string;
}

interface ChatMessage {
  id: string;
  content: string;
  sender: 'user' | 'bot';
  timestamp: Date;
  sources?: SourceCitation[];
  status?: 'sending' | 'sent' | 'delivered' | 'error';
}

interface ChatSession {
  id: string;
  messages: ChatMessage[];
  isLoading: boolean;
}

const ChatWindow: React.FC<{ onClose: () => void }> = ({ onClose }) => {
  const [session, setSession] = useState<ChatSession>({
    id: `session_${Date.now()}`,
    messages: [
      {
        id: 'initial',
        content: 'Hello! I\'m your AI assistant for the Physical AI & Humanoid Robotics textbook. How can I help you today?',
        sender: 'bot',
        timestamp: new Date(),
      }
    ],
    isLoading: false,
  });

  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom of messages when they change
  useEffect(() => {
    scrollToBottom();
  }, [session.messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleNewMessage = (message: Omit<ChatMessage, 'id' | 'timestamp'>) => {
    const newMessage: ChatMessage = {
      ...message,
      id: `msg_${Date.now()}`,
      timestamp: new Date(),
    };

    setSession(prev => {
      // If this is a bot message with status 'sending', update the last bot message
      if (message.sender === 'bot' && message.status === 'sending') {
        // Find the last bot message that is in 'sending' status
        let lastBotMessageIndex = -1;
        for (let i = prev.messages.length - 1; i >= 0; i--) {
          if (prev.messages[i].sender === 'bot' && prev.messages[i].status === 'sending') {
            lastBotMessageIndex = i;
            break;
          }
        }

        if (lastBotMessageIndex !== -1) {
          // Update the existing sending message
          const updatedMessages = [...prev.messages];
          updatedMessages[lastBotMessageIndex] = newMessage;
          return {
            ...prev,
            messages: updatedMessages,
          };
        } else {
          // No existing sending message, add as new message
          return {
            ...prev,
            messages: [...prev.messages, newMessage],
          };
        }
      } else {
        // For user messages or completed bot messages, add as new message
        return {
          ...prev,
          messages: [...prev.messages, newMessage],
          isLoading: message.sender === 'user', // Set loading when user sends message
        };
      }
    });
  };

  const handleLoadingChange = (isLoading: boolean) => {
    setSession(prev => ({
      ...prev,
      isLoading,
    }));
  };

  return (
    <div className={styles.chatWindow}>
      <div className={styles.chatHeader}>
        <h3>AI Assistant</h3>
        <button
          className={styles.closeButton}
          onClick={onClose}
          aria-label="Close chat"
        >
          ×
        </button>
      </div>

      <div className={styles.chatMessages}>
        {session.messages.map((message) => (
          <ChatMessage
            key={message.id}
            message={message}
          />
        ))}
        {session.isLoading && (
          <div className={styles.typingIndicator}>
            <span></span>
            <span></span>
            <span></span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <ChatInput
        onSendMessage={handleNewMessage}
        onLoadingChange={handleLoadingChange}
        isLoading={session.isLoading}
      />
    </div>
  );
};

export default ChatWindow;