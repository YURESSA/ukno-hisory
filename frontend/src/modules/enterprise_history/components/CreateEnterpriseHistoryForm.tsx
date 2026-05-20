import { useForm } from 'react-hook-form';
import { useCreateEnterpriseHistoryMutation } from '../api/enterpriseHistoryApi';

export const CreateEnterpriseHistoryForm = () => {
  const { register, handleSubmit, reset } = useForm();
  const [createHistory, { isLoading }] = useCreateEnterpriseHistoryMutation();

  const onSubmit = async (data: any) => {
    const formData = new FormData();
    formData.append('title', data.title);
    formData.append('general_subtitle', data.general_subtitle);
    formData.append('detail_subtitle', data.detail_subtitle);
    formData.append('short_description', data.short_description);
    formData.append('is_draft', String(data.is_draft));

    if (data.general_main_image?.[0]) {
      formData.append('general_main_image', data.general_main_image[0]);
    }
    if (data.detail_main_image?.[0]) {
      formData.append('detail_main_image', data.detail_main_image[0]);
    }

    try {
      await createHistory(formData).unwrap();
      alert('Запись создана!');
      reset();
    } catch (e) {
      console.error('Ошибка при создании:', e);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} style={{ display: 'flex', flexDirection: 'column', gap: '10px', maxWidth: '400px', padding: '20px', border: '1px solid #ccc' }}>
      <h3>Создать историю предприятия</h3>
      <input {...register('title')} placeholder="Заголовок" required />
      <input {...register('general_subtitle')} placeholder="Подзаголовок (общий)" />
      <input {...register('detail_subtitle')} placeholder="Подзаголовок (детальный)" />
      <textarea {...register('short_description')} placeholder="Краткое описание" />
      
      <label>
        <input type="checkbox" {...register('is_draft')} defaultChecked /> Черновик
      </label>

      <label>Общее изображение: 
        <input type="file" {...register('general_main_image')} accept="image/*" />
      </label>

      <label>Детальное изображение: 
        <input type="file" {...register('detail_main_image')} accept="image/*" />
      </label>

      <button type="submit" disabled={isLoading}>
        {isLoading ? 'Сохранение...' : 'Создать'}
      </button>
    </form>
  );
};
