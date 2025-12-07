import React, { useState, useEffect } from 'react';
import { useLocation, useHistory } from '@docusaurus/router';
import { translate } from '@docusaurus/Translate';

const LanguageSwitcher = () => {
  const [currentLocale, setCurrentLocale] = useState('en');
  const location = useLocation();
  const history = useHistory();

  // Detect current locale from URL or browser preference
  useEffect(() => {
    // Check URL for locale
    const pathname = location.pathname;
    const localeFromUrl = pathname.split('/')[1];

    // If URL starts with a valid locale, use it; otherwise default to 'en'
    if (['en', 'ur'].includes(localeFromUrl)) {
      setCurrentLocale(localeFromUrl);
    } else {
      // If no locale in URL, default to 'en'
      setCurrentLocale('en');
    }
  }, [location]);

  // Toggle between English and Urdu
  const toggleLanguage = () => {
    const newLocale = currentLocale === 'en' ? 'ur' : 'en';

    // Get the current path without the locale
    const currentPath = location.pathname;
    let newPath = currentPath;

    // Remove existing locale from path if present
    if (currentPath.startsWith('/en/') || currentPath.startsWith('/ur/')) {
      newPath = currentPath.substring(3); // Remove '/en' or '/ur'
    } else if (currentPath === '/en' || currentPath === '/ur') {
      newPath = '/';
    }

    // Construct new path with the new locale
    const finalPath = newLocale === 'en' ? newPath : `/${newLocale}${newPath}`;

    // Change the language by navigating to the new locale
    history.push(finalPath);
  };

  return (
    <button
      className="language-switcher"
      onClick={toggleLanguage}
      aria-label={translate({
        id: 'theme.navbar.language.switcher.ariaLabel',
        message: 'Switch language',
        description: 'The ARIA label for the language switcher button in the navbar'
      })}
    >
      {currentLocale === 'en' ? 'English ↔ اردو' : 'اردو ↔ English'}
    </button>
  );
};

export default LanguageSwitcher;