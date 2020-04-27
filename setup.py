from setuptools import setup


setup(
    name='neopixelflames',
    url='https://github.com/willbarton/neopixelflames',
    author='Will Barton',
    license='MIT',
    version='1.0.0',
    description='Fire simulator with Adafruit NeoPixels',
    long_description='Fire simulator with Adafruit NeoPixels',
    py_modules='neopixelflames',
    install_requires=[
        'adafruit-circuitpython-neopixel',
        'adafruit-circuitpython-fancyled',
        'colour',
    ],
    entry_points={
        'console_scripts': ['neopixelflames = neopixelflames:main', ]
    }
)
