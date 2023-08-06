import os
import subprocess
from glob import glob


def cmd(command):
    """
    Run a command, checking that the return code == 0
    """
    p = subprocess.run(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True
    )
    return p.stdout.decode()


def find_most_recent_file(path, suffix):
    """
    Find the most recent file in path with suffix
    """
    files = glob(os.path.join(path, "*"))
    last = None
    last_time = 0
    for f in files:
        if f.split(".")[-1] == suffix:
            m = os.path.getmtime(f)
            if m > last_time:
                last = f
                last_time = m
    return last, last_time
