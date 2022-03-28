import pandas as pd
import re

pd.set_option('display.max_columns', None)


def size_color_separator(row, option="size"):
    if option == "size":
        re_text = "size:"
    elif option == "color":
        re_text = "colou?r:"

    if row == "nan":
        sliced_str = ""
    else:
        try:
            str_end_pos = re.search(
                fr"\b{re_text}\b", row, re.IGNORECASE).end()
            sliced_str = row[str_end_pos:].split(",")[0]
        except AttributeError:
            sliced_str = ""

    return sliced_str


def clean_csv(df):
    # drop unnecessary columns
    remove_columns = ["weight", "tax_details", "customer_tax_exempt",
                      "customer_tax_id", "reversed_tax_applied",
                      "shipto_person_phone", "detail_discount", "order_weight",
                      "customer_ipaddress", "tips", "bill_person_phone", "referer_id", "surcharges",
                      "shipto_person_street_2", "bill_person_street_2", "affiliate_id", "gift_card_redemption", "masked_gift_card_code",
                      "volume_discount"]
    df.drop(remove_columns, inplace=True, axis=1)

    # replace newline values in options column with commas
    df = df.replace(r'\n', ',', regex=True)

    # place size and color in new columns
    df["size"] = df.apply(lambda row: size_color_separator(
        str(row["options"]), "size"), axis=1)
    df["color"] = df.apply(lambda row: size_color_separator(
        str(row["options"]), "color"), axis=1)
    
    # remove options columns
    df.drop("options", inplace=True, axis=1)

    return df