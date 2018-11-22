from flask import Flask, request, render_template
from werkzeug.utils import secure_filename

import tempfile
import setuptools

app = Flask('pitally_update', instance_relative_config=True)
app.config.from_object('pitally_update.config')

try:
    app.config.from_pyfile('config.py')
except FileNotFoundError as e:
    #todo log
    pass


import subprocess
import sys

def install(package):
    # todo retreive errors
    #fixme # does not work without internet. Need --no-deps
    subprocess.call([sys.executable, "-m", "pip", "install", "--ignore-installed",  "--no-deps",  package])


def reload_pitally():
    return subprocess.call(["pitally.sh", "--enable-service"])


@app.route('/update', methods=['POST'])
def update():
    #todo force syncrhone
    #fixme logging
    data = request.json
    print(data)
    file = request.files['package_file']
    if not ('.' in file.filename and "gz" == file.filename.rsplit('.', 1)[1].lower()):
        raise Exception("Wrong file type")
    filename = secure_filename(file.filename)

    new_file, tmpfilename = tempfile.mkstemp(suffix = "_" + filename)

    file.save(tmpfilename)
    install(tmpfilename)
    reload_pitally()
    return ""

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == "POST":
        update()
    return render_template('index.html')
