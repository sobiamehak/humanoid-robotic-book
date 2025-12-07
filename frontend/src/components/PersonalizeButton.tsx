import React, { useState } from 'react';
import { Button, Spinner } from 'react-bootstrap';

interface PersonalizeButtonProps {
  onPersonalize: () => Promise<string>;
  chapterId: string;
  disabled?: boolean;
}

const PersonalizeButton: React.FC<PersonalizeButtonProps> = ({ 
  onPersonalize, 
  chapterId, 
  disabled = false 
}) => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handlePersonalize = async () => {
    if (disabled) return;
    
    setIsLoading(true);
    setError(null);
    
    try {
      await onPersonalize();
    } catch (err) {
      console.error('Personalization error:', err);
      setError('Failed to personalize content. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="d-flex align-items-center">
      <Button
        variant="primary"
        onClick={handlePersonalize}
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
            Personalizing...
          </>
        ) : (
          'Personalize this chapter'
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

export default PersonalizeButton;