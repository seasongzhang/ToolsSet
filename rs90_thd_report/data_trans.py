import codecs
import os
import math
from win32com import client as wc
from easyoffice.easyexcel import EasyExcel as excel

doc_path = r"E:\SeaGit\ToolsSet\rs90_thd_report\data\R-000011.doc"
txt_path = r"E:\SeaGit\ToolsSet\rs90_thd_report\data\R-000011.txt"
xlsx_path = r"E:\SeaGit\ToolsSet\rs90_thd_report\data\R-000011.xlsx"


def word2txt(doc_path, txt_path):
    """
    将RS90生成的报告转换成txt文件
    :param doc_path:
    """
    word = wc.Dispatch('Word.Application')
    doc = word.Documents.Open(doc_path)
    doc.SaveAs(txt_path, 4)
    doc.Close()
    word.Quit()


def txt2data(txt_path):
    thd_data = list()
    with codecs.open(txt_path) as f:
        lines = f.readlines()
    phase_a = lines[21:82]
    phase_b = lines[167:228]
    phase_c = lines[313:379]

    def lines2dict(data_lines):

        d = dict()
        d['TableCategory'] = data_lines[3][21:22]
        d['Rsce'] = data_lines[3][30:33]
        d['TestDuration'] = data_lines[5][21:24]
        d['FileName'] = data_lines[5].split('\t')[-1][29:31]
        d['I-RMS'] = data_lines[14].strip().split('\t')[-1]
        d['I-Fund'] = float(data_lines[15].split('\t')[1])
        d['PowerFactor'] = data_lines[16].strip().split('\t')[-1]

        # 根据1-40次的有效值计算I-ref，而不是直接使用报告中提供的I-RMS，前者会比后者略小一点点
        # RS90计算limit值时就是使用上述计算所得的I-RMS，不知道为什么，本程序照着做
        # 照理来说，若按照61000-3-12:2004的标准，计算THD时是不需要I-ref的，只需要I-Fund
        # 本程序为了减少计算，直接使用报告中生成的THD，但需要根据I-ref和I-Fund的比例直接换算
        avg_list = [float(line.split('\t')[2]) for line in data_lines[20:59]]
        avg_rms = math.sqrt(sum([x * x for x in avg_list + [d['I-Fund']]]))
        # d['I-ref'] = float(data_lines[9].split('\t')[1][16:22])
        d['I-ref'] = avg_rms
        d['THD(%)'] = float(data_lines[10][10:14]) * d['I-ref'] / d['I-Fund']
        d['PWHD(%)'] = float(data_lines[10][54:58]) * d['I-ref'] / d['I-Fund']

        def harmonic_test(harmonic_data):
            limit = {'2': 0.08, '4': 0.04, '5': 0.31, '6': 0.0267, '7': 0.2,
                     '8': 0.02, '10': 0.016, '11': 0.12, '12': 0.0133,
                     '13': 0.07, 'THD': 0.37, 'PWHD': 0.38}
            dat = harmonic_data.strip().split('\t')
            order = dat[0]
            h_avg = float(dat[1])
            h_max = float(dat[4])
            s_avg = 100 * h_avg / (d['I-Fund'] * limit[order])
            s_max = 100 * h_max / (d['I-Fund'] * limit[order] * 1.5)
            if s_avg < 100 and s_max < 100:
                status = 'Pass'
            else:
                status = 'Fail'
            return [order, s_avg, s_max, status]

        harmonic_data = list()
        harmonic_data.append(harmonic_test(data_lines[20]))  # 2nd
        harmonic_data.append(harmonic_test(data_lines[22]))  # 4th
        harmonic_data.append(harmonic_test(data_lines[23]))  # 5th
        harmonic_data.append(harmonic_test(data_lines[24]))  # 6th
        harmonic_data.append(harmonic_test(data_lines[25]))  # 7th
        harmonic_data.append(harmonic_test(data_lines[26]))  # 8th
        harmonic_data.append(harmonic_test(data_lines[28]))  # 10th
        harmonic_data.append(harmonic_test(data_lines[29]))  # 11th
        harmonic_data.append(harmonic_test(data_lines[30]))  # 12th
        harmonic_data.append(harmonic_test(data_lines[31]))  # 13th

        # print(harmonic_data)

        d['HarmonicStatus'] = harmonic_data

        def pass_or_fail():
            for r in harmonic_data:
                if r[-1] == 'Fail':
                    return 'Fail'
            if d['THD(%)'] > 37 or d['PWHD(%)'] > 38:
                return 'Fail'
            return 'Pass'

        d['TestResult'] = pass_or_fail()

        return d

    thd_data.append(lines2dict(phase_a))
    thd_data.append(lines2dict(phase_b))
    thd_data.append(lines2dict(phase_c))

    return thd_data


def data2excel(book, thd_data, row):
    def data2sheet(d, phase):
        title = ['FileName', 'I-RMS', 'I-Fund', 'THD(%)', 'PWHD(%)', 'H-2nd',
                 'H-4th', 'H-5th', 'H-6th', 'H-7th', 'H-8th', 'H-10th', 'H-11th',
                 'H-12th', 'H-13th', 'Status']
        for c in range(len(title)):
            book.set_cell(phase, 1, c + 1, title[c])
        book.set_cell(phase, row, 1, d['FileName'])
        book.set_cell(phase, row, 2, d['I-RMS'])
        book.set_cell(phase, row, 3, d['I-Fund'])
        book.set_cell(phase, row, 4, d['THD(%)'])
        book.set_cell(phase, row, 5, d['PWHD(%)'])
        for n in range(10):
            book.set_cell(phase, row, n + 6, d['HarmonicStatus'][n][1])
        book.set_cell(phase, row, 16, d['TestResult'])

    data2sheet(thd_data[2], 'PhaseT')
    data2sheet(thd_data[1], 'PhaseS')
    data2sheet(thd_data[0], 'PhaseR')


if __name__ == "__main__":
    report_dir = r"E:\SeaGit\ToolsSet\rs90_thd_report\data"
    xlsx_path = os.path.join(report_dir, 'report.xlsx')
    if os.path.exists(xlsx_path):
        os.remove(xlsx_path)
    doc_list = [f for f in os.listdir(report_dir) if os.path.splitext(f)[1] == '.doc']
    row_num = 2
    book = excel(xlsx_path)
    book.add_sheet('PhaseT')
    book.add_sheet('PhaseS')
    book.add_sheet('PhaseR')
    book.delete_sheet('Sheet1')
    for doc in doc_list:
        txt_path = os.path.join(report_dir, os.path.splitext(doc)[0] + '.txt')
        word2txt(os.path.join(report_dir, doc), txt_path)
        data2excel(book, txt2data(txt_path), row_num)
        row_num += 1
    book.save(xlsx_path)
    book.close()
