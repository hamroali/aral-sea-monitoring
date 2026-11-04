"""Open-Meteo arxiv API'dan kunlik ob-havo ma'lumotlarini olish."""
import pandas as pd
import requests

from config import MUYNAK, OPEN_METEO_URL


def kunlik_ob_havo(oylar: list[str]) -> pd.DataFrame:
    boshi = pd.Period(min(oylar), freq="M").start_time.date()
    oxiri = pd.Period(max(oylar), freq="M").end_time.date()

    javob = requests.get(
        OPEN_METEO_URL,
        params={
            "latitude": MUYNAK[0],
            "longitude": MUYNAK[1],
            "start_date": str(boshi),
            "end_date": str(oxiri),
            "daily": "temperature_2m_mean,precipitation_sum",
            "timezone": "Asia/Tashkent",
        },
        timeout=60,
    )
    javob.raise_for_status()
    return pd.DataFrame(javob.json()["daily"])