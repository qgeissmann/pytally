from setuptools import setup

setup(
    name='pitally_update',
    version='1.0.1',
    long_description=__doc__,
    packages=['pitally_update'],
    scripts=['bin/pitally_update.sh'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask', 'flask_cors']
)
