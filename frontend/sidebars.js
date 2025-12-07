// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  // By default, Docusaurus generates a sidebar from the docs folder structure
  textbookSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Module 1: Foundations',
      items: [
        'chapter-01-introduction',
        'chapter-02-the-robotic-nervous-system-ros2'
      ],
      collapsed: false
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
      collapsed: false
    },
    {
      type: 'category',
      label: 'Module 3: Intelligence & Learning',
      items: [
        'chapter-08-learning',
        'chapter-09-cognition'
      ],
      collapsed: false
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
      collapsed: false
    },
    {
      type: 'category',
      label: 'Appendices',
      items: [
        'appendix-a-technical-specifications',
        'appendix-b-simulation-environments'
      ],
      collapsed: false
    }
  ],
};

module.exports = sidebars;