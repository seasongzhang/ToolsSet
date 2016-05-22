import os
import stat


import time
#获得当前时间时间戳
now = int(time.time())
timeArray = time.localtime(now)
otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
print(otherStyleTime)

# path = r"c:\d\a.txt"
# a = os.path.split(path)
# print(a)
# b = os.path.split(a[0])
# print(b)


# if not os.path.exists(path):
#     f = open(path, 'w')
#     f.close()
# mode = os.stat(path)[stat.ST_MODE]
# imode = stat.S_IMODE(mode)
# print(oct(imode))
# print(oct(imode+0o222))
# os.chmod(path, imode + 0o222)
# mode = os.stat(path)[stat.ST_MODE]
# imode = stat.S_IMODE(mode)
# print(oct(imode))
