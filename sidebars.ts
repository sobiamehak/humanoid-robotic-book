import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  // By default, Docusaurus generates a sidebar from the docs folder structure
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Module 1: Foundations',
      items: [
        'chapter-01-introduction',
        'chapter-02-the-robotic-nervous-system-ros2'
      ],
    },
    {
      type: 'category',
      label: 'Module 2: Core Concepts',
      items: [
        'chapter-03-kinematics',
        'chapter-04-dynamics',
        'chapter-05-perception',
        'chapter-06-locomotion',
        'chapter-07-manipulation'
      ],
    },
    {
      type: 'category',
      label: 'Module 3: Intelligence & Learning',
      items: [
        'chapter-08-learning',
        'chapter-09-cognition'
      ],
    },
    {
      type: 'category',
      label: 'Module 4: Applications & Future',
      items: [
        'chapter-10-humanoid-platforms',
        'chapter-11-applications',
        'chapter-12-future',
        'chapter-13-ethics'
      ],
    },
    {
      type: 'category',
      label: 'Appendices',
      items: [
        'appendix-a-technical-specifications',
        'appendix-b-simulation-environments'
      ],
    }
  ],
};

export default sidebars;
