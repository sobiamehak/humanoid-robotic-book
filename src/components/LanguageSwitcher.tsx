import React, { useState, useEffect } from 'react';
import clsx from 'clsx';
import styles from './LanguageSwitcher.module.css';

const LanguageSwitcher = () => {
  const [currentLang, setCurrentLang] = useState('en');

  useEffect(() => {
    // Check for saved language preference or default to 'en'
    const savedLang = localStorage.getItem('preferred-language') || 'en';
    setCurrentLang(savedLang);
    
    // Update HTML lang attribute
    document.documentElement.lang = savedLang;
  }, []);

  const toggleLanguage = () => {
    const newLang = currentLang === 'en' ? 'ur' : 'en';
    setCurrentLang(newLang);
    localStorage.setItem('preferred-language', newLang);
    
    // Update HTML lang attribute
    document.documentElement.lang = newLang;
  };

  return (
    <div className={clsx('dropdown dropdown--right dropdown--navbar', styles.languageSwitcher)}>
      <button 
        className={clsx('navbar__link', styles.switcherButton)}
        onClick={toggleLanguage}
        aria-label={`Switch to ${currentLang === 'en' ? 'Urdu' : 'English'}`}
      >
        {currentLang === 'en' ? 'English 🇺🇸' : 'اردو 🇵🇰'}
      </button>
    </div>
  );
};

export default LanguageSwitcher;