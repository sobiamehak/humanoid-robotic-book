import React from 'react';
import ChatBot from './components/ChatBot';

const Root = ({ children }) => {
  return (
    <>
      {children}
      <ChatBot />
    </>
  );
};

export default Root;