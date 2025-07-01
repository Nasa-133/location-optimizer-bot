#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Yandex Geocoder API bilan ishlash
Koordinatalarni manzilga aylantirish (reverse geocoding)
"""

import requests
import logging
from typing import Optional, Dict, Tuple

from data.config import YANDEX_API_KEY, YANDEX_GEOCODER_URL

logger = logging.getLogger(__name__)


class YandexGeocoder:
    """
    Yandex Geocoder API bilan ishlash klassi
    """

    def __init__(self):
        self.api_key = YANDEX_API_KEY
        self.base_url = YANDEX_GEOCODER_URL

    async def get_address_from_coordinates(self, latitude: float, longitude: float) -> Optional[str]:
        """
        Koordinatalardan manzilni olish (reverse geocoding)

        Args:
            latitude: Kenglik
            longitude: Uzunlik

        Returns:
            Manzil matni yoki None
        """
        try:
            params = {
                'apikey': self.api_key,
                'geocode': f"{longitude},{latitude}",  # Yandex'da lon,lat tartibida
                'format': 'json',
                'results': 1,
                'lang': 'uz_UZ'  # O'zbek tilida natija
            }

            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            # Javobdan manzilni ajratib olish
            try:
                geo_objects = data['response']['GeoObjectCollection']['featureMember']
                if geo_objects:
                    geo_object = geo_objects[0]['GeoObject']
                    address = geo_object['metaDataProperty']['GeocoderMetaData']['text']

                    # Manzilni tozalash va formatlash
                    address = self._format_address(address)

                    logger.info(f"Manzil topildi: {address}")
                    return address
                else:
                    logger.warning("Manzil topilmadi")
                    return None

            except (KeyError, IndexError) as e:
                logger.error(f"Javobni parsing qilishda xatolik: {e}")
                return None

        except requests.RequestException as e:
            logger.error(f"Yandex API so'rovida xatolik: {e}")
            return None
        except Exception as e:
            logger.error(f"Kutilmagan xatolik: {e}")
            return None

    async def get_coordinates_from_address(self, address: str) -> Optional[Tuple[float, float]]:
        """
        Manzildan koordinatalarni olish (direct geocoding)

        Args:
            address: Manzil matni

        Returns:
            (latitude, longitude) tuple yoki None
        """
        try:
            params = {
                'apikey': self.api_key,
                'geocode': address,
                'format': 'json',
                'results': 1,
                'lang': 'uz_UZ'
            }

            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            try:
                geo_objects = data['response']['GeoObjectCollection']['featureMember']
                if geo_objects:
                    geo_object = geo_objects[0]['GeoObject']
                    coords = geo_object['Point']['pos'].split()
                    longitude = float(coords[0])
                    latitude = float(coords[1])

                    logger.info(f"Koordinatalar topildi: {latitude}, {longitude}")
                    return latitude, longitude
                else:
                    logger.warning("Koordinatalar topilmadi")
                    return None

            except (KeyError, IndexError, ValueError) as e:
                logger.error(f"Koordinatalarni parsing qilishda xatolik: {e}")
                return None

        except requests.RequestException as e:
            logger.error(f"Yandex API so'rovida xatolik: {e}")
            return None
        except Exception as e:
            logger.error(f"Kutilmagan xatolik: {e}")
            return None

    def _format_address(self, address: str) -> str:
        """
        Manzilni formatlash va tozalash

        Args:
            address: Xom manzil

        Returns:
            Formatlangan manzil
        """
        # Yandex'dan kelgan manzilni tozalash
        if address:
            # "O'zbekiston" so'zini o'chirish
            address = address.replace("O'zbekiston, ", "")
            address = address.replace("Uzbekiston, ", "")
            address = address.replace("Uzbekistan, ", "")

            # Qo'shimcha formatlash
            address = address.strip()

            # Agar manzil juda uzun bo'lsa, qisqartirish
            if len(address) > 100:
                address = address[:97] + "..."

        return address

    async def validate_address(self, address: str) -> bool:
        """
        Manzilni tekshirish

        Args:
            address: Tekshiriladigan manzil

        Returns:
            True agar manzil to'g'ri bo'lsa
        """
        coordinates = await self.get_coordinates_from_address(address)
        return coordinates is not None


# Geocoder instance
geocoder = YandexGeocoder()