import { useForm } from 'react-hook-form';
import { useEffect } from 'react';
import { useUpdateTimelineMutation } from '../../api/timelineApi';
import { TimelineEvent } from '../../types';
import { 
  Dialog, 
  DialogTitle, 
  DialogContent, 
  DialogActions, 
  Button, 
  IconButton,
  CircularProgress
} from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';

interface Props {
  event: TimelineEvent;
  isOpen: boolean;
  onClose: () => void;
}

import { UpdateTimelineFormData } from '../../types';

export const EditTimelineModal = ({ event, isOpen, onClose }: Props) => {
  const [updateTimeline, { isLoading }] = useUpdateTimelineMutation();
  const { register, handleSubmit, reset } = useForm<UpdateTimelineFormData>();

  useEffect(() => {
    if (event) {
      reset({
        year: event.year,
        text: event.text,
      });
    }
  }, [event, reset]);

  const onSubmit = async (data: UpdateTimelineFormData) => {
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
    <Dialog open={isOpen} onClose={onClose} fullWidth maxWidth="sm">
      <DialogTitle sx={{ m: 0, p: 3, fontWeight: 800, color: 'var(--secondary-color)' }}>
        Редактировать событие #{event.id}
        <IconButton
          onClick={onClose}
          sx={{
            position: 'absolute',
            right: 16,
            top: 16,
            color: (theme) => theme.palette.grey[500],
          }}
        >
          <CloseIcon />
        </IconButton>
      </DialogTitle>
      
      <DialogContent dividers sx={{ p: 4 }}>
        <form 
          onSubmit={handleSubmit(onSubmit)} 
          id="edit-timeline-form"
          className="adm-form"
        >
          <div className="adm-form-group">
            <label className="adm-label">Год</label>
            <input 
              type="number" 
              {...register('year')} 
              placeholder="Год" 
              className="adm-input"
              required 
            />
          </div>

          <div className="adm-form-group">
            <label className="adm-label">Описание</label>
            <textarea 
              {...register('text')} 
              placeholder="Описание события..." 
              className="adm-input adm-textarea"
              rows={4}
              required 
            />
          </div>
        </form>
      </DialogContent>

      <DialogActions sx={{ p: 3, gap: 2 }}>
        <Button onClick={onClose} sx={{ color: '#666', fontWeight: 600 }}>
          Отмена
        </Button>
        <Button 
          type="submit" 
          form="edit-timeline-form" 
          variant="contained"
          disabled={isLoading}
          sx={{ 
            bgcolor: 'var(--primary-color)', 
            px: 4,
            borderRadius: '8px',
            boxShadow: 'none',
            '&:hover': { bgcolor: 'var(--primary-hover)', boxShadow: 'none' }
          }}
        >
          {isLoading ? <CircularProgress size={24} color="inherit" /> : 'Сохранить изменения'}
        </Button>
      </DialogActions>
    </Dialog>
  );
};
