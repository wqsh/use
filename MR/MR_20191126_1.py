FILE_NAME = 'E:\\work\\USE\\FILE\\results(1).txt'
'''
需要输入的文件路径改这个就行
'''

with open(FILE_NAME, 'r') as f:
    buffer = f.readlines()
flag_1 = 0
flag_2 = 0
need_rec = []

'''
提取Final Prediction的结果
'''
for line in buffer:
    #print(line)
    if line.startswith("  Final Prediction:"):
        flag_1 = 1
    elif flag_1 == 1:
        for i in range(len(line)):
            if (line[i] != ' ') & (flag_2 == 0):
                left = i
                flag_2 = 1
            elif ((line[i] == ' ') | (line[i] == '\n')) & (flag_2 == 1):
                right = i
                flag_2 = 0
                break
        need_rec.append(line[left:right])
        flag_1 = 0
need_result = []
result_num = []
'''
计数
'''
for i in need_rec:
    if i not in need_result:
        need_result.append(i)
        result_num.append(1)
    else:
        num_index = need_result.index(i)
        result_num[num_index] = result_num[num_index] + 1
'''
输出计数结果
'''
for i in range(len(need_result)):
    print(need_result[i], ":", result_num[i])
print("end")