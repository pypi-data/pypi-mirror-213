""" _main_ To be properly executed from crontab --> python -m pisensors """
from log_mgr import Logger
from .sensors import Sensors

logger = Logger('pisensors', log_file_name='pisensors')

sensors_instance = Sensors()
sensors_instance.sensor_read()
