""" Setup """
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pisensors",
    version="0.4.5",
    author="Ismael Raya",
    author_email="phornee@gmail.com",
    description="Raspberry Pi Sensors script for Temperature & Humidity",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Phornee/pisensors",
    packages=setuptools.find_packages(),
    package_data={
        '': ['*.yml'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Topic :: Home Automation"
    ],
    install_requires=[
        'config_yml>=0.3.1',
        'log_mgr>=0.1.1',
        'influxdb_wrapper>=0.0.5',
        'adafruit-circuitpython-dht>=3.5.1'
    ],
    python_requires='>=3.6',
)