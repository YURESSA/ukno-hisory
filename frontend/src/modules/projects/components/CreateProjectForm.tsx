import { useForm } from 'react-hook-form';
import { useCreateProjectMutation } from '../api/projectsApi';

export const CreateProjectForm = () => {
  const { register, handleSubmit, reset } = useForm();
  const [createProject, { isLoading }] = useCreateProjectMutation();

  const onSubmit = async (data: any) => {
    const formData = new FormData();
    
    // Добавляем текстовые поля согласно Swagger [cite: 2, 3]
    formData.append('title', data.title);
    formData.append('author', data.author);
    formData.append('short_description', data.short_description);
    formData.append('description', data.description);
    formData.append('year', data.year);
    formData.append('is_draft', String(data.is_draft));

    // Добавляем файл главной картинки [cite: 4]
    if (data.main_image?.[0]) {
      formData.append('main_image', data.main_image[0]);
    }

    try {
      await createProject(formData).unwrap();
      alert('Проект создан!');
      reset(); // Очистить форму
    } catch (e) {
      console.error('Ошибка при создании:', e);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} style={{ display: 'flex', flexDirection: 'column', gap: '10px', maxWidth: '400px', padding: '20px', border: '1px solid #ccc' }}>
      <h3>Создать проект</h3>
      <input {...register('title')} placeholder="Название проекта" required />
      <input {...register('author')} placeholder="Автор" />
      <textarea {...register('short_description')} placeholder="Краткое описание" />
      <input type="number" {...register('year')} placeholder="Год" />
      
      <label>
        <input type="checkbox" {...register('is_draft')} /> Черновик
      </label>

      <label>Главное изображение: 
        <input type="file" {...register('main_image')} accept="image/*" />
      </label>

      <button type="submit" disabled={isLoading}>
        {isLoading ? 'Сохранение...' : 'Создать проект'}
      </button>
    </form>
  );
};