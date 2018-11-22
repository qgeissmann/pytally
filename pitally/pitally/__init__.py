from flask import Flask, request, render_template, jsonify
from pitally.camera import DummyCamera, MyPiCamera, CameraException
import logging
import traceback

# http://fancyapps.com/fancybox/3/ lookt at that

app = Flask('pitally', instance_relative_config=True)
app.config.from_object('pitally.config')



try:
    app.config.from_pyfile('config.py')
except FileNotFoundError as e:
    #todo log
    pass


if app.testing is True:
    camClass = DummyCamera
    logging.basicConfig(level=logging.DEBUG)
    logging.info("Testing mode ON")
else:
    camClass= MyPiCamera

cam = camClass()


def error_decorator(func):
    """
    A simple decorator to return an error dict so we can display it the ui
    """
    def func_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as ex:
            logging.error(traceback.format_exc(chain=ex))
            return jsonify({'error': traceback.format_exc(chain=ex)})

    return func_wrapper


@app.route('/capture', methods=['POST'])
@app.route('/capture/<int:base64>', methods=['POST'])
@error_decorator
def capture(base64=0):
    #todo force syncrhone
    global cam
    data = request.json

    logging.info(request.json)

    # to make it simpler to programmatically request capture via curl
    if data is None:
        data = request.form

    w = int(data["w"])
    h = int(data["h"])
    iso = int(data["iso"])
    awb_gains = (float(data["awb_gain_r"]), float(data["awb_gain_b"]))
    shutter_speed = int(data["shutter_speed"])


    image = cam.capture((w, h), iso, awb_gains, shutter_speed)

    if base64 == 0:
        return image
    image = 'data:image/jpeg;base64,{}'.format(image.decode())
    out = {"image": image, **data, "results": {}}
    return jsonify(out)

@app.route('/restart_camera', methods=['POST'])
def restart_camera():
    global cam
    del cam
    cam = camClass()
    return ""

@app.route('/stop_server', methods=['POST'])
def stop_server():

    logging.info("stopping the server from post request")
    func = request.environ.get('werkzeug.server.shutdown')
    func()
    return ""


@app.route('/')
def index():
    return render_template('index.html')

