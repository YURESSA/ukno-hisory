import { useForm } from 'react-hook-form';
import { useEffect } from 'react';
import { useUpdateTimelineMutation } from '../api/timelineApi';
import { Modal } from '@/app/components/Modal';
import { TimelineEvent } from '../types';

interface Props {
  event: TimelineEvent;
  isOpen: boolean;
  onClose: () => void;
}

export const EditTimelineModal = ({ event, isOpen, onClose }: Props) => {
  const [updateTimeline, { isLoading }] = useUpdateTimelineMutation();
  const { register, handleSubmit, reset } = useForm();

  useEffect(() => {
    if (event) {
      reset({
        year: event.year,
        text: event.text,
      });
    }
  }, [event, reset]);

  const onSubmit = async (data: any) => {
    try {
      await updateTimeline({ id: event.id, data }).unwrap();
      alert('Событие обновлено!');
      onClose();
    } catch (e) {
      console.error(e);
      alert('Ошибка при обновлении');
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title={`Редактировать событие #${event.id}`}>
      <form onSubmit={handleSubmit(onSubmit)} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
        <input type="number" {...register('year')} placeholder="Год" required style={inputStyle} />
        <textarea {...register('text')} placeholder="Описание" required style={{ ...inputStyle, height: '100px' }} />
        
        <button type="submit" disabled={isLoading} style={saveButtonStyle}>
          {isLoading ? 'Сохранение...' : 'Сохранить изменения'}
        </button>
      </form>
    </Modal>
  );
};

const inputStyle = { padding: '10px', border: '1px solid #d9d9d9', borderRadius: '4px' };
const saveButtonStyle = { backgroundColor: '#1890ff', color: 'white', border: 'none', padding: '12px', borderRadius: '4px', cursor: 'pointer' };
