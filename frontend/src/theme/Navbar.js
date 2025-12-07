import React, { useState, useEffect } from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import { useLocation } from '@docusaurus/router';
import useBaseUrl from '@docusaurus/useBaseUrl';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import { translate } from '@docusaurus/Translate';
import styles from './Navbar.module.css';
import LanguageSwitcher from '@site/src/components/LanguageSwitcher';
import ChatbotButton from '@site/src/components/ChatbotButton';

function Navbar() {
  const location = useLocation();
  const [currentLocale, setCurrentLocale] = useState('en');
  const [sidebarShown, setSidebarShown] = useState(false);
  const [searchBarExpanded, setSearchBarExpanded] = useState(false);

  const {
    siteConfig: {
      themeConfig: {
        navbar: {
          title,
          logo,
          items
        }
      }
    }
  } = useDocusaurusContext();

  // Detect current locale from URL or browser preference
  useEffect(() => {
    const localeFromUrl = location.pathname.split('/')[1] || 'en';
    const detectedLocale = ['en', 'ur'].includes(localeFromUrl) ? localeFromUrl : 'en';
    setCurrentLocale(detectedLocale);
  }, [location]);

  const itemsToRender = items
    .filter((item) => !item?.hideOnNavbar)
    .map((item, index) => {
      // Special handling for custom components
      if (item.type === 'custom-LanguageSwitcher') {
        return <LanguageSwitcher key={`language-switcher-${index}`} />;
      }

      // Special handling for chatbot button
      if (item.type === 'custom-ChatbotButton') {
        return <ChatbotButton key={`chatbot-button-${index}`} />;
      }

      // Default handling for other items
      return (
        <NavbarItem
          {...item}
          key={`navbar-item-${index}`}
          sidebarShown={sidebarShown}
          setSidebarShown={setSidebarShown}
        />
      );
    });

  return (
    <nav
      role="navigation"
      className={clsx(
        'navbar navbar--fixed-top',
        styles.navbar,
        sidebarShown && styles.navbarSidebarShown,
      )}>
      <div className="navbar__inner">
        <div className="navbar__items">
          <div className="navbar__brand">
            {logo && (
              <Link
                className="navbar__item navbar__logo"
                to={useBaseUrl(logo.href || '/')}
                {...(logo.target && { target: logo.target })}
                rel={logo.rel}
                aria-label={logo.alt}>
                <img className="navbar__logo" src={useBaseUrl(logo.src)} alt={logo.alt} />
              </Link>
            )}
            {title != null && (
              <div className="navbar__title" data-sidebar="show">
                {title}
              </div>
            )}
          </div>

          {itemsToRender.filter((item, index) => items[index]?.position === 'left').map((item, index) => (
            <React.Fragment key={index}>{item}</React.Fragment>
          ))}
        </div>

        <div className="navbar__items navbar__items--right">
          {itemsToRender.filter((item, index) => items[index]?.position === 'right').map((item, index) => (
            <React.Fragment key={index}>{item}</React.Fragment>
          ))}
        </div>
      </div>

      {sidebarShown && (
        <div
          role="presentation"
          className="navbar-sidebar__backdrop"
          onClick={() => setSidebarShown(false)}
        />
      )}
    </nav>
  );
}

function NavbarItem({ className, to, href, label, position, ...props }) {
  const isExternalLink = href && !href.startsWith('/');
  const customProps = {
    className: clsx(
      'navbar__item navbar__link',
      position && `navbar__item--${position}`,
      className,
    ),
    ...props,
  };

  if (isExternalLink) {
    return <a href={href} {...customProps}>{label}</a>;
  }

  if (to) {
    // For internal links
    return (
      <Link to={to} {...customProps}>
        {label}
      </Link>
    );
  }

  return <div {...customProps}>{label}</div>;
}

export default Navbar;