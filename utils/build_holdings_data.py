import get_holdings_data as get_data
import pandas as pd
from argparse import ArgumentParser

def _build_parser():
    parser = ArgumentParser()
    parser.add_argument('--start',
                        type=str,
                        dest='start',
                        help='Start date. format: MMYYYY',
                        required=True)
    parser.add_argument('--end',
                        type=str,
                        dest='end',
                        help='End date. format: MMYYYY',
                        required=True)
    return parser

def _build_date_range(start, end):
    """ start and end come as MMYYYY, and this returns an iterable of year-month
    combinations """
    start_year = int(start[-4:])
    start_month = int(start[:2])
    end_year = int(end[-4:])
    end_month = int(end[:2])
    # TODO: Validate that end is later than start, that they're valid dates, etc.

    start_date = pd.Timestamp(year=start_year, month=start_month, day=1)
    end_date = pd.Timestamp(year=end_year, month=end_month, day=1)

    return pd.date_range(start_date, end_date, freq='MS')


def main():
    """ main func """
    parser = _build_parser()
    options = parser.parse_args()
    start = options.start
    end = options.end

    dates = _build_date_range(start, end)

    master_df = pd.DataFrame()
    for date in dates:
        month = date.month
        year = date.year
        print(f'Getting data for {month} - {year}')
        zero_padded_month = str(month).zfill(2)
        df = get_data.clean_holdings(zero_padded_month, str(year))
        master_df = pd.concat([master_df, df])
    return master_df

if __name__ == '__main__':
    df = main(2018, 2019)
    df.to_csv('holdings-2018-2019.csv', index=False)
