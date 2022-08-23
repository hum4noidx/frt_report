import asyncio
import datetime

import asyncpg
from aiogram import Router, Bot, Dispatcher
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, StartMode

from tgbot.configreader import config
from tgbot.services.repository import Repo
from tgbot.services.upload_photos import create_reports_page
from tgbot.states.user_states import UserGreeting

user_router = Router()


async def start(c: CallbackQuery, dialog_manager: DialogManager, repo: Repo, bot: Bot, **kwargs):
    await repo.add_user(c.from_user.id, c.from_user.full_name)
    await dialog_manager.start(UserGreeting.greeting, mode=StartMode.NORMAL)


async def test():
    conn = await asyncpg.connect(config.postgres_dsn)
    data = await conn.fetch('SELECT users.real_name, file_id, comment, user_id '
                            'FROM user_reports '
                            'LEFT JOIN users on user_reports.user_id = users.tg_id '
                            'WHERE report_date=$1', datetime.date.today())
    # data = await repo.get_today_reports()
    asyncio.create_task(create_reports_page(data))
    # TODO: fix this


def register_handlers_user(router: Router):
    router.message.register(test, commands=['reports'], state='*')
    router.message.register(start, commands=['start'], state='*')


def schedule_jobs(dp: Dispatcher, scheduler):
    """
    Schedule jobs to execute
    """
    scheduler.add_job(test, trigger='cron', hour=23, )
