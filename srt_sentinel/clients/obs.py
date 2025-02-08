import logging

from obswebsocket import obsws, requests

from srt_sentinel.settings import OBS_WS_HOST, OBS_WS_PASSWORD, OBS_WS_PORT

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
