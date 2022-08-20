from aiogram import Router, Bot
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

from tgbot.services.repository import Repo

admin_router = Router()


async def start(c: CallbackQuery, dialog_manager: DialogManager, repo: Repo, bot: Bot, **kwargs):
    await repo.add_user(c.from_user.id, c.from_user.full_name, bot.id)
    # await dialog_manager.start(MainSG.greeting, mode=StartMode.NORMAL)


def register_handlers_user(router: Router):
    router.message.register(start, commands=['start'], state='*')
