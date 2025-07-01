#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from aiogram.fsm.state import State, StatesGroup


class LocationStates(StatesGroup):

    waiting_location = State()

    confirming_address = State()

    adding_more = State()

    final_choice = State()


class AdminStates(StatesGroup):

    waiting_login = State()

    waiting_password = State()

    admin_panel = State()

    waiting_broadcast = State()