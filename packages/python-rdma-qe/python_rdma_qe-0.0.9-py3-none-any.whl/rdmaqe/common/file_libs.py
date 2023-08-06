"""file_libs.py"""

import random
import os


def generate_file(path, file_name, size=1024):
    """
    Generate a txt file, the default size is 1kB=1024B
    1KB=1024B;1MB=1024KB=1024*1024B
    1B=8 bits
    """
    file_full_path = path + "/" + file_name + ".txt"
    curr_size = 0
    with open(file_full_path, "w", encoding="utf-8") as f:
        while curr_size < size:
            f.write(str(round(random.randint(1, 10000))))
            f.write("\n")
            curr_size = os.stat(file_full_path).st_size

    total_size = os.stat(file_full_path).st_size
    print(total_size)

    return file_full_path


def configure_file(conf_file, *args):
    """
    @param conf_file: the file you want to write
    @param args: one or more strings
    @return: None
    """
    with open(conf_file, 'r+') as rf:
        for p in args:
            rf.seek(0)
            lines = rf.read()
            if p not in lines:
                with open(conf_file, 'a+') as wf:
                    wf.write(p)
                    wf.write('\n')
            else:
                print("INFO: It's all set already.")

