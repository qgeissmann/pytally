import base64
from io import BytesIO
import time
import logging
import threading


class CameraException(Exception):
    pass

try:
    from picamera import PiCamera, PiCameraError
except ImportError:
    pass

class BaseCamera(object):
    def __init__(self):
        pass
    def capture(self, resolution,):
        raise(NotImplementedError)



class DummyCamera(BaseCamera):

    def __init__(self):
        super(DummyCamera, self).__init__()

    def make_jpeg_buffer(self, stream, resolution,
                iso=200,
                awb_gains=(1,1),
                shutter_speed=1):
        w, h = resolution
        if iso == 123:
            raise Exception("dummy exception when iso == 123")
        from PIL import Image, ImageDraw, ImageFont
        import random
        image = Image.new('RGB',
                          (w, h),
                          (0, 128, 255))
        pixels = image.load()  # create the pixel map

        for i in range(image.size[0]):  # for every col:
            for j in range(image.size[1]):  # For every row
                pixels[i, j] = (i, j, random.randint(0, 255))  # set the colour accordingly

        draw = ImageDraw.Draw(image)

        draw.text((w // 2, h // 2),
                  str(time.time() % 256)
                  )

        image.save(stream, format="JPEG")


    def capture(self, resolution,
                iso=200,
                awb_gains=(1,1),
                shutter_speed=1):

        logging.info("Capturing with:" + str({'resolution': resolution,
                                              'iso': iso,
                                              'awb_gains': awb_gains,
                                              'shutter_speed': shutter_speed,
                                              }))

        buffered = BytesIO()
        self.make_jpeg_buffer(buffered, resolution,
                                        iso=200,
                                        awb_gains=(1,1),
                                        shutter_speed=1)

        img_str = base64.b64encode(buffered.getvalue())
        time.sleep(1)
        return img_str

    # @property
    # def picam(self):
    #     return self._picam

class MyPiCamera(BaseCamera):
    def __init__(self):

        self._pi_camera = PiCamera()
        #self._pi_camera.start_preview()

        # Camera warm-up time
        time.sleep(2)
        self._pi_camera.framerate = 10
        self._pi_camera.exposure_mode = 'off'
        self._pi_camera.awb_mode = 'off'


        super(MyPiCamera,self).__init__()

    @property
    def picam(self):
        return self._pi_camera

    def __del__(self):
        self._pi_camera.close()

    def capture(self, resolution = (3280, 2464),
                iso=400,
                awb_gains=(1, 1),
                shutter_speed=50000):
        #todo raise exception if camera is recording/busy
            try:
                my_stream = BytesIO()
                self._pi_camera.awb_gains = awb_gains
                self._pi_camera.shutter_speed = shutter_speed
                self._pi_camera.resolution = resolution
                self._pi_camera.capture(my_stream, 'jpeg', quality=95)
            except PiCameraError as e:
                raise CameraException(e)

            img_str = base64.b64encode(my_stream.getvalue())
            return img_str





class PiCameraThread(threading.Thread):
    _VIDEO_CHUNCK_DURATION = 60 * 1 #s
    def __init__(self,
                 camera,
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
            picam = self._camera.picam
            #todo set fps and such at run, not init
            picam.start_recording( self._make_video_name(i), bitrate=self._bitrate)
            # self._write_video_index()
            start_time = time.time()
            #i += 1
            while not self._stop:
                picam.wait_recording(2)
                #todo store in local buffer
                my_stream = BytesIO()
                picam.capture(my_stream, use_video_port=True, quality=75)
                self._last_image = my_stream
                if time.time() - start_time >= self._VIDEO_CHUNCK_DURATION:
                    i += 1
                    picam.split_recording(self._make_video_name(i))
                    #shutil.move("part_" + self._make_video_name(i) , self._make_video_name(i))
                    start_time = time.time()

            picam.wait_recording(1)
            picam.stop_recording()

        except Exception as e:
            logging.error("Error or starting video record:" + traceback.format_exc(e))

