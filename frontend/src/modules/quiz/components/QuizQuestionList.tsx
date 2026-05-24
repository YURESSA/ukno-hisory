import { useGetQuizQuestionsQuery, useDeleteQuizQuestionMutation } from '../api/quizApi';

export const QuizQuestionList = () => {
  const { data: questions, isLoading } = useGetQuizQuestionsQuery();
  const [deleteQuestion] = useDeleteQuizQuestionMutation();

  if (isLoading) return <div>Загрузка вопросов...</div>;

  const handleDelete = async (id: number) => {
    if (window.confirm('Вы уверены, что хотите удалить этот вопрос?')) {
      await deleteQuestion(id);
    }
  };

  return (
    <div>
      <h3>Список вопросов квиза</h3>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
        {questions?.map((q) => (
          <div key={q.id} style={{ padding: '15px', border: '1px solid #eee', borderRadius: '8px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <strong>{q.question}</strong>
              <button 
                onClick={() => handleDelete(q.id)}
                style={{ background: '#ff4d4f', color: 'white', border: 'none', padding: '4px 8px', borderRadius: '4px', cursor: 'pointer' }}
              >
                Удалить
              </button>
            </div>
            {q.image_url && (
              <img 
                src={`${import.meta.env.VITE_API_URL.replace('/api/v1', '')}${q.image_url}`} 
                alt="Вопрос" 
                style={{ maxWidth: '200px', marginTop: '10px' }} 
              />
            )}
            <ul style={{ marginTop: '10px' }}>
              {q.options.map((opt, i) => (
                <li key={i} style={{ color: opt.is_correct ? 'green' : 'inherit' }}>
                  {opt.text} {opt.is_correct && '✓'}
                </li>
              ))}
            </ul>
            {q.explanation && (
              <p style={{ fontSize: '12px', color: '#666', marginTop: '10px' }}>
                <em>Объяснение:</em> {q.explanation}
              </p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
