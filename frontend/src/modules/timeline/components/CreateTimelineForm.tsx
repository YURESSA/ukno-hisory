import { useForm } from 'react-hook-form';
import { useCreateTimelineMutation } from '../api/timelineApi';

export const CreateTimelineForm = () => {
  const { register, handleSubmit, reset } = useForm();
  const [createTimeline, { isLoading }] = useCreateTimelineMutation();

  const onSubmit = async (data: any) => {
    const formData = new FormData();
    formData.append('year', data.year);
    formData.append('text', data.text);
    
    if (data.image?.[0]) {
      formData.append('image', data.image[0]);
    }

    try {
      await createTimeline(formData).unwrap();
      alert('Событие добавлено в таймлайн!');
      reset();
    } catch (e) {
      console.error('Ошибка при создании:', e);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} style={{ display: 'flex', flexDirection: 'column', gap: '10px', maxWidth: '400px', padding: '20px', border: '1px solid #ccc' }}>
      <h3>Добавить событие</h3>
      <input type="number" {...register('year')} placeholder="Год" required />
      <textarea {...register('text')} placeholder="Описание события" required />
      
      <label>Изображение: 
        <input type="file" {...register('image')} accept="image/*" required />
      </label>

      <button type="submit" disabled={isLoading}>
        {isLoading ? 'Сохранение...' : 'Добавить'}
      </button>
    </form>
  );
};
