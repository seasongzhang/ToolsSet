import codecs
import os
import shutil
import time

TEST_BASE_DIR = r"..\test"
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
    codecs.open(os.path.join(src_dir, "A.txt"), "w").write("A.txt")
    shutil.copy2(os.path.join(src_dir, "A.txt"), dst_dir)

    # Create file in src but not in dst
    codecs.open(os.path.join(src_dir, "B.txt"), "w").write("B.txt")

    # Create file in dst but not in src
    codecs.open(os.path.join(dst_dir, "C.txt"), "w").write("C.txt")

    # Create file in src and changed in dst
    codecs.open(os.path.join(src_dir, "D.txt"), "w").write("D.txt")
    shutil.copy2(os.path.join(src_dir, "D.txt"), dst_dir)
    time.sleep(0.001)
    codecs.open(os.path.join(dst_dir, "D.txt"), "a").write("D.txt")

    # Create file in dst and changed in src
    codecs.open(os.path.join(dst_dir, "E.txt"), "w").write("E.txt")
    shutil.copy2(os.path.join(dst_dir, "E.txt"), src_dir)
    time.sleep(0.001)
    codecs.open(os.path.join(src_dir, "E.txt"), "a").write("E.txt")

    # Create same dirs both in src and dst
    os.mkdir(os.path.join(src_dir, "AA"))
    os.mkdir(os.path.join(dst_dir, "AA"))
    codecs.open(os.path.join(src_dir, "AA\A.txt"), "w").write("A.txt")
    shutil.copy2(os.path.join(src_dir, "AA\A.txt"), os.path.join(dst_dir, "AA"))

    # Create dir in src but not in dst
    os.mkdir(os.path.join(src_dir, "BB"))
    codecs.open(os.path.join(src_dir, "BB\B.txt"), "w").write("B.txt")

    # Create dir in src but not in dst
    os.mkdir(os.path.join(dst_dir, "CC"))
    codecs.open(os.path.join(dst_dir, "CC\C.txt"), "w").write("C.txt")

    # Create dir in src and changed in dst
    os.mkdir(os.path.join(src_dir, "DD"))
    codecs.open(os.path.join(src_dir, r"DD\D.txt"), "w").write("D.txt")
    shutil.copytree(os.path.join(src_dir, "DD"), os.path.join(dst_dir, "DD"))
    codecs.open(os.path.join(dst_dir, r"DD\D.txt"), "a").write("D.txt")

    # Create dir in dst and changed in src
    os.mkdir(os.path.join(dst_dir, "EE"))
    codecs.open(os.path.join(dst_dir, r"EE\E.txt"), "w").write("E.txt")
    shutil.copytree(os.path.join(dst_dir, "EE"), os.path.join(src_dir, "EE"))
    codecs.open(os.path.join(src_dir, r"EE\E.txt"), "a").write("E.txt")


def teardown():
    print("Package teardown.")
    if os.path.exists(TEST_DATA_DIR):
        shutil.rmtree(TEST_DATA_DIR)


try:
    setup()
except:
    pass
teardown()
