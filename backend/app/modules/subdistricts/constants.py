from enum import Enum


class Subdistrict(str, Enum):
    VERKHNEMAKAROVSKY = "ВЕРХНЕМАКАРОВСКИЙ"
    SHABROVSKY = "ШАБРОВСКИЙ"
    GORNOSHCHITSKY = "ГОРНОЩИТСКИЙ"
    SYSERTSKY = "СЫСЕРТСКИЙ"
    SULIMOVSKY = "СУЛИМОВСКИЙ"
    RUDNY = "РУДНЫЙ"
    KHIMMASH = "ХИММАШ"
    SOLNECHNY = "СОЛНЕЧНЫЙ"
    VTORCHERMET = "ВТОРЧЕРМЕТ"
    BOTANIKA = "БОТАНИКА"
    YUZHNY = "ЮЖНЫЙ"
    SHINNY = "ШИННЫЙ"
    ELIZAVET = "ЕЛИЗАВЕТ"
    SVETLY = "СВЕТЛЫЙ"
    UKTUS = "УКТУС"
    NIZHNEISSETSKY = "НИЖНЕИССЕТСКИЙ"

    @classmethod
    def values(cls) -> tuple[str, ...]:
        return tuple(item.value for item in cls)


SUBDISTRICT_NAMES = Subdistrict.values()
SUBDISTRICT_SET = frozenset(SUBDISTRICT_NAMES)


def normalize_subdistrict_name(value: str | None) -> str | None:
    if value is None:
        return None

    normalized = value.strip().upper()
    if not normalized:
        return None

    if normalized not in SUBDISTRICT_SET:
        raise ValueError("unknown_subdistrict")

    return normalized
