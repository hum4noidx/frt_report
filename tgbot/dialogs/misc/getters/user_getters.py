from aiogram_dialog import DialogManager

from tgbot.services.repository import Repo


class UserGetter:
    async def user_info(dialog_manager: DialogManager, **kwargs):
        repo: Repo = dialog_manager.data.get('repo')
        user_id = dialog_manager.event.from_user.id
        data = await repo.get_user(user_id)
        data = data[0]
        print(data)
        tinkoff_id = data['tinkoff_id']
        schedule = data['schedule']

        return {
            'user_id': user_id,
            'tinkoff_id': tinkoff_id,
            'user_schedule': schedule

        }

    async def get_schedules(dialog_manager: DialogManager, **kwargs):
        schedules = [['5/2', '5/2'], ['2/2', '2/2'], ['Другой', 'other']]

        return {
            'schedules': schedules
        }
