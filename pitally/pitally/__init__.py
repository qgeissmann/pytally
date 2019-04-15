from flask import Flask, request, render_template, jsonify, send_file
from pitally.camera import DummyCamera, MyPiCamera,  CameraException
from pitally.video_camera_thread import PiCameraVideoThread, DummyCameraVideoThread
from pitally.utils.map_devices import map_devices
from pitally.utils.first_boot_settings import first_boot
from pitally._version import __version__ as version
import logging
import traceback
import base64
import os
from datetime import datetime
import time
from flask_cors import CORS


if not os.environ.get("FAKE_PITALLY"):

    def file_in_dir_r(file, dir):
        file_dir_path = os.path.dirname(file).rstrip("//")
        dir_path = dir.rstrip("//")
        if file_dir_path == dir_path:
            return True
        elif file_dir_path == "":
            return False
        else:
            return file_in_dir_r(file_dir_path, dir_path)

    def set_auto_hostname(interface = "eth0"):
        import netifaces
        from subprocess import call, Popen
        import socket
        add = netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]["addr"]
        suffix = "".join(add.split(":")[3:6])
        machine_id ="pitally-" + suffix
        hostname = socket.gethostname()
        call(["hostnamectl", "set-hostname", machine_id])
        if hostname != machine_id:
            first_boot(app)
            logging.warning("Perfroming first boot")
        return machine_id

    app = Flask('pitally',
                instance_relative_config=True,
                static_url_path='')
    app.config.from_object('pitally.config')
    CORS(app)

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
        import socket
        # in this case, we use the machine hostname as ID, without setting it
        MACHINE_ID = socket.gethostname()

    else:
        camClass = MyPiCamera
        videoRecordingClass = PiCameraVideoThread
        MACHINE_ID = set_auto_hostname()

    device_info = {"id": MACHINE_ID, "status": "idle", "since": time.time(), "software_version": version}

    # id(=hostname), status (idle, recording, capturing, computing, stopping video), name, time,

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

    @app.route('/')
    def index():
        return app.send_static_file('index.html')



    @app.route('/capture', methods=['POST'])
    @app.route('/capture/<int:base64>', methods=['POST'])
    @error_decorator
    def capture(base64=0):
        #todo force synchrone
        global device_info
        device_info["status"] = "capturing"
        device_info["since"] = time.time()

        if video_recording_thread is not None:
            raise Exception("A video is being acquired, cannot capture a still image until it stops")

        global cam
        data = request.json

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

        device_info["status"] = "idle"
        device_info["since"] = time.time()
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



    @app.route('/stop_video', methods=['POST'])
    #@error_decorator
    def stop_video():
        global video_recording_thread
        data = request.json

        try:
            video_recording_thread.stop_video()
            video_recording_thread.join()

        finally:
            check_video_thread()
        return device()
    #

    @app.route('/start_video', methods=['POST'])
    # @error_decorator
    def start_video():
        global device_info
        global video_recording_thread
        global cam

        if video_recording_thread is not None:
            raise Exception("A video is being acquired, cannot record a new one until it stops")

        device_info["status"] = "recording"
        device_info["since"] = time.time()
        try:
            cam = None
            data = request.json

            # to make it simpler to programmatically request capture via curl
            if data is None:
                data = request.form

            logging.info(data)
            w = int(data["w"])
            h = int(data["h"])
            duration = float(data["duration"]) * 3600.0 # h to s

            bitrate = int(data["bitrate"])
            fps = int(data["fps"])
            prefix = data["prefix"] # todo replace _ with - in prefix (only allow for [a-Z]+ - )
            client_time = int(data["time"])

            client_time = datetime.utcfromtimestamp(client_time/1000).strftime('%Y-%m-%dT%H-%M-%S-UTC')
            prefix = client_time + "_" + MACHINE_ID + "_" + prefix # eg. 2018-12-13T12-00-01-UTC_pitally-ab01cd_my-video
            video_root_dir = os.path.join(app.config["STATIC_VIDEO_DIR"], MACHINE_ID, prefix)
            os.makedirs(video_root_dir, exist_ok=True)

            logging.info(video_root_dir)

            video_recording_thread = videoRecordingClass(resolution=(w, h),
                                                         video_prefix = prefix,
                                                         video_root_dir = video_root_dir,
                                                         fps = fps,
                                                         bitrate = bitrate,
                                                         duration=duration)

            video_recording_thread.start()
            # wait 30s to have preview, if none, we fail
            i = 0
            while i < 30:
                if video_recording_thread.last_image is not None:
                    break
                else:
                    i = i + 1
                if i is 30:
                    raise Exception("Timeout, camera would not start properly")
                time.sleep(1)
        except Exception as e:
            logging.info(e)
            stop_video()
            raise e

        return device()


    @app.route('/video_preview', methods=['POST'])
    # @error_decorator
    def video_preview(thumbnail = False):

        global video_recording_thread
        logging.debug("getting preview")
        if video_recording_thread is None:
            logging.debug("no recording thread (None)")
            check_video_thread()
            return jsonify(dict())

        elif not video_recording_thread.isAlive():
            logging.debug("recording thread is not running")
            return jsonify(dict())

        last_image = video_recording_thread.last_image

        if last_image is None:
            logging.debug("No last image yet (None)")
            return jsonify(dict())
        if thumbnail:
            pass # TODO resize image here!

        img_str = base64.b64encode(last_image.getvalue())
        image = 'data:image/jpeg;base64,{}'.format(img_str.decode())
        #logging.debug(img_str)

        out = {"image": image, "video_name": video_recording_thread.video_name}
        return jsonify(out)

    @app.route('/list_devices', methods=['GET'])
    def list_devices():
        if app.config["MOCK_DEVICE_MAP"]:
            from pitally.utils.fake_device_map import fake_dev_map
            return jsonify(fake_dev_map())
        out = jsonify(map_devices(MACHINE_ID))
        return out

    @app.route('/device_info', methods=['GET'])
    def device():
        check_video_thread()
        stats()
        return jsonify(device_info)

    @app.route('/list_video_on_ftp', methods=['GET'])
    def list_video_on_ftp():
        import subprocess
        import os
        import re
        # ftp = app.config["STATIC_VIDEO_DIR"]
        ftp = 'ftp://pitally-drive'
        command = 'lftp -e "find /;quit" "%s" | grep -e "^.*_0\{5\}-[0-9]\{5\}\.mp4$"' % ftp
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        out, _ = p.communicate()
        out = out.decode("utf8").split("\n")
        dir_vid = {}
        for o in sorted(out):
            if not o:
                continue
            dirname = os.path.dirname(o)
            basename = os.path.basename(o)
            dir_vid[dirname] = basename
        out = []
        for d, b in dir_vid.items():
            path = os.path.join(d,b)
            match = re.search(
                r"(?P<datetime>.*)_(?P<device>.*)_(?P<prefix>.*)_(?P<w>\d+)x(?P<h>\d+)@(?P<fps>\d+)_(?P<start>\d{5})-(?P<end>\d{5}).mp4",
                b)
            groups = match.groupdict()
            groups["path"] = path
            out.append(groups)
        return jsonify(out)

    def  check_video_thread():
        global device_info
        global video_recording_thread

        if video_recording_thread is not None:
            if not video_recording_thread.isAlive():
                video_recording_thread = None
                device_info["status"] = "idle"
                device_info["since"] = time.time()
    def stats():
        global device_info
        statvfs = os.statvfs('/')
        disk_gb_left = statvfs.f_frsize * statvfs.f_bavail / 1024 ** 3
        percent_disk_use = 100.0 - round(100 * statvfs.f_bavail / statvfs.f_blocks, 1)
        device_info["percent_disk_use"] = percent_disk_use
        device_info["disk_gb_left"] = disk_gb_left
