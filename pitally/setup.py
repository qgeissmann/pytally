from setuptools import setup, find_packages
exec(open('pitally/_version.py').read())

setup(
    name='pitally',
    version=__version__,
    long_description=__doc__,
    packages=find_packages(),
    scripts=['bin/pitally.sh', 'bin/pitally_backup.py', 'bin/pitally_drive.sh', 'bin/concat_video_chunks.py'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    extras_require={
        'production': ['picamera'],
        'server': ['Flask', "netifaces", 'flask_cors', "scapy~=2.4.3rc1"],
        'hardware': ['pyserial']
    },
)
