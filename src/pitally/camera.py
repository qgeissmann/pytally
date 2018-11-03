import base64
from io import BytesIO
import time


class BaseCamera(object):
    def __init__(self):
        pass
    def capture(self, resolution,):
        raise(NotImplementedError)

class DummyCamera(BaseCamera):
    def capture(self, resolution,
                iso=200,
                awb_gains=1,
                shutter_speed=1):
        w,h = resolution
        from PIL import Image, ImageDraw, ImageFont
        print('capture')
        image = Image.new('RGB',
                          (w, h),
                          (0, 128, 255))
        draw = ImageDraw.Draw(image)

        # use a bitmap font
#        font = ImageFont.truetype()

#         draw.text((w//2, h//2),
#                   str(n_clicks)
# #                 font=font
#                   )

        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue())
        time.sleep(1)
        return img_str

class MyPiCamera(BaseCamera):
    def __init__(self):
        from picamera import PiCamera
        self._pi_camera = PiCamera()
        self._pi_camera.start_preview()

        # Camera warm-up time
        time.sleep(2)
        self._pi_camera.exposure_mode = 'off'
        self._pi_camera.awb_mode = 'off'

        super(MyPiCamera,self).__init__()


    def capture(self, resolution = (2592, 1944),
                iso=400,
                awb_gains=1,
                shutter_speed=50000):

        self._pi_camera.awb_gains = awb_gains
        self._pi_camera.shutter_speed = shutter_speed
        self._pi_camera.resolution = resolution

        my_stream = BytesIO()
        self._pi_camera.capture(my_stream, 'jpeg')
        img_str = base64.b64encode(my_stream .getvalue())
        return img_str