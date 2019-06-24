import logging
import time
logging.basicConfig(level=logging.DEBUG)
from pitally.hardware.video_camera_thread import DummyCameraVideoThread


d = DummyCameraVideoThread((1000,1000), "test", "/tmp", 25, 1000, 1000, clip_duration=10)
d.start()
time.sleep(60)
d.stop_video()


