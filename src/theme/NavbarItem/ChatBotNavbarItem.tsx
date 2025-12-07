import React from 'react';
import NavbarItem from '@theme-original/NavbarItem';
import ChatBot from '../components/ChatBot';

export default function ChatBotNavbarItem(props) {
  return (
    <>
      <ChatBot />
      <NavbarItem {...props} />
    </>
  );
}