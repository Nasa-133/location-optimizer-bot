#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data.texts import (
    BTN_YES, BTN_NO, BTN_ADD_MORE,
    BTN_RETURN_HERE, BTN_ADD_ANOTHER
)


def get_confirm_address_keyboard() -> InlineKeyboardMarkup:

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=BTN_YES, callback_data="confirm_address_yes"),
            InlineKeyboardButton(text=BTN_NO, callback_data="confirm_address_no")
        ]
    ])
    return keyboard


def get_add_more_address_keyboard() -> InlineKeyboardMarkup:

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=BTN_ADD_MORE, callback_data="add_more_yes"),
            InlineKeyboardButton(text=BTN_NO, callback_data="add_more_no")
        ]
    ])
    return keyboard


def get_final_choice_keyboard() -> InlineKeyboardMarkup:

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=BTN_RETURN_HERE, callback_data="final_return_here")
        ],
        [
            InlineKeyboardButton(text=BTN_ADD_ANOTHER, callback_data="final_add_another")
        ]
    ])
    return keyboard


def get_location_request_keyboard() -> InlineKeyboardMarkup:

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📍 Lokatsiya yuborish", callback_data="request_location")
        ]
    ])
    return keyboard