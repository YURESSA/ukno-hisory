import { useState, useRef, useCallback } from 'react';
import styles from './InteractiveMap.module.css';
import { District, DISTRICTS } from './districts';

interface InteractiveMapProps {
  selectedDistrict: string | null;
  onDistrictClick: (districtName: string) => void;
}

export const InteractiveMap = ({ selectedDistrict, onDistrictClick }: InteractiveMapProps) => {
  const [hoveredDistrict, setHoveredDistrict] = useState<string | null>(null);
  const [tooltip, setTooltip] = useState<{ x: number; y: number; name: string } | null>(null);
  const svgRef = useRef<SVGSVGElement>(null);

  const handleMouseMove = useCallback((e: React.MouseEvent<SVGPolygonElement>, district: District) => {
    const svgEl = svgRef.current;
    if (!svgEl) return;
    const rect = svgEl.getBoundingClientRect();
    setTooltip({
      x: e.clientX - rect.left,
      y: e.clientY - rect.top - 16,
      name: district.name,
    });
  }, []);

  const handleMouseEnter = useCallback((district: District) => {
    setHoveredDistrict(district.id);
  }, []);

  const handleMouseLeave = useCallback(() => {
    setHoveredDistrict(null);
    setTooltip(null);
  }, []);

  const handleClick = useCallback((district: District) => {
    onDistrictClick(district.id);
  }, [onDistrictClick]);

  return (
    <div className={styles['map-container']}>
      <svg
        ref={svgRef}
        className={styles['interactive-svg']}
        viewBox="0 0 1094 702"
        xmlns="http://www.w3.org/2000/svg"
        aria-label="Интерактивная карта Чкаловского района"
      >
        <image
          href="/image/homePage/interact-map.svg"
          x="0"
          y="0"
          width="1094"
          height="702"
          preserveAspectRatio="xMidYMid meet"
        />

        {DISTRICTS.map((district) => {
          const isSelected = selectedDistrict === district.id;
          const isHovered = hoveredDistrict === district.id;

          return (
            <polygon
              key={district.id}
              points={district.points}
              className={`${styles['district-polygon']} ${
                isSelected ? styles['district-polygon--selected'] : ''
              } ${isHovered && !isSelected ? styles['district-polygon--hover'] : ''}`}
              onMouseEnter={() => handleMouseEnter(district)}
              onMouseMove={(e) => handleMouseMove(e, district)}
              onMouseLeave={handleMouseLeave}
              onClick={() => handleClick(district)}
              role="button"
              aria-label={district.name}
              aria-pressed={isSelected}
              tabIndex={0}
              onFocus={() => handleMouseEnter(district)}
              onBlur={handleMouseLeave}
              onKeyDown={(e) => e.key === 'Enter' && handleClick(district)}
            />
          );
        })}
      </svg>

      {tooltip && !selectedDistrict && (
        <div
          className={styles['tooltip']}
          style={{ left: tooltip.x, top: tooltip.y }}
          aria-live="polite"
        >
          {tooltip.name}
        </div>
      )}
    </div>
  );
};
