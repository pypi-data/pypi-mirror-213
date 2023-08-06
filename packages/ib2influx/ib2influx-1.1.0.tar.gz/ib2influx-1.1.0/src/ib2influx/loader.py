import logging
import sys
import time

from influxdb_client import InfluxDBClient

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class Loader:
    """
    Base class for loading IB stats into InfluxDB
    """

    def __init__(self, config):
        # Configure logging
        self.log = logging.getLogger("ib2influx")

        # Collection interval in seconds
        self.interval = config["interval"]

        self.influx_config = config["influxdb"]

        self.log.info(
            f"Writing to {self.influx_config['server']} at {self.interval}s intervals"
        )

        # Set up InfluxDB client
        self.influx_client = InfluxDBClient(
            url=self.influx_config["server"],
            token=self.influx_config["token"],
            org=self.influx_config["org"],
        )

        self.run()

    def run(self):
        """
        Collect statistics and write to InfluxDB at regular time intervals
        """

        while True:
            time_start = self.timestamp()

            self.influx_write(self.data_dict())

            time_finish = self.timestamp()

            dt = time_finish - time_start
            sleep_time = max(0, self.interval - dt)
            time.sleep(sleep_time)

    def influx_write(self, data):
        """
        Write data dictionary to InfluxDB
        """
        write_api = self.influx_client.write_api()

        # Dictionary-style write for each item in dict
        for host in data:
            entry = [
                {
                    "measurement": "infiniband",
                    "tags": {"host": host},
                    "fields": data[host],
                    "time": self.time,
                }
            ]

            write_api.write(
                self.influx_config["bucket"],
                self.influx_config["org"],
                entry,
                write_precision="s",
            )

        write_api.close()

    def set_time(self):
        """
        Sets self.time to the current time
        Used for getting the timestamp of the collected data
        """
        self.time = self.timestamp()

    @staticmethod
    def timestamp():
        """
        Return current timestamp
        """
        return int(time.time())
