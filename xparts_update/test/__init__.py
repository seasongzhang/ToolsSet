import filecmp
import codecs
import os
import shutil
import datetime

TEST_BASE_DIR = "test"
TEST_DATA_DIR = os.path.join(TEST_BASE_DIR, "data")


def setup():
    print("Package setup.")
    # Create src and dst directories
    if os.path.exists(TEST_DATA_DIR):
        shutil.rmtree(TEST_DATA_DIR)
    os.mkdir(TEST_DATA_DIR)
    src_dir = os.path.join(TEST_DATA_DIR, "src")
    dst_dir = os.path.join(TEST_DATA_DIR, "dst")
    os.mkdir(src_dir)
    os.mkdir(dst_dir)

    # Create same files in both src and dst
    codecs.open(os.path.join(src_dir, "A.txt"), "w", encoding="utf-8").write("A.txt")
    shutil.cop(os.path.join(src_dir, "A.txt"), dst_dir)
    metadata_src = os.stat(os.path.join(src_dir, "A.txt"))
    metadata_dst = os.stat(os.path.join(dst_dir, "A.txt"))
    filecmp.cmp

def teardown():
    print("Package teardown.")
    # shutil.rmtree(TEST_DATA_DIR)
