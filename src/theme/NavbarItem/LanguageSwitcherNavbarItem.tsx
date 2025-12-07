import React from 'react';
import NavbarItem from '@theme-original/NavbarItem';
import LanguageSwitcher from '../components/LanguageSwitcher';

export default function LanguageSwitcherNavbarItem(props) {
  return (
    <>
      <LanguageSwitcher />
      <NavbarItem {...props} />
    </>
  );
}