# coding=utf-8
import configparser
import hashlib
import os
import shutil
import time


def get_settings():
    conf = configparser.ConfigParser()
    if not os.path.exists('./settings.ini'):
        conf.add_section('section0')
        conf.set('section0', '根目录', r'\\192.168.1.221\Tcsoft')
        conf.set('section0', '账务', '高校财务信息化管理平台V6.0(账务) - 213')
        conf.set('section0', '网银', '网银6.0(oracle)')
        conf.set('section0', '工资', '高校财务信息化管理平台V6.0(工资) - 213')
        conf.set('section0', '个税', '高校财务信息化管理平台V6.0(个税)')
        conf.set('section0', '收费', '学生收费系统Oracle6.0')
        conf.set('section0', '学生酬金', '高校财务信息化管理平台V6.0(学生酬金)')
        conf.set('section0', '接单', '天财高校财务接单管理系统6.0')
        conf.set('section0', '银行对账', 'yhdz银行对账程序ORA财务')
        conf.set('section0', '票据', '天财高校财务信息化管理平台V6.0(综合票据)')
        conf.write(open('./settings.ini', 'a', encoding='utf-8'))
    conf.read('./settings.ini', encoding='utf-8')
    item = dict(conf.items('section0'))
    return item


def get_file_md5(file):  # 计算文件md5值
    m = hashlib.md5()  # 创建md5对象
    with open(file, 'rb') as fobj:
        while True:
            data = fobj.read(1048576)
            if not data:
                break
            m.update(data)  # 更新md5对象
    with open('./md5.txt', 'a', encoding='utf-8') as f:
        f.writelines(file+'\t'+m.hexdigest()+'\n')
    return m.hexdigest()


def get_dir_files(dir):  # 获取文件夹目录
    return os.listdir(dir)


def equal_file(file1, file2):  # 判断文件是否相同
    if not os.path.exists(file1):
        shutil.copy(file2, file1)
        with open('./log.txt', 'a', encoding='utf-8') as f:
            f.writelines(file1 + '\t' + file2 + '\n')
    elif get_file_md5(file2) != get_file_md5(file1):
        shutil.copy(file2, file1)
        with open('./log.txt', 'a', encoding='utf-8') as f:
            f.writelines(file1 + '\t' + file2 + '\n')


def remove_file():  # 移动文件
    global des_dir
    global rsc_dir
    if not get_dir_files(rsc_dir):
        rsc_dir = os.path.abspath(os.path.join((rsc_dir), os.path.pardir))
    else:
        for i in get_dir_files(rsc_dir):
            print(os.path.join(rsc_dir, i))
            if os.path.isfile(os.path.join(rsc_dir, i)):
                rsc_file = os.path.join(rsc_dir, i)
                # equal_file(des_file, rsc_file)
                # shutil.copy(rsc_file, des_file)
                get_file_md5(rsc_file)
            elif os.path.isdir(os.path.join(rsc_dir, i)):
                rsc_dir = os.path.join(rsc_dir, i)
                remove_file()
            if i == get_dir_files(rsc_dir)[-1]:
                rsc_dir = os.path.abspath(os.path.join((rsc_dir), os.path.pardir))


if __name__ == '__main__':  # main函数
    settings = get_settings()
    dict_program = {}
    count = 0
    rsc_list = []
    text = '选择程序（多选按空格分隔）：\n'
    for i in settings:
        if count == 0:
            dict_program['0'] = '全部'
            count += 1
            text = text+"0：全部；"
        else:
            dict_program[str(count)] = i
            text = text + str(count) + '：' + i + '；'
            count += 1
    print(text)
    choice = input()
    if '0' in choice.split(' '):
        for i in dict_program:
            if i != '0':
                rsc_list.append(os.path.join(settings['根目录'], settings[dict_program[i]]))
    else:
        for i in choice.split(' '):
            if i in dict_program:
                rsc_list.append(os.path.join(settings['根目录'], settings[dict_program[i]]))
    for i in rsc_list:
        rsc_dir = i
        time1 = time.perf_counter()
        remove_file()
        time2 = time.perf_counter()
        print('程序运行时间：%s 秒' % (time2 - time1))
