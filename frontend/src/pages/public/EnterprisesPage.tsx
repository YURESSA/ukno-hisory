import { PublicLayout } from '@/layouts/PublicLayout/PublicLayout';
import { useGetPublicEnterpriseHistoryQuery } from '@/modules/enterprise_history/api/enterpriseHistoryApi'
import styles from '@/styles/enterprisesPage.module.css';

export const EnterprisesPage = () => {
  const { data: enterprises, isLoading, error } = useGetPublicEnterpriseHistoryQuery();

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
        
      </section>
    </PublicLayout>
  );
};
