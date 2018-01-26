# AirMonitorBot
Telegram Bot created to display AirMonitor data, extracted
from database, collected by AirMonitorWebApp:

https://github.com/eclipse7/AirMonitorWebApp

### installation into venv (recommended):
```
virtualenv -p python3 .env #make sure you creating python3 venv
source .env/bin/activate
python3 -m pip install -r requirements.txt
```

### setup
1)open the file 'config.py.sample', enter your new database user's credentials, database name and your telegram bot API token 

2)launch the bot:
```
python3 main.py
```

