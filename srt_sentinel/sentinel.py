import asyncio
import logging

from srt_sentinel.clients.obs import OBSClient
from srt_sentinel.clients.sls import SLSClient
from srt_sentinel.settings import BACKUP_SCENE, MAIN_SCENE, POLL_INTERVAL

logger = logging.getLogger("SRT Sentinel")


class SRTSentinel:
    def __init__(self):
        self.obs_client = OBSClient()
        self.sls_client = SLSClient()
        # Track if the feed has ever been healthy
        # we do this to avoid switching if the feed isn't live yet
        self.feed_has_been_healthy = False

    async def initialize(self) -> None:
        # Check OBS connection
        if not await self.obs_client.connect():
            raise Exception("OBS connection failed.")

        # Check SRT stats page
        stats = await self.sls_client.fetch_stats()
        if not stats:
            raise Exception("SRT stats page is unavailable.")

        logger.info("Initialization checks passed. Starting monitoring...")

    async def wait_for_main_scene(self) -> str:
        """Wait until the current scene is MAIN_SCENE."""
        while True:
            current_scene = await self.obs_client.get_current_scene()
            if current_scene == MAIN_SCENE:
                logger.info(f"Current scene is '{current_scene}'. Starting monitoring.")
                return current_scene
            else:
                logger.warning(f"Current scene is '{current_scene}'. Waiting for '{MAIN_SCENE}'...")
                await asyncio.sleep(POLL_INTERVAL)

    async def monitor(self) -> None:
        # Wait until the current scene is MAIN_SCENE
        current_scene = await self.wait_for_main_scene()

        # Start monitoring the SRT feed and media status
        while True:
            sls_healthy = await self.sls_client.is_feed_healthy()
            current_scene = await self.obs_client.get_current_scene()

            logger.info(f"Current scene: {current_scene}, SLS: {sls_healthy}")

            if sls_healthy:
                self.feed_has_been_healthy = True  # Mark the feed as healthy
                if current_scene != MAIN_SCENE:
                    logger.info(f"Switching to {MAIN_SCENE}")
                    await self.obs_client.switch_scene(MAIN_SCENE)
            else:
                # Only switch to backup scene if the feed has been healthy at least once
                if self.feed_has_been_healthy and current_scene != BACKUP_SCENE:
                    logger.info(f"Switching to {BACKUP_SCENE}")
                    await self.obs_client.switch_scene(BACKUP_SCENE)

            await asyncio.sleep(POLL_INTERVAL)
