"""
This script loads coral disease .csv files from FWC, reformats
them, and inserts them into TODO:which database so the data is
accesible to the grafana-powered coral disease dashboard.

Example usage:
```
python fwc_data_transformer.py test-data\SCTLD_2014_2017.csv
```
"""
import sys
from argparse import ArgumentParser
from datetime import datetime

import pandas as pd


def main(filepath):
    print(filepath)
    data = pd.read_csv(filepath)

    # === parse date
    data = data.dropna(subset=['DATE', 'WPL_P_A'])
    data['time'] = [datetime.strptime(str(d), '%m/%d/%Y').timestamp() for d in data['DATE']]

    # === sort by date
    data = data.sort_values('time')

    # === calculate cumulative % infected
    n_sites = len(data['SITE_NAME'].unique())
    infected_sites = []
    data['cumulative_n_sites_infected'] = [0]*len(data)
    for index, row in data.iterrows():
        if row['WPL_P_A'] == 1 and row['SITE_NAME'] not in infected_sites:
            print("{} infected".format(row['SITE_NAME']))
            infected_sites.append(row['SITE_NAME'])
        data['cumulative_n_sites_infected'][index] = len(infected_sites)
    data['cumulative_percent_sites_infected'] = \
        data['cumulative_n_sites_infected'] / n_sites

    # === export data
    data.to_csv('data.csv')


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
