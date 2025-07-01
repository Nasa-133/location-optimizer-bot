#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Start handler va asosiy foydalanuvchi funksiyalari
"""

import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, Location
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from states.location_states import LocationStates
from utils.database.db import (
    add_user, get_user, set_user_session,
    add_address_to_session, get_session_addresses, clear_user_session
)
from utils.yandex_geocoder import geocoder
from utils.route_optimizer import route_optimizer
from keyboards.inline.location_keyboards import (
    get_confirm_address_keyboard, get_add_more_address_keyboard,
    get_final_choice_keyboard, get_location_request_keyboard
)
from data.texts import (
    START_MESSAGE, LOCATION_REQUEST, CONFIRM_ADDRESS,
    ADD_MORE_ADDRESS, FINAL_CHOICE, ROUTE_RESULT,
    ERROR_GEOCODING, ERROR_ROUTE, ADDRESS_ADDED, ROUTE_CALCULATING
)

logger = logging.getLogger(__name__)
router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    """
    /start buyrug'ini qayta ishlash

    Args:
        message: Kelgan xabar
        state: FSM holati
    """
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name

    # Foydalanuvchini ma'lumotlar bazasiga qo'shish
    if not get_user(user_id):
        add_user(user_id, username, first_name)
        logger.info(f"Yangi foydalanuvchi ro'yxatdan o'tdi: {user_id}")

    # Sessiyani tozalash
    clear_user_session(user_id)

    # Boshlang'ich holatga o'tish
    await state.set_state(LocationStates.waiting_location)

    await message.answer(
        text=START_MESSAGE,
        reply_markup=get_location_request_keyboard()
    )


@router.message(LocationStates.waiting_location, F.location)
async def handle_location(message: Message, state: FSMContext):
    """
    Lokatsiya xabarini qayta ishlash

    Args:
        message: Lokatsiya xabari
        state: FSM holati
    """
    user_id = message.from_user.id
    location: Location = message.location

    try:
        # Koordinatalarni manzilga aylantirish
        address = await geocoder.get_address_from_coordinates(
            location.latitude, location.longitude
        )

        if not address:
            await message.answer(ERROR_GEOCODING)
            return

        # Ma'lumotlarni holatga saqlash
        await state.update_data(
            current_address={
                'lat': location.latitude,
                'lon': location.longitude,
                'address': address
            }
        )

        # Manzilni tasdiqlashni so'rash
        await state.set_state(LocationStates.confirming_address)

        await message.answer(
            text=CONFIRM_ADDRESS.format(address=address),
            reply_markup=get_confirm_address_keyboard()
        )

    except Exception as e:
        logger.error(f"Lokatsiya qayta ishlashda xatolik: {e}")
        await message.answer(ERROR_GEOCODING)


@router.message(LocationStates.waiting_location, F.text)
async def handle_text_address(message: Message, state: FSMContext):
    """
    Matn ko'rinishidagi manzilni qayta ishlash

    Args:
        message: Matn xabari
        state: FSM holati
    """
    user_id = message.from_user.id
    address_text = message.text.strip()

    try:
        # Manzildan koordinatalarni olish
        coordinates = await geocoder.get_coordinates_from_address(address_text)

        if not coordinates:
            await message.answer(ERROR_GEOCODING + "\n\nIltimos, aniqroq manzil yozing yoki lokatsiya yuboring.")
            return

        latitude, longitude = coordinates

        # Koordinatalardan aniq manzilni qayta olish
        formatted_address = await geocoder.get_address_from_coordinates(latitude, longitude)
        final_address = formatted_address if formatted_address else address_text

        # Ma'lumotlarni holatga saqlash
        await state.update_data(
            current_address={
                'lat': latitude,
                'lon': longitude,
                'address': final_address
            }
        )

        # Manzilni tasdiqlashni so'rash
        await state.set_state(LocationStates.confirming_address)

        await message.answer(
            text=CONFIRM_ADDRESS.format(address=final_address),
            reply_markup=get_confirm_address_keyboard()
        )

    except Exception as e:
        logger.error(f"Matn manzilni qayta ishlashda xatolik: {e}")
        await message.answer(ERROR_GEOCODING)


@router.callback_query(LocationStates.confirming_address, F.data == "confirm_address_yes")
async def confirm_address_yes(callback: CallbackQuery, state: FSMContext):
    """
    Manzilni tasdiqlash - Ha

    Args:
        callback: Callback query
        state: FSM holati
    """
    user_id = callback.from_user.id

    try:
        # Holatdan ma'lumotlarni olish
        data = await state.get_data()
        current_address = data.get('current_address')

        if not current_address:
            await callback.answer("❌ Xatolik yuz berdi. Qaytadan boshlang.")
            await state.clear()
            return

        # Manzilni sessiyaga qo'shish
        add_address_to_session(user_id, current_address)

        # Keyingi holatga o'tish
        await state.set_state(LocationStates.adding_more)

        await callback.message.edit_text(
            text=f"{ADDRESS_ADDED}\n\n{ADD_MORE_ADDRESS}",
            reply_markup=get_add_more_address_keyboard()
        )

        await callback.answer()

    except Exception as e:
        logger.error(f"Manzilni tasdiqlashda xatolik: {e}")
        await callback.answer("❌ Xatolik yuz berdi")


@router.callback_query(LocationStates.confirming_address, F.data == "confirm_address_no")
async def confirm_address_no(callback: CallbackQuery, state: FSMContext):
    """
    Manzilni tasdiqlash - Yo'q

    Args:
        callback: Callback query
        state: FSM holati
    """
    # Qaytadan lokatsiya so'rash
    await state.set_state(LocationStates.waiting_location)

    await callback.message.edit_text(
        text=LOCATION_REQUEST,
        reply_markup=get_location_request_keyboard()
    )

    await callback.answer()


@router.callback_query(LocationStates.adding_more, F.data == "add_more_yes")
async def add_more_yes(callback: CallbackQuery, state: FSMContext):
    """
    Yana manzil qo'shish - Ha

    Args:
        callback: Callback query
        state: FSM holati
    """
    # Yangi manzil so'rash
    await state.set_state(LocationStates.waiting_location)

    await callback.message.edit_text(
        text="📍 Keyingi manzilni yuboring:",
        reply_markup=get_location_request_keyboard()
    )

    await callback.answer()


@router.callback_query(LocationStates.adding_more, F.data == "add_more_no")
async def add_more_no(callback: CallbackQuery, state: FSMContext):
    """
    Yana manzil qo'shish - Yo'q

    Args:
        callback: Callback query
        state: FSM holati
    """
    # Oxirgi tanlovga o'tish
    await state.set_state(LocationStates.final_choice)

    await callback.message.edit_text(
        text=FINAL_CHOICE,
        reply_markup=get_final_choice_keyboard()
    )

    await callback.answer()


@router.callback_query(LocationStates.final_choice, F.data == "final_return_here")
async def final_return_here(callback: CallbackQuery, state: FSMContext):
    """
    Oxirgi tanlov - Shu yerga qaytaman

    Args:
        callback: Callback query
        state: FSM holati
    """
    user_id = callback.from_user.id

    try:
        # Sessiyadan birinchi manzilni oxirgi sifatida qo'shish (round trip)
        addresses = get_session_addresses(user_id)

        if addresses:
            # Birinchi manzilni oxiriga qo'shish
            first_address = addresses[0].copy()
            add_address_to_session(user_id, first_address)

        await calculate_and_send_route(callback, state, user_id)

    except Exception as e:
        logger.error(f"Final return here xatoligi: {e}")
        await callback.answer("❌ Xatolik yuz berdi")


@router.callback_query(LocationStates.final_choice, F.data == "final_add_another")
async def final_add_another(callback: CallbackQuery, state: FSMContext):
    """
    Oxirgi tanlov - Boshqa manzil qo'shaman

    Args:
        callback: Callback query
        state: FSM holati
    """
    # Yangi manzil so'rash
    await state.set_state(LocationStates.waiting_location)

    await callback.message.edit_text(
        text="📍 Oxirgi manzilni yuboring:",
        reply_markup=get_location_request_keyboard()
    )

    await callback.answer()


async def calculate_and_send_route(callback: CallbackQuery, state: FSMContext, user_id: int):
    """
    Marshrut hisoblash va yuborish

    Args:
        callback: Callback query
        state: FSM holati
        user_id: Foydalanuvchi ID
    """
    try:
        # Hisoblash jarayoni haqida xabar
        await callback.message.edit_text(ROUTE_CALCULATING)

        # Sessiyadan manzillarni olish
        addresses = get_session_addresses(user_id)

        if len(addresses) < 2:
            await callback.message.edit_text("❌ Kamida 2 ta manzil kerak!")
            await state.clear()
            return

        # Marshrut optimallashtirish
        route_result = await route_optimizer.optimize_route(addresses)

        if not route_result:
            await callback.message.edit_text(ERROR_ROUTE)
            await state.clear()
            return

        # Natijani formatlash
        route_order = " → ".join([str(i) for i in route_result['optimal_order']])

        # Manzillar ro'yxatini yaratish
        addresses_list = []
        for i, addr in enumerate(route_result['ordered_addresses'], 1):
            addresses_list.append(f"{i}. {addr['address']}")

        addresses_text = "\n".join(addresses_list)

        # Yakuniy xabar
        result_text = ROUTE_RESULT.format(
            route_order=route_order,
            distance=route_result['total_distance'],
            duration=route_result['total_duration'],
            addresses=addresses_text,
            map_url=route_result['map_url']
        )

        await callback.message.edit_text(result_text)

        # Sessiyani tozalash
        clear_user_session(user_id)
        await state.clear()

        # Statistika uchun
        logger.info(f"Foydalanuvchi {user_id} uchun marshrut hisoblandi: {len(addresses)} manzil")

        await callback.answer()

    except Exception as e:
        logger.error(f"Marshrut hisoblashda xatolik: {e}")
        await callback.message.edit_text(ERROR_ROUTE)
        await state.clear()


@router.callback_query(F.data == "request_location")
async def request_location_callback(callback: CallbackQuery):
    """
    Lokatsiya so'rash callback

    Args:
        callback: Callback query
    """
    await callback.message.edit_text(LOCATION_REQUEST)
    await callback.answer()


# Boshqa xabarlarni qayta ishlash
@router.message()
async def handle_other_messages(message: Message, state: FSMContext):
    """
    Boshqa xabarlarni qayta ishlash

    Args:
        message: Kelgan xabar
        state: FSM holati
    """
    current_state = await state.get_state()

    if current_state is None:
        # Agar holatda bo'lmasa, start ga yo'naltirish
        await message.answer(
            "🎯 Botdan foydalanish uchun /start buyrug'ini bosing.",
            reply_markup=get_location_request_keyboard()
        )
    else:
        # Agar holatda bo'lsa, qo'llanma
        await message.answer(
            "📍 Iltimos, lokatsiya yuboring yoki tugmalardan foydalaning."
        )