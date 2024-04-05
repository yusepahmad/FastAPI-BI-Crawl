import asyncio
from calendar import month_abbr

from fastapi import APIRouter, Query
from typing import Optional
from ..utils.softcode import SoftCode

router = APIRouter()


def get_date_dropdown_options_int():
    days = [str(day).zfill(2) for day in range(1, 32)]
    months_int = [str(month).zfill(2) for month in range(1, 13)]
    years = [str(year) for year in range(2020, 2030)]
    months_str = [month[:3] for month in month_abbr[1:]]

    return days, months_int, months_str, years

days, months_int, months_str, years = get_date_dropdown_options_int()


@router.get("/data_inflasi")
async def data_inflation(
        mm_start: Optional[str] = Query(None, description="Bulan Awal", enum=months_int),
        yy_start: Optional[str] = Query(None, description="Tahun Awal", enum=years),
        mm_end: Optional[str] = Query(None, description="Bulan Akhir", enum=months_int),
        yy_end: Optional[str] = Query(None, description="Tahun Akhir", enum=years),
):
    start_date = f'{mm_start}/{yy_start}' if mm_start and yy_start else None
    end_date = f'{mm_end}/{yy_end}' if mm_end and yy_end else None

    response = await SoftCode().data_inflasi(start_date, end_date)
    return response

@router.get("/data_tingkat_suku_bunga")
async def data_data_tingkat_duku_bunga(
        dd_start: Optional[str] = Query(None, description="Hari Awal", enum=days),
        mm_start: Optional[str] = Query(None, description="Bulan Awal", enum=months_int),
        yy_start: Optional[str] = Query(None, description="Tahun Awal", enum=years),
        dd_end: Optional[str] = Query(None, description="Hari Akhir", enum=days),
        mm_end: Optional[str] = Query(None, description="Bulan Akhir", enum=months_int),
        yy_end: Optional[str] = Query(None, description="Tahun Akhir", enum=years),
):
    start_date = f'{dd_start}/{mm_start}/{yy_start}' if dd_start and mm_start and yy_start else None
    end_date = f'{dd_end}/{mm_end}/{yy_end}' if dd_end and mm_end and yy_end else None

    response = await SoftCode().data_suku_bunga(start_date, end_date)
    return response


@router.get("/kurs")
async def kurs_route(
        akses: Optional[str] = Query(None, description="Pilih akses", enum=[
            "Harian", "Time Series"
        ]),
        options: Optional[str] = Query(None, description="Pilih opsi", enum=[
            "AUD", "BND", "CAD", "CHF", "CNH", "CNY", "DKK", "EUR", "GBP",
            "HKD", "JPY", "KRW", "KWD", "LAK", "MYR", "NOK", "NZD", "PGK",
            "PHP", "SAR", "SEK", "SGD", "THB", "USD", "VND"
        ]),
        dd_start: Optional[str] = Query(None, description="Hari Awal", enum=days),
        mm_start: Optional[str] = Query(None, description="Bulan Awal", enum=months_str),
        yy_start: Optional[str] = Query(None, description="Tahun Awal", enum=years),
        dd_end: Optional[str] = Query(None, description="Hari Akhir", enum=days),
        mm_end: Optional[str] = Query(None, description="Bulan Akhir", enum=months_str),
        yy_end: Optional[str] = Query(None, description="Tahun Akhir", enum=years),
):
    start_date = f'{dd_start}-{mm_start}-{yy_start}' if dd_start and mm_start and yy_start else None
    end_date = f'{dd_end}-{mm_end}-{yy_end}' if dd_end and mm_end and yy_end else None

    response = await SoftCode().kurs_data(options, akses, start_date, end_date)
    return response
