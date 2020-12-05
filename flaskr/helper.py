import re

# helper function to perform sort
def num_sort(chapter_name):
    return list(map(int, re.findall(r'\d+', chapter_name)))[0]
