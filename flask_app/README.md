Flight Agent Backend
====================

OS Requirements
---------------
* Python 3^
* pip
* venv

Installation
------------
```bash
cd FlightAgentBack
```

```bash
git checkout develop
```

```bash
git pull
```

```bash
virtualenv -p python3 venv
```

```bash
source venv/bin/activate
```

```bash
pip install -r requirements.txt
```

Running app
-----------

```bash
python main.py
```

Running app with PM2
-----------
```bash
pm2 start --only flight_agent_back-dev
```