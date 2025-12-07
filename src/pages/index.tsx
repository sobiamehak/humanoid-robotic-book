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
              👋 Welcome to the Physical AI & Humanoid Robotics Textbook
            </h1>

            <p style={styles.subtitle}>
              This textbook is designed to introduce learners to the future of robotics —
              a world where <strong>AI, machines, and humans work together</strong>.
            </p>

            <div style={styles.contentBlock}>
              <h2 style={styles.sectionTitle}>🤖 What is Physical AI & Humanoid Robotics?</h2>
              <p style={styles.paragraph}>
                <strong>Physical AI</strong> represents the convergence of artificial intelligence with the physical world, focusing on how machines can perceive, reason, and interact with their tangible environment. Unlike traditional AI that operates primarily in digital domains, Physical AI integrates sensing, computation, and actuation to enable robots to navigate, manipulate, and interact with the physical world intelligently.
              </p>

              <p style={styles.paragraph}>
                <strong>Humanoid Robotics</strong> is a specialized field focused on creating robots with human-like characteristics and capabilities. These robots often feature:
              </p>

              <ul style={styles.list}>
                <li style={styles.listItem}>Human-like form and movement patterns</li>
                <li style={styles.listItem}>Bipedal locomotion and dexterous manipulation</li>
                <li style={styles.listItem}>Advanced perception systems for human environments</li>
                <li style={styles.listItem}>Social interaction capabilities</li>
              </ul>
            </div>

            <div style={styles.contentBlock}>
              <h2 style={styles.sectionTitle}>🧠 Core Pillars of Physical AI & Humanoid Robotics</h2>

              <h3 style={styles.subsectionTitle}>1. Perception</h3>
              <p style={styles.paragraph}>Humanoid robots must understand their environment through:</p>
              <ul style={styles.list}>
                <li style={styles.listItem}>Visual processing (computer vision)</li>
                <li style={styles.listItem}>Spatial awareness (LiDAR, depth sensors)</li>
                <li style={styles.listItem}>Tactile feedback (touch sensors)</li>
                <li style={styles.listItem}>Audio processing (speech recognition)</li>
              </ul>

              <h3 style={styles.subsectionTitle}>2. Cognition</h3>
              <p style={styles.paragraph}>The "brain" of the robot processes information to:</p>
              <ul style={styles.list}>
                <li style={styles.listItem}>Plan actions and movements</li>
                <li style={styles.listItem}>Learn from experiences</li>
                <li style={styles.listItem}>Make real-time decisions</li>
                <li style={styles.listItem}>Adapt to changing environments</li>
              </ul>

              <h3 style={styles.subsectionTitle}>3. Action</h3>
              <p style={styles.paragraph}>Physical execution of tasks through:</p>
              <ul style={styles.list}>
                <li style={styles.listItem}>Precise motor control</li>
                <li style={styles.listItem}>Balance and locomotion systems</li>
                <li style={styles.listItem}>Manipulation and grasping</li>
                <li style={styles.listItem}>Safe human interaction</li>
              </ul>

              <h3 style={styles.subsectionTitle}>4. Embodiment</h3>
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
                This textbook is thoughtfully created and organized by <strong>Sobia Mehak</strong>,
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
              <h2 style={styles.sectionTitle}>📘 How to Use This Book</h2>
              <p style={styles.paragraph}>
                Start with <strong>Module 1</strong> for basics,
                move through <strong>Core Concepts</strong>,
                learn advanced intelligence in <strong>Module 3</strong>,
                and explore real-world applications in <strong>Module 4</strong>.
              </p>
            </div>

            <div style={styles.contentBlock}>
              <h2 style={styles.sectionTitle}>🦾 Why This Textbook Matters</h2>
              <p style={styles.paragraph}>
                Humanoid robots are transforming industries:
                healthcare, education, manufacturing, security, and home automation.
              </p>
              <p style={styles.paragraph}>
                This book prepares you for <strong>the next generation of robotics engineers and AI innovators</strong>.
              </p>
            </div>

            <div style={styles.ctaContainer}>
              <Link
                to="/docs/chapter-01-introduction"
                style={styles.ctaButton}
              >
                📖 Start Reading Chapter 1
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
    backgroundColor: '#f8f9fa',
    minHeight: '100vh',
    fontFamily: 'system-ui, -apple-system, sans-serif'
  },
  section: {
    maxWidth: '800px',
    margin: '0 auto',
    padding: '30px',
    backgroundColor: 'white',
    borderRadius: '10px',
    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
  },
  title: {
    textAlign: 'center' as const,
    fontSize: '2.5rem',
    marginBottom: '15px',
    color: '#2c3e50',
    fontWeight: 'bold' as const,
  },
  subtitle: {
    fontSize: '1.2rem',
    lineHeight: '1.6',
    marginBottom: '30px',
    color: '#34495e',
    textAlign: 'center' as const,
    padding: '15px',
    backgroundColor: '#ecf0f1',
    borderRadius: '8px',
  },
  contentBlock: {
    marginBottom: '30px',
    padding: '20px',
    borderRadius: '8px',
    borderLeft: '4px solid #3498db',
    backgroundColor: '#f8f9fa',
  },
  sectionTitle: {
    fontSize: '1.8rem',
    marginBottom: '15px',
    color: '#2c3e50',
    borderBottom: '2px solid #3498db',
    paddingBottom: '8px',
  },
  subsectionTitle: {
    fontSize: '1.4rem',
    marginBottom: '10px',
    color: '#34495e',
    marginTop: '20px',
  },
  paragraph: {
    fontSize: '1.1rem',
    lineHeight: '1.7',
    marginBottom: '15px',
    color: '#2c3e50',
  },
  list: {
    paddingLeft: '20px',
    marginBottom: '15px',
  },
  listItem: {
    fontSize: '1.1rem',
    marginBottom: '8px',
    color: '#34495e',
    lineHeight: '1.6',
  },
  ctaContainer: {
    textAlign: 'center' as const,
    marginTop: '40px',
    marginBottom: '10px',
    padding: '20px',
  },
  ctaButton: {
    backgroundColor: '#3498db',
    color: 'white',
    padding: '16px 32px',
    textDecoration: 'none',
    borderRadius: '30px',
    fontSize: '1.2rem',
    fontWeight: 'bold' as const,
    display: 'inline-block',
    transition: 'all 0.3s ease',
    boxShadow: '0 4px 6px rgba(52, 152, 219, 0.3)',
  },
  // Hover effect would need to be handled differently in actual implementation
};