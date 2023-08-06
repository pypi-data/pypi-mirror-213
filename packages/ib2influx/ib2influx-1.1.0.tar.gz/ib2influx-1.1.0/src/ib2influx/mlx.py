from .loader import Loader
from .utils import cmd, find_most_recent_file


class LoaderMLX(Loader):
    """
    Loader for Mellanox hardware
    """

    def ib_port_map(self):
        """
        Generate a host to switch port mapping
        """

        # Location of IB files
        ib_path = "/root/ib"

        # Get the most recent ibnetdiscover file
        ibnetdiscover_file, _ = find_most_recent_file(ib_path, "ibnetdiscover")

        with open(ibnetdiscover_file, "r") as f:
            lines = f.readlines()

        # Dictionary of mapping
        self.port_map = {}
        self.switch_lids = []
        self.switch_port_count = []

        for line in lines:
            items = line.split()

            if len(items) == 0:
                continue

            # If line describes a switch
            if items[0] == "Switch":
                # Exclude spine switches
                if "spine" in items[4]:
                    continue

                # Get number of ports on the switch (minus one for the base port)
                self.switch_port_count += [int(items[1]) - 1]

                # Get the switch LID
                for i, txt in enumerate(items):
                    if txt == "lid":
                        switch_lid = items[i + 1]
                        self.switch_lids += [switch_lid]
                        break

            # If the first item matches a number inside square brackets
            elif items[0][0] == "[" and items[0][-1] == "]":
                # Get the port number
                port = items[0][1:-1]
                # Get the host name
                host = items[3]

                # If not a spine switch
                if "spine" in host:
                    continue

                # If not a port on a spine switch
                if "Quantum-2" in host:
                    continue

                self.port_map[(switch_lid, port)] = host.lstrip('"')

    def query_switches(self):
        """
        Query a switch for performance data
        """
        self.set_time()

        data = {}
        host = None

        # Loop over switches
        for lid, n in zip(self.switch_lids, self.switch_port_count):
            output = cmd(f"perfquery -x -l {lid} 1-{n}")

            for line in output.split("\n"):
                if "PortSelect" in line:
                    # Get the number at the end of line separated by "."
                    port = line.split(".")[-1]

                    # Look up host in dict, default to None
                    host = self.port_map.get((lid, port), None)
                    # Host variable is now set for reading subsequent values
                    if host is not None:
                        data[host] = {}

                # Read values only if this is an actual host
                if host is not None:
                    # Note: Xmit = in and Rcv = out because this is on the switch side
                    # Counters are in units of 32 bits, so multiply by 4 to get bytes

                    if "PortXmitData" in line:
                        data[host]["bytes_in"] = int(line.split(".")[-1]) * 4

                    elif "PortRcvData" in line:
                        data[host]["bytes_out"] = int(line.split(".")[-1]) * 4

                    elif "PortXmitPkts" in line:
                        data[host]["pkts_in"] = int(line.split(".")[-1])

                    elif "PortRcvPkts" in line:
                        data[host]["pkts_out"] = int(line.split(".")[-1])

        return data

    def data_dict(self):
        self.ib_port_map()
        return self.query_switches()
