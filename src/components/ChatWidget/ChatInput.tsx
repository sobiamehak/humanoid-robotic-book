import React, { useState, useRef, useEffect } from 'react';
import clsx from 'clsx';
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

interface ChatInputProps {
  onSendMessage: (message: Omit<ChatMessage, 'id' | 'timestamp'>) => void;
  onLoadingChange: (loading: boolean) => void;
  isLoading: boolean;
}

interface SSEData {
  event: 'chunk' | 'sources' | 'done';
  data: string;
}

const ChatInput: React.FC<ChatInputProps> = ({ onSendMessage, onLoadingChange, isLoading }) => {
  const [inputValue, setInputValue] = useState('');
  const abortControllerRef = useRef<AbortController | null>(null);

  useEffect(() => {
    // Cleanup on unmount
    return () => {
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
    };
  }, []);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (inputValue.trim() === '' || isLoading) {
      return;
    }

    // Add user message to chat
    onSendMessage({
      content: inputValue,
      sender: 'user',
    });

    // Create a new AbortController for this request
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
    abortControllerRef.current = new AbortController();

    try {
      onLoadingChange(true);

      // Connect to the backend API using fetch with streaming
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: inputValue,
          selected_text: null,
          current_page: null,
        }),
        signal: abortControllerRef.current.signal,
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
        let sources: { title: string; url: string }[] = [];
        let isComplete = false;

        if (!reader) {
          throw new Error('No response body');
        }

        while (!isComplete) {
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
                  const data = JSON.parse(dataStr);
                  const sseData: SSEData = data;

                  switch (sseData.event) {
                    case 'chunk':
                      botMessageContent += sseData.data;
                      // Update the temporary bot message with new content
                      onSendMessage({
                        content: botMessageContent,
                        sender: 'bot',
                        status: 'sending',
                      });
                      break;
                    case 'sources':
                      try {
                        sources = JSON.parse(sseData.data);
                      } catch (e) {
                        console.error('Error parsing sources:', e);
                      }
                      break;
                    case 'done':
                      // Send final bot message with sources
                      onSendMessage({
                        content: botMessageContent,
                        sender: 'bot',
                        sources: sources,
                        status: 'delivered',
                      });
                      onLoadingChange(false);
                      setInputValue('');
                      isComplete = true;
                      break;
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
        onSendMessage({
          content: data.response || data.answer || 'Sorry, I could not process your request.',
          sender: 'bot',
        });
        onLoadingChange(false);
        setInputValue('');
      }
    } catch (error) {
      console.error('Error sending message:', error);

      if (error instanceof Error && error.name !== 'AbortError') {
        // Handle network errors and other non-abort errors
        let errorMessage = 'Sorry, I encountered an error while processing your request. Please try again.';

        if (error.message.includes('fetch')) {
          errorMessage = 'Network error: Unable to connect to the AI service. Please check your internet connection.';
        } else if (error.message.includes('404') || error.message.includes('405')) {
          errorMessage = 'Service error: The AI service is temporarily unavailable. Please try again later.';
        }

        onSendMessage({
          content: errorMessage,
          sender: 'bot',
          status: 'error',
        });
      }

      onLoadingChange(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e as any); // Type assertion to allow form event
    }
  };

  return (
    <form onSubmit={handleSubmit} className={styles.chatInputForm}>
      <input
        type="text"
        value={inputValue}
        onChange={handleInputChange}
        onKeyDown={handleKeyDown}
        placeholder="Type your message..."
        className={styles.chatInput}
        disabled={isLoading}
        aria-label="Type your message"
      />
      <button
        type="submit"
        className={styles.sendButton}
        disabled={isLoading || inputValue.trim() === ''}
        aria-label="Send message"
      >
        {isLoading ? 'Sending...' : 'Send'}
      </button>
    </form>
  );
};

export default ChatInput;