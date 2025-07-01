#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from typing import Dict, List, Optional
import json

logger = logging.getLogger(__name__)

DATABASE = {
    'users': {},  # user_id: user_data
    'user_sessions': {},  # user_id: session_data
    'admin_sessions': {}  # user_id: admin_data
}


def init_db():
    """
    Ma'lumotlar bazasini ishga tushirish
    """
    logger.info("Ma'lumotlar bazasi (RAM dict) ishga tushirildi")
    return True


def add_user(user_id: int, username: str = None, first_name: str = None):
    """
    Yangi foydalanuvchi qo'shish
    """
    DATABASE['users'][user_id] = {
        'user_id': user_id,
        'username': username,
        'first_name': first_name,
        'addresses': [],
        'last_activity': None
    }
    logger.info(f"Yangi foydalanuvchi qo'shildi: {user_id}")


def get_user(user_id: int) -> Optional[Dict]:

    return DATABASE['users'].get(user_id)


def get_all_users() -> Dict:
    """
    Barcha foydalanuvchilarni olish
    """
    return DATABASE['users']


def update_user_addresses(user_id: int, addresses: List[Dict]):
    """
    Foydalanuvchi manzillarini yangilash
    """
    if user_id in DATABASE['users']:
        DATABASE['users'][user_id]['addresses'] = addresses
        logger.info(f"Foydalanuvchi {user_id} manzillari yangilandi")


def get_user_session(user_id: int) -> Optional[Dict]:
    """
    Foydalanuvchi sessiyasini olish
    """
    return DATABASE['user_sessions'].get(user_id, {})


def set_user_session(user_id: int, session_data: Dict):
    """
    Foydalanuvchi sessiyasini saqlash
    """
    DATABASE['user_sessions'][user_id] = session_data
    logger.info(f"Foydalanuvchi {user_id} sessiyasi saqlandi")


def clear_user_session(user_id: int):
    """
    Foydalanuvchi sessiyasini tozalash
    """
    if user_id in DATABASE['user_sessions']:
        del DATABASE['user_sessions'][user_id]
        logger.info(f"Foydalanuvchi {user_id} sessiyasi tozalandi")


def add_address_to_session(user_id: int, address_data: Dict):
    """
    Sessiyaga manzil qo'shish
    """
    session = get_user_session(user_id)
    if 'addresses' not in session:
        session['addresses'] = []

    session['addresses'].append(address_data)
    set_user_session(user_id, session)
    logger.info(f"Foydalanuvchi {user_id} sessiyasiga manzil qo'shildi")


def get_session_addresses(user_id: int) -> List[Dict]:
    """
    Sessiyadan manzillarni olish
    """
    session = get_user_session(user_id)
    return session.get('addresses', [])


def set_admin_session(user_id: int, is_authenticated: bool = False):
    """
    Admin sessiyasini o'rnatish
    """
    DATABASE['admin_sessions'][user_id] = {
        'is_authenticated': is_authenticated,
        'login_attempts': 0
    }


def get_admin_session(user_id: int) -> Optional[Dict]:
    """
    Admin sessiyasini olish
    """
    return DATABASE['admin_sessions'].get(user_id)


def is_admin_authenticated(user_id: int) -> bool:
    """
    Admin autentifikatsiya holatini tekshirish
    """
    session = get_admin_session(user_id)
    return session and session.get('is_authenticated', False)


def get_database_stats() -> Dict:
    """
    Ma'lumotlar bazasi statistikasi
    """
    return {
        'total_users': len(DATABASE['users']),
        'active_sessions': len(DATABASE['user_sessions']),
        'admin_sessions': len(DATABASE['admin_sessions'])
    }


def backup_database() -> str:
    """
    Ma'lumotlar bazasini JSON formatda eksport qilish
    """
    return json.dumps(DATABASE, ensure_ascii=False, indent=2)


def restore_database(backup_data: str) -> bool:
    """
    Ma'lumotlar bazasini JSON'dan tiklash
    """
    try:
        global DATABASE
        DATABASE = json.loads(backup_data)
        logger.info("Ma'lumotlar bazasi muvaffaqiyatli tiklandi")
        return True
    except Exception as e:
        logger.error(f"Ma'lumotlar bazasini tiklashda xatolik: {e}")
        return False