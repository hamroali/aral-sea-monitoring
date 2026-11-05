"""Planetary Computer STAC API'dan Sentinel-2 tasvirlarini olish."""
import logging
import time

import pandas as pd
import planetary_computer
import pystac_client
from odc.stac import configure_rio
from odc.stac import load as stac_load

from config import ARAL_BBOX, BULUT_CHEGARASI, RESOLUTION, STAC_URL

log = logging.getLogger("aral_etl")

# Internet uzilishlarida GDAL o'zi ham qayta urinsin
configure_rio(cloud_defaults=True, GDAL_HTTP_MAX_RETRY="5", GDAL_HTTP_RETRY_DELAY="3")

URINISHLAR = 3   # butun oy uchun necha marta qayta urinish


def katalog_ochish():
    return pystac_client.Client.open(STAC_URL, modifier=planetary_computer.sign_inplace)


def oylik_tasvirlar(catalog, oy: str):
    """Bir oy uchun tasvirlarni yuklaydi. Qaytaradi: (dataset yoki None, tasvirlar soni)."""
    davr = pd.Period(oy, freq="M")
    vaqt = f"{davr.start_time:%Y-%m-%d}/{davr.end_time:%Y-%m-%d}"

    for urinish in range(1, URINISHLAR + 1):
        try:
            items = catalog.search(
                collections=["sentinel-2-l2a"],
                bbox=ARAL_BBOX,
                datetime=vaqt,
                query={"eo:cloud_cover": {"lt": BULUT_CHEGARASI}},
            ).item_collection()

            if len(items) == 0:
                return None, 0

            ds = stac_load(
                items,
                bands=["B03", "B08", "SCL"],
                bbox=ARAL_BBOX,
                crs="EPSG:32640",
                resolution=RESOLUTION,
                groupby="solar_day",
            )
            return ds, len(items)

        except Exception as xato:
            if urinish == URINISHLAR:
                raise
            kutish = 30 * urinish
            log.warning(f"{oy}: {urinish}-urinish muvaffaqiyatsiz ({xato}). {kutish} s dan keyin qayta...")
            time.sleep(kutish)