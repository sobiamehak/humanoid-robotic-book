import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import styles from './styles.module.css';

const FeatureList = [
  {
    title: 'AI-Native Learning',
    description: (
      <>
        Experience the world's first AI-native textbook with embedded RAG chatbot,
        personalization, and Urdu translation capabilities for enhanced learning.
      </>
    ),
  },
  {
    title: 'Hands-On Robotics',
    description: (
      <>
        Learn practical humanoid robotics through interactive chapters,
        Python/ROS 2 code examples, and simulation environments.
      </>
    ),
  },
  {
    title: 'Cutting-Edge Content',
    description: (
      <>
        Stay current with the latest developments in Physical AI,
        NVIDIA Isaac, ROS 2, and humanoid platforms.
      </>
    ),
  },
];

function Feature({Svg, title, description}) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <div className={styles.featureSvg}>
          <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M12 4.5v15m7.5-7.5h-15"></path>
          </svg>
        </div>
      </div>
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}