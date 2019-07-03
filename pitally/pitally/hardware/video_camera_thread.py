import time
import threading
import logging
import traceback
import os
from io import BytesIO


class PiCameraVideoThread(threading.Thread):

    def __init__(self,
                 resolution,
                 video_prefix,
                 video_root_dir,
                 fps,
                 bitrate,
                 duration,
                 start_time=time.time(),
                 clip_duration=60 * 5,
                 end_of_clip_hardware_controller=None):

        self._resolution = resolution
        self._fps = fps
        self._bitrate = bitrate
        self._video_prefix = video_prefix
        self._video_root_dir = video_root_dir
        self._stop_vid = None
        self._last_image = None
        self._duration = duration
        self._start_time = start_time
        self._clip_duration = clip_duration
        self._end_of_clip_hardware_controller = end_of_clip_hardware_controller
        if duration <= 0:
            self._has_duration = False
        else:
            self._has_duration = True
        super(PiCameraVideoThread, self).__init__()
    def get_picam_instance(self):
        import picamera
        picam = picamera.PiCamera()
        return picam

    def _make_video_name(self, i, part=True):
        w, h = self._resolution
        part_pref = ""
        if part:
            part_pref = "part_"
        video_info= "%ix%i@%i" % (w, h, self._fps)
        return '%s_%s_%05d.h264' % (os.path.join(self._video_root_dir, part_pref + self._video_prefix), video_info, i)

    def _rename_part_file(self, i):
        os.rename(self._make_video_name(i - 1), self._make_video_name(i - 1, part=False))  # the final file

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

        while time.time() < self._start_time:
            time.sleep(1)
            if self._stop_vid:
                logging.warning("Video stopped before scheduled start (at %i)" % self._start_time)
                return

        picam = None
        try:
            i = 0
            if self._end_of_clip_hardware_controller:
                self._end_of_clip_hardware_controller.send(i)
            # picam = self._camera.picam
            picam = self.get_picam_instance()
            time.sleep(1)
            picam.framerate = self._fps
            picam.resolution = self._resolution
            picam.start_recording(self._make_video_name(i), bitrate=self._bitrate)

            logging.debug("recording %s" % (self._make_video_name(i),))
            logging.debug(os.getcwd())
            logging.debug("Planned duration = %i" % self._duration)

            # self._write_video_index()
            # start_time_chunk = time.time()
            # i += 1

            while not self._stop_vid:
                picam.wait_recording(2)
                my_stream = BytesIO()
                picam.capture(my_stream, format="jpeg", use_video_port=True, quality=75)
                self._last_image = my_stream

                if time.time() > self._start_time + (i + 1) * self._clip_duration:
                    i += 1
                    if self._end_of_clip_hardware_controller:
                        self._end_of_clip_hardware_controller.send(i)
                    logging.info("Making new chunk: %i" % (i,))
                    picam.split_recording(self._make_video_name(i))
                    self._rename_part_file(i)
                if self._has_duration and (time.time() - self._start_time) > self._duration:
                    logging.debug("Reached max duration, stopping")
                    self.stop_video()

            picam.wait_recording(1)
            picam.stop_recording()
            self._rename_part_file(i + 1)
            picam.close()

        except Exception as e:
            logging.error('Critical camera failure!!!')
            logging.error(traceback.format_exc(chain=e))
            if picam is not None:
                picam.stop_recording()

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
        from pitally.hardware.camera import DummyCamera
        logging.info("capturing snapshot for preview")
        DummyCamera().make_jpeg_buffer(stream, self._resolution)


class DummyCameraVideoThread(PiCameraVideoThread):
    def get_picam_instance(self):
        return DummyPiCam()

    def _rename_part_file(self, i):
        logging.info("%s -> %s", self._make_video_name(i - 1), self._make_video_name(i - 1, part=False))  # the final file

