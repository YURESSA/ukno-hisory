import { IconButton, CircularProgress } from '@mui/material';
import { Delete as DeleteIcon, HelpOutlined as QuestionIcon, CheckCircleOutlined as CorrectIcon } from '@mui/icons-material';
import { useGetQuizQuestionsQuery, useDeleteQuizQuestionMutation } from '../../api/quizApi';
import { resolveBackendUrl } from '@/config/env';

export const QuizQuestionList = () => {
  const { data: questions, isLoading, error } = useGetQuizQuestionsQuery();
  const [deleteQuestion] = useDeleteQuizQuestionMutation();

  if (isLoading) return (
    <div className="adm-card" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '300px' }}>
      <CircularProgress sx={{ color: 'var(--primary-color)' }} />
    </div>
  );

  if (error) return (
    <div className="adm-card">
      <p style={{ color: 'var(--error-color)' }}>Ошибка загрузки вопросов</p>
    </div>
  );

  const handleDelete = async (id: number) => {
    if (window.confirm('Вы уверены, что хотите удалить этот вопрос?')) {
      await deleteQuestion(id);
    }
  };

  return (
    <div className="adm-quiz-list">
      <h3 className="adm-title" style={{ paddingLeft: '10px' }}>
        <QuestionIcon sx={{ color: 'var(--primary-color)' }} />
        Список вопросов квиза
      </h3>
      
      <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
        {questions?.map((q) => (
          <div key={q.id} className="adm-card">
            <div className="adm-list-header">
              <span className="adm-quiz-q-text">{q.question}</span>
              <IconButton 
                onClick={() => handleDelete(q.id)}
                sx={{ color: 'var(--error-color)' }}
              >
                <DeleteIcon />
              </IconButton>
            </div>
            
            {q.image_url && (
              <div style={{ margin: '15px 0' }}>
                <img 
                  src={resolveBackendUrl(q.image_url)} 
                  alt="Вопрос" 
                  className="adm-image-preview"
                  style={{ width: '200px', height: 'auto', borderRadius: '12px' }}
                />
              </div>
            )}

            <div style={{ marginTop: '20px' }}>
              <div className="adm-label">Варианты ответов:</div>
              {q.options.map((opt, i) => (
                <div key={i} className={`adm-quiz-option-row ${opt.is_correct ? 'is-correct' : ''}`}>
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
              <div className="adm-quiz-explanation" style={{ 
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
          <div className="adm-card" style={{ textAlign: 'center', padding: '40px 0', color: '#999' }}>
            Вопросов пока нет
          </div>
        )}
      </div>
    </div>
  );
};
