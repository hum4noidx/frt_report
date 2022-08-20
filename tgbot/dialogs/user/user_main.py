from aiogram import Router, Bot
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode
from aiogram import Router, types, Bot
from aiogram.filters import ChatMemberUpdatedFilter, JOIN_TRANSITION
from tgbot.services.repository import Repo
from tgbot.states.user_states import UserGreeting

user_router = Router()


async def start(c: CallbackQuery, dialog_manager: DialogManager, repo: Repo, bot: Bot, **kwargs):
    await repo.add_user(c.from_user.id, c.from_user.full_name)
    await dialog_manager.start(UserGreeting.greeting, mode=StartMode.NORMAL)


# async def on_user_join(event: types.ChatMemberUpdated, bot: Bot):
#     print(event)
#     await bot.send_message(chat_id=event.chat.id, text="Hello, user!")


def register_handlers_user(router: Router):
    router.message.register(start, commands=['start'], state='*')
