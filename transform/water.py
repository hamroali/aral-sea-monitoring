"""Sun'iy yo'ldosh tasvirlaridan suv maydonini hisoblash (NDWI)."""
from config import RESOLUTION

# SCL klasslari: 0=bo'sh, 1=nosoz, 3=bulut soyasi, 8/9=bulut, 10=sirrus
YAROQSIZ_SCL = [0, 1, 3, 8, 9, 10]


def suv_maydoni(ds, tasvirlar_soni: int) -> dict:
    if ds is None:
        return {"suv_maydoni_km2": None, "qamrov_foiz": 0.0,
                "tasvirlar_soni": 0, "ochiq_kunlar": 0}

    # 1. Bulutli va bo'sh piksellarni olib tashlaymiz
    yaroqsiz = ds["SCL"].isin(YAROQSIZ_SCL)
    green = ds["B03"].where(~yaroqsiz & (ds["B03"] > 0))
    nir = ds["B08"].where(~yaroqsiz & (ds["B08"] > 0))

    # 2. NDWI: suvda musbat, quruqlikda manfiy; oy bo'yicha median
    ndwi = ((green - nir) / (green + nir)).median(dim="time")

    # 3. Suv piksellarini sanab, km² ga aylantiramiz
    suv_piksel = int((ndwi > 0).sum())
    qamrov = float(ndwi.notnull().mean()) * 100

    return {
        "suv_maydoni_km2": round(suv_piksel * RESOLUTION ** 2 / 1_000_000, 1),
        "qamrov_foiz": round(qamrov, 1),
        "tasvirlar_soni": tasvirlar_soni,
        "ochiq_kunlar": int(ds.sizes["time"]),
    }
