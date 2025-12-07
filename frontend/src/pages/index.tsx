import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';

import Heading from '@theme/Heading';
import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <div className="text--center">
          <div className="avatar avatar--vertical">
            <img
              className={clsx('avatar__photo', styles.avatarPhoto)}
              src="/img/logo.svg"
              alt="Humanoid Robotics Logo"
              style={{ width: '120px', height: '120px', objectFit: 'contain' }}
            />
          </div>
        </div>
        <Heading as="h1" className="hero__title">
          {siteConfig.title}
        </Heading>
        <p className="hero__subtitle">
          {siteConfig.tagline}
        </p>
        <p className="hero__description">
          The world's first AI-native textbook on Physical AI & Humanoid Robotics with personalized learning, Urdu translation, and interactive RAG chatbot.
        </p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/intro">
            📖 Start Reading - 5min ⏱️
          </Link>
          <Link
            className="button button--primary button--lg margin-left--sm"
            to="/docs/chapter-01-introduction">
            🚀 Jump to Chapter 1
          </Link>
        </div>
      </div>
    </header>
  );
}

function HomepageFeaturesSection() {
  return (
    <section className={styles.featuresSection}>
      <div className="container padding-horiz--xl">
        <div className="row">
          <div className="col col--4">
            <div className={clsx('card', styles.featureCard)}>
              <div className="card__header">
                <h3>🤖 Interactive Learning</h3>
              </div>
              <div className="card__body">
                <p>
                  Embedded RAG chatbot with full-book and selected-text query modes, providing answers with citations.
                </p>
              </div>
            </div>
          </div>
          <div className="col col--4">
            <div className={clsx('card', styles.featureCard)}>
              <div className="card__header">
                <h3>🌍 Multilingual Support</h3>
              </div>
              <div className="card__body">
                <p>
                  Real-time Urdu translation with the "اردو میں ترجمہ کریں" button for enhanced accessibility.
                </p>
              </div>
            </div>
          </div>
          <div className="col col--4">
            <div className={clsx('card', styles.featureCard)}>
              <div className="card__header">
                <h3>👤 Personalized Content</h3>
              </div>
              <div className="card__body">
                <p>
                  Content adapts dynamically based on user profile with the "Personalize this chapter" feature.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Welcome - ${siteConfig.title}`}
      description="AI-Native Textbook on Physical AI & Humanoid Robotics">
      <HomepageHeader />
      <main>
        <HomepageFeaturesSection />
        <section className={styles.aboutSection}>
          <div className="container padding-horiz--xl">
            <div className="row">
              <div className="col col--6">
                <Heading as="h2">About This Textbook</Heading>
                <p>
                  This comprehensive textbook covers all aspects of humanoid robotics from fundamentals to advanced topics.
                  Designed for undergraduate & graduate students in CS, Robotics, AI, and Electrical Engineering, as well as
                  professionals transitioning to Physical AI & Humanoid Robotics.
                </p>
                <p>
                  The curriculum follows the official 4-module syllabus covering:
                </p>
                <ul>
                  <li><strong>Module 1:</strong> The Robotic Nervous System (ROS 2)</li>
                  <li><strong>Module 2:</strong> The Digital Twin (Gazebo & Unity)</li>
                  <li><strong>Module 3:</strong> The AI-Robot Brain (NVIDIA Isaac)</li>
                  <li><strong>Module 4:</strong> Vision-Language-Action (VLA) & Humanoid Mastery</li>
                </ul>
              </div>
              <div className="col col--6">
                <Heading as="h2">Key Features</Heading>
                <div className={clsx('card', styles.keyFeaturesCard)}>
                  <div className="card__body">
                    <ul className={styles.featureList}>
                      <li>✓ 13 Comprehensive Chapters + 2 Appendices</li>
                      <li>✓ Theory, Code, Simulation, and Exercises</li>
                      <li>✓ Interactive RAG Chatbot with Citations</li>
                      <li>✓ User Authentication & Profiling</li>
                      <li>✓ Personalized Content Adaptation</li>
                      <li>✓ Real-time Urdu Translation</li>
                      <li>✓ Complete Simulation Environments</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}