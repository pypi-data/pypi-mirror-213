import shutil
import sys
from pathlib import Path

import yaml

from . import mlx, opa


def run(argv=sys.argv):
    if len(argv) < 2:
        print("Usage: ib2influx config.yml")
    else:
        config_file = Path(argv[1])
        if config_file.is_file():
            with open(config_file, "r") as f:
                config = yaml.safe_load(f)
        else:
            raise FileNotFoundError

        # Check if we are using OPA by checking if the opaextractperf executable is in the path
        path = shutil.which("opaextractperf")
        if path is not None:
            print("OPA found")
            opa.LoaderOPA(config)

        # Check if we are using Mellanox by checking if the ibnetdiscover executable is in the path
        path = shutil.which("ibnetdiscover")
        if path is not None:
            print("Mellanox found")
            mlx.LoaderMLX(config)
