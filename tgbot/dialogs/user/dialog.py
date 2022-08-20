import operator

from aiogram.types import ContentType
from aiogram_dialog import Dialog, Window, StartMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Start, Cancel, SwitchTo, Select, Back, Button
from aiogram_dialog.widgets.text import Format, Const, Multi

from tgbot.dialogs.misc.getters.user_getters import UserGetter
from tgbot.dialogs.misc.on_click_funcs.user_on_click import on_schedule_change, photo_handler
from tgbot.states.user_states import UserMain, UserGreeting, UserChange, SendReport

user_greeting = Dialog(
    Window(
        Format(
            '<b>Привет!</b>\n'
            'Мне ты можешь скидывать отчёты о закрытых встречах\n'
            '==================================\n'
            'По всем вопросам <a href="https://t.me/wswwvw">сюда</a>\n'),
        Start(Const('Ну давай'), id='start', state=UserMain.main_menu, mode=StartMode.NORMAL),
        state=UserGreeting.greeting,
        disable_web_page_preview=True,

    )
)
user_main_menu = Dialog(
    Window(
        Multi(
            Format('<b>Твой ID:</b> {user_id}'),
            Format('<b>Твой график:</b> {user_schedule}'),
            Format('<b>Твой Tinkoff ID:</b> <code>{tinkoff_id}</code>'),

        ),
        Start(Const('Изменить'), id='change', state=UserChange.info),
        Start(Const('Новый отчёт'), id='new_report', state=SendReport.info, mode=StartMode.NORMAL),
        getter=UserGetter.user_info,
        state=UserMain.main_menu
    ),
)

user_change_info = Dialog(
    Window(
        Format('Настройки'),
        SwitchTo(Const('Изменить расписание'), id='change_schedule', state=UserChange.change_schedule),
        Cancel(Const('Назад')),
        state=UserChange.info,
    ),
    Window(
        Const('Выбери свой график'),
        Const('<i>Скоро появится возможность выбирать дни недели</i>'),
        Select(
            Format('{item[0]}'),
            id='schedule',
            item_id_getter=operator.itemgetter(1),
            items='schedules',
            on_click=on_schedule_change
        ),
        Back(Const('Назад')),
        state=UserChange.change_schedule,
        getter=UserGetter.get_schedules
    )
)


user_send_report = Dialog(
    Window(
        Const('С недавнего времени появилось новое правило - ежедневный отчёт о закрытых сменах.\n'
              'После того как все встречи выполнены, нужно отправить отчёт в виде скриншота из приложения\n'
              'На скриншоте должно быть видно, что нет активных встреч и все встречи находятся во вкладке "Завершено"\n'
              'По желанию можешь написать комментарий'),
        state=SendReport.info
    ),
    Window(
        Const('Пришли скриншот из MAgent, на котором видно, что нет встреч в статусе "В работе"'),
        MessageInput(photo_handler, content_types=ContentType.ANY),
        Cancel(Const('Назад')),
        state=SendReport.send_photo,
    ),
    Window(
        Const('Скриншот загружен.\nМожешь добавить комментарий для руководителя или нажать кнопку "отправить отчёт"'),
        # Button(Const('Отправить отчёт'), id='send_report', on_click=),
    )
)
