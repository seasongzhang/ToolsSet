import os


def getdirsize(dir):
    size = 0
    for root, dirs, files in os.walk(dir):
        # print(root, dirs, files)
        size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
    return size


for root, dirs, files in os.walk("C:\\"):
    try:
        for dirname in dirs:
            dirsize = getdirsize(os.path.join(root, dirname))
            if dirsize > 1073741824:
                print("*" + dirname, str(dirsize // 1024 // 1024 // 1024) + "G")

        for filename in files:
            filesize = os.path.getsize(os.path.join(root, filename))
            if filesize > 1073741824:
                print(filename, str(filesize // 1024 // 1024) + "M")
    except PermissionError:
        continue

"""
def SelectLargeFile(dirname,level):
    #dirname = "E:\\Workspace\\Python"
    for each_item in os.listdir(dirname):
        item_path = os.path.join(dirname, each_item)
        if os.path.isfile(item_path):
            size = os.path.getsize(item_path)
            if size > 100000000:
                for tab_stop in range(level):
                    pass
                    #print("\t",end='')
                print(each_item,str(size/1024//1024)+"M")
        elif os.path.isdir(item_path):
            try:
                SelectLargeFile(item_path,level+1)
                sizedir = os.path.getsize(item_path)
                if sizedir > 1000000000:
                    print("**"+each_item,str(size/1024//1024)+"M")
            except PermissionError:
                continue
            finally:
                pass
                #print(each_item,str)
 """
