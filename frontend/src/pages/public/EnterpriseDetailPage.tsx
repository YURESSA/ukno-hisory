import { useState } from 'react';
import { PublicLayout } from "@/layouts/PublicLayout/PublicLayout";
import { useParams } from 'react-router-dom';
import { resolveBackendUrl } from '@/config/env';
import styles  from "@/styles/enterpriseDetailPage.module.css";
import { useGetPublicEnterpriseHistoryQuery } from "@/modules/enterprise_history/api/enterpriseHistoryApi";
import { Box, IconButton, MobileStepper, useTheme, useMediaQuery } from '@mui/material';
import { KeyboardArrowLeft, KeyboardArrowRight } from '@mui/icons-material';

export const EnterpriseDetailPage = () => {
  const { id } = useParams<{ id: string }>();
  const { data: enterprise, isLoading, error } = useGetPublicEnterpriseHistoryQuery(Number(id));
  const [activeStep, setActiveStep] = useState(0);

  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const visibleItems = isMobile ? 1 : 3;

  const gallery = enterprise?.gallery ?? [];
  const totalSteps = Math.max(0, gallery.length - visibleItems + 1);
  const lastStep = totalSteps - 1;

  const handleNext = () => setActiveStep((prev) => Math.min(prev + 1, lastStep));
  const handleBack = () => setActiveStep((prev) => Math.max(prev - 1, 0));

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
            <h4>КАК ЭТО БЫЛО?</h4>
            <div className={styles['slides']}>
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

            {gallery.length > 0 && (
              <div className={styles['detail-gallery-section']}>
                <h4>КАК ЭТО БЫЛО?</h4>

                <Box sx={{ position: 'relative' }}>
                  <Box sx={{ overflow: 'hidden', width: '100%' }}>
                    <Box
                      sx={{
                        display: 'flex',
                        width: `calc(${gallery.length} * 100% / ${visibleItems})`,
                        transform: `translateX(calc(-${activeStep} * 100% / ${gallery.length}))`,
                        transition: 'transform 0.45s cubic-bezier(0.4, 0, 0.2, 1)',
                      }}
                    >
                      {gallery.map((img) => (
                        <Box
                          key={img.id}
                          sx={{
                            width: `calc(100% / ${gallery.length})`,
                            flexShrink: 0,
                            paddingInline: isMobile ? '0' : '10px',
                            boxSizing: 'border-box',
                          }}
                        >
                          <img
                            src={resolveBackendUrl(img.image)}
                            alt=""
                            loading="lazy"
                            style={{
                              width: '100%',
                              height: isMobile ? '300px' : '580px',
                              objectFit: 'cover',
                              objectPosition: 'center',
                              borderRadius: '18px',
                              display: 'block',
                            }}
                          />
                        </Box>
                      ))}
                    </Box>
                  </Box>

                  {!isMobile && (
                    <>
                      <IconButton
                        onClick={handleBack}
                        disabled={activeStep === 0}
                        sx={{
                          position: 'absolute',
                          left: -26,
                          top: '50%',
                          transform: 'translateY(-50%)',
                          backgroundColor: 'white',
                          boxShadow: '0 2px 12px rgba(0,0,0,0.12)',
                          width: 52,
                          height: 52,
                          '&:hover': { backgroundColor: '#f5f5f5' },
                          '&.Mui-disabled': { opacity: 0.25 },
                        }}
                      >
                        <KeyboardArrowLeft sx={{ fontSize: 32, color: '#333' }} />
                      </IconButton>

                      <IconButton
                        onClick={handleNext}
                        disabled={activeStep === lastStep}
                        sx={{
                          position: 'absolute',
                          right: -26,
                          top: '50%',
                          transform: 'translateY(-50%)',
                          backgroundColor: 'white',
                          boxShadow: '0 2px 12px rgba(0,0,0,0.12)',
                          width: 52,
                          height: 52,
                          '&:hover': { backgroundColor: '#f5f5f5' },
                          '&.Mui-disabled': { opacity: 0.25 },
                        }}
                      >
                        <KeyboardArrowRight sx={{ fontSize: 32, color: '#333' }} />
                      </IconButton>
                    </>
                  )}
                </Box>

                {(isMobile || totalSteps > 1) && (
                  <MobileStepper
                    steps={totalSteps}
                    position="static"
                    activeStep={activeStep}
                    nextButton={
                      isMobile ? (
                        <IconButton size="small" onClick={handleNext} disabled={activeStep === totalSteps - 1}>
                          <KeyboardArrowRight />
                        </IconButton>
                      ) : null
                    }
                    backButton={
                      isMobile ? (
                        <IconButton size="small" onClick={handleBack} disabled={activeStep === 0}>
                          <KeyboardArrowLeft />
                        </IconButton>
                      ) : null
                    }
                    sx={{
                      justifyContent: 'center',
                      background: 'transparent',
                      mt: 2.5,
                      '& .MuiMobileStepper-dot': {
                        width: 8,
                        height: 8,
                        mx: '4px',
                        backgroundColor: '#D9D9D9',
                        transition: 'all 0.3s ease',
                      },
                      '& .MuiMobileStepper-dotActive': {
                        backgroundColor: '#FF6C36',
                        width: 24,
                        borderRadius: '4px',
                      },
                    }}
                  />
                )}
              </div>
            )}
          </section>
        </>
      )}
    </PublicLayout>
  )
}
