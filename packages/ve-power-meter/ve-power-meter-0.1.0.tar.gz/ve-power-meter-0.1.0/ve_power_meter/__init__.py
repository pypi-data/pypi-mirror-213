#!/usr/bin/env python3

import datetime
import re
import subprocess
import time

RE_CORE_TEMP = re.compile(r"Chip\s+Core\s+\d+\s+:\s+([\d\.]+)\s+C")
RE_HBM_TEMP = re.compile(r"HBM\s+\d+\s+:\s+([\d\.]+)\s+C")
RE_AUX_V = re.compile(r"AUX\s+12V\s+V\s+:\s+([\d\.]+)\s+V")
RE_EDGE_V = re.compile(r"Edge\s+12V\s+V\s+:\s+([\d\.]+)\s+V")
RE_AUX_C = re.compile(r"AUX\s+12V\s+C\s+:\s+([\d\.]+)\s+mA")
RE_EDGE_C = re.compile(r"Edge\s+12V\s+C\s+:\s+([\d\.]+)\s+mA")


def read_temp(out):
    core_temps = [float(t) for t in re.findall(RE_CORE_TEMP, out)]
    hbm_temps = [float(t) for t in re.findall(RE_HBM_TEMP, out)]

    return sum(core_temps) / len(core_temps), sum(hbm_temps) / len(hbm_temps)


def read_power(out):
    aux_12v = float(re.search(RE_AUX_V, out).group(1))
    edge_12v = float(re.search(RE_EDGE_V, out).group(1))

    aux_12c = float(re.search(RE_AUX_C, out).group(1))
    edge_12c = float(re.search(RE_EDGE_C, out).group(1))

    power = aux_12v * (aux_12c / 1000) + edge_12v * (edge_12c / 1000)

    return power


def main():
    print("timestamp,power.draw,temperature.core,temperature.memory")
    while True:
        res = subprocess.run(["/opt/nec/ve/mmm/bin/vecmd", "info"],
                             capture_output=True)
        out = res.stdout.decode("utf-8")

        now = datetime.datetime.now()
        timestamp = now.strftime("%Y/%m/%d %H:%M:%S.%f")[:-3]
        power = read_power(out)
        core_temp, hbm_temp = read_temp(out)

        print(f"{timestamp},{power:.2f},{core_temp:.0f},{hbm_temp:.0f}")

        time.sleep(1)


if __name__ == "__main__":
    main()
