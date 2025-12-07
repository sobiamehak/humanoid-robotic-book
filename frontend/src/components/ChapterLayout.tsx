import React, { useState, useEffect } from 'react';
import clsx from 'clsx';
import styles from './ChapterLayout.module.css';
import PersonalizeButton from './PersonalizeButton';
import UrduTranslateButton from './UrduTranslateButton';

type ChapterLayoutProps = {
  children: React.ReactNode;
  title: string;
  chapterId: string;
  userId?: string;
  theory?: string;
  codeBlock?: string;
  simulation?: string;
  exercises?: string;
};

const ChapterLayout: React.FC<ChapterLayoutProps> = ({
  children,
  title,
  chapterId,
  userId,
  theory,
  codeBlock,
  simulation,
  exercises
}) => {
  const [personalizedContent, setPersonalizedContent] = useState({
    theory: theory,
    codeBlock: codeBlock,
    simulation: simulation,
    exercises: exercises
  });
  const [isPersonalized, setIsPersonalized] = useState(false);
  const [isTranslated, setIsTranslated] = useState(false);

  // Reset to original content when changing chapters
  useEffect(() => {
    setPersonalizedContent({
      theory: theory,
      codeBlock: codeBlock,
      simulation: simulation,
      exercises: exercises
    });
    setIsPersonalized(false);
    setIsTranslated(false);
  }, [chapterId, theory, codeBlock, simulation, exercises]);

  const handlePersonalize = async () => {
    try {
      // In a real implementation, this would call the backend API to personalize content
      // For now, we'll simulate by appending a note to the content
      const personalizeContent = async (content: string | undefined) => {
        if (!content) return content;
        // Simulate API call with a delay
        await new Promise(resolve => setTimeout(resolve, 1000));
        return `${content}\n\n[Content personalized for user: ${userId || 'guest'}]`;
      };

      const personalizedTheory = await personalizeContent(theory);
      const personalizedCodeBlock = await personalizeContent(codeBlock);
      const personalizedSimulation = await personalizeContent(simulation);
      const personalizedExercises = await personalizeContent(exercises);

      setPersonalizedContent({
        theory: personalizedTheory,
        codeBlock: personalizedCodeBlock,
        simulation: personalizedSimulation,
        exercises: personalizedExercises
      });
      setIsPersonalized(true);
    } catch (error) {
      console.error('Error personalizing content:', error);
    }
  };

  const handleUrduTranslation = async () => {
    try {
      // In a real implementation, this would call the backend API for Urdu translation
      // For now, we'll simulate by replacing content with placeholder text
      const translateToUrdu = async (content: string | undefined) => {
        if (!content) return content;
        // Simulate API call with a delay
        await new Promise(resolve => setTimeout(resolve, 1000));
        return `[اردو ترجمہ: ${content.substring(0, Math.min(50, content.length))}...]`;
      };

      const urduTheory = await translateToUrdu(theory);
      const urduCodeBlock = await translateToUrdu(codeBlock);
      const urduSimulation = await translateToUrdu(simulation);
      const urduExercises = await translateToUrdu(exercises);

      setPersonalizedContent({
        theory: urduTheory,
        codeBlock: urduCodeBlock,
        simulation: urduSimulation,
        exercises: urduExercises
      });
      setIsTranslated(true);
    } catch (error) {
      console.error('Error translating content:', error);
    }
  };

  return (
    <div className={styles.chapterContainer}>
      <header className={styles.chapterHeader}>
        <h1 className={styles.chapterTitle}>{title}</h1>
        <div className={styles.chapterActions}>
          <PersonalizeButton
            onPersonalize={handlePersonalize}
            chapterId={chapterId}
            disabled={isPersonalized && !isTranslated}
          />
          <UrduTranslateButton
            onTranslate={handleUrduTranslation}
            chapterId={chapterId}
          />
        </div>
      </header>

      {children}

      {personalizedContent.theory && (
        <section className={styles.section}>
          <h2> Theory </h2>
          <div className={styles.theoryContent}>{personalizedContent.theory}</div>
        </section>
      )}

      {personalizedContent.codeBlock && (
        <section className={styles.section}>
          <h2> Code Implementation </h2>
          <pre className={styles.codeBlock}>
            <code>{personalizedContent.codeBlock}</code>
          </pre>
        </section>
      )}

      {personalizedContent.simulation && (
        <section className={styles.section}>
          <h2> Simulation </h2>
          <div className={styles.simulationContent}>{personalizedContent.simulation}</div>
        </section>
      )}

      {personalizedContent.exercises && (
        <section className={styles.section}>
          <h2> Exercises </h2>
          <div className={styles.exercisesContent}>{personalizedContent.exercises}</div>
        </section>
      )}
    </div>
  );
};

export default ChapterLayout;