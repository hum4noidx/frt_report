from types import NoneType
from typing import Any

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.manager.protocols import ManagedDialogAdapterProto

from tgbot.services.repository import Repo


async def on_schedule_change(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    repo: Repo = manager.data.get('repo')
    await repo.update_schedule(manager.event.from_user.id, item_id)
    await c.answer('Расписание изменено', show_alert=True)
    await manager.done()


async def photo_handler(m: Message, dialog: ManagedDialogAdapterProto, manager: DialogManager):
    try:
        print(m.photo[-1].file_id)
    except NoneType:
        pass
    await manager.dialog().next()

# async def on_send_report(c: CallbackQuery, widget: Any, manager: DialogManager):
