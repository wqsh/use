def PeptideAndModloc(test):
    '''
    :param test:鉴定出的带修饰的肽段
    :return: 返回list,包括肽段和发生修饰的位点
    '''

    new = ''
    cut = 0
    num = 0
    loc = []
    flag = 1
    for i in range(len(test)):
        if (test[i] >= 'A') & (test[i] <= 'Z'):
            new = new + test[i]
            flag = 0
            cut = cut + num
            num = 0
        else:
            num = num + 1
            if flag == 0:
                loc.append(i - cut)
                flag = 1
    output = [new, loc]
    return output
class CPhospho:
    pro_index = []  #索引txt中的行号，方便去excel(这个值要+1)中反查，
    pro_name = []  #蛋白名
    pro_site = []  #修饰位点
    pro_site_num = []  #修饰数量
    pro_pep = []  #给出的鉴定肽段
    pro_pep_num = []  #肽段数
    pro_pep_window = []  #肽段修饰窗
    site_loc = []  #发生磷酸化修饰的位置

    out_pep = []

def readpro(FILE_PATH):
    protein = {}
    f=open(FILE_PATH)
    protein_buffer = ''
    pro_name = ''
    for line in f:
        if not line.startswith('>'):
            protein_buffer = protein_buffer + line.replace('\n', '')#去掉行尾的换行符真的很重要！  
        else:
            protein[pro_name] = protein_buffer
            protein_buffer = ''
            pro_name = line.split(' ')[0].replace('>', '')
    f.close()
    protein[pro_name] = protein_buffer
    protein.pop('')
    return protein


need_left_len = 10
need_right_len = 10

'''
修改文件路径
'''
FILE_NAME = 'E:\\work\\USE\\FILE\\Phospho (ST)Sites.txt'
PRO_PATH = 'E:\\work\\USE\\FILE\\uniprot-proteome%3AUP000000589+reviewed%3Ayes.fasta'
with open(FILE_NAME, 'r') as f:
    buffer = f.readlines()
phospho = CPhospho()
'''
要需要的那一列数据
'''
line_num = 1
for line in buffer:
    list_line = line.split('\t')
    if list_line[0].startswith('sp'):
        if list_line[12] == '':
            pass
        else:
            phospho.pro_index.append(line_num)
            phospho.pro_name.append(list_line[0].split(';'))
            phospho.pro_site.append(list_line[1])
            phospho.pro_site_num.append(list_line[12].split(';'))
            phospho.pro_pep.append(list_line[14].split(';'))
            phospho.pro_pep_num.append(len(list_line[14].split(';')))
            phospho.pro_pep_window.append(list_line[15])
    line_num = line_num + 1


