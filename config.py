"""Loyihaning barcha sozlamalari bitta joyda."""
from pathlib import Path

BOSHLANISH = "2023-01"
ARAL_BBOX = [58.0, 43.4, 61.8, 46.9]
MUYNAK = (43.77, 59.02)
RESOLUTION = 200
BULUT_CHEGARASI = 30

STAC_URL = "https://planetarycomputer.microsoft.com/api/stac/v1"
OPEN_METEO_URL = "https://archive-api.open-meteo.com/v1/archive"

PAPKA = Path(__file__).resolve().parent / "data"
CSV_FAYL = PAPKA / "aral_monthly.csv"
LOG_FAYL = PAPKA / "etl.log"

USTUNLAR = [
    "oy", "suv_maydoni_km2", "qamrov_foiz", "tasvirlar_soni", "ochiq_kunlar",
    "ortacha_harorat_c", "yogingarchilik_mm", "yangilangan",
]