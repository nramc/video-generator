import datetime
import os


def get_file_name_with_date(file_name):
    base_name = os.path.basename(file_name)
    name, ext = os.path.splitext(base_name)

    date_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    new_name = f"{name}_{date_str}{ext}"

    return new_name