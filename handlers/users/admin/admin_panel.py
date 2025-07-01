#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Admin panel handlerlari
Login/parol bilan kirish va admin funksiyalari
"""

import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from states.location_states import AdminStates
from utils.database.db import (
    get_all_users, get_database_stats,
    set_admin_session, get_admin_session, is_admin_authenticated
)
from keyboards.inline.admin_keyboards import (
    get_admin_main_keyboard, get_admin_back_keyboard,
    get_admin_users_keyboard, get_broadcast_confirm_keyboard
)
from data.config import ADMIN_ID, ADMIN_LOGIN, ADMIN_PASSWORD
from data.texts import (
    ADMIN_WELCOME, ADMIN_USERS_LIST, ADMIN_BROADCAST_REQUEST,
    ADMIN_BROADCAST_SUCCESS, ADMIN_ACCESS_DENIED,
    ADMIN_LOGIN_REQUEST, ADMIN_PASSWORD_REQUEST,
    ADMIN_LOGIN_SUCCESS, ADMIN_LOGIN_FAILED
)

logger = logging.getLogger(__name__)
router = Router()


@router.message(Command("admin"))
async def admin_command(message: Message, state: FSMContext):
    """
    /admin buyrug'ini qayta ishlash

    Args:
        message: Kelgan xabar
        state: FSM holati
    """
    user_id = message.from_user.id

    # Asosiy admin ID tekshiruvi
    if user_id != ADMIN_ID:
        await message.answer(ADMIN_ACCESS_DENIED)
        return

    # Admin sessiyasini tekshirish
    if is_admin_authenticated(user_id):
        # Agar autentifikatsiya qilingan bo'lsa, panelni ko'rsatish
        await show_admin_panel(message, state)
    else:
        # Login so'rash
        await state.set_state(AdminStates.waiting_login)
        await message.answer(ADMIN_LOGIN_REQUEST)


async def show_admin_panel(message: Message, state: FSMContext):
    """
    Admin panelini ko'rsatish

    Args:
        message: Xabar
        state: FSM holati
    """
    await state.set_state(AdminStates.admin_panel)

    await message.answer(
        text=ADMIN_WELCOME,
        reply_markup=get_admin_main_keyboard()
    )


@router.message(AdminStates.waiting_login, F.text)
async def handle_admin_login(message: Message, state: FSMContext):
    """
    Admin login ni qayta ishlash

    Args:
        message: Login xabari
        state: FSM holati
    """
    user_id = message.from_user.id
    login = message.text.strip()

    if login == ADMIN_LOGIN:
        # Login to'g'ri, parol so'rash
        await state.update_data(login=login)
        await state.set_state(AdminStates.waiting_password)
        await message.answer(ADMIN_PASSWORD_REQUEST)
    else:
        # Noto'g'ri login
        await message.answer(ADMIN_LOGIN_FAILED + "\n" + ADMIN_LOGIN_REQUEST)


@router.message(AdminStates.waiting_password, F.text)
async def handle_admin_password(message: Message, state: FSMContext):
    """
    Admin parolni qayta ishlash

    Args:
        message: Parol xabari
        state: FSM holati
    """
    user_id = message.from_user.id
    password = message.text.strip()

    if password == ADMIN_PASSWORD:
        # Parol to'g'ri, admin panelini ochish
        set_admin_session(user_id, True)
        await message.answer(ADMIN_LOGIN_SUCCESS)
        await show_admin_panel(message, state)

        logger.info(f"Admin {user_id} panelga kirdi")
    else:
        # Noto'g'ri parol, qaytadan login so'rash
        await state.set_state(AdminStates.waiting_login)
        await message.answer(ADMIN_LOGIN_FAILED + "\n" + ADMIN_LOGIN_REQUEST)


@router.callback_query(AdminStates.admin_panel, F.data == "admin_users")
async def admin_users(callback: CallbackQuery, state: FSMContext):
    """
    Foydalanuvchilar ro'yxatini ko'rsatish

    Args:
        callback: Callback query
        state: FSM holati
    """
    try:
        users = get_all_users()

        if not users:
            users_text = "Hech qanday foydalanuvchi yo'q"
        else:
            users_list = []
            for user_id, user_data in users.items():
                username = user_data.get('username', 'Username yo\'q')
                first_name = user_data.get('first_name', 'Ism yo\'q')
                users_list.append(f"👤 {first_name} (@{username if username else 'No username'}) - ID: {user_id}")

            users_text = "\n".join(users_list)

        full_text = ADMIN_USERS_LIST.format(users=users_text)

        await callback.message.edit_text(
            text=full_text,
            reply_markup=get_admin_users_keyboard()
        )

        await callback.answer()

    except Exception as e:
        logger.error(f"Foydalanuvchilar ro'yxatini olishda xatolik: {e}")
        await callback.answer("❌ Xatolik yuz berdi")


@router.callback_query(AdminStates.admin_panel, F.data == "admin_stats")
async def admin_stats(callback: CallbackQuery):
    """
    Ma'lumotlar bazasi statistikasi

    Args:
        callback: Callback query
    """
    try:
        stats = get_database_stats()

        stats_text = f"""
📊 Ma'lumotlar bazasi statistikasi:

👥 Jami foydalanuvchilar: {stats['total_users']}
🔄 Faol sessiyalar: {stats['active_sessions']}
🔑 Admin sessiyalar: {stats['admin_sessions']}
        """

        await callback.message.edit_text(
            text=stats_text.strip(),
            reply_markup=get_admin_users_keyboard()
        )

        await callback.answer()

    except Exception as e:
        logger.error(f"Statistika olishda xatolik: {e}")
        await callback.answer("❌ Xatolik yuz berdi")


@router.callback_query(AdminStates.admin_panel, F.data == "admin_broadcast")
async def admin_broadcast(callback: CallbackQuery, state: FSMContext):
    """
    Xabar yuborish funksiyasi

    Args:
        callback: Callback query
        state: FSM holati
    """
    await state.set_state(AdminStates.waiting_broadcast)