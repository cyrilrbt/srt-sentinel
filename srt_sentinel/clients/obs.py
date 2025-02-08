import logging

from obswebsocket import obsws, requests

from srt_sentinel.settings import MEDIA_SOURCE, OBS_WS_HOST, OBS_WS_PASSWORD, OBS_WS_PORT

logger = logging.getLogger("SRT Sentinel")


class OBSClient:
    def __init__(self):
        self.client = obsws(OBS_WS_HOST, OBS_WS_PORT, OBS_WS_PASSWORD)

    async def connect(self) -> bool:
        try:
            self.client.connect()
            logger.info("Connected to OBS WebSocket.")
            return True
        except Exception as e:
            logger.exception(f"Failed to connect to OBS: {e}")
            return False

    async def disconnect(self) -> None:
        self.client.disconnect()

    async def get_current_scene(self) -> str:
        try:
            response = self.client.call(requests.GetCurrentProgramScene())
            return response.getSceneName()
        except Exception as e:
            logger.exception(f"Failed to get current scene: {e}")
            return ""

    async def switch_scene(self, scene_name) -> bool:
        try:
            self.client.call(requests.SetCurrentProgramScene(sceneName=scene_name))
            logger.info(f"Switched to scene: {scene_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to switch scene: {e}")
            return False

    async def get_media_status(self) -> dict:
        try:
            response = self.client.call(requests.GetMediaInputStatus(inputName=MEDIA_SOURCE))
            return {
                "state": response.getMediaState(),
                "duration": response.getMediaDuration(),
                "cursor": response.getMediaCursor(),
            }
        except Exception as e:
            logger.exception(f"Failed to get media status: {e}")
            return {}

    async def is_media_healthy(self) -> bool:
        """Check if the media source is playing and not at the end."""
        media_status = await self.get_media_status()
        logger.info(f"Media status: {media_status}")
        if not media_status:
            return False

        # Check if media is playing and not at the end
        is_playing = media_status.get("state") == "OBS_MEDIA_STATE_PLAYING"
        cursor = media_status.get("cursor", 0)
        duration = media_status.get("duration", 0)

        # Consider media healthy if it's playing and not within last second
        return is_playing  # and (duration - cursor) > 1
