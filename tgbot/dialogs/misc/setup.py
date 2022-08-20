from aiogram import Dispatcher, Router
from aiogram_dialog import DialogRegistry

from tgbot.dialogs.user import dialog


def setup_dialogs(dp: Dispatcher):
    dialogs_router = Router()
    dp.include_router(dialogs_router)
    registry = DialogRegistry(dp)
    for _ in [
        dialog.user_greeting,
        dialog.user_main_menu,
        dialog.user_change_info,
        dialog.user_send_report

    ]:
        registry.register(_, router=dialogs_router)
