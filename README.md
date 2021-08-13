# Telegram BDateBot

[![Version](https://img.shields.io/badge/version-0.1-red.svg)](https://github.com/Leucist/te_bdatebot)
[![author](https://img.shields.io/badge/author-leucist-blue)](https://github.com/Leucist/)

> Author: [leucist](https://github.com/Leucist)

This is an [aiogram](https://docs.aiogram.dev/en/latest/) Python bot for Telegram\
The aim of this bot is to simply inform when some of your friends have birthday that day (or later).\
Users are able to add their friends' information to the database (unique for each user) through the bot and then get notified when someone from the list has birthday.
```diff 
! Heroku, the server I will probably use, 
! doesn't support adequate data saving in databases.
! JSON as well. So the way of data saving shall be changed later
```
'config.py' file is required.\
'config.py':
```python
TOKEN = # bot token from BotFather. String
admin_id = # Telegram id of the admin. Integer
```
