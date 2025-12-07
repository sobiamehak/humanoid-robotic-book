import React, { useState, useEffect, useRef } from 'react';
import { Button, Modal } from 'react-bootstrap';
import Chatbot from './Chatbot';

interface ChapterContentProps {
  content: string;
}

const ChapterContent: React.FC<ChapterContentProps> = ({ content }) => {
  const [selectedText, setSelectedText] = useState<string>('');
  const [showChatbotModal, setShowChatbotModal] = useState(false);
  const [showSelectedTextAlert, setShowSelectedTextAlert] = useState(false);
  const contentRef = useRef<HTMLDivElement>(null);

  // Function to handle text selection
  const handleTextSelection = () => {
    const selection = window.getSelection();
    if (selection && selection.toString().trim() !== '') {
      const selectedTextContent = selection.toString();
      if (selectedTextContent.length > 0) {
        setSelectedText(selectedTextContent);
        setShowSelectedTextAlert(true);
        
        // Hide the alert after 3 seconds
        setTimeout(() => {
          setShowSelectedTextAlert(false);
        }, 3000);
      }
    }
  };

  // Add event listeners for text selection
  useEffect(() => {
    const contentElement = contentRef.current;
    if (contentElement) {
      contentElement.addEventListener('mouseup', handleTextSelection);
      // For mobile devices
      contentElement.addEventListener('touchend', handleTextSelection);
    }

    // Cleanup event listeners
    return () => {
      if (contentElement) {
        contentElement.removeEventListener('mouseup', handleTextSelection);
        contentElement.removeEventListener('touchend', handleTextSelection);
      }
    };
  }, []);

  const handleOpenChatbotWithSelection = () => {
    if (selectedText) {
      setShowChatbotModal(true);
    }
  };

  return (
    <div>
      <div 
        ref={contentRef} 
        className="chapter-content"
        style={{ position: 'relative' }}
      >
        <div dangerouslySetInnerHTML={{ __html: content }} />
      </div>

      {/* Alert shown when text is selected */}
      {showSelectedTextAlert && selectedText && (
        <div 
          style={{
            position: 'fixed',
            bottom: '20px',
            right: '20px',
            backgroundColor: '#007bff',
            color: 'white',
            padding: '10px 15px',
            borderRadius: '5px',
            zIndex: 1000,
            boxShadow: '0 2px 10px rgba(0,0,0,0.2)'
          }}
        >
          <span>
            Text selected: {selectedText.substring(0, 30)}{selectedText.length > 30 ? '...' : ''}
          </span>
          <Button 
            variant="light" 
            size="sm" 
            className="ms-2"
            onClick={handleOpenChatbotWithSelection}
          >
            Ask Chatbot
          </Button>
        </div>
      )}

      {/* Modal for the chatbot */}
      <Modal 
        show={showChatbotModal} 
        onHide={() => setShowChatbotModal(false)} 
        size="lg"
        dialogClassName="chatbot-modal"
      >
        <Modal.Header closeButton>
          <Modal.Title>Chapter Context Chatbot</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <p className="text-muted">
            <small>
              <strong>Selected text:</strong> {selectedText.substring(0, 100)}{selectedText.length > 100 ? '...' : ''}
            </small>
          </p>
          <Chatbot />
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowChatbotModal(false)}>
            Close
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
};

export default ChapterContent;