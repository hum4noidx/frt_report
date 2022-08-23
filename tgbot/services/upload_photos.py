import datetime
import logging

from aiogram import Bot
from aiographfix import Telegraph

from tgbot.configreader import config

directory = 'images'

HTML = '<p>{header}</p>' \
       '<figure>' \
       '<img src="{image}" alt="missing" />' \
       '<figcaption>{comment}</figcaption>' \
       '</figure>' \
       '<br>'


async def create_reports_page(data, chat_id=657869363):
    logging.info('Start report creating')
    try:
        telegraph = Telegraph()
        today = datetime.date.today()
        await telegraph.create_account("frt-demo")
        new_html = ''
        photos_list = []
        bot = Bot(token=config.bot_token, parse_mode="HTML")

        for user_report in data:
            print(user_report)
            file_id = user_report['file_id']
            name = user_report['real_name']
            comment = user_report['comment']
            path = f"images/{user_report['user_id']}_{datetime.date.today().strftime('%d.%m.%Y')}.jpg"
            await bot.download(file_id, destination=path)
            photo = (await telegraph.upload(path, full=False))[0]
            new_html = new_html + HTML.format(image=photo, header=name, comment=comment)
            photos_list.append((await telegraph.upload(path, full=False))[0])
        page = await telegraph.create_page(f"Отчёт за {today.strftime('%d/%m/%Y')}", new_html)
        print("Created page:", page.url)
        await bot.send_message(chat_id=chat_id, text=f"Created page: {page.url}")
        await telegraph.close()
        await bot.session.close()
        return page.url
    except:
        logging.error('No photos')
