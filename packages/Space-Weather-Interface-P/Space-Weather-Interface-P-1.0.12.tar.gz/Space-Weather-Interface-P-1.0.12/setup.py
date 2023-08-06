from setuptools import setup

VERSION = '1.0.12'
DESCRIPTION = 'Displays Space Weather Data, and downloads and compiles images of the sun into videos.'

# Setting up
setup(
    name="Space-Weather-Interface-P",
    version=VERSION,
    author="Stefan Randow",
    author_email="mail@example.com",
    description=DESCRIPTION,
    install_requires=['opencv-python'],
    keywords=['python', 'video'],
    entry_points={
        'console_scripts': [
            'SpaceWeather = Space_Weather_Interface_P.main:main',
        ],
    },
)
