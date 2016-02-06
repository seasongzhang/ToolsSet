"""
    This script is used for:
    1. check whether directory r"J:\\UGNX\\NX_LIB", including all the files
    and dirs inside, has been updated. If YES, find the ones which

    testdata design:


    需要一个增量式的log，记录每一次的变更

    Functions:
    1. Read dirs and files information;
    2. For dirs or files that exist in src but not in dst, record into add_list;
    3. For files that both exist in src and dst, compare the update time,
       if not consist, record into diff_list with dir's name;
    4. For dirs that both exist in src and dst, step into 2.

"""
import os


class Log:
    def __init__(self, src, dst):
        pass
        # self.log_

    def log_last_status(self):
        pass

    def dump_log(self):
        pass


class SrcChecker:

    def __init__(self):
        pass

        # def find_
    def src_equal_file(self):
        pass


# class


if __name__ == "__main__":
    print(os.getcwd())
    dir_src = r"xparts_update\testdata\src"
    dir_dst = r"xparts_update\testdata\dst"
    for x in os.listdir(dir_src):
        print(x)
    pass
