import codecs
import csv
import os

dir_path = r"E:\SyncPrj\交流电抗器ACR与直流电抗器DCR方案研究\4.ACR_DCR分档策略\合同数据\EIS导出数据"

subcomp_list = []
contract_list = []

contract_file = os.path.join(dir_path, r"contract_list.csv")

"If output file exists, delete it."
if os.path.exists(contract_file):
    os.remove(contract_file)

"Read all csv_files's data into contract list without head title"
for file in os.listdir(dir_path):
    ele_type = file.split("_")[0]
    ele_speed = file.split("_")[1]
    # print(file.split("_")[2])
    ele_cap = file.split("_")[2].split(".")[0]
    # print((ele_type, ele_speed, ele_cap))
    with codecs.open(os.path.join(dir_path, file)) as f:
        rd = csv.reader(f)
        for r in rd:
            if not r[0] == r"版本":
                contract_list.append((r[1], r[4], ele_speed, ele_cap, r[5], r[6], r[7], r[2], r[3]))
                # if r[7] not in subcomp_list:
                #     subcomp_list.append(r[7])

# TODO-seasong pre-process contract list

"Write contract list into contract.csv."
with open(os.path.join(dir_path, "contract_list.csv"), 'w', newline='') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerow((r'合同号', r'电梯类型', r'速度(m/min)', r'载重(kg)', r'交货期', r'客户名称', r'分公司', r'梯号', r'配方类别'))
    for r in contract_list:
        writer.writerow(r)
