import { useEffect } from 'react';
import { useGetSubdistrictDetailQuery } from '@/modules/subdistricts/api/subdistrictsApi';
import { resolveBackendUrl } from '@/config/env';
import { Link } from 'react-router-dom';
import { DISTRICTS } from '../InteractiveMap/districts';
import styles from './DistrictPanel.module.css';

interface DistrictPanelProps {
  districtName: string | null;
  aboutMode: boolean;
  onClose: () => void;
  onSelectDistrict?: (name: string) => void;
  onBackToAbout?: () => void;
}

const ABOUT_FACTS = [
  { icon: '📍', label: 'Площадь', value: '~770 км²' },
  { icon: '👥', label: 'Население', value: '≈ 290 000 чел.' },
  { icon: '🏭', label: 'Промышленность', value: 'Машиностроение, металлургия' },
  { icon: '📅', label: 'Основан', value: '1942 год' },
];

const ABOUT_TEXT = `Чкаловский район — один из семи районов Екатеринбурга, расположенный в южной части города. Назван в честь советского лётчика Валерия Чкалова.

Район охватывает разнообразные территории: от плотной городской застройки на севере до живописных пригородных зон и природных массивов на юге. Здесь соседствуют промышленные предприятия советской эпохи, современные жилые кварталы и исторические посёлки.

На карте района — 16 микрорайонов и исторических поселений, каждое из которых имеет свой характер и свою историю. Нажми на любую область, чтобы узнать больше.`;

export const DistrictPanel = ({
  districtName,
  aboutMode,
  onClose,
  onSelectDistrict,
  onBackToAbout,
}: DistrictPanelProps) => {
  const isOpen = !!districtName || aboutMode;

  const { data, isLoading, isFetching } = useGetSubdistrictDetailQuery(
    districtName ?? '',
    { skip: !districtName }
  );

  useEffect(() => {
    const checkAndLock = () => {
      if (isOpen && window.innerWidth <= 768) {
        document.body.style.overflow = 'hidden';
      } else {
        document.body.style.overflow = '';
      }
    };
    checkAndLock();
    window.addEventListener('resize', checkAndLock);
    return () => {
      document.body.style.overflow = '';
      window.removeEventListener('resize', checkAndLock);
    };
  }, [isOpen]);

  return (
    <aside
      className={`${styles['panel']} ${isOpen ? styles['panel--open'] : ''} ${
        aboutMode ? styles['panel--about'] : ''
      }`}
      aria-label="Информация о районе"
      role="complementary"
    >
      {/* Кнопка закрытия */}
      <button className={styles['close-btn']} onClick={onClose} aria-label="Закрыть">
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
          <path d="M15 5L5 15M5 5l10 10" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
        </svg>
      </button>

      <div className={styles['panel-body']}>

        {/* ── Режим «О карте» ── */}
        {aboutMode && (
          <>
            <div className={styles['about-header']}>
              <span className={styles['about-badge']}>О РАЙОНЕ</span>
              <h5 className={styles['panel-title']}>Чкаловский район</h5>
              <p className={styles['about-subtitle']}>Екатеринбург</p>
            </div>

            <div className={styles['facts-grid']}>
              {ABOUT_FACTS.map((f) => (
                <div key={f.label} className={styles['fact-card']}>
                  <span className={styles['fact-icon']}>{f.icon}</span>
                  <span className={styles['fact-label']}>{f.label}</span>
                  <span className={styles['fact-value']}>{f.value}</span>
                </div>
              ))}
            </div>

            <p className={`text-medium ${styles['panel-description']}`}>{ABOUT_TEXT}</p>

            <div className={styles['about-hint']}>
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                <circle cx="8" cy="8" r="7" stroke="#FF6C36" strokeWidth="1.5"/>
                <path d="M8 7v4M8 5h.01" stroke="#FF6C36" strokeWidth="1.5" strokeLinecap="round"/>
              </svg>
              <span>Нажми на район на карте, чтобы узнать о нём подробнее</span>
            </div>

            <div className={styles['mobile-districts-list-wrapper']}>
              <p className={styles['districts-list-title']}>Районы Чкаловского</p>
              <div className={styles['districts-list']}>
                {DISTRICTS.map((d) => (
                  <button
                    key={d.id}
                    className={styles['district-item-btn']}
                    onClick={() => onSelectDistrict?.(d.id)}
                  >
                    <span>{d.name}</span>
                    <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                      <path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                  </button>
                ))}
              </div>
            </div>
          </>
        )}

        {/* ── Режим конкретного района ── */}
        {!aboutMode && (
          <>
            {onBackToAbout && (
              <button className={styles['back-btn']} onClick={onBackToAbout} aria-label="Назад к списку районов">
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                  <path d="M13 8H3M3 8l4-4M3 8l4 4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
                <span>К списку районов</span>
              </button>
            )}

            {(isLoading || isFetching) && (
              <div className={styles['skeleton-wrap']}>
                <div className={`${styles['skeleton']} ${styles['skeleton--img']}`} />
                <div className={`${styles['skeleton']} ${styles['skeleton--title']}`} />
                <div className={`${styles['skeleton']} ${styles['skeleton--text']}`} />
                <div className={`${styles['skeleton']} ${styles['skeleton--text']} ${styles['skeleton--short']}`} />
              </div>
            )}

            {data && !isFetching && (
              <>
                {/* Фото района */}
                {data.image ? (
                  <div className={styles['panel-image-wrap']}>
                    <img
                      src={resolveBackendUrl(data.image)}
                      alt={data.name}
                      className={styles['panel-image']}
                    />
                  </div>
                ) : (
                  <div className={styles['panel-image-placeholder']}>
                    <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
                      <rect width="48" height="48" rx="12" fill="#F0F0F0" />
                      <path d="M14 34l8-10 6 7 4-5 6 8H14z" fill="#D0D0D0" />
                      <circle cx="32" cy="18" r="4" fill="#D0D0D0" />
                    </svg>
                  </div>
                )}

                {/* Название */}
                <h5 className={styles['panel-title']}>{data.name}</h5>

                {/* Описание */}
                {data.description ? (
                  <p className={`text-medium ${styles['panel-description']}`}>{data.description}</p>
                ) : (
                  <p className={`text-medium ${styles['panel-empty']}`}>Описание района пока не добавлено.</p>
                )}

                {/* Предприятия */}
                {data.enterprises && data.enterprises.length > 0 && (
                  <div className={styles['enterprises-block']}>
                    <p className={styles['enterprises-label']}>ПРЕДПРИЯТИЯ</p>
                    <ul className={styles['enterprises-list']}>
                      {data.enterprises.map((e) => (
                        <li key={e.id}>
                          <Link
                            to={`/enterprise/${e.id}`}
                            className={styles['enterprise-link']}
                          >
                            <span>{e.title}</span>
                            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                              <path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                            </svg>
                          </Link>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </>
            )}
          </>
        )}
      </div>
    </aside>
  );
};
