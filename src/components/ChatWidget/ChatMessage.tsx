import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import clsx from 'clsx';
import SourceCitations from './SourceCitations';
import styles from './ChatWidget.module.css';

// Define TypeScript interfaces (reusing from ChatWindow)
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

interface ChatMessageProps {
  message: ChatMessage;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const isUser = message.sender === 'user';
  const messageClasses = clsx(
    styles.message,
    {
      [styles.userMessage]: isUser,
      [styles.botMessage]: !isUser,
    }
  );

  return (
    <div className={messageClasses}>
      <div className={styles.messageText}>
        <ReactMarkdown
          remarkPlugins={[remarkGfm]}
          components={{
            // Customize rendering for different markdown elements
            p: ({ node, ...props }) => <p {...props} />,
            h1: ({ node, ...props }) => <h1 className={styles.heading} {...props} />,
            h2: ({ node, ...props }) => <h2 className={styles.heading} {...props} />,
            h3: ({ node, ...props }) => <h3 className={styles.heading} {...props} />,
            h4: ({ node, ...props }) => <h4 className={styles.heading} {...props} />,
            h5: ({ node, ...props }) => <h5 className={styles.heading} {...props} />,
            h6: ({ node, ...props }) => <h6 className={styles.heading} {...props} />,
            code: ({ node, ...props }) => (
              <code className={styles.code} {...props} />
            ),
            pre: ({ node, ...props }) => (
              <pre className={styles.codeBlock} {...props} />
            ),
            a: ({ node, ...props }) => (
              <a
                className={styles.link}
                target="_blank"
                rel="noopener noreferrer"
                {...props}
              />
            ),
            li: ({ node, ...props }) => <li className={styles.listItem} {...props} />,
            ul: ({ node, ...props }) => <ul className={styles.list} {...props} />,
            ol: ({ node, ...props }) => <ol className={styles.list} {...props} />,
          }}
        >
          {message.content}
        </ReactMarkdown>
      </div>
    </div>
  );
};

export default ChatMessage;