#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
YANDEX_API_KEY = os.getenv("YANDEX_API_KEY")
ORS_API_KEY = os.getenv("ORS_API_KEY")
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))

ADMIN_LOGIN = os.getenv("ADMIN_LOGIN", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

YANDEX_GEOCODER_URL = "https://geocode-maps.yandex.ru/1.x/"
ORS_URL = "https://api.openrouteservice.org/v2/directions/driving-car"
ORS_OPTIMIZATION_URL = "https://api.openrouteservice.org/optimization"

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN .env faylida ko'rsatilmagan!")
if not YANDEX_API_KEY:
    raise ValueError("YANDEX_API_KEY .env faylida ko'rsatilmagan!")
if not ORS_API_KEY:
    raise ValueError("ORS_API_KEY .env faylida ko'rsatilmagan!")
if not ADMIN_ID:
    raise ValueError("ADMIN_ID .env faylida ko'rsatilmagan!")