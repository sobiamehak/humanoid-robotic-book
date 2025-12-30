import React, { useState } from 'react';
import clsx from 'clsx';
import styles from './ChatWidget.module.css';

interface SourceCitation {
  title: string;
  url: string;
}

interface SourceCitationsProps {
  sources: SourceCitation[];
}

const SourceCitations: React.FC<SourceCitationsProps> = ({ sources }) => {
  const [expanded, setExpanded] = useState(true);

  const toggleExpanded = () => {
    setExpanded(!expanded);
  };

  return (
    <div className={styles.sourcesSection}>
      <div
        className={clsx(styles.sourcesHeader, { [styles.collapsed]: !expanded })}
        onClick={toggleExpanded}
        aria-expanded={expanded}
      >
        Sources
      </div>
      {expanded && (
        <div className={styles.sourcesList}>
          {sources.map((source, index) => (
            <div key={index} className={styles.sourceItem}>
              <a
                href={source.url}
                className={styles.sourceLink}
                target="_blank"
                rel="noopener noreferrer"
              >
                {source.title}
              </a>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default SourceCitations;