import { useState } from 'react';
import { IconButton, CircularProgress, Tooltip } from '@mui/material';
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
    <div className={styles['adm-card']} style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '300px' }}>
      <CircularProgress sx={{ color: 'var(--primary-color)' }} />
    </div>
  );

  if (error) return (
    <div className={styles['adm-card']}>
      <p style={{ color: 'var(--error-color)' }}>Ошибка загрузки вопросов</p>
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
      
      <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
        {questions?.map((q) => (
          <div key={q.id} className={styles['adm-card']}>
            <div className={styles['adm-list-header']} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
              <span className={styles['adm-quiz-q-text']} style={{ fontWeight: 700, fontSize: '1.1rem', color: 'var(--secondary-color)' }}>{q.question}</span>
              <div style={{ display: 'flex', gap: '4px' }}>
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
              <div style={{ margin: '15px 0' }}>
                <img 
                  src={resolveBackendUrl(q.image)} 
                  alt="Вопрос" 
                  className={styles['adm-image-preview']}
                  style={{ width: '200px', height: 'auto', borderRadius: '12px' }}
                />
              </div>
            )}

            <div style={{ marginTop: '20px' }}>
              <div className={styles['adm-label']}>Варианты ответов:</div>
              {q.options.map((opt, i) => (
                <div key={i} className={`${styles['adm-quiz-option-row']} ${opt.is_correct ? styles['is-correct'] : ''}`}>
                  {opt.is_correct ? (
                    <CorrectIcon sx={{ color: 'var(--success-color)', fontSize: 20 }} />
                  ) : (
                    <div style={{ width: 20 }} />
                  )}
                  <span>{opt.text}</span>
                </div>
              ))}
            </div>

            {q.explanation && (
              <div className={styles['adm-quiz-explanation']} style={{ 
                marginTop: '20px', 
                padding: '16px', 
                backgroundColor: 'var(--accent-color-2)', 
                borderRadius: '12px',
                borderLeft: '4px solid var(--primary-color)',
                fontSize: '0.95rem'
              }}>
                <strong>Объяснение:</strong> {q.explanation}
              </div>
            )}
          </div>
        ))}

        {questions?.length === 0 && (
          <div className={styles['adm-card']} style={{ textAlign: 'center', padding: '40px 0', color: '#999' }}>
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