#初提取，筛选没有磷酸化的，超出提供范围的和边界的都进入蛋白库匹配取二次提取
for i in range(len(phospho.pro_index)):  #遍历所有候选肽段
    if len(phospho.pro_name[i]) > 1:  #出现对应多个蛋白，分别求其肽段
        if len(phospho.pro_name[i]) == phospho.pro_pep_num[i]: #一个蛋白有一个肽段序列
            all_need_pep = []
            pep_site_loc = []

            mod_site = []
            list_window = phospho.pro_pep_window[i].split(';')
            mod_num = 0
            for k in range(len(list_window)):  #它们的修饰位点都是一样的
                if list_window[k] == 'Phospho (ST)':
                    mod_site.append(k - mod_num)
                elif list_window[k] == 'Phospho (STY)':
                    mod_num = mod_num + 1
            for k in range(len(phospho.pro_name[i])):
                pep_site_loc.append(mod_site)

            for j in range(len(phospho.pro_name[i])):  #分别找每个蛋白对应的肽段序列
                need_pep = []
                if len(pep_site_loc[0]) == 0:

                    need_pep.append("none_find")
                else:

                    if phospho.pro_pep[i][j][0] == '_':
                        for k in range(len(phospho.pro_pep[i])):
                            if phospho.pro_pep[i][j][k] != '_':
                                len_pep = len(phospho.pro_pep[i][j]) - k
                                break
                    elif phospho.pro_pep[i][j][-1] == '_':
                        for k in range(len(phospho.pro_pep[i])):
                            if phospho.pro_pep[i][j][k] != '_':
                                len_pep = len(phospho.pro_pep[i][j]) - k
                                break
                    else:

                        len_pep = len(phospho.pro_pep[i][j])
                    index = 0
                    for pep_site_loc_index in pep_site_loc[j]:  # 直接从给定参考肽段里取肽段

                        if (-1 < pep_site_loc[k][index] - need_left_len) & (
                                pep_site_loc[k][index] + need_right_len < len_pep):  # 直接从给定参考肽段里取肽段
                            if len_pep < 31:
                                need_pep.append('out_of_find_unipro')
                            else:
                                need_pep.append(phospho.pro_pep[i][j][(pep_site_loc_index - need_left_len):(
                                            pep_site_loc_index + need_right_len + 1)])
                        else:
                            need_pep.append('out_of_find_unipro')
                        index = index + 1
                all_need_pep.append(need_pep)

            phospho.site_loc.append(mod_site)  # 存其修饰位点位置
            phospho.out_pep.append(all_need_pep)

        elif len(phospho.pro_name[i]) > phospho.pro_pep_num[i]: #多个蛋白都对应这个肽段
            pep_site_loc = []
            all_need_pep = []

            for j in range(len(phospho.pro_name[i])):

                list_window = phospho.pro_pep_window[i].split(';')
                need_pep = []
                mod_site = []
                if phospho.pro_pep[i][0][0] == '_':
                    for k in range(len(phospho.pro_pep[i])):
                        if phospho.pro_pep[i][0][k] != '_':
                            len_pep = len(phospho.pro_pep[i][0]) - k
                            break
                elif phospho.pro_pep[i][0][-1] == '_':
                    for k in range(len(phospho.pro_pep[i])):
                        if phospho.pro_pep[i][0][k] == '_':
                            len_pep = k - 1
                            break
                else:
                    len_pep = len(phospho.pro_pep[i][0])
                mod_num = 0
                for k in range(len(list_window)):
                    if list_window[k] == 'Phospho (ST)':
                        mod_site.append(k - mod_num)
                    elif list_window[k] == 'Phospho (STY)':
                        mod_num = mod_num + 1
                pep_site_loc.append(mod_site)

                if len(pep_site_loc[j]) == 0:
                    need_pep.append('none_find')
                else:
                    index = 0
                    for pep_site_loc_index in pep_site_loc[j]:  # 直接从给定参考肽段里取肽段
                        if (-1 < pep_site_loc[j][index] - need_left_len) & (pep_site_loc[j][index] + need_right_len < len_pep):# 直接从给定参考肽段里取肽段
                            if len_pep < 31:
                                need_pep.append('out_of_find_unipro')
                            else:
                                need_pep.append(phospho.pro_pep[i][0][(pep_site_loc_index - need_left_len):(pep_site_loc_index + need_right_len + 1)])
                        else:
                            need_pep.append('out_of_find_unipro')
                        index = index + 1
                all_need_pep.append(need_pep)
            phospho.site_loc.append(mod_site)  # 存其修饰位点位置
            phospho.out_pep.append(all_need_pep)

    else:  #只对应一个蛋白的一个肽段
        list_window = phospho.pro_pep_window[i].split(';')
        mod_site = []
        need_pep = []
        all_need_pep = []
        mod_num = 0
        for j in range(len(list_window)):
            if list_window[j] == 'Phospho (ST)':
                mod_site.append(j - mod_num)
            elif list_window[j] == 'Phospho (STY)':
                mod_num = mod_num + 1
        phospho.site_loc.append(mod_site)
        if phospho.pro_pep[i][0][0] == '_':
            for k in range(len(phospho.pro_pep[i][0])):
                if phospho.pro_pep[i][0][k] != '_':
                    len_pep = len(phospho.pro_pep[i][0]) - k
                    break
        elif phospho.pro_pep[i][0][-1] == '_':
            for k in range(len(phospho.pro_pep[i][0])):
                if phospho.pro_pep[i][0][k] == '_':
                    len_pep = k - 1
                    break
        else:
            len_pep = len(phospho.pro_pep[i][0])
        if len(phospho.site_loc[i]) == 0: #没有磷酸化修饰
            need_pep.append('none_find')
        else:

            index = 0
            for pep_site_loc_index in phospho.site_loc[i]:
                if (-1 < phospho.site_loc[i][index] - need_left_len) & (phospho.site_loc[i][index] + need_right_len < len_pep):# 直接从给定参考肽段里取肽段
                    if len_pep < 31:
                        need_pep.append('out_of_find_unipro')

                    else:
                        need_pep.append(phospho.pro_pep[i][0][(pep_site_loc_index - need_left_len):(pep_site_loc_index + need_right_len + 1)])
                else:
                    need_pep.append('out_of_find_unipro')

                index = index + 1
        all_need_pep.append(need_pep)
        phospho.out_pep.append(all_need_pep)

