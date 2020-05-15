"""
This script loads coral disease .csv files from FWC, reformats
them, and inserts them into TODO:which database so the data is
accesible to the grafana-powered coral disease dashboard.
"""
import sys
from argparse import ArgumentParser

import pandas as pd


def main(filepath):
    print(filepath)
    data = pd.read_csv(filepath)
    print(data)

def parse_args(argvs):
    # =========================================================================
    # === set up arguments
    # =========================================================================
    parser = ArgumentParser(
        description=__doc__
    )
    # === arguments for the main command
    # parser.add_argument("-v", "--verbose", help="increase output verbosity",
    #                     action="count",
    #                     default=0
    # )
    parser.add_argument(
        "filepath",
        help="File path to .csv file to ingest."
    )
    args = parser.parse_args(argvs)
    return args


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    args = vars(args)  # convert args to dict
    main(**args)
