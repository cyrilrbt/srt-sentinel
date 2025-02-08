import os

from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv(override=True)

# OBS Configuration
OBS_WS_HOST: str = os.getenv("OBS_WS_HOST", "").strip()
OBS_WS_PORT: int = int(os.getenv("OBS_WS_PORT", "4455"))
OBS_WS_PASSWORD: str = os.getenv("OBS_WS_PASSWORD", "").strip()

# SRT Configuration
SLS_STATS_URL: str = os.getenv("SLS_STATS_URL", "").strip()
SLS_PUBLISHER: str = os.getenv("SLS_PUBLISHER", "").strip()
BITRATE_THRESHOLD: int = int(os.getenv("BITRATE_THRESHOLD", "500"))

# Scene Configuration
MAIN_SCENE: str = os.getenv("MAIN_SCENE", "").strip()
BACKUP_SCENE: str = os.getenv("BACKUP_SCENE", "").strip()

# Polling Interval
POLL_INTERVAL: int = int(os.getenv("POLL_INTERVAL", "10"))

# Validate Required Variables
required_env_vars = {
    "OBS_WS_HOST": OBS_WS_HOST,
    "OBS_WS_PASSWORD": OBS_WS_PASSWORD,
    "SLS_STATS_URL": SLS_STATS_URL,
    "MAIN_SCENE": MAIN_SCENE,
    "BACKUP_SCENE": BACKUP_SCENE,
}

missing_vars = [var for var, value in required_env_vars.items() if not value]
if missing_vars:
    raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
