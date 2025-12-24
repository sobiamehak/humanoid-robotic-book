import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';

// Landing page that serves as the homepage and redirects to the intro content
export default function HomePage() {
  return (
    <Layout title="Physical AI & Humanoid Robotics Textbook">
      <div style={styles.container}>
        <main>
          <section style={styles.section}>
            <h1 style={styles.title}>
              🤖 Welcome to the Physical AI & Humanoid Robotics Textbook
            </h1>

            <p style={styles.subtitle}>
              This textbook is designed to introduce learners to the future of robotics —
              a world where <strong style={{color: '#667eea'}}>AI, machines, and humans work together</strong>.
            </p>

            <div style={styles.contentBlock}>
              <h2 style={styles.sectionTitle}>🧠 What is Physical AI & Humanoid Robotics?</h2>
              <p style={styles.paragraph}>
                <strong style={{color: '#667eea'}}>Physical AI</strong> represents the convergence of artificial intelligence with the physical world, focusing on how machines can perceive, reason, and interact with their tangible environment. Unlike traditional AI that operates primarily in digital domains, Physical AI integrates sensing, computation, and actuation to enable robots to navigate, manipulate, and interact with the physical world intelligently.
              </p>

              <p style={styles.paragraph}>
                <strong style={{color: '#667eea'}}>Humanoid Robotics</strong> is a specialized field focused on creating robots with human-like characteristics and capabilities. These robots often feature:
              </p>

              <ul style={styles.list}>
                <li style={styles.listItem}>Human-like form and movement patterns</li>
                <li style={styles.listItem}>Bipedal locomotion and dexterous manipulation</li>
                <li style={styles.listItem}>Advanced perception systems for human environments</li>
                <li style={styles.listItem}>Social interaction capabilities</li>
              </ul>
            </div>

            <div style={styles.contentBlock}>
              <h2 style={styles.sectionTitle}>🏗️ Core Pillars of Physical AI & Humanoid Robotics</h2>

              <h3 style={styles.subsectionTitle}>🎯 1. Perception</h3>
              <p style={styles.paragraph}>Humanoid robots must understand their environment through:</p>
              <ul style={styles.list}>
                <li style={styles.listItem}>Visual processing (computer vision)</li>
                <li style={styles.listItem}>Spatial awareness (LiDAR, depth sensors)</li>
                <li style={styles.listItem}>Tactile feedback (touch sensors)</li>
                <li style={styles.listItem}>Audio processing (speech recognition)</li>
              </ul>

              <h3 style={styles.subsectionTitle}>🧠 2. Cognition</h3>
              <p style={styles.paragraph}>The "brain" of the robot processes information to:</p>
              <ul style={styles.list}>
                <li style={styles.listItem}>Plan actions and movements</li>
                <li style={styles.listItem}>Learn from experiences</li>
                <li style={styles.listItem}>Make real-time decisions</li>
                <li style={styles.listItem}>Adapt to changing environments</li>
              </ul>

              <h3 style={styles.subsectionTitle}>🏃 3. Action</h3>
              <p style={styles.paragraph}>Physical execution of tasks through:</p>
              <ul style={styles.list}>
                <li style={styles.listItem}>Precise motor control</li>
                <li style={styles.listItem}>Balance and locomotion systems</li>
                <li style={styles.listItem}>Manipulation and grasping</li>
                <li style={styles.listItem}>Safe human interaction</li>
              </ul>

              <h3 style={styles.subsectionTitle}>🏗️ 4. Embodiment</h3>
              <p style={styles.paragraph}>The physical form factor and integration:</p>
              <ul style={styles.list}>
                <li style={styles.listItem}>Mechanical design and kinematics</li>
                <li style={styles.listItem}>Sensor and actuator placement</li>
                <li style={styles.listItem}>Power systems and mobility</li>
                <li style={styles.listItem}>Human-centered design</li>
              </ul>
            </div>

            <div style={styles.contentBlock}>
              <h2 style={styles.sectionTitle}>✍️ About the Author</h2>
              <p style={styles.paragraph}>
                This textbook is thoughtfully created and organized by <strong style={{color: '#667eea'}}>Sobia Mehak</strong>,
                whose passion for learning, teaching, and modern technology inspired the making of this resource.
                Her dedication reflects in every chapter — making robotics easier, clearer, and exciting for learners.
              </p>
            </div>

            <div style={styles.contentBlock}>
              <h2 style={styles.sectionTitle}>🚀 What You Will Learn</h2>
              <ul style={styles.list}>
                <li style={styles.listItem}>Foundations of Physical AI</li>
                <li style={styles.listItem}>Robot Operating System (ROS 2)</li>
                <li style={styles.listItem}>Humanoid robot hardware & sensors</li>
                <li style={styles.listItem}>Motion planning & control</li>
                <li style={styles.listItem}>Machine learning for robotics</li>
                <li style={styles.listItem}>Practical applications</li>
                <li style={styles.listItem}>Ethical and future considerations</li>
              </ul>
            </div>

            <div style={styles.contentBlock}>
              <h2 style={styles.sectionTitle}>📘 How to Navigate This Book</h2>
              <p style={styles.paragraph}>
                Start with <strong style={{color: '#667eea'}}>Module 1</strong> for foundational concepts,
                progress through <strong style={{color: '#667eea'}}>Core Concepts</strong>,
                learn advanced intelligence in <strong style={{color: '#667eea'}}>Module 3</strong>,
                and explore real-world applications in <strong style={{color: '#667eea'}}>Module 4</strong>.
              </p>
            </div>

            <div style={styles.contentBlock}>
              <h2 style={styles.sectionTitle}>🦾 Transforming Industries</h2>
              <p style={styles.paragraph}>
                Humanoid robots are transforming industries:
                healthcare, education, manufacturing, security, and home automation.
              </p>
              <p style={styles.paragraph}>
                This book prepares you for <strong style={{color: '#667eea'}}>the next generation of robotics engineers and AI innovators</strong>.
              </p>
            </div>

            <div style={styles.ctaContainer}>
              <Link
                to="/docs/chapter-01-introduction"
                style={styles.ctaButton}
                onMouseEnter={(e) => {
                  const target = e.target as HTMLElement;
                  target.style.transform = 'translateY(-5px)';
                  target.style.boxShadow = '0 12px 30px rgba(102, 126, 234, 0.5)';
                }}
                onMouseLeave={(e) => {
                  const target = e.target as HTMLElement;
                  target.style.transform = 'translateY(0)';
                  target.style.boxShadow = '0 8px 25px rgba(102, 126, 234, 0.4)';
                }}
              >
                📖 Start Your Learning Journey
              </Link>
            </div>
          </section>
        </main>
      </div>
    </Layout>
  );
}

