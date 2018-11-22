from setuptools import setup

setup(
    name='pitally',
    version='1.1',
    long_description=__doc__,
    packages=['pitally'],
    scripts=['bin/pitally.sh'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask']
)
