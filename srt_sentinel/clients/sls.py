import logging

import aiohttp

from srt_sentinel.settings import BITRATE_THRESHOLD, SLS_PUBLISHER, SLS_STATS_URL

logger = logging.getLogger("SRT Sentinel")


class SLSClient:
    async def fetch_stats(self) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(SLS_STATS_URL) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"Failed to fetch SRT stats: {response.status}")
                    return {}

    def is_feed_healthy(self, stats: dict) -> bool:
        if not stats or stats.get("status") != "ok":
            return False

        publishers = stats.get("publishers", {})
        publisher = publishers.get(SLS_PUBLISHER)

        if not publisher:
            logger.warning(f"Publisher '{SLS_PUBLISHER}' is missing.")
            return False

        if publisher.get("bitrate", 0) < BITRATE_THRESHOLD:
            logger.warning(
                f"Publisher '{SLS_PUBLISHER}' has low bitrate: {publisher.get('bitrate')}."
            )
            return False

        return True
