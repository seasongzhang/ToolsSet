import os
import shutil
import codecs


# This script is used for:
# 1. check whether directory r"J:\\UGNX\\NX_LIB", including all the files
# and dirs inside, has been updated. If YES, find the ones which
#
# testdata design:
#
#
# 需要一个增量式的log，记录每一次的变更
#
# Functions:
# 1. Read dirs and files information;
# 2. For dirs or files that exist in src but not in dst, record into add_list;
# 3. For files that both exist in src and dst, compare the update time,
#    if not consist, record into diff_list with dir's name;
# 4. For dirs that both exist in src and dst, step into 2.


class Log:
    def __init__(self, dir_src, dir_dst):
        self.dir_src = dir_src
        self.dir_dst = dir_dst
        self.log_not_in_dst = []
        self.log_src_is_newer = []

    def src_to_dst(self, file_path):
        return file_path.replace(self.dir_src, self.dir_dst)

    def walk(self, dir_src):
        root, dirs, files = os.walk(dir_src).__next__()
        for f in files:
            file_path = os.path.join(root, f)
            if not (os.path.exists(self.src_to_dst(file_path))):
                self.log_not_in_dst.append(file_path)
            elif os.stat(file_path).st_mtime_ns > os.stat(self.src_to_dst(file_path)).st_mtime_ns:
                self.log_src_is_newer.append(file_path)
        for d in dirs:
            self.walk(os.path.join(root, d))

    def show(self):
        with codecs.open("xparts_log.txt", "w", encoding='utf-8') as f:
            print("These files are in src but not in dst.")
            f.write("These files are in src but not in dst.\r\n")
            for x in self.log_not_in_dst:
                print(x)
                f.write(x + "\r\n")
            print()
            f.write("\r\n  ")
            print("These files are newer src than in dst.")
            f.write("These files are newer src than in dst.\r\n")
            for x in self.log_src_is_newer:
                print(x)
                f.write(x + "\r\n")

    def do(self):
        for f in self.log_src_is_newer:
            try:
                shutil.copyfile(f, self.src_to_dst(f))
            except PermissionError:
                os.chmod(self.src_to_dst(f), )
            print("Copy " + f + " from src to dst.")

        for f in self.log_not_in_dst:
            shutil.copyfile(f, self.src_to_dst(f))
            print("Copy " + f + " from src to dst.")


if __name__ == "__main__":
    ds = r"D:\Backup\NX_LIB"
    dd = r"D:\Backup\XParts"
    log = Log(ds, dd)
    log.walk(ds)
    log.show()
    log.do()
