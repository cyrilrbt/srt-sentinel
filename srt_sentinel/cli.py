import asyncio
import logging

from srt_sentinel.sentinel import SRTSentinel

# Epic ASCII Art Header
ASCII_HEADER = r"""
  ██████  ██▀███  ▄▄▄█████▓     ██████ ▓█████  ███▄    █ ▄▄▄█████▓ ██▓ ███▄    █ ▓█████  ██▓
▒██    ▒ ▓██ ▒ ██▒▓  ██▒ ▓▒   ▒██    ▒ ▓█   ▀  ██ ▀█   █ ▓  ██▒ ▓▒▓██▒ ██ ▀█   █ ▓█   ▀ ▓██▒
░ ▓██▄   ▓██ ░▄█ ▒▒ ▓██░ ▒░   ░ ▓██▄   ▒███   ▓██  ▀█ ██▒▒ ▓██░ ▒░▒██▒▓██  ▀█ ██▒▒███   ▒██░
  ▒   ██▒▒██▀▀█▄  ░ ▓██▓ ░      ▒   ██▒▒▓█  ▄ ▓██▒  ▐▌██▒░ ▓██▓ ░ ░██░▓██▒  ▐▌██▒▒▓█  ▄ ▒██░
▒██████▒▒░██▓ ▒██▒  ▒██▒ ░    ▒██████▒▒░▒████▒▒██░   ▓██░  ▒██▒ ░ ░██░▒██░   ▓██░░▒████▒░██████▒
▒ ▒▓▒ ▒ ░░ ▒▓ ░▒▓░  ▒ ░░      ▒ ▒▓▒ ▒ ░░░ ▒░ ░░ ▒░   ▒ ▒   ▒ ░░   ░▓  ░ ▒░   ▒ ▒ ░░ ▒░ ░░ ▒░▓  ░
░ ░▒  ░ ░  ░▒ ░ ▒░    ░       ░ ░▒  ░ ░ ░ ░  ░░ ░░   ░ ▒░    ░     ▒ ░░ ░░   ░ ▒░ ░ ░  ░░ ░ ▒  ░
░  ░  ░    ░░   ░   ░         ░  ░  ░     ░      ░   ░ ░   ░       ▒ ░   ░   ░ ░    ░     ░ ░
      ░     ░                       ░     ░  ░         ░           ░           ░    ░  ░    ░  ░
"""

# Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger("SRT Sentinel")


async def async_main():
    print(ASCII_HEADER)
    logger.info("Starting SRT Sentinel...")

    # Validate settings
    import srt_sentinel.settings  # noqa

    sentinel = SRTSentinel()
    try:
        await sentinel.initialize()
        await sentinel.monitor()
    except Exception as e:
        logger.exception(f"Initialization failed: {e}")
    finally:
        await sentinel.obs_client.disconnect()


def main():
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        logger.info("Script terminated by user.")
