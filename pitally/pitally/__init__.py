from flask import Flask, request, render_template, jsonify
from pitally.camera import DummyCamera, MyPiCamera

# http://fancyapps.com/fancybox/3/ lookt at that

app = Flask('pitally', instance_relative_config=True)
app.config.from_object('pitally.config')

try:
    app.config.from_pyfile('config.py')
except FileNotFoundError as e:
    #todo log
    pass


# preview
# tab name

if app.testing is True:
    cam = DummyCamera()
else:
    cam = MyPiCamera()


@app.route('/capture', methods=['POST'])
@app.route('/capture/<int:base64>', methods=['POST'])
def capture(base64=0):
    #todo force syncrhone
    #fixme logging
    data = request.json

    if data is None:
        data = request.form

    w = int(data["w"])
    h = int(data["h"])
    iso= int(data["iso"])
    awb_gains = float(data["awb_gains"])
    shutter_speed = int(data["shutter_speed"])
    image = cam.capture((w, h), iso, awb_gains, shutter_speed)
    if base64 == 0:
        return image
    image = 'data:image/jpeg;base64,{}'.format(image.decode())
    out = {"image": image, **data, "results": {}}
    return jsonify(out)

@app.route('/')
def index():
    return render_template('index.html')
