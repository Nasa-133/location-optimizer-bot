#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bot holatlarini (States) boshqarish
FSM uchun state'lar
"""

from aiogram.fsm.state import State, StatesGroup


class LocationStates(StatesGroup):
    """
    Lokatsiya bilan ishlash uchun state'lar
    """
    # Manzil kiritish
    waiting_location = State()

    # Manzilni tasdiqlash
    confirming_address = State()

    # Keyingi manzil qo'shish
    adding_more = State()

    # Oxirgi tanlov
    final_choice = State()


class AdminStates(StatesGroup):
    """
    Admin panel uchun state'lar
    """
    # Admin login
    waiting_login = State()

    # Admin parol
    waiting_password = State()

    # Admin panel
    admin_panel = State()

    # Broadcast xabar
    waiting_broadcast = State()