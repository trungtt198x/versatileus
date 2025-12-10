# Setup localhost dev

Run the following cmds to setup localhost dev.

## Install Python and its venv

```bash
sudo apt upgrade -y
sudo apt install python3 python3-pip python3-venv -y
sudo apt install -y python3-dev build-essential
sudo apt install -y libffi-dev libssl-dev
```

## Install deps

```bash
cd versatileus
python3 -m venv venv
venv/bin/python -m pip install -r requirements.txt
```

**Notice**

If encountering error related to `aiohttp`, comment it out in the file `requirements.txt` and then run the below cmds:

```bash
venv/bin/python -m pip install --only-binary=:all: aiohttp
venv/bin/python -m pip install -r requirements.txt
```

## Start the bot on localhost

```bash
./versatileus-bot.sh
```