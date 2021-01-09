import re
import os

# helper function to perform sort
def num_sort(chapter_name):
    return list(map(int, re.findall(r'\d+', chapter_name)))[0]

def size_of_directory(directory: str):
    size_of_dir_in_bytes = 0
    for item in os.scandir(directory):
        if item.is_file():
            size_of_dir_in_bytes += item.stat().st_size
        if item.is_dir():
            print("Scanning inner folder ", directory+item.name)
            size_of_dir_in_bytes += size_of_directory(directory+item.name+"/")

    return size_of_dir_in_bytes


# https://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size#
# idk if im supposed to cite stackoverflow code, not sure if SO has inherent licensing
def sizeof_fmt(num, suffix='B'):
    for unit in ['','K','M','G']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

def clear_directory(directory: str):
    for item in os.scandir(directory):
        if item.is_dir():
            clear_directory(directory+item.name+"/")
            os.rmdir(item)
        if item.is_file():
            os.remove(item)
