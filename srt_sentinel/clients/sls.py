import logging

import aiohttp

from srt_sentinel.settings import BITRATE_THRESHOLD, SLS_PUBLISHER, SLS_STATS_URL

logger = logging.getLogger("SRT Sentinel")


class SLSClient:
    """
    Example response:
    {
        "publishers": {
            "publish/live/feed1": {
                "bitrate": 697,
                "bytesRcvDrop": 0,
                "bytesRcvLoss": 382160,
                "mbpsBandwidth": 9.564,
                "mbpsRecvRate": 1.2892594018958692,
                "msRcvBuf": 2944,
                "pktRcvDrop": 0,
                "pktRcvLoss": 281,
                "rtt": 15.742,
                "uptime": 7
            }
        },
        "status": "ok"
    }

    """

    async def fetch_stats(self) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(SLS_STATS_URL) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"Failed to fetch SRT stats: {response.status}")
                    return {}

    async def is_feed_healthy(self) -> bool:
        stats = await self.fetch_stats()

        if not stats or stats.get("status") != "ok":
            return False

        publishers = stats.get("publishers", {})
        publisher = publishers.get(SLS_PUBLISHER)

        if not publisher:
            return False

        logger.info(f"SLS stats: {publisher}")

        if publisher.get("bitrate", 0) < BITRATE_THRESHOLD:
            logger.warning(
                f"Publisher '{SLS_PUBLISHER}' has low bitrate: {publisher.get('bitrate')}."
            )
            return False

        return True
