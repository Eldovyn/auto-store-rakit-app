import yaml
import os
from dotenv import load_dotenv

load_dotenv()

with open("./configs/config.yaml", "r", encoding="utf8") as f:
    data = yaml.safe_load(f) or {}

# Helper to parse lists
def parse_list(val):
    if not val:
        return []
    return [int(x.strip()) if x.strip().isdigit() else x.strip() for x in val.split(",")]

def parse_int_or_str(val):
    if not val:
        return val
    if val.isdigit():
        return int(val)
    return val

# Environment mappings
env_mapping = {
    "token": ("TOKEN", str),
    "mongodb_url": ("MONGODB_URL", str),
    "username_webhook": ("USERNAME_WEBHOOK", str),
    "guild_id": ("GUILD_ID", parse_list),
    "role_admin": ("ROLE_ADMIN", parse_list),
    "role_buyer": ("ROLE_BUYER", parse_int_or_str),
    "channel_id_status": ("CHANNEL_ID_STATUS", parse_int_or_str),
    "message_id_status": ("MESSAGE_ID_STATUS", parse_int_or_str),
    "thumbnail": ("THUMBNAIL", str),
    "webhook_update_balance": ("WEBHOOK_UPDATE_BALANCE", str),
    "webhook_reputation": ("WEBHOOK_REPUTATION", str),
    "channel_reputation": ("CHANNEL_REPUTATION", parse_int_or_str),
    "mode": ("MODE", str),
    "server_key": ("SERVER_KEY", str),
    "client_key": ("CLIENT_KEY", str),
}

for key, (env_key, parser) in env_mapping.items():
    env_val = os.getenv(env_key)
    if env_val is not None:
        data[key] = parser(env_val)
    elif key not in data:
        # Provide defaults if missing
        if parser == parse_list:
            data[key] = []
        else:
            data[key] = ""

