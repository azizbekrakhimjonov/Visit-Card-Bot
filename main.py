import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InputFile
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove

from buttons import result, start_button, cancel_button
from config import token
from image_crop import create_visitCard

logging.basicConfig(level=logging.INFO)

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# (fullname, job, phone, email, address, website):

class FSMAdmin(StatesGroup):
    fullname = State()
    job = State()
    phone = State()
    email = State()
    address = State()
    website = State()
    photo = State()
    make = State()


async def cm_start(message: types.Message):
    await FSMAdmin.fullname.set()
    await message.reply("Enter Fullname:", reply_markup=cancel_button)


async def load_id(message: types.Message, state: FSMContext):
    if message.text == 'Cancel':
        await message.answer('Bot ready create new Card', reply_markup=ReplyKeyboardRemove())
        await cm_start(message)
    else:
        await state.update_data(fullname=message.text.strip())
        await FSMAdmin.next()
        await message.reply("Enter your job:")


async def load_job(message: types.Message, state: FSMContext):
    if message.text == 'Cancel':
        await message.answer('Bot ready create new Card', reply_markup=ReplyKeyboardRemove())
        await cm_start(message)
    else:
        await state.update_data(job=message.text.strip())
        await FSMAdmin.next()
        await message.reply("Enter your phone:")


async def load_phone(message: types.Message, state: FSMContext):
    if message.text == 'Cancel':
        await message.answer('Bot ready create new Card', reply_markup=ReplyKeyboardRemove())
        await cm_start(message)
    else:
        await state.update_data(phone=message.text.strip())
        await FSMAdmin.next()
        await message.reply("Enter your email:")


async def load_email(message: types.Message, state: FSMContext):
    if message.text == 'Cancel':
        await message.answer('Bot ready create new Card', reply_markup=ReplyKeyboardRemove())
        await cm_start(message)
    else:
        await state.update_data(email=message.text.strip())
        await FSMAdmin.next()
        await message.reply("Enter your address:")


async def load_address(message: types.Message, state: FSMContext):
    if message.text == 'Cancel':
        await message.answer('Bot ready create new Card', reply_markup=ReplyKeyboardRemove())
        await cm_start(message)
    else:
        await state.update_data(address=message.text.strip())
        await FSMAdmin.next()
        await message.reply("Enter your website:")


async def load_website(message: types.Message, state: FSMContext):
    if message.text == 'Cancel':
        await message.answer('Bot ready create new Card', reply_markup=ReplyKeyboardRemove())
        await cm_start(message)
    else:
        await state.update_data(website=message.text.strip())
        await FSMAdmin.next()
        await message.reply("Send your photo:")


async def load_photo(message: types.Message, state: FSMContext):
    if message.text == 'Cancel':
        await message.answer('Bot ready create new Card', reply_markup=ReplyKeyboardRemove())
        await cm_start(message)
    else:
        async with state.proxy() as data:
            # f = data['fullname']
            # await message.photo[-1].download(destination_file=f"{f}.jpg", make_dirs=False)
            # await state.update_data(photo=message.photo[0].file_id)
            # create_visitCard(data['fullname'], data['job'])

            f = data['fullname']
            photo_id = message.photo[-1].file_id  # Get the file_id of the last photo
            file_info = await bot.get_file(photo_id)
            photo_path = file_info.file_path

            downloaded_file = await bot.download_file(photo_path)
            with open(f"{f}.jpg", 'wb') as new_file:
                new_file.write(downloaded_file.read())

            await state.update_data(photo=photo_id)
            create_visitCard(data['fullname'], data['job'], data['phone'], data['email'], data['address'],
                             data['website'])

        await FSMAdmin.next()
        await message.reply("Congratulations! Click to «Get Visit Card»", reply_markup=result)


async def load_make(message: types.Message, state: FSMContext):
    if message.text == 'Get Visit Card':
        async with state.proxy() as data:
            try:
                print("Image is sending...")
                with open(f'{data["fullname"]}.png', 'rb') as fg:
                    await bot.send_document(message.chat.id, InputFile(fg))
                with open('2.png', 'rb') as fg2:
                    await bot.send_document(message.chat.id, InputFile(fg2))

            except Exception as e:
                print(f"An error: {str(e)}")
                await message.answer('Some error to image', reply_markup=ReplyKeyboardRemove())
                await cm_start(message)

        await message.answer('/start', reply_markup=start_button)
        os.system(f'rm {data["fullname"]}.png')
        await state.finish()
        print("Image is deleting...")


def register_handler_admin(dp1: Dispatcher):
    dp1.register_message_handler(cm_start, commands=['start'], state=None)  # start
    dp1.register_message_handler(load_id, state=FSMAdmin.fullname)  # fullname
    dp1.register_message_handler(load_job, state=FSMAdmin.job)  # job
    dp1.register_message_handler(load_phone, state=FSMAdmin.phone)  # phone
    dp1.register_message_handler(load_email, state=FSMAdmin.email)  # email
    dp1.register_message_handler(load_address, state=FSMAdmin.address)  # address
    dp1.register_message_handler(load_website, state=FSMAdmin.website)  # website
    dp1.register_message_handler(load_photo, state=FSMAdmin.photo, content_types="photo")  # photo
    dp1.register_message_handler(load_make, state=FSMAdmin.make)  # make


if __name__ == '__main__':
    from aiogram import executor

    register_handler_admin(dp)
    executor.start_polling(dp, skip_updates=True)
