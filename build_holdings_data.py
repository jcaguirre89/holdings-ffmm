import get_holdings_data as get_data
import pandas as pd

def main(start, end):
    """ main func """
    master_df = pd.DataFrame()
    for year in range(start, end + 1):
        for month in range(1, 13):
            print(f'Getting data for {month} - {year}')
            zero_padded_month = str(month).zfill(2)
            df = get_data.clean_holdings(zero_padded_month, str(year))
            master_df = pd.concat([master_df, df])
    return master_df

if __name__ == '__main__':
    df = main(2018, 2019)
    df.to_csv('out_many.csv')