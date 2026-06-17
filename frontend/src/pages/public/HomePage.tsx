import { useState, useMemo, useCallback } from 'react';
import { PublicLayout } from '@/layouts/PublicLayout/PublicLayout';
import styles from '@/styles/homePage.module.css';
import { useGetTimelineQuery } from '@/modules/timeline/api/timelineApi';
import { resolveBackendUrl } from '@/config/env';
import { Link } from 'react-router-dom';
import { InteractiveMap } from '@/modules/subdistricts/components/InteractiveMap/InteractiveMap';
import { DistrictPanel } from '@/modules/subdistricts/components/DistrictPanel/DistrictPanel';

export const HomePage = () => {
  const [selectedDistrict, setSelectedDistrict] = useState<string | null>(null);
  const [aboutMode, setAboutMode] = useState(false);

  const toggleAbout = () => {
    setAboutMode((prev) => !prev);
    setSelectedDistrict(null);
  };

  const handleDistrictClick = useCallback((name: string) => {
    setAboutMode(false);
    setSelectedDistrict((prev) => (prev === name ? null : name));
  }, []);

  const handleBackToAbout = useCallback(() => {
    setAboutMode(true);
    setSelectedDistrict(null);
  }, []);

  const handleClosePanel = useCallback(() => {
    setSelectedDistrict(null);
    setAboutMode(false);
  }, []);

  const { data: timelineEvents, isLoading, error } = useGetTimelineQuery();

  const sortedTimeline = useMemo(() => {
    if (!timelineEvents) return [];
    return [...timelineEvents].sort((a, b) => a.year - b.year);
  }, [timelineEvents]);

  const sortedYears = useMemo(() => {
    if (!timelineEvents) return [];

    return Array.from(new Set(timelineEvents.map(e => e.year)))
      .sort((a, b) => a - b)
      .map(String);
  }, [timelineEvents]);

  return (
    <PublicLayout>
      <section className={styles['hero-wrapper']}>
        <div className={styles['hero-bg']}>
          
        </div>
        <div className={styles['hero-content']}>
            <h1 className={styles['left-title']}>Чкаловский</h1>
            <h1 className={styles['right-title']}>Район</h1>
            <p className='text-big'>Район, где хочется <span className={styles['emoji']}><img src="/image/homePage/emoji/people.png" alt="" /></span> гулять, <span className={styles['emoji']}><img src="/image/homePage/emoji/eyes.png" alt="" /></span> разглядывать детали и чувствовать <span className={styles['emoji']}><img src="/image/homePage/emoji/heart+clock.png" alt="" /></span> время!</p>
        </div>
        <div className={styles['city-bg']}></div>
      </section>
      <section id='map' className={styles['map-wrapper']}>
        <div className={`${styles['map-content']} ${(selectedDistrict || aboutMode) ? styles['map-content--modal-open'] : ''}`}>
          <div className={styles['map-title']}>
            <h4>КАРТА РАЙОНА</h4>
            <p className='text-medium'>Исследуй Чкаловский на карте. Найди скверы, заводы, школы и знаковые места — открой район заново.</p>
          </div>
          <div className={`${styles['map']} ${(selectedDistrict || aboutMode) ? styles['map--shifted'] : ''}`}>
            <DistrictPanel
              districtName={selectedDistrict}
              aboutMode={aboutMode}
              onClose={handleClosePanel}
              onSelectDistrict={handleDistrictClick}
              onBackToAbout={handleBackToAbout}
            />
            <div className={`${styles['map-inner']} ${(selectedDistrict || aboutMode) ? styles['map-inner--shifted'] : ''}`}>
              <button
                className={`${styles['about-map']} ${aboutMode ? styles['active'] : ''}`}
                onClick={toggleAbout}
              >
                <h6>О КАРТЕ</h6>
              </button>
              <InteractiveMap
                selectedDistrict={selectedDistrict}
                onDistrictClick={handleDistrictClick}
              />
            </div>
          </div>
        </div>
      </section>
      <section id='history' className={styles['timeline-wrapper']}>
        <div className={styles['history-title']}>
          <h4>НАША ИСТОРИЯ</h4>
          <p className='text-standart'>
            Хроника Чкаловского: от заводов <br />
            до небоскребов. Главные события района 
            на временной линии.
          </p>
        </div>
        <div className={styles['timeline-content']}>
          {isLoading && <p>Загрузка таймлайна...</p>}
          {error && <p>Ошибка при загрузке данных</p>}
          <div className={styles['years-nav']}>
            {sortedYears.map((year) => (
              <Link to={`/#${year}`}>
                <div className={styles['year']}>
                  <h6>{year}</h6>
                </div>
              </Link>
            ))}
          </div>
          <div className={styles['timeline-list']}>
            {sortedTimeline.map((event, index) => {
              const vectors = [
                '/image/homePage/vectors/orange-vector.png',
                '/image/homePage/vectors/red-vector.png',
                '/image/homePage/vectors/white-vector.png'
              ];
              
              return (
                <div 
                  id={event.year.toString()} 
                  key={event.id} 
                  className={`${styles['timeline-item']} ${styles[`timeline-item-${(index % 3) + 1}`]}`}
                >
                  <img src={vectors[index % 3]} className={styles['card-vector']} alt="" />
                  <div className={styles['year-title']}>
                    {(index % 3 + 1 == 2) && (
                      <> 
                        <h2>—{event.year}</h2>
                      </>
                    )}
                    {(index % 3 + 1 != 2) && (
                      <> 
                        <h2>{event.year}—</h2>
                      </>
                    )}
                    <p>{event.text}</p>
                  </div>
                  {event.image && (
                    <img src={resolveBackendUrl(event.image)} alt='Изображение года' />
                  )}
                </div>
              );
            })}
          </div>
        </div>
      </section>
    </PublicLayout>
  );
};
