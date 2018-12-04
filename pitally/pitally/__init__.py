from flask import Flask, request, render_template, jsonify
from pitally.camera import DummyCamera, MyPiCamera,  CameraException
from pitally.video_camera_thread import PiCameraVideoThread, DummyCameraVideoThread
import logging
import traceback
import base64

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
    videoRecordingClass = DummyCameraVideoThread
    logging.basicConfig(level=logging.DEBUG)
    logging.info("Testing mode ON")
else:
    camClass = MyPiCamera
    videoRecordingClass = PiCameraVideoThread

cam = camClass()
video_recording_thread = None

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
    if video_recording_thread is not None:
        raise Exception("A video is being acquired, cannot capture a still image until it stops")

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

    if cam is None:
        cam = camClass()

    image = cam.capture((w, h), iso, awb_gains, shutter_speed)

    if base64 == 0:
        return image
    image = 'data:image/jpeg;base64,{}'.format(image.decode())
    out = {"image": image, **data, "results": {}}
    return jsonify(out)

#
@app.route('/restart_camera', methods=['POST'])
#@error_decorator
def restart_camera():
    global cam

    cam  = None #
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



@app.route('/stop_video', methods=['POST'])
#@error_decorator
def stop_video():
    global video_recording_thread
    data = request.json
    video_recording_thread.stop_video()
    try:
        video_recording_thread.join()
    finally:
        video_recording_thread = None

    return "stopping video"#todo
#

@app.route('/start_video', methods=['POST'])
# @error_decorator
def start_video():
    global video_recording_thread
    global cam
    cam = None

    data = request.json

    video_recording_thread = videoRecordingClass(resolution=(1280, 960),
                                                 video_prefix = "video_test",
                                                 video_root_dir = "/tmp/",
                                                 fps=25,
                                                 bitrate=500000)


    video_recording_thread.start()
    out = data
    return jsonify(out)


@app.route('/video_preview', methods=['POST'])
# @error_decorator
def video_preview():

    global video_recording_thread
    logging.debug("getting preview")
    if video_recording_thread is None:
        logging.debug("no recording thread (None)")
        return jsonify(dict())

    elif not video_recording_thread.isAlive():
        logging.debug("recodring thread is not running")
        return jsonify(dict())

    last_image = video_recording_thread.last_image

    if last_image is None:
        logging.debug("No last image yet (None)")
        return jsonify(dict())


    img_str = base64.b64encode(last_image.getvalue())
    image = 'data:image/jpeg;base64,{}'.format(img_str.decode())
    #logging.debug(img_str)
    out =  {"image": image}
    return jsonify(out)



@app.route('/video')
def video():
    return render_template('video.html')

