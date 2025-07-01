#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Marshrut optimallashtirish (TSP - Traveling Salesman Problem)
OpenRouteService API yordamida
"""

import requests
import logging
from typing import List, Dict, Optional, Tuple
from data.config import ORS_API_KEY, ORS_OPTIMIZATION_URL

logger = logging.getLogger(__name__)


class RouteOptimizer:
    """
    Marshrut optimallashtirish klassi
    OpenRouteService API yordamida TSP yechimi
    """

    def __init__(self):
        self.api_key = ORS_API_KEY
        self.optimization_url = ORS_OPTIMIZATION_URL
        self.headers = {
            'Authorization': self.api_key,
            'Content-Type': 'application/json'
        }

    async def optimize_route(self, addresses: List[Dict]) -> Optional[Dict]:
        """
        Manzillar ro'yxatini optimal tartibda joylash

        Args:
            addresses: Manzillar ro'yxati [{'lat': float, 'lon': float, 'address': str}, ...]

        Returns:
            Optimal marshrut ma'lumotlari yoki None
        """
        if len(addresses) < 2:
            logger.warning("Kamida 2 ta manzil kerak")
            return None

        try:
            # ORS Optimization API uchun ma'lumotlarni tayyorlash
            jobs = []
            for i, addr in enumerate(addresses):
                jobs.append({
                    "id": i + 1,
                    "location": [addr['lon'], addr['lat']],  # ORS'da [lon, lat] tartibida
                    "description": addr['address']
                })

            vehicles = [{
                "id": 1,
                "start": [addresses[0]['lon'], addresses[0]['lat']],
                "end": [addresses[0]['lon'], addresses[0]['lat']],  # Boshi va oxiri bir xil (round trip)
                "profile": "driving-car"
            }]

            # So'rov ma'lumotlari
            payload = {
                "jobs": jobs,
                "vehicles": vehicles,
                "options": {
                    "g": True  # Geometriya ma'lumotlarini ham olish
                }
            }

            # API ga so'rov yuborish
            response = requests.post(
                self.optimization_url,
                json=payload,
                headers=self.headers,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                return await self._process_optimization_result(data, addresses)
            else:
                logger.error(f"ORS API xatolik: {response.status_code} - {response.text}")
                # Agar optimization API ishlamasa, oddiy tartibda qaytarish
                return await self._fallback_route_calculation(addresses)

        except requests.RequestException as e:
            logger.error(f"ORS API so'rov xatoligi: {e}")
            return await self._fallback_route_calculation(addresses)
        except Exception as e:
            logger.error(f"Marshrut optimallashtirish xatoligi: {e}")
            return await self._fallback_route_calculation(addresses)

    async def _process_optimization_result(self, data: Dict, addresses: List[Dict]) -> Dict:
        """
        ORS Optimization natijasini qayta ishlash

        Args:
            data: ORS API javobi
            addresses: Asl manzillar ro'yxati

        Returns:
            Formatlangan marshrut ma'lumotlari
        """
        try:
            routes = data.get('routes', [])
            if not routes:
                return await self._fallback_route_calculation(addresses)

            route = routes[0]
            steps = route.get('steps', [])

            # Optimal tartibni aniqlash
            optimal_order = []
            ordered_addresses = []

            for step in steps:
                if step.get('type') == 'job':
                    job_id = step.get('job')
                    if job_id and job_id <= len(addresses):
                        optimal_order.append(job_id)
                        ordered_addresses.append(addresses[job_id - 1])

            # Masofa va vaqtni hisoblash
            total_distance = route.get('distance', 0) / 1000  # metrdan km ga
            total_duration = route.get('duration', 0) / 60  # soniyadan daqiqaga

            # Yandex Maps linki yaratish
            map_url = self._create_yandex_maps_url(ordered_addresses)

            return {
                'optimal_order': optimal_order,
                'ordered_addresses': ordered_addresses,
                'total_distance': round(total_distance, 2),
                'total_duration': round(total_duration, 1),
                'map_url': map_url,
                'route_geometry': route.get('geometry')
            }

        except Exception as e:
            logger.error(f"Optimization natijasini qayta ishlashda xatolik: {e}")
            return await self._fallback_route_calculation(addresses)

    async def _fallback_route_calculation(self, addresses: List[Dict]) -> Dict:
        """
        Oddiy marshrut hisoblash (agar optimization ishlamasa)

        Args:
            addresses: Manzillar ro'yxati

        Returns:
            Oddiy marshrut ma'lumotlari
        """
        try:
            # Oddiy tartibda qoldirish
            optimal_order = list(range(1, len(addresses) + 1))
            ordered_addresses = addresses.copy()

            # Taxminiy masofa va vaqtni hisoblash
            total_distance = await self._calculate_approximate_distance(addresses)
            total_duration = total_distance * 2  # Taxminiy vaqt (2 daqiqa/km)

            # Yandex Maps linki
            map_url = self._create_yandex_maps_url(addresses)

            return {
                'optimal_order': optimal_order,
                'ordered_addresses': ordered_addresses,
                'total_distance': round(total_distance, 2),
                'total_duration': round(total_duration, 1),
                'map_url': map_url,
                'route_geometry': None
            }

        except Exception as e:
            logger.error(f"Fallback marshrut hisoblashda xatolik: {e}")
            return None

    async def _calculate_approximate_distance(self, addresses: List[Dict]) -> float:
        """
        Taxminiy masofani hisoblash

        Args:
            addresses: Manzillar ro'yxati

        Returns:
            Taxminiy masofa (km)
        """
        if len(addresses) < 2:
            return 0.0

        total_distance = 0.0

        for i in range(len(addresses) - 1):
            current = addresses[i]
            next_addr = addresses[i + 1]

            # Haversine formulasi bilan taxminiy masofa
            distance = self._haversine_distance(
                current['lat'], current['lon'],
                next_addr['lat'], next_addr['lon']
            )
            total_distance += distance

        return total_distance

    def _haversine_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Haversine formulasi bilan ikki nuqta orasidagi masofani hisoblash

        Args:
            lat1, lon1: Birinchi nuqta koordinatalari
            lat2, lon2: Ikkinchi nuqta koordinatalari

        Returns:
            Masofa (km)
        """
        import math

        # Radianlarga aylantirish
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

        # Haversine formulasi
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.asin(math.sqrt(a))

        # Yer radiusi (km)
        r = 6371

        return c * r

    def _create_yandex_maps_url(self, addresses: List[Dict]) -> str:
        """
        Yandex Maps URL yaratish

        Args:
            addresses: Manzillar ro'yxati

        Returns:
            Yandex Maps URL
        """
        if not addresses:
            return ""

        # Koordinatalarni rtext formatiga aylantirish
        rtext_parts = []
        for addr in addresses:
            rtext_parts.append(f"{addr['lat']},{addr['lon']}")

        # Aylanma marshrut uchun boshiga qaytish
        if len(addresses) > 1:
            rtext_parts.append(f"{addresses[0]['lat']},{addresses[0]['lon']}")

        rtext = "~".join(rtext_parts)

        return f"https://yandex.com/maps/?rtext={rtext}&rtt=auto"


# Route optimizer instance
route_optimizer = RouteOptimizer()