import time
import threading
import picamera

class PiCameraVideoThread(threading.Thread):
    _VIDEO_CHUNCK_DURATION = 60 * 5 #s
    def __init__(self,
                 video_prefix,
                 video_root_dir,
                 fps,
                 bitrate):
        self._camera = camera
        self._fps = fps
        self._bitrate = bitrate
        self._video_prefix = video_prefix
        self._video_root_dir = video_root_dir
        self._stop = None
        self._last_image = None
        super(PiCameraThread, self).__init__()

    def _make_video_name(self, i):
        w, h = 1, 2 #fixme
        video_info= "%ix%i@%i" %(w, h, self._fps)
        return '%s_%s_%05d.h264' % (self._video_prefix, video_info, i)

    def stop(self):
        self._stop = True

    @property
    def last_image(self):
        return self._last_image

    def run(self):
        i = 0
        self._stop = False
        try:
            # picam = self._camera.picam
            picam = picamera.PiCamera()
            time.sleep(1)
            #todo set fps and such at run, not init
            picam.start_recording(self._make_video_name(i), bitrate=self._bitrate)
            # self._write_video_index()
            start_time = time.time()
            i += 1
            while not self._stop:
                picam.wait_recording(2)
                #todo store in local buffer
                my_stream = BytesIO()
                picam.capture(my_stream, use_video_port=True, quality=75)
                self._last_image = my_stream

                if time.time() - start_time >= self._VIDEO_CHUNCK_DURATION:
                    picam.split_recording(self._make_video_name(i))
                    # self._write_video_index()
                    start_time = time.time()
                    i += 1

            picam.wait_recording(1)
            picam.stop_recording()

        except Exception as e:
            pass #todo
#            logging.error("Error or starting video record:" + traceback.format_exc(e))

#from pitally.camera import  MyPiCamera

import time

cam = MyPiCamera()

cam.capture(resolution=(1280, 960))

video_recording_thread = PiCameraThread(None, "/tmp/", "my_video", 25, 500000)

video_recording_thread.run()

while True:
    time.sleep(1)
    print("yo")
