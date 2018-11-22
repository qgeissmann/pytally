import base64
from io import BytesIO
import time
import logging

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
    def capture(self, resolution,
                iso=200,
                awb_gains=(1,1),
                shutter_speed=1):

        logging.info("Capturing with:" + str({'resolution': resolution,
                                              'iso': iso,
                                              'awb_gains': awb_gains,
                                              'shutter_speed': shutter_speed,
                                              }))
        w,h = resolution
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
                pixels[i, j] = (i, j, random.randint(0,255))  # set the colour accordingly

        draw = ImageDraw.Draw(image)

        draw.text((w//2, h//2),
                str(time.time() % 256)
                  )

        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue())
        time.sleep(1)
        return img_str

class MyPiCamera(BaseCamera):
    def __init__(self):

        self._pi_camera = PiCamera()
        self._pi_camera.start_preview()

        # Camera warm-up time
        time.sleep(2)
        self._pi_camera.framerate = 10
        self._pi_camera.exposure_mode = 'off'
        self._pi_camera.awb_mode = 'off'


        super(MyPiCamera,self).__init__()


    def capture(self, resolution = (3280, 2464),
                iso=400,
                awb_gains=(1, 1),
                shutter_speed=50000):
            try:
                my_stream = BytesIO()
                self._pi_camera.awb_gains = awb_gains
                self._pi_camera.shutter_speed = shutter_speed
                self._pi_camera.resolution = resolution
                self._pi_camera.capture(my_stream, 'jpeg', quality=95)
            except PiCameraError as e:
                raise CameraException(e)

            img_str = base64.b64encode(my_stream .getvalue())
            return img_str
