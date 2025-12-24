import React from 'react';
import ChatBot from '../components/ChatBot';

// Root component that wraps the entire Docusaurus application
const Root = ({ children }) => {
  return (
    <>
      {children}
      <ChatBot />
    </>
  );
};

export default Root;