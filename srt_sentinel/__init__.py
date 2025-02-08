import asyncio
import logging
import os

from srt_sentinel.clients.obs import OBSClient
from srt_sentinel.clients.sls import SLSClient

logger = logging.getLogger("SRT Sentinel")


class SRTSentinel:
    def __init__(self):
        self.obs_client = OBSClient()
        self.sls_client = SLSClient()
        self.main_scene = os.getenv("MAIN_SCENE")
        self.backup_scene = os.getenv("BACKUP_SCENE")
        self.poll_interval = int(os.getenv("POLL_INTERVAL"))
        # Track if the feed has ever been healthy
        # we do this to avoid switching if the feed isn't live yet
        self.feed_has_been_healthy = False

    async def initialize(self):
        # Check OBS connection
        if not await self.obs_client.connect():
            raise Exception("OBS connection failed.")

        # Check SRT stats page
        stats = await self.sls_client.fetch_stats()
        if not stats:
            raise Exception("SRT stats page is unavailable.")

        logger.info("Initialization checks passed. Starting monitoring...")

    async def wait_for_main_scene(self):
        """Wait until the current scene is MAIN_SCENE."""
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
        # Wait until the current scene is MAIN_SCENE
        current_scene = await self.wait_for_main_scene()

        # Start monitoring the SRT feed
        while True:
            stats = await self.sls_client.fetch_stats()
            if stats:
                if self.sls_client.is_feed_healthy(stats):
                    self.feed_has_been_healthy = True  # Mark the feed as healthy
                    if current_scene != self.main_scene:
                        await self.obs_client.switch_scene(self.main_scene)
                        current_scene = self.main_scene
                else:
                    # Only switch to backup scene if the feed has been healthy at least once
                    if self.feed_has_been_healthy and current_scene != self.backup_scene:
                        logger.warning("Feed is unhealthy. Switching to backup scene.")
                        await self.obs_client.switch_scene(self.backup_scene)
                        current_scene = self.backup_scene
            await asyncio.sleep(self.poll_interval)
