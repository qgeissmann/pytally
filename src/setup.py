from setuptools import setup, find_packages
#import os

DESCRIPTION = """
TODO
"""

# ---------------------------------------------------------------------------------------------------------
setup(
    name='pitally',
    version='1.0.0',

    description='TODO',
    long_description=DESCRIPTION,

    author='Quentin Geissmann',
    author_email='qgeissmann@gmail.com',

    url='https://github.com/qgeissmann/pitally',
    license='MIT',

    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering'
    ],
    keywords=['TODO'],

    packages=find_packages(),

#    setup_requires=[
#       'numpy>=1.6.1',  # Numpy has to be installed before others
#  ],
    install_requires=[
        'dash',
    'dash_html_components',
    'dash_core_components'
    ],
    tests_require=['nose'],
    test_suite='nose.collector'
)