from datetime import date, datetime, timedelta
from typing import Generator

import requests

from .models import ElectricityPrice

BASE_URL = "https://www.elprisenligenu.dk/api/"


class Client:

    HEADERS = {
        "Content-Type": "application/json",
    }

    def __init__(self, version: str = "v1"):
        self.base_url = BASE_URL
        self.version = version

    def _get(
        self,
        endpoint: str,
        params: dict = {},
    ) -> list[ElectricityPrice]:

        today = date.today()

        year = params.get("year", today.year)
        month = params.get("month", today.month)
        day = params.get("day", today.day)
        area = params.get("area", "DK1")

        url = f"{self.base_url}/{self.version}/{endpoint}/{year}/{month}-{day}_{area}.json"

        response = requests.get(url, headers=self.HEADERS)
        if not response.ok:
            response.raise_for_status()

        response = response.json()

        if not isinstance(response, list):
            response = [response]

        data = [
            ElectricityPrice(
                dkk_per_kwh=item["DKK_per_kWh"],
                eur_per_kwh=item["EUR_per_kWh"],
                exchange_rate=item["EXR"],
                start=datetime.strptime(item["time_start"], "%Y-%m-%dT%H:%M:%S%z"),
                end=datetime.strptime(item["time_end"], "%Y-%m-%dT%H:%M:%S%z"),
            )
            for item in response
        ]
        return data

    def get_prices(
        self,
        start: date | None = None,
        end: date | None = None,
        area: str = "DK1",
    ) -> Generator[ElectricityPrice]:
        if start is None:
            start = date.today()
        if end is None:
            end = date.today()

        while start <= end:
            params = {
                "area": area,
                "year": f"{start.year:04d}",
                "month": f"{start.month:02d}",
                "day": f"{start.day:02d}",
            }
            yield from self._get(endpoint="prices", params=params)
            start += timedelta(days=1)
