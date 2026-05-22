import { useForm } from 'react-hook-form';
import { useEffect } from 'react';
import { 
  useGetAdminEnterpriseHistoryQuery, 
  useUpdateEnterpriseHistoryMutation, 
  useAddHistorySlideMutation, 
  useDeleteHistorySlideMutation,
  useAddHistoryGalleryImagesMutation,
  useDeleteHistoryGalleryImageMutation
} from '../api/enterpriseHistoryApi';
import { Modal } from '@/app/components/Modal';
import { resolveBackendUrl } from '@/config/env';

interface Props {
  itemId: number;
  isOpen: boolean;
  onClose: () => void;
}

export const EditEnterpriseHistoryModal = ({ itemId, isOpen, onClose }: Props) => {
  const { data: item, isLoading: isFetching } = useGetAdminEnterpriseHistoryQuery(itemId, { skip: !isOpen });
  const [updateItem, { isLoading: isUpdating }] = useUpdateEnterpriseHistoryMutation();
  const [addSlide] = useAddHistorySlideMutation();
  const [deleteSlide] = useDeleteHistorySlideMutation();
  const [addGallery] = useAddHistoryGalleryImagesMutation();
  const [deleteGallery] = useDeleteHistoryGalleryImageMutation();

  const { register, handleSubmit, reset } = useForm();

  useEffect(() => {
    if (item) {
      reset({
        title: item.title,
        general_subtitle: item.general_subtitle,
        detail_subtitle: item.detail_subtitle,
        short_description: item.short_description,
        is_draft: item.is_draft,
      });
    }
  }, [item, reset]);

  const onSubmit = async (data: any) => {
    try {
      await updateItem({ id: itemId, data }).unwrap();
      alert('Обновлено!');
    } catch (e) {
      console.error(e);
      alert('Ошибка обновления');
    }
  };

  const handleAddSlide = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files?.[0]) {
      const formData = new FormData();
      formData.append('image', e.target.files[0]);
      formData.append('text', 'Новый слайд');
      try {
        await addSlide({ id: itemId, formData }).unwrap();
      } catch (e) {
        console.error(e);
      }
    }
  };

  const handleGalleryUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const formData = new FormData();
      Array.from(e.target.files).forEach(file => {
        formData.append('images', file);
      });
      try {
        await addGallery({ id: itemId, formData }).unwrap();
      } catch (e) {
        console.error(e);
      }
    }
  };

  if (isFetching) return null;

  return (
    <Modal isOpen={isOpen} onClose={onClose} title={`Редактировать историю #${itemId}`}>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '30px' }}>
        <form onSubmit={handleSubmit(onSubmit)} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
          <h3>Основные данные</h3>
          <input {...register('title')} placeholder="Заголовок" style={inputStyle} />
          <input {...register('general_subtitle')} placeholder="Подзаголовок (общий)" style={inputStyle} />
          <input {...register('detail_subtitle')} placeholder="Подзаголовок (детальный)" style={inputStyle} />
          <textarea {...register('short_description')} placeholder="Краткое описание" style={{ ...inputStyle, height: '100px' }} />
          
          <label style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <input type="checkbox" {...register('is_draft')} /> Черновик
          </label>

          <button type="submit" disabled={isUpdating} style={saveButtonStyle}>
            {isUpdating ? 'Сохранение...' : 'Сохранить изменения'}
          </button>
        </form>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          <div>
            <h3>Слайды ("Как это было")</h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', marginBottom: '10px' }}>
              {item?.how_it_was.map((slide) => (
                <div key={slide.id} style={{ display: 'flex', gap: '10px', alignItems: 'center', border: '1px solid #eee', padding: '10px' }}>
                  {slide.image && <img src={resolveBackendUrl(slide.image)} style={{ width: '50px', height: '50px', objectFit: 'cover' }} />}
                  <span style={{ flex: 1, fontSize: '12px' }}>{slide.text || 'Без текста'}</span>
                  <button onClick={() => deleteSlide({ historyId: itemId, slideId: slide.id })} style={{ color: 'red', border: 'none', background: 'none', cursor: 'pointer' }}>Удалить</button>
                </div>
              ))}
            </div>
            <label style={uploadButtonStyle}>
              + Добавить слайд
              <input type="file" onChange={handleAddSlide} style={{ display: 'none' }} accept="image/*" />
            </label>
          </div>

          <div>
            <h3>Галерея</h3>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(80px, 1fr))', gap: '8px', marginBottom: '10px' }}>
              {item?.gallery.map((img) => (
                <div key={img.id} style={{ position: 'relative' }}>
                  <img src={resolveBackendUrl(img.image)} style={{ width: '100%', height: '60px', objectFit: 'cover' }} />
                  <button onClick={() => deleteGallery({ historyId: itemId, imageId: img.id })} style={deleteImgButtonStyle}>&times;</button>
                </div>
              ))}
            </div>
            <label style={uploadButtonStyle}>
              + Фото в галерею
              <input type="file" multiple onChange={handleGalleryUpload} style={{ display: 'none' }} accept="image/*" />
            </label>
          </div>
        </div>
      </div>
    </Modal>
  );
};

const inputStyle = { padding: '10px', border: '1px solid #d9d9d9', borderRadius: '4px' };
const saveButtonStyle = { backgroundColor: '#1890ff', color: 'white', border: 'none', padding: '12px', borderRadius: '4px', cursor: 'pointer' };
const uploadButtonStyle = { display: 'block', padding: '8px', border: '1px dashed #1890ff', color: '#1890ff', textAlign: 'center' as const, borderRadius: '4px', cursor: 'pointer', fontSize: '14px' };
const deleteImgButtonStyle = { position: 'absolute' as const, top: 0, right: 0, background: 'red', color: 'white', border: 'none', width: '18px', height: '18px', fontSize: '12px', cursor: 'pointer' };
