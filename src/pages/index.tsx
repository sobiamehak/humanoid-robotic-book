
import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';

export default function HomePage() {
  return (
    <Layout title="Physical AI & Humanoid Robotics Textbook">
      {/* Hero Section */}
      <div style={styles.hero}>
        <div style={styles.heroOverlay} />
        <div style={styles.heroContent}>
          <h1 style={styles.heroTitle}>
            🤖 Physical AI <br />& Humanoid Robotics
          </h1>
          <p style={styles.heroSubtitle}>
            Where AI meets the physical world — building intelligent machines that move, think, and collaborate with humans.
          </p>
          <Link to="/docs/chapter-01-introduction" style={styles.heroCta}>
            Start Learning 🚀
          </Link>
        </div>
      </div>

      {/* Main Content */}
      <div style={styles.container}>
        <main style={styles.main}>
          {/* Core Pillars - Horizontal */}
          <section style={styles.pillars}>
            <h2 style={styles.sectionTitle}>Core Pillars</h2>
            <div style={styles.pillarsHorizontal}>
              {pillars.map((pillar, i) => (
                <div key={i} style={styles.pillarItem}>
                  <span style={styles.pillarIcon}>{pillar.icon}</span>
                  <span style={styles.pillarLabel}>{pillar.title}</span>
                  {i < pillars.length - 1 && <span style={styles.separator}>•</span>}
                </div>
              ))}
            </div>
          </section>

          {/* What You'll Learn */}
          <section style={styles.learning}>
            <h2 style={styles.sectionTitle}>What You'll Learn</h2>
            <ul style={styles.learningList}>
              {topics.map((topic, i) => (
                <li key={i} style={styles.learningItem}>
                  {topic}
                </li>
              ))}
            </ul>
          </section>

          {/* Author & CTA */}
          <section style={styles.footerSection}>
            <p style={styles.authorText}>
              Created with passion by <strong style={{ color: '#4f46e5' }}>Sobia Mehak</strong>
            </p>
            <Link to="/docs/chapter-01-introduction" style={styles.finalCta}>
              Begin Your Journey 📖
            </Link>
          </section>
        </main>
      </div>

      {/* Global CSS with Animations - Fully Responsive */}
      <style>{`
        @keyframes fadeUp {
          from {
            opacity: 0;
            transform: translateY(30px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        @keyframes scaleIn {
          from {
            opacity: 0;
            transform: scale(0.9);
          }
          to {
            opacity: 1;
            transform: scale(1);
          }
        }

        .pillar-item {
          opacity: 0;
          animation: fadeUp 0.8s ease-out forwards;
        }

        .pillar-item:nth-child(1) { animation-delay: 0.2s; }
        .pillar-item:nth-child(2) { animation-delay: 0.4s; }
        .pillar-item:nth-child(3) { animation-delay: 0.6s; }
        .pillar-item:nth-child(4) { animation-delay: 0.8s; }
        .pillar-item:nth-child(5) { animation-delay: 1.0s; }

        .topic-item {
          opacity: 0;
          animation: scaleIn 0.6s ease-out forwards;
        }

        .topic-item:nth-child(1) { animation-delay: 0.1s; }
        .topic-item:nth-child(2) { animation-delay: 0.2s; }
        .topic-item:nth-child(3) { animation-delay: 0.3s; }
        .topic-item:nth-child(4) { animation-delay: 0.4s; }
        .topic-item:nth-child(5) { animation-delay: 0.5s; }
        .topic-item:nth-child(6) { animation-delay: 0.6s; }
        .topic-item:nth-child(7) { animation-delay: 0.7s; }

        /* Hover effects */
        a:hover, button:hover {
          transform: translateY(-4px);
          box-shadow: 0 20px 40px rgba(99, 102, 241, 0.3);
        }

        @media (max-width: 768px) {
          .hero-title {
            font-size: 3rem !important;
          }
          .hero-subtitle {
            font-size: 1.2rem !important;
          }
          .pillars-horizontal {
            flex-direction: column;
            gap: 20px !important;
          }
          .separator {
            display: none !important;
          }
          .section-title {
            font-size: 2.2rem !important;
          }
          .learning-list {
            grid-template-columns: 1fr !important;
          }
        }

        @media (max-width: 480px) {
          .hero-title {
            font-size: 2.5rem !important;
          }
          .hero-cta, .final-cta {
            padding: 16px 36px !important;
            font-size: 1.2rem !important;
          }
        }
      `}</style>
    </Layout>
  );
}

