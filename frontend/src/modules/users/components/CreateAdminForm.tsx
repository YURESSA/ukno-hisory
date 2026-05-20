import { useForm } from 'react-hook-form';
import { useCreateAdminMutation } from '../api/usersApi';

export const CreateAdminForm = () => {
  const { register, handleSubmit, reset } = useForm();
  const [createAdmin, { isLoading }] = useCreateAdminMutation();

  const onSubmit = async (data: any) => {
    try {
      await createAdmin({ email: data.email }).unwrap();
      alert('Приглашение отправлено! Администратор создан (пароль нужно сбросить через почту или задать вручную).');
      reset();
    } catch (e) {
      console.error('Ошибка при создании:', e);
      alert('Ошибка при создании администратора (возможно, у вас недостаточно прав)');
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} style={{ display: 'flex', flexDirection: 'column', gap: '10px', maxWidth: '400px', padding: '20px', border: '1px solid #ccc' }}>
      <h3>Создать администратора</h3>
      <p style={{ fontSize: '12px', color: '#666' }}>Только для супер-администраторов</p>
      <input type="email" {...register('email')} placeholder="Email нового админа" required />
      
      <button type="submit" disabled={isLoading}>
        {isLoading ? 'Сохранение...' : 'Добавить админа'}
      </button>
    </form>
  );
};