protein = readpro(PRO_PATH)






'''
以上部分目前没问题
'''

for i in range(len(phospho.pro_index)):
    find_pep_left = -1
    find_pep_right = -1
    find_pro_name = phospho.pro_name[i]
    pro_num = len(phospho.pro_name[i])

    for j in range(pro_num):
        site_num = len(phospho.site_loc[i])
        find_pro_name = phospho.pro_name[i][j]
        pep_num = len(phospho.pro_pep[i])
        if find_pro_name in protein.keys():
            find_pro_pep = protein[find_pro_name]
        else:
            continue
        for n in range(pep_num):
            for k in range(site_num):  #遍历修饰位点
                if phospho.out_pep[i][n][k] == 'none_find':
                    pass
                    #phospho.out_pep[i][n][k] = ''
                elif phospho.out_pep[i][n][k] == 'out_of_find_unipro': #这些是超出索引的，让它们取蛋白库找
                    find_pep = phospho.pro_pep[i][n]
                    for index in range(len(find_pep)):  #处理那些在链端的肽段
                        if (find_pep[index] >= 'A') & (find_pep[index] <= 'Z'):
                            if find_pep_left == -1:
                                find_pep_left = index
                        if (find_pep_left != -1) & ((find_pep[index] < 'A') | (find_pep[index] > 'Z')):
                            find_pep_right = index - 1
                            break
                    if find_pep_right == -1:
                        find_pep_right = len(find_pep) - 1
                    find_site = phospho.site_loc[i]

                    len_find_pep = find_pep_right - find_pep_left + 1

                    for m in range(len(find_pro_pep)):  #蛋白库的肽段
                        if m > len(find_pro_pep) - find_pep_right - 1:
                            phospho.out_pep[i][n][k] = 'none_find'
                            break
                        else:
                            if (find_pro_pep[m] == find_pep[find_pep_left]) & (find_pro_pep[m + len_find_pep - 1] == find_pep[find_pep_right]):
                                if find_pro_pep[m: m + len_find_pep] == find_pep.replace('_', ''):
                                    if (find_site[k] + m - need_left_len < 0) | (find_site[k] + m + need_right_len + 1 > len(find_pro_pep)):
                                        phospho.out_pep[i][n][k] = 'none_find'
                                        break
                                    else:
                                        phospho.out_pep[i][n][k] = find_pro_pep[find_site[k] + m - need_left_len: find_site[k] + m + need_right_len + 1]
                                        break
                            else:
                                pass
                else:
                    pass

output = open('data.txt', 'w', encoding='gbk')
output.write('pro_name\tout_pep\tpro_pep\n')
for i in range(len(phospho.pro_name)):
    for j in range(len(phospho.pro_pep[i])):
        output.write(str(phospho.pro_index[i]))
        output.write('\t')
        output.write(str(phospho.pro_name[i][j]))
        output.write('\t')#相当于Tab一下，换一个单元格
        output.write(str(phospho.out_pep[i][j]))
        output.write('\n')       #写完一行立马换行
output.close()


'''
for i in range(len(phospho.pro_name)):
    for j in range(len(phospho.pro_pep[i])):
        for k in range(len(phospho.out_pep[i][j])):
            for l in range(10):
                acid_left = phospho.out_pep[i][j][k][20 - l]
                acid_right = phospho.out_pep[i][j][k][20 + l]
'''
print('haha')