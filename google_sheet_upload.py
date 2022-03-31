import pygsheets
import pandas as pd
from csv_cleaner import *
from secrets import secrets
import argparse
import os
import datetime
import sys
from google.auth.exceptions import TransportError


def latest_dataset_finder(dataset_names):
    format = '%Y-%m-%d_%H-%M'
    dataset_names = sorted(dataset_names, key=lambda x: datetime.datetime.strptime(
        x[7:-4], format), reverse=True)
    return dataset_names[0]


def load_dataset():
    all_dataset_names = []
    for file in os.listdir(secrets["DATASET_FILE_DIR"]):
        if file.endswith(".csv"):
            all_dataset_names.append(file)

    try:
        latest_dataset_name = latest_dataset_finder(all_dataset_names)
        print(f"Latest dataset found:{latest_dataset_name}")
        df = pd.read_csv(secrets["DATASET_FILE_DIR"] +
                         latest_dataset_name, encoding="UTF-8")
        df = clean_csv(df)
        df = df.sort_values(by=["order_number"], ascending=True)
    except IndexError as IE:
        print(f"No dataset found! \nError:{IE}")
        sys.exit(1)
    return df


def update_df(working_sheet, new_df):

    existing_order_values = working_sheet.get_col(
        1, include_tailing_empty=False)
    last_existing_order_num = int(existing_order_values[-1])
    next_empty_row = len(existing_order_values)+1

    latest_order_num = new_df['order_number'].max()

    if latest_order_num > last_existing_order_num:
        extra_df = new_df.loc[new_df['order_number'] > last_existing_order_num,:]
        working_sheet.set_dataframe(
            extra_df.copy(), (next_empty_row, 1), copy_head=False)
        print(f"{extra_df.shape[0]} Rows are updated.")
        print(
            f"Remaining rows: {100000-((next_empty_row-1)+extra_df.shape[0])}")
    else:
        print("No new data to update.")
        print(f"Remaining rows: {100000-(next_empty_row-1)}")

    return None


def main(args):
    gc = pygsheets.authorize(
        service_file=secrets["GC_AUTH_FILE"])

    new_data = load_dataset()

    try:
        sheet = gc.open(secrets["GOOGLE_SHEET_FILE"])
    except TransportError as e:
        print(f"Can't connect to sheets (net down maybe?).\n{e}\n\n")
        sys.exit(0)
    working_sheet = sheet[0]

    if args.create == True:
        # update the first sheet with df, starting at cell B2.
        working_sheet.clear()
        working_sheet.set_dataframe(new_data, (1, 1))
        print("New dataset uploaded.")
    else:
        update_df(working_sheet, new_data)

    return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Create a new df or update existing df (default) in Google Sheet')
    parser.add_argument(
        "-c", "--create", action="store_true", help="Create new df at starting position of sheet")
    args = parser.parse_args()
    main(args)
