import { PublicLayout } from '@/layouts/PublicLayout/PublicLayout';
import styles from '@/styles/projectPage.module.css';
import { useGetPublicProjectsQuery } from '@/modules/projects/api/projectsApi';
import { resolveBackendUrl } from '@/config/env';
import { Link } from 'react-router-dom';

export const ProjectsPage = () => {
  const { data: projects, isLoading, error } = useGetPublicProjectsQuery();

  return (
    <PublicLayout>
      <section className={styles['hero-wrapper']}>
        <div className={styles['idol-wrapper']}>
          <img src='/image/projects/idol.svg' className={styles['idol']}/>
          <div className={styles['hero-content']}>
            <img src='/image/projects/icon/Vector.svg' className={styles['vector']}/>
            <div className={styles['hero-title']}>
              <h3 className={styles['left-title']}>История района</h3>
              <h3 className={styles['right-title']}>глазами детей</h3>
              <div className={styles['star1']}/>
              <div className={styles['star2']}/>
            </div>
            <div className={`text-standart ${styles['descript']}`}>
              <p>ПРОЕКТЫ УЧЕНИКОВ ШКОЛ <br />
              <span className={styles['custom-descript-title']}>ЧКАЛОВСКОГО РАЙОНА:</span><br />
              <span className={styles['custom-descript-text']}>от архивных исследований</span>  до 3D-макетов</p>
            </div>
          </div>
        </div>
      </section>

      <section className={styles['project-wrapper']}>
        <div className={styles['project-list-title']}>
          <h4>ПРОЕКТЫ</h4>
          <p className='text-standart'>Исследуй район глазами его юных жителей. Школьные проекты об истории, людях и будущем Чкаловского. Смотри их проекты о том, как меняется и чем дышит Чкаловский.</p>
        </div>
        <div className={styles['projects-list']}>
          {isLoading && <p>Загрузка проектов...</p>}
          {error && <p>Ошибка при загрузке проектов</p>}
          {projects && projects.map((project, index) => {
            const variant = (index % 4) + 1;
            return (
              <div
                key={project.id}
                className={`${styles['project-item']} ${styles[`project-item-${variant}`]}`}
              >
                {/* Варианты 1 и 3: фото слева, текст справа */}
                {(variant === 1 || variant === 3) && (
                  <>
                    {project.main_image && (
                      <Link to={`/project/${project.id}`} className={styles['project-img-wrap']}>
                        <img
                          src={resolveBackendUrl(project.main_image)}
                          alt={project.title}
                          className={styles['project-img']}
                        />
                      </Link>
                    )}
                    <div className={styles['project-text']}>
                      {project.author && (
                        <div className={styles['project-author-block']}>
                          <div>
                            <span>Автор: {project.author}</span>
                          </div>
                          <Link to={`/project/${project.id}`} className={styles['project-title-link']}>
                            <h4 className={styles['project-title']}>{project.title}</h4>
                          </Link>
                        </div>
                      )}
                      {project.short_description && (
                        <p className={`text-standart ${styles['project-desc']}`}>{project.short_description}</p>
                      )}
                    </div>
                  </>
                )}

                {/* Варианты 2 и 4: текст слева, фото справа */}
                {(variant === 2 || variant === 4) && (
                  <>
                    <div className={styles['project-text']}>
                      {project.author && (
                        <div className={styles['project-author-block']}>
                          <div>
                            <span>Автор: {project.author}</span>
                          </div>
                          <Link to={`/project/${project.id}`} className={styles['project-title-link']}>
                            <h4 className={styles['project-title']}>{project.title}</h4>
                          </Link>
                        </div>
                      )}
                      {project.short_description && (
                        <p className={`text-standart ${styles['project-desc']}`}>{project.short_description}</p>
                      )}
                    </div>
                    {project.main_image && (
                      <Link to={`/project/${project.id}`} className={styles['project-img-wrap']}>
                        <img
                          src={resolveBackendUrl(project.main_image)}
                          alt={project.title}
                          className={styles['project-img']}
                        />
                      </Link>
                    )}
                  </>
                )}
              </div>
            );
          })}
        </div>
      </section>
    </PublicLayout>
  );
};
