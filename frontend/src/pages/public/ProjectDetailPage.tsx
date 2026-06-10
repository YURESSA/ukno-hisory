import { useState } from 'react';
import { useParams } from 'react-router-dom';
import { PublicLayout } from '@/layouts/PublicLayout/PublicLayout';
import { useGetPublicProjectQuery } from '@/modules/projects/api/projectsApi';
import { resolveBackendUrl } from '@/config/env';
import styles from '@/styles/projectDetailPage.module.css';
import { Box, IconButton, MobileStepper } from '@mui/material';
import { KeyboardArrowLeft, KeyboardArrowRight } from '@mui/icons-material';

const VISIBLE = 3;

export const ProjectDetailPage = () => {
  const { id } = useParams<{ id: string }>();
  const { data: project, isLoading, error } = useGetPublicProjectQuery(Number(id));
  const [activeStep, setActiveStep] = useState(0);

  const gallery = project?.gallery ?? [];
  const totalSteps = Math.max(0, gallery.length - VISIBLE + 1);
  const lastStep = totalSteps - 1;

  const handleNext = () => setActiveStep((prev) => Math.min(prev + 1, lastStep));
  const handleBack = () => setActiveStep((prev) => Math.max(prev - 1, 0));

  return (
    <PublicLayout>
      {isLoading && <p>Загрузка...</p>}
      {error && <p>Ошибка при загрузке проекта</p>}

      {project && (
        <>
          <div className={styles['detail-hero']}>
            {project.main_image && (
              <img
                src={resolveBackendUrl(project.main_image)}
                alt={project.title}
                className={styles['detail-main-img']}
              />
            )}

            <div className={styles['detail-hero-info']}>
              <h3 className={styles['detail-title']}>{project.title}</h3>

              {project.short_description && (
                <p className={styles['detail-short-desc']}>{project.short_description}</p>
              )}

              <div className={styles['detail-tags']}>
                <div className={styles['detail-tags-row']}>
                  {project.tags.author && (
                    <h6 className={`${styles['detail-tag']} ${styles['detail-tag-1']}`}>Автор: {project.tags.author}</h6>
                  )}
                  {project.tags.year && (
                    <h6 className={`${styles['detail-tag']} ${styles['detail-tag-2_3']}`}>{project.tags.year} г.</h6>
                  )}
                </div>
                {(project.tags.tag_one || project.tags.tag_two) && (
                  <div className={styles['detail-tags-row']}>
                      <h6 className={`${styles['detail-tag']} ${styles['detail-tag-2_3']}`}>{project.tags.tag_one}</h6>
                      <h6 className={`${styles['detail-tag']} ${styles['detail-tag-4']}`}>{project.tags.tag_two}</h6>
                  </div>
                )}
              </div>
            </div>
          </div>

          {project.description && (
            <div className={styles['detail-description-section']}>
              <h4 className={styles['detail-section-title']}>Описание проекта</h4>
              <div className={styles['detail-description-text']}>
                {project.description.split('\n').filter(p => p.trim()).map((paragraph, i) => (
                  <p key={i}>{paragraph}</p>
                ))}
              </div>
            </div>
          )}

          {gallery.length > 0 && (
            <div className={styles['detail-gallery-section']}>
              <h4 className={styles['detail-gallery-title']}>Как это было?</h4>

              <Box sx={{ position: 'relative' }}>
                <Box sx={{ overflow: 'hidden', width: '100%' }}>
                  <Box
                    sx={{
                      display: 'flex',
                      width: `calc(${gallery.length} * 100% / ${VISIBLE})`,
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
                          paddingInline: '10px',
                          boxSizing: 'border-box',
                        }}
                      >
                        <img
                          src={resolveBackendUrl(img.image)}
                          alt=""
                          loading="lazy"
                          style={{
                            width: '100%',
                            height: '580px',
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
              </Box>

              {totalSteps > 1 && (
                <MobileStepper
                  steps={totalSteps}
                  position="static"
                  activeStep={activeStep}
                  nextButton={null}
                  backButton={null}
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
        </>
      )}
    </PublicLayout>
  );
};
