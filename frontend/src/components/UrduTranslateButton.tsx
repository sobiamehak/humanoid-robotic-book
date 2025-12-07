import React, { useState } from 'react';
import { Button, Spinner } from 'react-bootstrap';

interface UrduTranslateButtonProps {
  onTranslate: () => Promise<void>;
  chapterId: string;
  disabled?: boolean;
}

const UrduTranslateButton: React.FC<UrduTranslateButtonProps> = ({ 
  onTranslate, 
  chapterId, 
  disabled = false 
}) => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleClick = async () => {
    if (disabled) return;
    
    setIsLoading(true);
    setError(null);
    
    try {
      await onTranslate();
    } catch (err) {
      console.error('Translation error:', err);
      setError('Failed to translate content. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="d-flex align-items-center">
      <Button
        variant="success"
        onClick={handleClick}
        disabled={isLoading || disabled}
        className="d-flex align-items-center"
      >
        {isLoading ? (
          <>
            <Spinner
              as="span"
              animation="border"
              size="sm"
              role="status"
              className="me-2"
            />
            Translating...
          </>
        ) : (
          'اردو میں ترجمہ کریں'
        )}
      </Button>
      
      {error && (
        <div className="text-danger ms-2">
          {error}
        </div>
      )}
    </div>
  );
};

export default UrduTranslateButton;