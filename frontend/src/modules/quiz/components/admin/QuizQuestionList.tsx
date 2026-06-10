import { useState } from 'react';
import { IconButton, CircularProgress, Tooltip, Box, Typography } from '@mui/material';
import { 
  Delete as DeleteIcon, 
  HelpOutlined as QuestionIcon, 
  CheckCircleOutlined as CorrectIcon,
  Edit as EditIcon
} from '@mui/icons-material';
import { useGetQuizQuestionsQuery, useDeleteQuizQuestionMutation } from '../../api/quizApi';
import { resolveBackendUrl } from '@/config/env';
import styles from '@/styles/admin.module.css';
import { EditQuizQuestionModal } from './EditQuizQuestionModal';

export const QuizQuestionList = () => {
  const { data: questions, isLoading, error } = useGetQuizQuestionsQuery();
  const [deleteQuestion] = useDeleteQuizQuestionMutation();
  
  const [editingId, setEditingId] = useState<number | null>(null);

  if (isLoading) return (
    <div className={`${styles['adm-card']} ${styles['adm-flex-center']}`} style={{ minHeight: '300px' }}>
      <CircularProgress sx={{ color: 'var(--primary-color)' }} />
    </div>
  );

  if (error) return (
    <div className={styles['adm-card']}>
      <Typography sx={{ color: 'var(--error-color)' }}>Ошибка загрузки вопросов</Typography>
    </div>
  );

  const handleDelete = async (id: number) => {
    if (window.confirm('Вы уверены, что хотите удалить этот вопрос?')) {
      await deleteQuestion(id);
    }
  };

  return (
    <div className={styles['adm-quiz-list']}>
      <h3 className={styles['adm-title']} style={{ paddingLeft: '10px' }}>
        <QuestionIcon sx={{ color: 'var(--primary-color)' }} />
        Список вопросов квиза
      </h3>
      
      <div className={styles['adm-flex-column']}>
        {questions?.map((q) => (
          <div key={q.id} className={styles['adm-card']}>
            <div className={styles['adm-flex-between-start']}>
              <Typography className={styles['adm-quiz-q-text']}>{q.question}</Typography>
              <div className={styles['adm-flex-gap-4']}>
                <Tooltip title="Редактировать">
                  <IconButton 
                    onClick={() => setEditingId(q.id)}
                    sx={{ color: 'var(--primary-color)' }}
                  >
                    <EditIcon />
                  </IconButton>
                </Tooltip>
                <Tooltip title="Удалить">
                  <IconButton 
                    onClick={() => handleDelete(q.id)}
                    sx={{ color: 'var(--error-color)' }}
                  >
                    <DeleteIcon />
                  </IconButton>
                </Tooltip>
              </div>
            </div>
            
            {q.image && (
              <div className={styles['adm-mt-15']}>
                <img 
                  src={resolveBackendUrl(q.image)} 
                  alt="Вопрос" 
                  className={styles['adm-img-200']}
                />
              </div>
            )}

            <div className={styles['adm-mt-20']}>
              <div className={styles['adm-label']}>Варианты ответов:</div>
              {q.options.map((opt, i) => (
                <div key={i} className={`${styles['adm-quiz-option-row']} ${opt.is_correct ? styles['is-correct'] : ''}`}>
                  {opt.is_correct ? (
                    <CorrectIcon sx={{ color: 'var(--success-color)', fontSize: 20 }} />
                  ) : (
                    <Box sx={{ width: 20 }} />
                  )}
                  <Typography variant="body2">{opt.text}</Typography>
                </div>
              ))}
            </div>

            {q.explanation && (
              <div className={styles['adm-quiz-explanation']}>
                <strong>Объяснение:</strong> {q.explanation}
              </div>
            )}
          </div>
        ))}

        {questions?.length === 0 && (
          <div className={`${styles['adm-card']} ${styles['adm-empty-centered']}`}>
            Вопросов пока нет
          </div>
        )}
      </div>

      {editingId && (
        <EditQuizQuestionModal 
          questionId={editingId}
          isOpen={true}
          onClose={() => setEditingId(null)}
        />
      )}
    </div>
  );
};
