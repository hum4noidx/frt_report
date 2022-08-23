import datetime
from types import NoneType
from typing import Any

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.manager.protocols import ManagedDialogAdapterProto
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.managed import ManagedWidgetAdapter

from tgbot.services.repository import Repo


async def next_window(c: CallbackQuery, widget: Any, manager: DialogManager):
    await manager.dialog().next()


async def on_schedule_change(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    repo: Repo = manager.data.get('repo')
    await repo.update_schedule(manager.event.from_user.id, item_id)
    await c.answer('Расписание изменено', show_alert=True)
    await manager.done()


async def photo_handler(m: Message, dialog: ManagedDialogAdapterProto, manager: DialogManager):
    try:
        print(m.photo[-1].file_id)
        manager.current_context().dialog_data['photo_id'] = m.photo[-1].file_id
    except NoneType:
        pass
    await manager.dialog().next()


async def on_send_report(c: CallbackQuery, widget: Any, manager: DialogManager):
    file_id = manager.current_context().dialog_data.get('photo_id', '')
    comment = manager.current_context().dialog_data.get('comment', '')

    repo: Repo = manager.data.get('repo')
    await repo.save_report_file(manager.event.from_user.id, file_id, datetime.date.today(), comment)
    # bot = Bot(token=config.bot_token, parse_mode="HTML")
    # await bot.download(file_id,
    #                    destination=f"images/{manager.event.from_user.id}_"
    #                                f"{datetime.date.today().strftime('%d.%m.%Y')}.jpg")
    # await bot.session.close()
    await c.answer('Отчёт отправлен руководителю', show_alert=True)
    await manager.done()


async def change_name(m: Message, widget: ManagedWidgetAdapter[TextInput], manager: DialogManager,
                      data: str):
    manager.show_mode = ShowMode.SEND
    repo: Repo = manager.data.get('repo')
    await repo.user_save_name(manager.event.from_user.id, m.text)
    await manager.done()
