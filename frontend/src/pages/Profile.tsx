import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Button, Form } from 'react-bootstrap';
import { useHistory } from 'react-router-dom';

interface UserProfile {
  user_id: string;
  email: string;
  background_info: {
    academicLevel?: string;
    areasOfInterest?: string;
    learningStyle?: string;
  };
  created_at: string;
  updated_at: string;
}

const ProfilePage: React.FC = () => {
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [isEditing, setIsEditing] = useState(false);
  const [updatedBackgroundInfo, setUpdatedBackgroundInfo] = useState({
    academicLevel: '',
    areasOfInterest: '',
    learningStyle: ''
  });
  const history = useHistory();

  useEffect(() => {
    // In a real application, this would fetch the user's profile from the backend
    // For now, we'll use mock data or localStorage
    const mockProfile: UserProfile = {
      user_id: 'mock-user-id',
      email: 'user@example.com',
      background_info: {
        academicLevel: 'graduate',
        areasOfInterest: 'Locomotion, Manipulation',
        learningStyle: 'visual'
      },
      created_at: '2025-12-01T10:00:00Z',
      updated_at: '2025-12-01T10:00:00Z'
    };
    
    setProfile(mockProfile);
    setUpdatedBackgroundInfo({
      academicLevel: mockProfile.background_info.academicLevel || '',
      areasOfInterest: mockProfile.background_info.areasOfInterest || '',
      learningStyle: mockProfile.background_info.learningStyle || ''
    });
  }, []);

  const handleEditClick = () => {
    setIsEditing(true);
  };

  const handleSaveClick = async () => {
    // In a real application, this would save the profile updates to the backend
    console.log('Saving updated profile:', updatedBackgroundInfo);
    
    if (profile) {
      const updatedProfile = {
        ...profile,
        background_info: updatedBackgroundInfo
      };
      setProfile(updatedProfile);
      setIsEditing(false);
    }
  };

  const handleCancelClick = () => {
    if (profile) {
      setUpdatedBackgroundInfo({
        academicLevel: profile.background_info.academicLevel || '',
        areasOfInterest: profile.background_info.areasOfInterest || '',
        learningStyle: profile.background_info.learningStyle || ''
      });
    }
    setIsEditing(false);
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setUpdatedBackgroundInfo(prev => ({
      ...prev,
      [name]: value
    }));
  };

  if (!profile) {
    return <div>Loading...</div>;
  }

  return (
    <Container className="mt-5">
      <Row className="justify-content-center">
        <Col md={8}>
          <Card>
            <Card.Header>
              <h2>User Profile</h2>
            </Card.Header>
            <Card.Body>
              <Form>
                <Form.Group className="mb-3" controlId="profileEmail">
                  <Form.Label>Email</Form.Label>
                  <Form.Control
                    type="email"
                    value={profile.email}
                    disabled
                  />
                </Form.Group>

                <Form.Group className="mb-3" controlId="academicLevel">
                  <Form.Label>Academic Level</Form.Label>
                  {isEditing ? (
                    <Form.Select
                      name="academicLevel"
                      value={updatedBackgroundInfo.academicLevel}
                      onChange={handleInputChange}
                    >
                      <option value="">Select your academic level</option>
                      <option value="undergraduate">Undergraduate</option>
                      <option value="graduate">Graduate</option>
                      <option value="phd">PhD</option>
                      <option value="professional">Professional</option>
                      <option value="other">Other</option>
                    </Form.Select>
                  ) : (
                    <Form.Control
                      type="text"
                      value={profile.background_info.academicLevel || ''}
                      disabled
                    />
                  )}
                </Form.Group>

                <Form.Group className="mb-3" controlId="areasOfInterest">
                  <Form.Label>Areas of Interest</Form.Label>
                  {isEditing ? (
                    <Form.Control
                      type="text"
                      name="areasOfInterest"
                      value={updatedBackgroundInfo.areasOfInterest}
                      onChange={handleInputChange}
                      placeholder="e.g., Locomotion, Manipulation, Perception"
                    />
                  ) : (
                    <Form.Control
                      type="text"
                      value={profile.background_info.areasOfInterest || ''}
                      disabled
                    />
                  )}
                </Form.Group>

                <Form.Group className="mb-3" controlId="learningStyle">
                  <Form.Label>Learning Style</Form.Label>
                  {isEditing ? (
                    <Form.Select
                      name="learningStyle"
                      value={updatedBackgroundInfo.learningStyle}
                      onChange={handleInputChange}
                    >
                      <option value="">Select your learning style</option>
                      <option value="visual">Visual</option>
                      <option value="auditory">Auditory</option>
                      <option value="reading">Reading/Writing</option>
                      <option value="kinesthetic">Kinesthetic</option>
                    </Form.Select>
                  ) : (
                    <Form.Control
                      type="text"
                      value={profile.background_info.learningStyle || ''}
                      disabled
                    />
                  )}
                </Form.Group>

                <Form.Group className="mb-3" controlId="createdDate">
                  <Form.Label>Member Since</Form.Label>
                  <Form.Control
                    type="text"
                    value={new Date(profile.created_at).toLocaleDateString()}
                    disabled
                  />
                </Form.Group>

                <div className="d-grid gap-2 d-md-flex justify-content-md-end">
                  {!isEditing ? (
                    <>
                      <Button variant="primary" onClick={handleEditClick}>
                        Edit Profile
                      </Button>
                    </>
                  ) : (
                    <>
                      <Button variant="secondary" onClick={handleCancelClick}>
                        Cancel
                      </Button>
                      <Button variant="primary" onClick={handleSaveClick}>
                        Save Changes
                      </Button>
                    </>
                  )}
                </div>
              </Form>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default ProfilePage;