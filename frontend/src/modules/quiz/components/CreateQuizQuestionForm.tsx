import { useForm, useFieldArray } from 'react-hook-form';
import { useCreateQuizQuestionMutation } from '../api/quizApi';

export const CreateQuizQuestionForm = () => {
  const { register, control, handleSubmit, reset } = useForm({
    defaultValues: {
      question: '',
      explanation: '',
      options: [
        { text: '', is_correct: false },
        { text: '', is_correct: false }
      ]
    }
  });

  const { fields, append, remove } = useFieldArray({
    control,
    name: 'options'
  });

  const [createQuestion, { isLoading }] = useCreateQuizQuestionMutation();

  const onSubmit = async (data: any) => {
    try {
      const formData = new FormData();
      formData.append('question', data.question);
      if (data.explanation) formData.append('explanation', data.explanation);
      
      // Бэкенд ожидает JSON-строку для options в multipart/form-data
      formData.append('options', JSON.stringify(data.options));
      
      if (data.image && data.image[0]) {
        formData.append('image', data.image[0]);
      }

      await createQuestion(formData).unwrap();
      reset();
      alert('Вопрос создан!');
    } catch (err) {
      console.error('Ошибка создания вопроса:', err);
      alert('Ошибка при создании вопроса');
    }
  };

  return (
    <div style={{ padding: '20px', border: '1px solid #ddd', borderRadius: '8px' }}>
      <h3>Создать вопрос квиза</h3>
      <form onSubmit={handleSubmit(onSubmit)} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
        <input {...register('question')} placeholder="Текст вопроса" required />
        <textarea {...register('explanation')} placeholder="Объяснение (необязательно)" />
        <input {...register('image')} type="file" accept="image/*" />

        <div>
          <h4>Варианты ответа:</h4>
          {fields.map((field, index) => (
            <div key={field.id} style={{ display: 'flex', gap: '10px', marginBottom: '10px' }}>
              <input 
                {...register(`options.${index}.text` as const)} 
                placeholder={`Вариант ${index + 1}`} 
                required 
                style={{ flex: 1 }}
              />
              <label>
                <input 
                  type="checkbox" 
                  {...register(`options.${index}.is_correct` as const)} 
                />
                Верный
              </label>
              <button type="button" onClick={() => remove(index)}>Удалить</button>
            </div>
          ))}
          <button type="button" onClick={() => append({ text: '', is_correct: false })}>
            Добавить вариант
          </button>
        </div>

        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Создание...' : 'Создать вопрос'}
        </button>
      </form>
    </div>
  );
};
