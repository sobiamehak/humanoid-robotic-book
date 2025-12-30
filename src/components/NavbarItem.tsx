import React from 'react';
import clsx from 'clsx';
import styles from './NavbarItem.module.css';

// Custom component for language toggle in navbar
const NavbarItem: React.FC = () => {
  return (
    <div className={clsx('navbar__item', styles.navbarItem)}>
      <div className="navbar__item--language-toggle">
       
      </div>
    </div>
  );
};

export default NavbarItem;