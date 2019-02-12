from setuptools import setup
exec(open('pitally/_version.py').read())

setup(
    name='pitally',
    version=__version__,
    long_description=__doc__,
    packages=['pitally', 'pitally.utils'],
    scripts=['bin/pitally.sh', 'bin/pitally_backup.py', 'bin/pitally_drive.sh', 'bin/concat_video_chunks.py'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask', "netifaces", "scapy", 'flask_cors'],
    extras_require={
        'production': ['picamera'],
    },
)
