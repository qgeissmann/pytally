from setuptools import setup

setup(
    name='pitally',
    version='1.2',
    long_description=__doc__,
    packages=['pitally', 'pitally.utils'],
    scripts=['bin/pitally.sh', 'bin/pitally_backup.py'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask', "netifaces"]
)
