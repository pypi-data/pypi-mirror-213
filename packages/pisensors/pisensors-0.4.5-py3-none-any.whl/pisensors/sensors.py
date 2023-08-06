""" Read DHT22 sensors """
import os
from pathlib import Path
import logging

from influxdb_wrapper import influxdb_factory
from config_yml import Config


class Sensors():
    """Read inputs from DHT22 sensors (temperature & humidity) and write it to influx database"""

    def __init__(self, template_config_path: str = None, dry_run: bool = False):
        self.logger = logging.getLogger()

        if dry_run:
            dry_run_abs_path = ""
        else:
            dry_run_abs_path = None

        if not template_config_path:
            template_config_path = os.path.join(Path(__file__).parent.resolve(), './config-template.yml')

        self.config = Config(package_name=self.class_name(),
                             template_path=template_config_path,
                             config_file_name="config.yml",
                             dry_run=dry_run,
                             dry_run_abs_path=dry_run_abs_path)

        influx_conn_type = self.config['influxdbconn'].get('type', 'influx')
        self.conn = influxdb_factory(influx_conn_type)
        self.conn.open_conn(self.config['influxdbconn'])

    @classmethod
    def class_name(cls):
        """ Class name """
        return "sensors"

    def sensor_read(self):
        """
        Read sensors information
        """
        have_readings = False

        try:
            import adafruit_dht  # pylint: disable=import-outside-toplevel

            self.logger.debug("Initializing DHT22 sensor...")
            dht_sensor = adafruit_dht.DHT22(self.config["pin"])
            humidity = dht_sensor.humidity
            temp_c = dht_sensor.temperature
            dht_sensor.exit()
            have_readings = True
        except (ModuleNotFoundError, NameError):
            self.logger.warning("No adafruit supported: returning default values.")
            humidity = 50
            temp_c = 25
            have_readings = True
        except RuntimeError as ex:
            self.logger.error("Error reading sensor DHT22: %s", ex)

        if have_readings:
            try:
                points = [
                    {
                        "tags": {"sensorid": self.config["id"]},
                        "fields": {"temp": float(temp_c), "humidity": float(humidity)},
                    }
                ]
                self.conn.insert("DHT22", points)

                self.logger.info("Temp: %s | Humid: %s", temp_c, humidity)

            except RuntimeError as ex:
                self.logger.error("RuntimeError: %s", ex)
                self.logger.error("influxDB conn = %s", self.config['influxdbconn'])
