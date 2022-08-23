
# Daily reports bot

This bot will help different companies working with employees to receive daily reports on the work done
## Features

- Sending reports directly to bot
- Daily summary for the manager
- Generating pages on the Telegraph


## Tech Stack


Aiogram3,
Aiogram-dialog,
Asyncpg,
PostgreSQL,
Redis,
Telegram,



## Environment Variables

To run this project, you will need to add the following environment variables to your .ini file

`BOT_TOKEN`

`REDIS_DSN`

`POSTGRES_DSN`


## Run Locally

Clone the project

```bash
  git clone https://github.com/hum4noidx/frt_report
```

Go to the project directory

```bash
  cd frt_report
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the bot

```bash
  python bot.py
```

