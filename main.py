#!/usr/bin/env python3

import argparse
import csv
import re

from micropyGPS import MicropyGPS

parser = argparse.ArgumentParser()
parser.add_argument("src_ts")
args = parser.parse_args()

if __name__ == "__main__":
    with open(args.src_ts, mode="rb") as ts:
        with open("result.csv", mode="w") as f:
            csv_writer = csv.writer(f)
            for binaries in iter(lambda: ts.read(188), b""):
                my_gps = MicropyGPS(local_offset=9)  # JST = UTC + 9
                if b"$GPRMC" in binaries:
                    print(binaries)
                    gprmc = re.search(rb"\$GPRMC.*\r\n", binaries).group().decode()
                    print(gprmc)
                    for x in gprmc:
                        my_gps.update(x)
                    print(
                        f"{my_gps.date_string()} {my_gps.timestamp} -> {my_gps.latitude_string()} / {my_gps.longitude_string()}")
                    csv_writer.writerow(gprmc.split(","))

                if b"$GSENSORD" in binaries:
                    gsensord = re.search(rb"\$GSENSORD,.*", binaries).group().decode()
                    print(gsensord)
