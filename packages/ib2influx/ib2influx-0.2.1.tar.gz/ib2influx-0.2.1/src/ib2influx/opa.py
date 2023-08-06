import csv

from .loader import Loader
from .utils import cmd


class LoaderOPA(Loader):
    """
    Loader for OPA hardware
    """

    # Key of node name
    NAME_KEY = "NodeDesc"

    # Mapping of OPA keys to InfluxDB keys
    KEYS = {
        "bytes_in": "RcvData",
        "bytes_out": "XmitData",
        "pkts_in": "RcvPkts",
        "pkts_out": "XmitPkts",
    }

    def extractperf(self):
        """
        Run `opaextractperf` and returns raw output as string
        """
        self.set_time()
        return cmd("opaextractperf")

    def data_table(self):
        """
        Returns a list of table headers, and a list of lists of values
        """

        output = self.extractperf()

        table = list(csv.reader(output.splitlines(), delimiter=";"))

        header = table[0]
        body = table[1:]

        return header, body

    def data_dict(self):
        """
        Returns a dictionary of rates for each node
        """

        header, body = self.data_table()

        # Column of node name
        name_col = header.index(self.NAME_KEY)

        key_col = {}
        # Columns of keys to include
        for k in self.KEYS.values():
            key_col[k] = header.index(k)

        # Create dictionary
        data = {}

        for row in body:
            # name is a string: "hostname interface"
            name = row[name_col].split(" ")

            # If name is only one word, then it is not a node
            if len(name) == 2:
                host = name[0]
                # interface = name[1]

                # If this host is already in the dict, then it has 2 interfaces
                if host in data:
                    raise NotImplementedError("Host has more than one IB interface")

                data[host] = {}

                for influx_key, opa_key in self.KEYS.items():
                    # Convert from string to int
                    value = int(row[key_col[opa_key]])

                    # Perform conversion and add to dict using the InfluxDB key
                    if "Data" in opa_key:
                        data[host][influx_key] = self.convert_opa_units(value)
                    else:
                        data[host][influx_key] = value

        return data

    @staticmethod
    def convert_opa_units(x):
        """
        opaextractperf's rates are in units of 8 bytes
        return 8x the value to get bytes
        """
        return x * 8
