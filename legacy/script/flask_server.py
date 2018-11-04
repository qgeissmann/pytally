from flask import Flask, request, render_template
from pitally.camera import DummyCamera

app = Flask(__name__)


@app.route('/capture', methods=['POST'])
def capture():
    #todo force syncrhone
    data = request.json
    w = int(data["w"])
    h = int(data["h"])
    iso= int(data["iso"])
    awb_gains = int(data["awb_gains"])
    shutter_speed = int(data["shutter_speed"])

    image = cam.capture((w,h),iso, awb_gains, shutter_speed)
 #   image_str = 'data:image/jpeg;base64,{}'.format(image.decode())
    out = {"image" = image, ** data, results = {}}
    print(out)
    return out
        #'<img src ="%s"/>' % (image_str,)



@app.route('/')
def index():
    return render_template('index.html')


#cam = MyPiCamera()
cam = DummyCamera()

#curl -d '{"w":"1280", "h":"960"}' -H "Content-Type: application/json" -X POST http://localhost:5000/capture
#curl -d '{"w":"2592", "h":"1944", "iso": "400", "awb_gains":"1", "shutter_speed":"5000"}' -H "Content-Type: application/json" -X POST http://raspberrypi:5000/capture | base64 -d > /tmp/image2.jpg && eog /tmp/image2.jpg