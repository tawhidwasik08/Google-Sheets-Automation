import pygsheets
import pandas as pd
from csv_cleaner import *
from secrets import secrets

def load_dataset():

    df = pd.read_csv(secrets["DATASET_FILE"], encoding="UTF-8")
    df = clean_csv(df)
    df = df.sort_values(by=["order_number"], ascending=True)
    return df


def create_df():

    return None


def update_df(working_sheet, new_df):

    existing_df = working_sheet.get_as_df()
    print(existing_df["order_number"])
    latest_order_number = existing_df['order_number'].max()

    extra_df = new_df.loc[new_df['order_number'] > latest_order_number]

    if extra_df.shape[0] >=1:
        updated_df = pd.concat([existing_df, extra_df]
                               ).drop_duplicates().reset_index(drop=True)
        # working_sheet.set_dataframe(updated_df, (1, 1))
        print("update done!")
    else:
        print("No new data to update")

    return None


def main():

    gc = pygsheets.authorize(
        service_file=secrets["GC_AUTH_FILE"])

    new_data = load_dataset()

    sheet = gc.open(secrets["GOOGLE_SHEET_FILE"])
    working_sheet = sheet[0]
    # update the first sheet with df, starting at cell B2.
    # working_sheet.set_dataframe(new_data, (1, 1))
    # print("Upload Done")
    update_df(working_sheet, new_data)


if __name__ == '__main__':
    main()
