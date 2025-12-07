import React, { useState } from 'react';
import { Form, Button, Container, Row, Col, Tabs, Tab } from 'react-bootstrap';

interface SignUpFormData {
  email: string;
  password: string;
  confirmPassword: string;
  backgroundInfo: {
    academicLevel: string;
    areasOfInterest: string;
    learningStyle: string;
  };
}

interface SignInFormData {
  email: string;
  password: string;
}

const AuthPage: React.FC = () => {
  const [signUpData, setSignUpData] = useState<SignUpFormData>({
    email: '',
    password: '',
    confirmPassword: '',
    backgroundInfo: {
      academicLevel: '',
      areasOfInterest: '',
      learningStyle: ''
    }
  });

  const [signInData, setSignInData] = useState<SignInFormData>({
    email: '',
    password: ''
  });

  const handleSignUpChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    
    if (name.startsWith('background_')) {
      const backgroundField = name.split('_')[1];
      setSignUpData(prev => ({
        ...prev,
        backgroundInfo: {
          ...prev.backgroundInfo,
          [backgroundField]: value
        }
      }));
    } else {
      setSignUpData(prev => ({
        ...prev,
        [name]: value
      }));
    }
  };

  const handleSignInChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setSignInData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSignUpSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Basic validation
    if (signUpData.password !== signUpData.confirmPassword) {
      alert('Passwords do not match');
      return;
    }

    try {
      const response = await fetch('/api/auth/signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: signUpData.email,
          password: signUpData.password,
          background_info: signUpData.backgroundInfo
        }),
      });

      if (response.ok) {
        alert('Sign up successful!');
        // Redirect or update UI as needed
      } else {
        const errorData = await response.json();
        alert(`Sign up failed: ${errorData.detail}`);
      }
    } catch (error) {
      console.error('Sign up error:', error);
      alert('An error occurred during sign up');
    }
  };

  const handleSignInSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const response = await fetch('/api/auth/signin', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(signInData),
      });

      if (response.ok) {
        const userData = await response.json();
        alert(`Sign in successful! Welcome back, ${userData.email}`);
        // Redirect or update UI as needed
      } else {
        const errorData = await response.json();
        alert(`Sign in failed: ${errorData.detail}`);
      }
    } catch (error) {
      console.error('Sign in error:', error);
      alert('An error occurred during sign in');
    }
  };

  return (
    <Container className="mt-5">
      <Row className="justify-content-md-center">
        <Col md={6}>
          <Tabs defaultActiveKey="signup" id="auth-tabs" className="mb-3">
            <Tab eventKey="signup" title="Sign Up">
              <Form onSubmit={handleSignUpSubmit}>
                <Form.Group className="mb-3" controlId="signupEmail">
                  <Form.Label>Email address</Form.Label>
                  <Form.Control
                    type="email"
                    name="email"
                    value={signUpData.email}
                    onChange={handleSignUpChange}
                    required
                  />
                </Form.Group>

                <Form.Group className="mb-3" controlId="signupPassword">
                  <Form.Label>Password</Form.Label>
                  <Form.Control
                    type="password"
                    name="password"
                    value={signUpData.password}
                    onChange={handleSignUpChange}
                    required
                  />
                </Form.Group>

                <Form.Group className="mb-3" controlId="signupConfirmPassword">
                  <Form.Label>Confirm Password</Form.Label>
                  <Form.Control
                    type="password"
                    name="confirmPassword"
                    value={signUpData.confirmPassword}
                    onChange={handleSignUpChange}
                    required
                  />
                </Form.Group>

                <Form.Group className="mb-3" controlId="academicLevel">
                  <Form.Label>Academic Level</Form.Label>
                  <Form.Select
                    name="background_academicLevel"
                    value={signUpData.backgroundInfo.academicLevel}
                    onChange={handleSignUpChange}
                  >
                    <option value="">Select your academic level</option>
                    <option value="undergraduate">Undergraduate</option>
                    <option value="graduate">Graduate</option>
                    <option value="phd">PhD</option>
                    <option value="professional">Professional</option>
                    <option value="other">Other</option>
                  </Form.Select>
                </Form.Group>

                <Form.Group className="mb-3" controlId="areasOfInterest">
                  <Form.Label>Areas of Interest</Form.Label>
                  <Form.Control
                    type="text"
                    name="background_areasOfInterest"
                    value={signUpData.backgroundInfo.areasOfInterest}
                    onChange={handleSignUpChange}
                    placeholder="e.g., Locomotion, Manipulation, Perception"
                  />
                </Form.Group>

                <Form.Group className="mb-3" controlId="learningStyle">
                  <Form.Label>Learning Style</Form.Label>
                  <Form.Select
                    name="background_learningStyle"
                    value={signUpData.backgroundInfo.learningStyle}
                    onChange={handleSignUpChange}
                  >
                    <option value="">Select your learning style</option>
                    <option value="visual">Visual</option>
                    <option value="auditory">Auditory</option>
                    <option value="reading">Reading/Writing</option>
                    <option value="kinesthetic">Kinesthetic</option>
                  </Form.Select>
                </Form.Group>

                <Button variant="primary" type="submit">
                  Sign Up
                </Button>
              </Form>
            </Tab>
            <Tab eventKey="signin" title="Sign In">
              <Form onSubmit={handleSignInSubmit}>
                <Form.Group className="mb-3" controlId="signinEmail">
                  <Form.Label>Email address</Form.Label>
                  <Form.Control
                    type="email"
                    name="email"
                    value={signInData.email}
                    onChange={handleSignInChange}
                    required
                  />
                </Form.Group>

                <Form.Group className="mb-3" controlId="signinPassword">
                  <Form.Label>Password</Form.Label>
                  <Form.Control
                    type="password"
                    name="password"
                    value={signInData.password}
                    onChange={handleSignInChange}
                    required
                  />
                </Form.Group>

                <Button variant="primary" type="submit">
                  Sign In
                </Button>
              </Form>
            </Tab>
          </Tabs>
        </Col>
      </Row>
    </Container>
  );
};

export default AuthPage;