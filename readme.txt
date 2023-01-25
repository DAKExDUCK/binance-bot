Подготовка:

1. Открыть .env файл
2. Отредактировать значение TOKEN (Токен телеграм бота, https://t.me/BotFather)
3. Отредактировать значение admin_id (Telegram User id получателя уведомлений, https://t.me/chatIDrobot)
4. `python -m venv venv`
5. `venv\Scripts\activate.bat`
6. `pip install -r requirements.txt`


Запуск: `python main.py`

1. Указать фиатную валюту
2. Ввести желаемый price
3. Ввести баланс
4. Ввести Банки, через запятую с пробелом ('Wise, NEO, PUMB')
5. Отсканировать QR, закрыть окно с QR
6. Ожидать уведомления в телеграмм 

Список банков:
PUMB, A-Bank, Sportbank, Monobank, Wise, NEO, Bank Pivdenny, Advcash, Sense SuperApp, Izibank, Bank Vlasnyi Rakhunok