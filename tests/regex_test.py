import re

def size_finder(test_list):
    for item in test_list:
        if item != "":
            size_end_pos = re.search(r"\bsize:\b", item, re.IGNORECASE).end()
            sliced_str = item[size_end_pos:].split(",")[0]
            print(sliced_str)

        else:
            print(f"{item}: Empty string")
    
    return None


def color_finder(test_list):
    for item in test_list:
        if item != "":
            try:
                size_end_pos = re.search(
                    r"\bcolou?r:\b", item, re.IGNORECASE).end()
                sliced_str = item[size_end_pos:].split(",")[0]
                print(sliced_str)
            except AttributeError:
                sliced_str = ""
                print(": Empty string")

        else:
            print(f"{item}: Empty string")
    
    return None


def main():

    test_list = ["", "Size:XS,Colour:Beige", "Size:S, Color:Black",
                 "SET SIZE:M", "Set Size:S, Colour:Red"]
    
    print(f"Test List:{test_list}")
    
    # print("Sizes:")
    # size_finder(test_list)

    print("Colors:")
    color_finder(test_list)

    return None


if __name__ == '__main__':
    main()