import { PublicLayout } from "@/layouts/PublicLayout/PublicLayout";
import { useParams } from 'react-router-dom';
import { resolveBackendUrl } from '@/config/env';
import styles  from "@/styles/enterpriseDetailPage.module.css";
import { useGetPublicEnterpriseHistoryQuery } from "@/modules/enterprise_history/api/enterpriseHistoryApi";

export const EnterpriseDetailPage = () => {
  const { id } = useParams<{ id: string }>();
  const { data: enterprise, isLoading, error } = useGetPublicEnterpriseHistoryQuery(Number(id));

  return (
    <PublicLayout>
      {isLoading && <p>Загрузка...</p>}
      {error && <p>Ошибка при загрузке проекта</p>}

      {enterprise && (
        <>
          <section className={styles['hero-wrapper']}>
            <div className={styles['hero-block']}>
              <img src="/image/enterprises/detail-vector.svg" className={styles['hero-vector']} alt="" />
              <div className={styles['hero-title']}>
                <h3>{ enterprise.title }</h3>
                <p className='text-standart'>
                  { enterprise.subtitle }
                </p>
              </div>
              <img src={resolveBackendUrl(enterprise.main_image)} className={styles['enterprise-image']} alt="Изображение предприятия" />
            </div>
          </section>
          <section className={styles['enterprise-slides']}>
            <h4>ИСТОРИЯ</h4>
            <div className={styles['enterprise-description']}>
              <p className="text-standart">{ enterprise.short_description }</p>
            </div>
            <div className={styles['slides']}>
              <h4>КАК ЭТО БЫЛО?</h4>

              {(() => {
                let mixedSlideCount = 0;
                return enterprise.how_it_was && [...enterprise.how_it_was]
                  .sort((a, b) => a.order_index - b.order_index)
                  .map((slide) => {
                    const hasText = !!slide.text;
                    const hasImage = !!slide.image;

                    
                    if (hasText && !hasImage) {
                      return (
                        <div key={slide.id} className={styles['slide-full-width']}>
                          <p className={`text-standart ${styles['slide-full-width-text']}`}>
                            {slide.text}
                          </p>
                        </div>
                      );
                    }

                    
                    if (!hasText && hasImage) {
                      return (
                        <div key={slide.id} className={styles['slide-full-width']}>
                          <img 
                            src={resolveBackendUrl(slide.image!)} 
                            alt="Слайд истории" 
                            className={styles['slide-full-width-img']} 
                          />
                        </div>
                      );
                    }

                    
                    if (hasText && hasImage) {
                      const isImageLeft = mixedSlideCount % 2 !== 0;
                      mixedSlideCount++;

                      return (
                        <div 
                          key={slide.id} 
                          className={`${styles['slide-split']} ${isImageLeft ? styles['image-left'] : ''}`}
                        >
                          <div className={styles['slide-split-text']}>
                            <p className='text-standart'>{slide.text}</p>
                          </div>
                          <div className={styles['slide-split-img-wrapper']}>
                            <img 
                              src={resolveBackendUrl(slide.image!)} 
                              alt="Слайд истории" 
                              className={styles['slide-split-img']} 
                            />
                          </div>
                        </div>
                      );
                    }

                    return null;
                  });
              })()}
            </div>
          </section>
        </>
      )}
    </PublicLayout>
  )
}