const styles = {
  container: {
    padding: '40px 20px',
    background: 'linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%)',
    minHeight: '100vh',
    fontFamily: 'system-ui, -apple-system, sans-serif'
  },
  section: {
    maxWidth: '900px',
    margin: '0 auto',
    padding: '40px',
    backgroundColor: 'white',
    borderRadius: '20px',
    boxShadow: '0 10px 30px rgba(102, 126, 234, 0.15)',
    backdropFilter: 'blur(10px)',
    border: '1px solid rgba(102, 126, 234, 0.1)',
  },
  title: {
    textAlign: 'center' as const,
    fontSize: '2.8rem',
    marginBottom: '20px',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    WebkitBackgroundClip: 'text' as const,
    WebkitTextFillColor: 'transparent',
    fontWeight: '800' as const,
    lineHeight: '1.2',
  },
  subtitle: {
    fontSize: '1.3rem',
    lineHeight: '1.7',
    marginBottom: '40px',
    color: '#555',
    textAlign: 'center' as const,
    padding: '25px',
    backgroundColor: '#f8f9ff',
    borderRadius: '15px',
    border: '1px solid rgba(102, 126, 234, 0.1)',
    boxShadow: '0 4px 15px rgba(102, 126, 234, 0.08)',
  },
  contentBlock: {
    marginBottom: '35px',
    padding: '25px',
    borderRadius: '16px',
    border: '1px solid rgba(102, 126, 234, 0.1)',
    backgroundColor: '#f8f9ff',
    boxShadow: '0 4px 15px rgba(102, 126, 234, 0.08)',
    position: 'relative' as const,
    overflow: 'hidden',
  },
  contentBlockBefore: {
    content: '""',
    position: 'absolute' as const,
    top: 0,
    left: 0,
    height: '4px',
    width: '100%',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
  },
  sectionTitle: {
    fontSize: '1.9rem',
    marginBottom: '20px',
    color: '#667eea',
    fontWeight: '700' as const,
    position: 'relative' as const,
    display: 'inline-block',
    paddingBottom: '12px',
  },
  sectionTitleAfter: {
    content: '""',
    position: 'absolute' as const,
    bottom: 0,
    left: 0,
    width: '60px',
    height: '3px',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    borderRadius: '2px',
  },
  subsectionTitle: {
    fontSize: '1.5rem',
    marginBottom: '15px',
    color: '#667eea',
    marginTop: '25px',
    fontWeight: '600' as const,
    display: 'flex' as const,
    alignItems: 'center' as const,
  },
  paragraph: {
    fontSize: '1.15rem',
    lineHeight: '1.8',
    marginBottom: '18px',
    color: '#555',
    textAlign: 'justify' as const,
  },
  list: {
    paddingLeft: '25px',
    marginBottom: '20px',
    marginTop: '10px',
  },
  listItem: {
    fontSize: '1.15rem',
    marginBottom: '12px',
    color: '#555',
    lineHeight: '1.7',
    position: 'relative' as const,
  },
  listItemBefore: {
    content: '"•"',
    color: '#667eea',
    fontWeight: 'bold' as const,
    position: 'absolute' as const,
    left: '-20px',
  },
  ctaContainer: {
    textAlign: 'center' as const,
    marginTop: '50px',
    marginBottom: '20px',
    padding: '30px',
  },
  ctaButton: {
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    color: 'white',
    padding: '20px 40px',
    textDecoration: 'none',
    borderRadius: '35px',
    fontSize: '1.3rem',
    fontWeight: '700' as const,
    display: 'inline-block',
    transition: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
    boxShadow: '0 8px 25px rgba(102, 126, 234, 0.4)',
    border: 'none',
    cursor: 'pointer',
    position: 'relative' as const,
    overflow: 'hidden',
    zIndex: 1,
  },
  ctaButtonHover: {
    transform: 'translateY(-5px)',
    boxShadow: '0 12px 30px rgba(102, 126, 234, 0.5)',
  },
  ctaButtonBefore: {
    content: '""',
    position: 'absolute' as const,
    top: 0,
    left: 0,
    width: '100%',
    height: '100%',
    background: 'linear-gradient(135deg, #764ba2 0%, #667eea 100%)',
    zIndex: -1,
    transition: 'opacity 0.4s ease',
    opacity: 0,
  },
  ctaButtonHoverBefore: {
    opacity: 1,
  },
};