const pillars = [
  { icon: '🎯', title: 'Perception' },
  { icon: '🧠', title: 'Cognition' },
  { icon: '🏃', title: 'Action' },
  { icon: '🏗️', title: 'Embodiment' },
];

const topics = [
  'Foundations of Physical AI',
  'Robot Operating System (ROS 2)',
  'Humanoid hardware & sensors',
  'Motion planning & control',
  'Machine learning for robotics',
  'Real-world applications',
  'Ethics & future impact',
];

const styles: { [key: string]: React.CSSProperties } = {
  hero: {
    position: 'relative',
    height: '85vh',
    minHeight: '600px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    background: 'linear-gradient(135deg, #1e293b 0%, #4338ca 50%, #6366f1 100%)',
    overflow: 'hidden',
  },
  heroOverlay: {
    position: 'absolute',
    inset: 0,
    background: 'rgba(0,0,0,0.35)',
  },
  heroContent: {
    position: 'relative',
    textAlign: 'center',
    maxWidth: '800px',
    padding: '0 24px',
    color: 'white',
    zIndex: 1,
  },
  heroTitle: {
    fontSize: '4.5rem',
    fontWeight: 900,
    lineHeight: 1.1,
    marginBottom: '24px',
    textShadow: '0 4px 30px rgba(0,0,0,0.5)',
  },
  heroSubtitle: {
    fontSize: '1.5rem',
    marginBottom: '40px',
    opacity: 0.95,
    lineHeight: 1.6,
  },
  heroCta: {
    background: 'white',
    color: '#4338ca',
    padding: '18px 44px',
    borderRadius: '50px',
    fontSize: '1.4rem',
    fontWeight: 'bold',
    textDecoration: 'none',
    boxShadow: '0 12px 40px rgba(0,0,0,0.3)',
    transition: 'all 0.3s ease',
    display: 'inline-block',
  },

  container: {
    padding: '100px 20px 80px',
    background: '#f8fafc',
  },
  main: {
    maxWidth: '1100px',
    margin: '0 auto',
  },
  sectionTitle: {
    fontSize: '2.8rem',
    textAlign: 'center',
    marginBottom: '60px',
    color: '#1e293b',
    fontWeight: 800,
  },

  // Pillars
  pillars: { marginBottom: '100px' },
  pillarsHorizontal: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    flexWrap: 'wrap',
    gap: '40px',
    fontSize: '1.8rem',
    color: '#475569',
  },
  pillarItem: {
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
  },
  pillarIcon: {
    fontSize: '2.2rem',
  },
  pillarLabel: {
    fontWeight: 600,
    color: '#1e293b',
  },
  separator: {
    color: '#94a3b8',
    fontSize: '2rem',
    margin: '0 20px',
  },

  // Learning
  learning: { marginBottom: '100px' },
  learningList: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
    gap: '20px',
    padding: 0,
    listStyle: 'none',
  },
  learningItem: {
    background: 'white',
    padding: '20px 28px',
    borderRadius: '16px',
    fontSize: '1.2rem',
    color: '#475569',
    boxShadow: '0 6px 20px rgba(0,0,0,0.05)',
    borderLeft: '4px solid #6366f1',
  },

  // Footer CTA
  footerSection: {
    textAlign: 'center',
    padding: '80px 0',
    background: 'linear-gradient(135deg, #eef2ff 0%, #e0e7ff 100%)',
    borderRadius: '32px',
  },
  authorText: {
    fontSize: '1.3rem',
    marginBottom: '32px',
    color: '#475569',
  },
  finalCta: {
    background: 'linear-gradient(135deg, #4f46e5 0%, #6366f1 100%)',
    color: 'white',
    padding: '20px 50px',
    borderRadius: '50px',
    fontSize: '1.5rem',
    fontWeight: 'bold',
    textDecoration: 'none',
    boxShadow: '0 12px 35px rgba(99,102,241,0.4)',
    transition: 'all 0.3s ease',
    display: 'inline-block',
  },
};