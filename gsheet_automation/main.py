from pandas import DataFrame
import pygsheets
from utilities import *
import json
import argparse
import os
import datetime
import sys
from google.auth.exceptions import TransportError
from pathlib import Path


def latest_dataset_finder(dataset_names: list) -> str:
    """find the latest dataset based on the file name.

    Args:
        dataset_names: list of the csv file names in the directory.
    Returns:
        the latest dataset name's string.
    Raises:
        None.

    """
    format = '%Y-%m-%d_%H-%M'
    dataset_names = sorted(dataset_names, key=lambda x: datetime.datetime.strptime(
        x[7:-4], format), reverse=True)
    return dataset_names[0]


def load_dataset(dataset_loc: str) -> DataFrame:
    """Go through all .csv in the directory, find the latest one.

    Args:
        dataset_loc: directory where .csv are located.
    Returns:
        latest dataframe found in the directory.     
    Raises:
        IndexError: if no dataset is found.

    """
    all_dataset_names = []
    for file in os.listdir(dataset_loc):
        if file.endswith(".csv"):
            all_dataset_names.append(file)

    try:
        latest_dataset_name = latest_dataset_finder(all_dataset_names)
        print(f"Latest dataset found:{latest_dataset_name}")
        df = pd.read_csv(dataset_loc +
                         latest_dataset_name, encoding="UTF-8")
        df = clean_csv(df)
        df = df.sort_values(by=["order_number"], ascending=True)
    except IndexError as IE:
        print(f"No dataset found! \nError:{IE}")
        sys.exit(1)
    return df


def update_df(working_sheet: pygsheets.worksheet.Worksheet, new_df: DataFrame) -> None:
    """updates the existing googlesheet with only new rows.

    Args:
        working_sheet: the existing googlesheet connected.
        new_df: latest datasets dataframe found in the directory.
    Returns:
        None.
    Raises:
        None.

    """

    existing_order_values = working_sheet.get_col(
        1, include_tailing_empty=False)
    last_existing_order_num = int(existing_order_values[-1])
    next_empty_row = len(existing_order_values)+1

    latest_order_num = new_df['order_number'].max()

    if latest_order_num > last_existing_order_num:
        extra_df = new_df.loc[new_df['order_number']
                              > last_existing_order_num, :]
        working_sheet.set_dataframe(
            extra_df.copy(), (next_empty_row, 1), copy_head=False)
        print(f"{extra_df.shape[0]} Rows are updated.")
        print(
            f"Remaining rows: {100000-((next_empty_row-1)+extra_df.shape[0])}")
    else:
        print("No new data to update.")
        print(f"Remaining rows: {100000-(next_empty_row-1)}")

    return None


def main(args: argparse.Namespace, project_path: str) -> None:
    """Read secret information, connects with gsheet, uploads whole dataset if 
    namespace is true, else updates only new rows.

    Args:
        args: namespace for creating the whole dataset.
    Returns:
        None.
    Raises:
        TransportError: if can't connect to/authorize gsheet.

    """
    f = open(f"{project_path}/data/secrets.json")
    secrets = json.load(f)

    gc = pygsheets.authorize(
        service_file=secrets["GC_AUTH_FILE"])

    new_data = load_dataset(secrets["DATASET_FILE_DIR"])

    try:
        sheet = gc.open(secrets["GOOGLE_SHEET_FILE"])
    except TransportError as e:
        print(f"Can't connect to sheets (net down maybe?).\n{e}\n\n")
        sys.exit(1)
    working_sheet = sheet[0]

    if args.create == True:
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
        "-c", "--create", action="store_true", help="Create new df at starting position of google sheet")
    args = parser.parse_args()
    project_path = Path(__file__).resolve().parents[1]
    main(args, project_path)
