from PIL import Image, ImageDraw, ImageFont
import base64
from io import BytesIO
import time


class BaseCamera(object):
    def __init__(self, w=1280//4, h=960//4):
        self._width = w
        self._height = h

    def capture(self, n_clicks):
        raise(NotImplementedError)

class DummyCamera(BaseCamera):
    def capture(self, n_clicks):
        print('capture')
        image = Image.new('RGB',
                          (self._width, self._height),
                          (0, 128, 255))
        draw = ImageDraw.Draw(image)

        # use a bitmap font
#        font = ImageFont.truetype()

        draw.text((self._width//2, self._height//2),
                  str(n_clicks)
#                 font=font
                  )

        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue())
        time.sleep(3)
        return img_str
