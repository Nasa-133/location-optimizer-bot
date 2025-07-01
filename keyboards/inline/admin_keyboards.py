#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Admin panel uchun inline klaviaturalar
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data.texts import (
    BTN_ADMIN_USERS, BTN_ADMIN_BROADCAST,
    BTN_ADMIN_KEYWORDS, BTN_ADMIN_BACK
)


def get_admin_main_keyboard() -> InlineKeyboardMarkup:

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=BTN_ADMIN_USERS, callback_data="admin_users")
        ],
        [
            InlineKeyboardButton(text=BTN_ADMIN_BROADCAST, callback_data="admin_broadcast")
        ],
        [
            InlineKeyboardButton(text=BTN_ADMIN_KEYWORDS, callback_data="admin_keywords")
        ]
    ])
    return keyboard


def get_admin_back_keyboard() -> InlineKeyboardMarkup:

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=BTN_ADMIN_BACK, callback_data="admin_back")
        ]
    ])
    return keyboard


def get_admin_users_keyboard() -> InlineKeyboardMarkup:
    """
    Foydalanuvchilar ro'yxati klaviaturasi

    Returns:
        InlineKeyboardMarkup
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📊 Statistika", callback_data="admin_stats")
        ],
        [
            InlineKeyboardButton(text="🔄 Yangilash", callback_data="admin_users")
        ],
        [
            InlineKeyboardButton(text=BTN_ADMIN_BACK, callback_data="admin_back")
        ]
    ])
    return keyboard


def get_broadcast_confirm_keyboard() -> InlineKeyboardMarkup:

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Yuborish", callback_data="broadcast_confirm"),
            InlineKeyboardButton(text="❌ Bekor qilish", callback_data="broadcast_cancel")
        ]
    ])
    return keyboard