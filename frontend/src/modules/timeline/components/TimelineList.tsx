import { useState } from 'react';
import { useGetTimelineQuery, useDeleteTimelineMutation } from '../api/timelineApi';
import { EditTimelineModal } from './EditTimelineModal';
import { TimelineEvent } from '../types';
import { resolveBackendUrl } from '@/config/env';

export const TimelineList = () => {
  const { data: timeline, isLoading, error } = useGetTimelineQuery();
  const [deleteTimeline] = useDeleteTimelineMutation();
  
  const [editingEvent, setEditingEvent] = useState<TimelineEvent | null>(null);

  if (isLoading) return <p>Загрузка таймлайна...</p>;
  if (error) return <p>Ошибка загрузки таймлайна</p>;

  return (
    <div style={{ marginTop: '20px' }}>
      <h3>Таймлайн событий</h3>
      <table border={1} cellPadding={10} style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            <th>Год</th>
            <th>Текст</th>
            <th>Изображение</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          {timeline?.map((item) => (
            <tr key={item.id}>
              <td>{item.year}</td>
              <td>{item.text}</td>
              <td>
                <img 
                  src={resolveBackendUrl(item.image)} 
                  alt={item.text} 
                  style={{ width: '100px', height: 'auto' }} 
                />
              </td>
              <td>
                <div style={{ display: 'flex', gap: '10px' }}>
                  <button 
                    onClick={() => setEditingEvent(item)}
                    style={{ color: '#1890ff', cursor: 'pointer' }}
                  >
                    Изменить
                  </button>
                  <button 
                    onClick={() => {
                      if (confirm('Удалить событие?')) deleteTimeline(item.id);
                    }} 
                    style={{ color: 'red', cursor: 'pointer' }}
                  >
                    Удалить
                  </button>
                </div>
              </td>
            </tr>
          ))}
          {timeline?.length === 0 && (
            <tr>
              <td colSpan={4} style={{ textAlign: 'center' }}>Событий пока нет</td>
            </tr>
          )}
        </tbody>
      </table>

      {editingEvent && (
        <EditTimelineModal 
          event={editingEvent}
          isOpen={true}
          onClose={() => setEditingEvent(null)}
        />
      )}
    </div>
  );
};
