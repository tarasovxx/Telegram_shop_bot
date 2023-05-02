@echo off

call %~dp0venv\Scripts\activate

python create_bot.py
python bot_config.py

pause