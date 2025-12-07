/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'An AI-Native Textbook',
  url: 'https://your-org.github.io',
  baseUrl: '/humanoid-robotic-book/',
  onBrokenLinks: 'ignore',
  onBrokenMarkdownLinks: 'ignore',
  favicon: 'img/docusaurus.ico',
  organizationName: 'your-org',
  projectName: 'humanoid-robotic-book',
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'ur'],
    localeConfigs: {
      en: {
        label: 'English',
        direction: 'ltr',
      },
      ur: {
        label: 'اردو',
        direction: 'rtl',
      },
    },
  },
  presets: [
    [
      '@docusaurus/preset-classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          path: '../docs',
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl: 'https://github.com/your-org/humanoid-robotic-book/tree/main/',
        },
        blog: {
          showReadingTime: true,
          editUrl: 'https://github.com/your-org/humanoid-robotic-book/tree/main/',
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      navbar: {
        title: 'Physical AI & Humanoid Robotics',
        style: 'dark',
        items: [
          {
            type: 'doc',
            docId: 'intro',
            position: 'left',
            label: '📚 Textbook',
          },
          {
            to: '/docs/chapter-01-introduction',
            label: '📖 Chapters',
            position: 'left',
          },
          {
            type: 'custom-LanguageSwitcher',
            position: 'right',
            className: 'language-switcher',
          },
          {
            type: 'custom-ChatbotButton',
            position: 'right',
            className: 'chatbot-button',
          },
          {
            href: 'https://github.com/your-org/humanoid-robotic-book',
            label: '🐙 GitHub',
            position: 'right',
          },
          {
            href: 'https://panaversity.org',
            label: '🌐 Panaversity',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: '📚 Textbook',
            items: [
              {
                label: 'Chapter 1: Introduction',
                to: '/docs/chapter-01-introduction',
              },
              {
                label: 'All Chapters',
                to: '/docs/category/module-1-foundations',
              },
            ],
          },
          {
            title: '🎓 Academic',
            items: [
              {
                label: 'Panaversity',
                href: 'https://panaversity.org',
              },
              {
                label: 'GIAIC',
                href: 'https://www.giaic.io',
              },
              {
                label: 'PIAIC',
                href: 'https://www.piaic.org',
              },
            ],
          },
          {
            title: '🔗 Resources',
            items: [
              {
                label: 'GitHub Repo',
                href: 'https://github.com/your-org/humanoid-robotic-book',
              },
              {
                label: 'Issue Tracker',
                href: 'https://github.com/your-org/humanoid-robotic-book/issues',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics Textbook. An AI-Native Educational Resource.`,
      },
      prism: {
        theme: require('prism-react-renderer/themes/github'),
        darkTheme: require('prism-react-renderer/themes/dracula'),
      },
    }),
};

module.exports = config;
