import asyncio
import logging
import os

import aiohttp
from dotenv import load_dotenv
from obswebsocket import obsws, requests

# Load environment variables
load_dotenv()

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


class OBSClient:
    def __init__(self):
        self.client = obsws(
            os.getenv("OBS_WS_HOST"),
            int(os.getenv("OBS_WS_PORT")),
            os.getenv("OBS_WS_PASSWORD"),
        )

    async def connect(self):
        try:
            self.client.connect()
            logger.info("Connected to OBS WebSocket.")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to OBS: {e}")
            return False

    async def disconnect(self):
        self.client.disconnect()

    async def get_current_scene(self):
        try:
            response = self.client.call(requests.GetCurrentProgramScene())
            return response.getSceneName()
        except Exception as e:
            logger.error(f"Failed to get current scene: {e}")
            return None

    async def switch_scene(self, scene_name):
        try:
            self.client.call(requests.SetCurrentProgramScene(sceneName=scene_name))
            logger.info(f"Switched to scene: {scene_name}")
        except Exception as e:
            logger.error(f"Failed to switch scene: {e}")


class SRTClient:
    def __init__(self):
        self.url = os.getenv("SRT_STATS_URL")
        self.configured_publishers = os.getenv("CONFIGURED_PUBLISHERS").split(",")
        self.bitrate_threshold = int(os.getenv("BITRATE_THRESHOLD"))

    async def fetch_stats(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"Failed to fetch SRT stats: {response.status}")
                    return None

    def is_feed_healthy(self, stats):
        if not stats or stats.get("status") != "ok":
            return False

        publishers = stats.get("publishers", {})

        for publisher_key in self.configured_publishers:
            publisher = publishers.get(publisher_key)

            if not publisher:
                logger.warning(f"Publisher '{publisher_key}' is missing.")
                return False

            if publisher.get("bitrate", 0) < self.bitrate_threshold:
                logger.warning(
                    f"Publisher '{publisher_key}' has low bitrate: {publisher.get('bitrate')}."
                )
                return False

        return True


class SRTSentinel:
    def __init__(self):
        self.obs_client = OBSClient()
        self.srt_client = SRTClient()
        self.main_scene = os.getenv("MAIN_SCENE")
        self.backup_scene = os.getenv("BACKUP_SCENE")
        self.poll_interval = int(os.getenv("POLL_INTERVAL"))

    async def initialize(self):
        # Check OBS connection
        if not await self.obs_client.connect():
            raise Exception("OBS connection failed.")

        # Check SRT stats page
        stats = await self.srt_client.fetch_stats()
        if not stats:
            raise Exception("SRT stats page is unavailable.")

        logger.info("Initialization checks passed. Starting monitoring...")

    async def wait_for_main_scene(self):
        """Wait until the current scene is either MAIN_SCENE."""
        while True:
            current_scene = await self.obs_client.get_current_scene()
            if current_scene != self.main_scene:
                logger.info(f"Current scene is '{current_scene}'. Starting monitoring.")
                return current_scene
            else:
                logger.warning(
                    f"Current scene is '{current_scene}'. Waiting for '{self.main_scene}'..."
                )
                await asyncio.sleep(self.poll_interval)

    async def monitor(self):
        # Wait until the current scene is MAIN_SCENE or BACKUP_SCENE
        current_scene = await self.wait_for_main_scene()

        # Start monitoring the SRT feed
        while True:
            stats = await self.srt_client.fetch_stats()
            if stats:
                if self.srt_client.is_feed_healthy(stats):
                    if current_scene != self.main_scene:
                        await self.obs_client.switch_scene(self.main_scene)
                        current_scene = self.main_scene
                else:
                    if current_scene != self.backup_scene:
                        logger.warning("Feed is unhealthy. Switching to backup scene.")
                        await self.obs_client.switch_scene(self.backup_scene)
                        current_scene = self.backup_scene
            await asyncio.sleep(self.poll_interval)


async def main():
    print(ASCII_HEADER)
    logger.info("Starting SRT Sentinel...")

    sentinel = SRTSentinel()
    try:
        await sentinel.initialize()
        await sentinel.monitor()
    except Exception as e:
        logger.error(f"Initialization failed: {e}")
    finally:
        await sentinel.obs_client.disconnect()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Script terminated by user.")
