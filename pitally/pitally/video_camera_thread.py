import time
import threading
import logging
import traceback
import os

from io import BytesIO


class PiCameraVideoThread(threading.Thread):
    _VIDEO_CHUNCK_DURATION = 60 * 5 #s

    def __init__(self,
                 resolution,
                 video_prefix,
                 video_root_dir,
                 fps,
                 bitrate,
                 duration):


        self._resolution = resolution
        self._fps = fps
        self._bitrate = bitrate
        self._video_prefix = video_prefix
        self._video_root_dir = video_root_dir
        self._stop_vid = None
        self._last_image = None
        self._duration = duration
        super(PiCameraVideoThread, self).__init__()
    def get_picam_instance(self):
        import picamera
        picam = picamera.PiCamera()
        return picam

    def _make_video_name(self, i):
        w, h = self._resolution
        video_info= "%ix%i@%i" % (w, h, self._fps)
        return '%s_%s_%05d.h264' % (os.path.join(self._video_root_dir, self._video_prefix), video_info, i)

    def stop_video(self):
        self._stop_vid = True

    @property
    def last_image(self):
        return self._last_image

    @property
    def video_name(self):
        return self._video_prefix

    def run(self):
        i = 0
        self._stop_vid = False
        start_time = time.time()
        try:
            # picam = self._camera.picam
            picam = self.get_picam_instance()

            time.sleep(1)

            picam.framerate = self._fps
            picam.resolution = self._resolution
            picam.start_recording(self._make_video_name(i), bitrate=self._bitrate)

            logging.debug("recording %s" % (self._make_video_name(i),))
            logging.debug(os.getcwd())
            # self._write_video_index()
            start_time_chunk = time.time()
            i += 1
            while not self._stop_vid:
                picam.wait_recording(2)
                #todo store in local buffer
                my_stream = BytesIO()
                picam.capture(my_stream, format="jpeg", use_video_port=True, quality=75)
                logging.warning("stream")
                self._last_image = my_stream

                if time.time() - start_time_chunk >= self._VIDEO_CHUNCK_DURATION:
                    picam.split_recording(self._make_video_name(i))
                    # self._write_video_index()
                    start_time_chunk = time.time()
                    i += 1
                if time.time() - start_time > self._duration:
                    self.stop_video()
                    
            picam.wait_recording(1)
            picam.stop_recording()
            picam.close()

        except Exception as e:
            logging.error(traceback.format_exc(chain=e))


class DummyPiCam(object):
    _resolution = (1260, 980)
    _framerate = 15
    def wait_recording(self, t):
        time.sleep(2)

    def start_recording(self, name, bitrate):
        logging.info("recording on %s.  bitrate = %i. resolution = %s. fps = %i!" % (name, bitrate, str(self._resolution), self._framerate))

    def split_recording(self, name):
        logging.info("split recording")

    def stop_recording(self):
        logging.info("stop recording")

    def close(self):
        logging.info("closing cam")

    def capture(self, stream, format, use_video_port, quality):
        from pitally.camera import DummyCamera
        logging.info("capturing snapshot for preview")
        DummyCamera().make_jpeg_buffer(stream, self._resolution)

class DummyCameraVideoThread(PiCameraVideoThread):

    def get_picam_instance(self):
        return DummyPiCam()
