import hashlib
import filecmp
import os
import sys


# Reference: https://rcmdnk.com/blog/2015/07/18/computer-python/
def get_md5_hash(file):
    md5 = hashlib.md5()
    with open(file, 'rb') as f:
        for chunk in iter(lambda: f.read(2048 * md5.block_size), b''):
            md5.update(chunk)
    return md5.hexdigest()


def get_file_list(dir):
    file_list = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list


def check_manipulation(original_dir, revised_dir):
    manipulation_flag = False
    difference_log = []

    # Confirm directory structure
    original_file_list = get_file_list(original_dir)
    original_file_set = set(map(lambda x: x.replace(original_dir, ""), original_file_list))
    revised_file_list = get_file_list(revised_dir)
    revised_file_set = set(map(lambda x: x.replace(revised_dir, ""), revised_file_list))
    if original_file_set != revised_file_set:
        manipulation_flag = True
        only_original_set = original_file_set - revised_file_set
        difference_log.extend(list(map(lambda x: "[Only original]: " + original_dir + x, only_original_set)))
        only_revised_set = revised_file_set - original_file_set
        difference_log.extend(list(map(lambda x: "[Only revised]: " + revised_dir + x, only_revised_set)))    

    # Confirm file content
    for root, dirs, files in os.walk(original_dir):
        for file in files:
            original_file = os.path.join(root, file)
            original_hash = get_md5_hash(original_file)

            revised_file = original_file.replace(original_dir, revised_dir)
            revised_hash = ""
            if os.path.exists(revised_file):
                revised_hash = get_md5_hash(revised_file)
            
            if original_hash != revised_hash:
                manipulation_flag = True
                difference_log.append("[Hash difference]: " + original_file + ", " + revised_file)

    return manipulation_flag, difference_log
