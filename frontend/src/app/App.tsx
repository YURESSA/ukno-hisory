import { useGetProjectsQuery } from '@/modules/projects/api/projectsApi';

function App() {
  const { data, error, isLoading } = useGetProjectsQuery();

  console.log('Данные с бэка:', data);
  console.log('Ошибка:', error);

  if (isLoading) return <div>Загрузка...</div>;

  return (
    <div>
      <h1>Проверка связи с API</h1>
      {error ? (
        <p style={{ color: 'red' }}>Ошибка: {JSON.stringify(error)}</p>
      ) : (
        <pre>{JSON.stringify(data, null, 2)}</pre>
      )}
    </div>
  );
}

export default App;