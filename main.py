from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ChatJoinRequest,Message, user
import asyncio
from dotenv import load_dotenv
load_dotenv()
import os

bot =Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()
pending_requests = {}

async def decline(user_id:int, chat_id:int):
    await asyncio.sleep(60)

    if user_id in pending_requests:
        await bot.decline_chat_join_request(chat_id=chat_id, user_id=user_id)
        await bot.send_message(user_id, "Время вышло, заявка отклонена.")
        del pending_requests[user_id]

@dp.chat_join_request()
async def join_request(join_request:ChatJoinRequest):
    user_id = join_request.from_user.id
    chat_id = join_request.chat.id

    task = asyncio.create_task(decline(user_id,chat_id))
    pending_requests[user_id] = task

    await bot.send_message(user_id, "Вы подали заявку, напишите любое сообщение в течение 1 минуты, или заявка будет отклонена.")


@dp.message()
async def any_message(message:Message):
    user_id = message.from_user.id

    if user_id in pending_requests:
        pending_requests[user_id].cancel()
        del pending_requests[user_id]


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Shutting down')