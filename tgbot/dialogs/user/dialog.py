import operator

from aiogram.types import ContentType
from aiogram_dialog import Dialog, Window, StartMode
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.kbd import Start, Cancel, SwitchTo, Select, Back, Button
from aiogram_dialog.widgets.text import Format, Const, Multi

from tgbot.dialogs.misc.getters.user_getters import UserGetter
from tgbot.dialogs.misc.on_click_funcs.user_on_click import on_schedule_change, photo_handler, on_send_report, \
    next_window, change_name
from tgbot.states.user_states import UserMain, UserGreeting, UserChange, SendReport

user_greeting = Dialog(
    Window(
        Format(
            '<b>Привет!</b>\n'
            'Мне ты можешь скидывать отчёты о закрытых встречах\n'
            '==================================\n'
            'По всем вопросам <a href="#">сюда</a>\n'),
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
            Format('<b>Твой # ID:</b> <code>{custom_id}</code>'),
            Format('<b>ФИ:</b> {real_name}'),

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
        SwitchTo(Const('Изменить ФИ'), id='change_name', state=UserChange.change_name),

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
    ),
    Window(
        Const('Введи ФИ в формате: <i>Павел Дуров</i>'),
        TextInput(id='input_name', on_success=change_name),
        Cancel(Const('Назад')),
        state=UserChange.change_name
    ),
)

user_send_report = Dialog(
    Window(
        Const(
            'На скриншоте должно быть видно, что <b>нет активных встреч</b> '
            'и все встречи находятся во вкладке <b>"Завершено"</b>\n\n'
            'По желанию можешь написать комментарий'),
        Button(Const('Отправить'), id='send_photo', on_click=next_window),
        Cancel(Const('Назад')),
        state=SendReport.info
    ),
    Window(
        Const('Пришли скриншот из your_app, на котором видно, что нет встреч в статусе "В работе"\n'
              '<b>Обрати внимание, что при повторной отправке скриншота в этот же день,'
              ' он перезапишется и руководитель получит только последний скриншот!</b>'),
        MessageInput(photo_handler, content_types=ContentType.ANY),
        Cancel(Const('Назад')),
        state=SendReport.send_photo,
    ),
    Window(
        Const('Скриншот загружен.\nМожешь добавить комментарий для руководителя или нажать кнопку "отправить отчёт"'),
        Button(Const('Отправить отчёт'), id='send_report', on_click=on_send_report),
        state=SendReport.additional_info
    ),
)
