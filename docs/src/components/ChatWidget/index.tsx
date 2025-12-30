import React, { useState, useEffect } from 'react';
import clsx from 'clsx';
import ChatWindow from './ChatWindow';
import styles from './ChatWidget.module.css';

const ChatWidget = () => {
  const [isOpen, setIsOpen] = useState(false);

  // Close chat when user clicks outside of chat window
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (isOpen) {
        const chatWindow = document.querySelector(`.${styles.chatWindow}`);
        const chatButton = document.querySelector(`.${styles.chatButton}`);

        if (chatWindow && !chatWindow.contains(event.target as Node) &&
            chatButton && !chatButton.contains(event.target as Node)) {
          setIsOpen(false);
        }
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen]);

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className={styles.chatContainer}>
      {/* Floating chat button */}
      <button
        className={clsx(styles.chatButton, { [styles.open]: isOpen })}
        onClick={toggleChat}
        aria-label={isOpen ? 'Close chat' : 'Open chat'}
        title="Chat with our AI assistant"
      >
        💬
      </button>

      {/* Chat window - only render when open for better performance */}
      {isOpen && <ChatWindow onClose={toggleChat} />}
    </div>
  );
};

export default ChatWidget;