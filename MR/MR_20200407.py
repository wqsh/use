import csv
import numpy as np

'''
修改这里
=================================================
'''
SCORE_THRESHOLD = 0.1  # 分数阈值
MAX_NUM = 5  # 最多输出数量
MIN_NUM = 2  # 最少得有数量
FILE_PATH = 'E:\\work\\USE\\MR\\human+reviewed_yes20191224_2020.01.15.filtered_cross-linked_sites.csv' # 读入文件
OUT_PATH = 'test1.csv'  # 输出文件
'''
=================================================
'''

OUT = []
buffer = []
title = []
flag = 0
num = 0
line_num = 0
last_line = [[]]
with open(FILE_PATH, 'r') as csvFile:
    reader = csv.reader(csvFile)
    for line in reader:
        #print(line)
        if line_num < 2:
            OUT.append(line)
            line_num = line_num + 1
            continue
        if len(last_line[0]) == 0:
            if len(line[0]) != 0:
                score = []
                for item in buffer:
                    score.append(float(item[9]))
                sort_score_index = np.argsort(np.array(score))
                num = 0
                out_buffer = []
                for item in sort_score_index:
                    if score[item] < SCORE_THRESHOLD:
                        num = num + 1
                        if num <= MAX_NUM:
                            out_buffer.append(buffer[item])
                        else:
                            break
                    else:
                        break
                if len(out_buffer) != 0 and len(out_buffer) >= MIN_NUM:
                    for item in title:
                        OUT.append(item)
                    for item in out_buffer:
                        OUT.append(item)
                title = []
                buffer = []
                num = 0
                title.append(line)
            else:
                buffer.append(line)
        else:
            if len(line[0]) != 0:
                title.append(line)
            else:
                buffer.append(line)
        line_num = line_num + 1
        last_line = line

with  open(OUT_PATH,'w', newline='') as csvFile:
    writer = csv.writer(csvFile)
    #先写columns_name
    #writer.writerow(OUT[0])
    #写入多行用writerows
    writer.writerows(OUT)