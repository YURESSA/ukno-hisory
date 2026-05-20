import { useForm } from 'react-hook-form';
import { useLoginMutation } from '../api/authApi';

export const LoginForm = () => {
  const { register, handleSubmit } = useForm();
  const [login, { isLoading, error }] = useLoginMutation();

const onSubmit = async (data: any) => {
  try {
    const result = await login({
      email: data.email,
      password: data.password
    }).unwrap();
    
    localStorage.setItem('token', result.access_token);
    window.location.reload();
  } catch (err) {
    console.error('Ошибка входа:', err);
  }
};

  return (
    <div style={{ maxWidth: '300px', margin: '100px auto', padding: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
      <h2>Вход в админку</h2>
      <form onSubmit={handleSubmit(onSubmit)} style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
        <input {...register('email')} type="email" placeholder="Email" required />
        <input {...register('password')} type="password" placeholder="Пароль" required />
        
        {error && <p style={{ color: 'red', fontSize: '12px' }}>Неверный логин или пароль</p>}
        
        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Вход...' : 'Войти'}
        </button>
      </form>
    </div>
  );
};