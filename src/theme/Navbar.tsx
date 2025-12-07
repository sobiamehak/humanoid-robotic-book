import React from 'react';
import Navbar from '@theme-original/Navbar';
import LanguageSwitcher from '../components/LanguageSwitcher';
import ChatBot from '../components/ChatBot';

export default function NavbarWrapper(props) {
  return (
    <>
      <Navbar {...props} />
      <div style={{ position: 'fixed', top: '10px', right: '10px', zIndex: '1000' }}>
        <LanguageSwitcher />
      </div>
      <ChatBot />
    </>
  );
}