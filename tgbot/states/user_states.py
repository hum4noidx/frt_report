from aiogram.fsm.state import StatesGroup, State


class UserGreeting(StatesGroup):
    greeting = State()


class UserMain(StatesGroup):
    main_menu = State()


class UserChange(StatesGroup):
    info = State()
    change_schedule = State()
    change_t_id = State()
    change_name = State()


class SendReport(StatesGroup):
    info = State()
    send_photo = State()
    additional_info = State()
    confirm = State()
