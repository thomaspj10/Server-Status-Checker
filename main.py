import requests
import time
import json
import os.path
from enum import StrEnum
from typing import Any

class Color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class ConfigField(StrEnum):
    NOTIFICATION_WEBHOOK = "notification_webhook"
    SERVERS = "servers"

CONFIG_FILE = "config.json"
REQUIRED_CONFIG_FIELDS = [ConfigField.NOTIFICATION_WEBHOOK, ConfigField.SERVERS]

if not os.path.exists(CONFIG_FILE):
    print(Color.FAIL + f"Json file {CONFIG_FILE} does not exist. Creating a new one.." + Color.ENDC)

    with open(CONFIG_FILE, "w") as f:
        json.dump({
            ConfigField.NOTIFICATION_WEBHOOK: "",
            ConfigField.SERVERS: []
        }, f, indent=4)

    exit()

with open(CONFIG_FILE, "r") as f:
    config: list[dict[str, Any]] = json.load(f)

for field in REQUIRED_CONFIG_FIELDS:
    if field not in config:
        print(Color.FAIL + f"Field '{field}' is missing in {CONFIG_FILE}." + Color.ENDC)
        exit()

notification_webhook = config[ConfigField.NOTIFICATION_WEBHOOK]
servers = config[ConfigField.SERVERS]

for server in servers:
    available = True
    try:
        response = requests.get(server)

        if response.status_code != 200:
            available = False
    except Exception:
        available = False

    if not available:
        try:
            requests.post(notification_webhook, data={
                "content": f"@everyone\n\nUnable to reach **{server}**."
            })
        except Exception as e:
            print(e)

    time.sleep(0.5)
