import requests
import time
from typing import List, Dict, Any, Optional


class AeroplanesAPI:
    """Класс для работы с API Nominatim и Opensky."""

    def get_country_coordinates(self, country_name: str) -> Optional[List[float]]:
        """
        Получает boundingbox (координаты) страны через Nominatim.
        Возвращает список из 4 чисел: [south, north, west, east]
        """
        url = "https://nominatim.openstreetmap.org/search"
        params = {"q": country_name, "format": "json", "limit": 1}
        headers = {"User-Agent": "airplanes_coursework_project"}

        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            if not data:
                print(f"⚠️ Страна {country_name} не найдена")
                return None

            # В ответе приходит строка, превращаем в float
            bbox = data[0]["boundingbox"]
            return [float(coord) for coord in bbox]

        except Exception as e:
            print(f"❌ Ошибка при получении координат {country_name}: {e}")
            return None

    def get_aeroplanes(self, bbox: List[float]) -> List[List[Any]]:
        """
        Получает данные о самолетах в заданном прямоугольнике (bounding box).
        Возвращает список списков (сырые данные от opensky).
        """
        url = "https://opensky-network.org/api/states/all"
        # bbox = [south, north, west, east]
        params = {
            "lamin": bbox[0],
            "lamax": bbox[1],
            "lomin": bbox[2],
            "lomax": bbox[3]
        }

        try:
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()

            if data and 'states' in data:
                return data['states']
            return []

        except Exception as e:
            print(f"❌ Ошибка при получении самолетов: {e}")
            return []
