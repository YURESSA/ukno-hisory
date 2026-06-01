import { useState } from 'react';
import { PublicLayout } from '@/layouts/PublicLayout/PublicLayout';
import styles from '@/styles/quizPage.module.css';
import { useGetQuizQuestionsQuery } from '@/modules/quiz/api/quizApi';
import { resolveBackendUrl } from '@/config/env';

type Phase = 'start' | 'quiz' | 'results';

interface Answer {
  questionId: number;
  selectedOptionId: number;
  isCorrect: boolean;
}

export const QuizPage = () => {
  const { data: quiz = [], isLoading } = useGetQuizQuestionsQuery();

  const [phase, setPhase] = useState<Phase>('start');
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<Answer[]>([]);
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [revealed, setRevealed] = useState(false);

  const currentQuestion = quiz[currentIndex];
  const total = quiz.length;
  const score = answers.filter((a) => a.isCorrect).length;

  const handleStart = () => {
    setPhase('quiz');
    setCurrentIndex(0);
    setAnswers([]);
    setSelectedId(null);
    setRevealed(false);
  };

  const handleSelect = (optionId: number, isCorrect: boolean) => {
    if (revealed) return;
    setSelectedId(optionId);
    setRevealed(true);
    setAnswers((prev) => [
      ...prev,
      { questionId: currentQuestion.id, selectedOptionId: optionId, isCorrect },
    ]);
  };

  const handleNext = () => {
    if (currentIndex + 1 < total) {
      setCurrentIndex((i) => i + 1);
      setSelectedId(null);
      setRevealed(false);
    } else {
      setPhase('results');
    }
  };

  const handleRestart = () => {
    setPhase('start');
    setCurrentIndex(0);
    setAnswers([]);
    setSelectedId(null);
    setRevealed(false);
  };

  if (isLoading) {
    return (
      <PublicLayout>
        <section className={styles['hero-wrapper']}>
          <div className={styles['quiz-start-block']}>
            <img src="/image/quiz/quiz-hero-block.svg" alt="" className={styles['quiz-bg-img']} aria-hidden="true" />
            <div className={styles['quiz-loading']}>Загрузка...</div>
          </div>
        </section>
      </PublicLayout>
    );
  }

  if (phase === 'start') {
    return (
      <PublicLayout>
        <section className={styles['hero-wrapper']}>
          <div className={styles['quiz-start-block']}>
            <img src="/image/quiz/quiz-hero-block.svg" alt="" className={styles['quiz-bg-img']} aria-hidden="true" />
            <div className={styles['title']}>
              <h6>ЧКАЛОВСКИЙ</h6>
              <h6>РАЙОН</h6>
            </div>
            <div className={styles['quiz-start']}>
              <div className={styles['tags']}>
                <h6>ПРОЙТИ КВИЗ!</h6>
              </div>
              <div className={styles['quiz-title']}>
                <h5>ЗНАЕШЬ ЛИ ТЫ ЧКАЛОВСКИЙ РАЙОН?</h5>
              </div>
              <button className={styles['action-btn']} onClick={handleStart}>
                <span className={styles['text-small']}>Начать</span>
              </button>
            </div>
          </div>
        </section>
      </PublicLayout>
    );
  }

  if (phase === 'quiz' && currentQuestion) {
    const sortedOptions = [...currentQuestion.options].sort(
      (a, b) => (a.position ?? 0) - (b.position ?? 0)
    );

    return (
      <PublicLayout>
        <section className={styles['quiz-question-wrapper']}>
          <div className={styles['quiz-question-inner']}>

            <div className={styles['quiz-progress-bar']}>
              <div
                className={styles['quiz-progress-fill']}
                style={{ width: `${((currentIndex) / total) * 100}%` }}
              />
            </div>
            <p className={styles['quiz-progress-text']}>
              Вопрос {currentIndex + 1} из {total}
            </p>

            <div className={styles['quiz-question-layout']}>
              <div className={styles['quiz-vector']}>
                <img src="/image/quiz/quiz-vector.svg" alt="" />
              </div>
              {currentQuestion.image && (
                <div className={styles['quiz-question-img-wrap']}>
                  <img
                    src={resolveBackendUrl(currentQuestion.image)}
                    alt=""
                    className={styles['quiz-question-img']}
                  />
                </div>
              )}

              {/* Вопрос + варианты */}
              <div className={styles['quiz-question-content']}>
                <h4 className={styles['quiz-question-text']}>{currentQuestion.question}</h4>

                <div className={styles['quiz-options']}>
                  {sortedOptions.map((opt) => {
                    const isSelected = selectedId === opt.id;
                    let optClass = styles['quiz-option'];
                    if (revealed && isSelected) {
                      optClass += ' ' + (opt.is_correct ? styles['quiz-option--correct'] : styles['quiz-option--wrong']);
                    } else if (revealed && opt.is_correct) {
                      optClass += ' ' + styles['quiz-option--correct'];
                    }
                    return (
                      <button
                        key={opt.id}
                        className={optClass}
                        onClick={() => handleSelect(opt.id!, opt.is_correct)}
                        disabled={revealed}
                      >
                        {opt.text}
                      </button>
                    );
                  })}
                </div>

                {/* Пояснение */}
                {revealed && currentQuestion.explanation && (
                  <div className={styles['quiz-explanation']}>
                    <p>{currentQuestion.explanation}</p>
                  </div>
                )}

                {revealed && (
                  <button className={styles['action-btn']} onClick={handleNext}>
                    <span className={styles['text-small']}>
                      {currentIndex + 1 < total ? 'Следующий вопрос' : 'Завершить'}
                    </span>
                  </button>
                )}
              </div>
            </div>
          </div>
        </section>
      </PublicLayout>
    );
  }

  // ── РЕЗУЛЬТАТЫ ────────────────────────────────────────────────────────────
  return (
    <PublicLayout>
      <section className={styles['quiz-results-wrapper']}>
        <div className={styles['quiz-results-inner']}>
          <div className={styles['quiz-score-block']}>
            <p className={styles['quiz-score-label']}>Ваш результат</p>
            <p className={styles['quiz-score-number']}>{score} / {total}</p>
            <p className={styles['quiz-score-sub']}>
              {score === total
                ? 'Отлично! Вы всё знаете о Чкаловском районе!'
                : score >= total / 2
                ? 'Хороший результат! Есть куда расти.'
                : 'Стоит узнать район получше!'}
            </p>
            <button className={styles['action-btn']} onClick={handleRestart}>
              <span className={styles['text-small']}>Попробовать снова</span>
            </button>
          </div>

          {/* Разбор ответов */}
          <div className={styles['quiz-review']}>
            <h4 className={styles['quiz-review-title']}>Разбор вопросов</h4>
            {quiz.map((q, idx) => {
              const userAnswer = answers.find((a) => a.questionId === q.id);
              const correct = q.options.find((o) => o.is_correct);
              return (
                <div
                  key={q.id}
                  className={
                    styles['quiz-review-item'] +
                    ' ' +
                    (userAnswer?.isCorrect ? styles['quiz-review-item--correct'] : styles['quiz-review-item--wrong'])
                  }
                >
                  <p className={styles['quiz-review-q']}>
                    <span className={styles['quiz-review-num']}>{idx + 1}.</span> {q.question}
                  </p>
                  <p className={styles['quiz-review-answer']}>
                    Правильный ответ: <strong>{correct?.text}</strong>
                  </p>
                  {q.explanation && (
                    <p className={styles['quiz-review-explanation']}>{q.explanation}</p>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      </section>
    </PublicLayout>
  );
};
