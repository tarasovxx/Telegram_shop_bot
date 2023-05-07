@echo off

call %~dp0venv\Scripts\activate

python App\create_bot.py
python App\bot_config.py

pause