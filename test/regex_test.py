import re


test_list = ["", "Size:XS,Colour:Beige", "Size:S, Color:Black",
             "SET SIZE:M", "Set Size:S, Colour:Red"]


for item in test_list:
    if item != "":
        size_end_pos = re.search(r"\bsize:\b", item, re.IGNORECASE).end()
        sliced_str = item[size_end_pos:].split(",")[0]
        print(sliced_str)

    else:
        print(f"{item}: Empty string")


for item in test_list:
    if item != "":
        try:
            size_end_pos = re.search(
                r"\bcolou?r:\b", item, re.IGNORECASE).end()
            sliced_str = item[size_end_pos:].split(",")[0]
            print(sliced_str)
        except AttributeError:
            sliced_str = ""

    else:
        sliced_str = ""
