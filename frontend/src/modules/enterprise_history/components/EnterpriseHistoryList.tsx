import { useState } from 'react';
import { 
  useGetAdminEnterpriseHistoriesQuery, 
  useDeleteEnterpriseHistoryMutation,
  useUpdateEnterpriseHistoryMutation
} from '../api/enterpriseHistoryApi';
import { EditEnterpriseHistoryModal } from './EditEnterpriseHistoryModal';

export const EnterpriseHistoryList = () => {
  const { data: histories, isLoading, error } = useGetAdminEnterpriseHistoriesQuery();
  const [deleteHistory] = useDeleteEnterpriseHistoryMutation();
  const [updateHistory] = useUpdateEnterpriseHistoryMutation();

  const [editingId, setEditingId] = useState<number | null>(null);

  if (isLoading) return <p>Загрузка историй предприятий...</p>;
  if (error) return <p>Ошибка загрузки данных</p>;

  const handleToggleDraft = async (id: number, currentStatus: boolean) => {
    try {
      await updateHistory({ id, data: { is_draft: !currentStatus } }).unwrap();
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div style={{ marginTop: '20px' }}>
      <h3>История предприятий</h3>
      <table border={1} cellPadding={10} style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            <th>ID</th>
            <th>Заголовок</th>
            <th>Подзаголовок</th>
            <th>Статус</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          {histories?.map((history) => (
            <tr key={history.id}>
              <td>{history.id}</td>
              <td>{history.title}</td>
              <td>{history.general_subtitle}</td>
              <td>
                <button 
                  onClick={() => handleToggleDraft(history.id, history.is_draft)}
                  style={{ 
                    padding: '5px 10px', 
                    cursor: 'pointer',
                    background: history.is_draft ? '#fffbe6' : '#f6ffed',
                    border: `1px solid ${history.is_draft ? '#ffe58f' : '#b7eb8f'}`,
                    borderRadius: '4px'
                  }}
                >
                  {history.is_draft ? '📝 Черновик' : '✅ Опубликован'}
                </button>
              </td>
              <td style={{ display: 'flex', gap: '10px' }}>
                <button 
                  onClick={() => setEditingId(history.id)}
                  style={{ color: '#1890ff', cursor: 'pointer' }}
                >
                  Изменить
                </button>
                <button 
                  onClick={() => {
                    if (confirm('Удалить запись?')) deleteHistory(history.id);
                  }} 
                  style={{ color: 'red', cursor: 'pointer' }}
                >
                  Удалить
                </button>
              </td>
            </tr>
          ))}
          {histories?.length === 0 && (
            <tr>
              <td colSpan={5} style={{ textAlign: 'center' }}>Записей пока нет</td>
            </tr>
          )}
        </tbody>
      </table>

      {editingId && (
        <EditEnterpriseHistoryModal 
          itemId={editingId} 
          isOpen={true} 
          onClose={() => setEditingId(null)} 
        />
      )}
    </div>
  );
};
