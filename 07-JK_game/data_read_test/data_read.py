import json
import os
import numpy as np
import xml.etree.cElementTree as ET
import xmltodict
import pandas as pd
import xlwt

def get_task(path):
    fi = open(path, 'r')
    txt = fi.readlines()
    i = 0
    for w in txt:
        txt[i] = w.replace(',\n', '').replace('\'', '').replace(' ', '').replace('[[', '[').replace(')', '').replace(
            '((', '').replace('[', '').split(',')
        i += 1

    unit_task = [[] for _ in range(53)]
    unit_task_context = [[] for _ in range(53)]
    unit_task_num = [0 for _ in range(53)]
    unit_index = 0
    for i in range(len(txt)):
        if len(txt[i]) == 1:
            unit_task[unit_index].append(100)

            unit_index += 1
        else:
            # unit_task[unit_index].append(int(txt[i][0][0]))
            unit_task[unit_index].append(int(txt[i][0]))
            unit_task_context[unit_index].append(txt[i][2:5])
            unit_task_num[unit_index] += 1
            if txt[i][-1][-1] == ']':
                unit_index += 1

    unit_task_now = [unit_task[i][0] for i in range(53)]
    unit_task_num_now = [0 for _ in range(53)]

    return unit_task, unit_task_context, unit_task_now, unit_task_num, unit_task_num_now

def get_task_from_xml(data_path):
    task, task_context, task_now, task_num, task_num_now = get_task('outputdataforbeihang.txt')
    return task, task_context, task_now, task_num, task_num_now

def get_task_from_json(data_path):
    task, task_context, task_now, task_num, task_num_now = get_task('outputdataforbeihang.txt')
    return task, task_context, task_now, task_num, task_num_now

def get_task_from_xlsx(data_path):
    task, task_context, task_now, task_num, task_num_now = get_task('outputdataforbeihang.txt')
    return task, task_context, task_now, task_num, task_num_now

def save_txt_xml(data_path):
    task, task_context, task_now, task_num, task_num_now = get_task('outputdataforbeihang.txt')
    root = ET.Element("root")
    for i in range(len(task)):
        name='task_info_'+str(i)
        taskinfo = ET.SubElement(root, name)
        ET.SubElement(taskinfo, "task").text = str(task[i])
        ET.SubElement(taskinfo, "task_context").text = str(task_context[i])
        ET.SubElement(taskinfo, "task_now").text = str(task_now[i])
        ET.SubElement(taskinfo, "task_num").text = str(task_num[i])
        ET.SubElement(taskinfo, "task_num_now").text = str(task_num_now[i])
    tree = ET.ElementTree(root)
    tree.write('outputdataforbeihang.xml')

def save_txt_json(data_path):
    task, task_context, task_now, task_num, task_num_now = get_task('outputdataforbeihang.txt')
    xml_file = open('outputdataforbeihang.xml', 'r', encoding="utf-8")
    xml_str = xml_file.read()
    json_data = xmltodict.parse(xml_str, encoding="utf-8")
    info = json.loads(json.dumps((json_data)))

    with open('outputdataforbeihang.json', "w") as f:
        json.dump(json_data)
    print(1)


def save_txt_xlsx(data_path):
    task, task_context, task_now, task_num, task_num_now = get_task('outputdataforbeihang.txt')
    xml_file = open('outputdataforbeihang.xml', 'r', encoding="utf-8")
    xml_str = xml_file.read()
    json_data = xmltodict.parse(xml_str, encoding="utf-8")
    info = json.loads(json.dumps((json_data)))
    info = info['root']
    info_list = list(info.values())
    df = pd.DataFrame(list(info_list))
    file_path = pd.ExcelWriter('outputdataforbeihang.xlsx')
    df.to_excel(file_path, encoding='utf-8', index=False)
    file_path.save()


if __name__ == '__main__':
    xml_data_path = 'outputdataforbeihang.xml'
    json_data_path = 'outputdataforbeihang.json'
    xlsx_data_path = 'outputdataforbeihang.xlsx'

    # txt转其他三种格式
    # task, task_context, task_now, task_num, task_num_now = get_task('outputdataforbeihang.txt')
    #
    # save_txt_xml('outputdataforbeihang.txt')
    # save_txt_json('outputdataforbeihang.txt')
    # save_txt_xlsx('outputdataforbeihang.txt')


    # task, task_context, task_now, task_num, task_num_now = get_task_from_xml(xml_data_path)

    task, task_context, task_now, task_num, task_num_now = get_task_from_json(json_data_path)
    #
    # task, task_context, task_now, task_num, task_num_now = get_task_from_xlsx(xlsx_data_path)
    task_num_list = []
    for task_single in task:
        for task_num in task_single:
            if task_num not in task_num_list and task_num != 100 and task_num != -1:
                task_num_list.append(task_num)

    print(task_num_list)



