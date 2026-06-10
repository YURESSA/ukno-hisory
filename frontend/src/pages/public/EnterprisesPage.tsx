import { PublicLayout } from '@/layouts/PublicLayout/PublicLayout';
import { useGetPublicEnterprisesHistoryQuery } from '@/modules/enterprise_history/api/enterpriseHistoryApi'
import styles from '@/styles/enterprisesPage.module.css';
import { resolveBackendUrl } from '@/config/env';
import { Link } from 'react-router-dom';

export const EnterprisesPage = () => {
  const { data: enterprises, isLoading, error } = useGetPublicEnterprisesHistoryQuery();

  return (
    <PublicLayout>
      <section className={styles['hero-wrapper']}>
        <div className={styles['title']}>
          <h3>ИСТОРИЯ ПРЕДПРИЯТИЙ <br /> ЧКАЛОВСКОГО РАЙОНА</h3>
        </div>
        <div className={styles['hero-blocks']}>
          <div className={styles['orange-block']}>
            <p className='text-standart'>Наденьте наушники. Напротив вас — старый пульт.</p>
            <img src="/image/enterprises/purple-block-img.png" alt="" />
          </div>
          <div className={styles['purple-block']}>
            <p className='text-standart'>Соберите свою версию завода. На большом металлическом листе разбросаны магниты-детали</p>
            <img src="/image/enterprises/orange-block-img.png" alt="" />
          </div>
        </div>
        <div className={styles['description']}>
          <p className='text-standart'>На этой странице — ключевые вехи промышленности Чкаловского района. Вы узнаете о судьбе знаменитых заводов, о том, как война и перестройка изменили карту местных производств, и о действующих предприятиях, которые продолжают традиции качества.Листайте хронику, фото цехов и знакомьтесь с героями-рабочими</p>
        </div>
      </section>
      <section className={styles['enterprises-feed']}>
        <img src="/image/enterprises/Vector-feed.svg" className={styles['enterprises-feed-background']} alt="" />
        {isLoading && <p>Загрузка проектов...</p>}
        {error && <p>Ошибка при загрузке проектов</p>}
        { enterprises && enterprises.map((enterprise, index) => {
          return (
            <div className={styles['enterprise-wrapper']} key={enterprise.id}>
              <div className={styles['enterprise-title-wrapper']}>
                <div className={styles['enterprise-title']}>
                  <p className={styles['text-medium']}>
                    { enterprise.subtitle }
                  </p>
                  <h4>{enterprise.title}</h4>
                </div>
                <h3>{ index+1 }</h3>
              </div>
              
              <div className={styles['enterprise-description']}>
                <p>{enterprise.short_description}</p>
              </div>
              
              <img src={resolveBackendUrl(enterprise.main_image)} alt="Изображение предприятия" className={styles['enterprise-img']} />

              <Link to={`/enterprise/${enterprise.id}`} className={styles['enterprise-link']}>Узнать больше <img src="/image/enterprises/arrow.svg" alt="Переход на страницу предприятия" /></Link>

            </div>
          )
        }) }
      </section>
    </PublicLayout>
  );
};
