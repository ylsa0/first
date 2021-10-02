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
        conf.set('section0', '根目录', 'Y:\\')
        conf.set('section0', '账务', '高校财务信息化管理平台V6.0(账务) - 213')
        conf.set('section0', '网银', '网银6.0(oracle)')
        conf.set('section0', '工资', '高校财务信息化管理平台V6.0(工资)-213')
        conf.set('section0', '个税', '高校财务信息化管理平台V6.0(个税)')
        conf.set('section0', '收费', '学生收费系统Oracle6.0')
        conf.set('section0', '学生酬金', '高校财务信息化管理平台V6.0(学生酬金)')
        conf.set('section0', '接单', '天财高校财务接单管理系统6.0')
        conf.set('section0', '银行对账', 'yhdz银行对账程序ORA财务')
        conf.set('section0', '票据', '天财高校财务信息化管理平台V6.0(综合票据)')
        conf.add_section('section1')
        conf.set('section1', '本地目录', r'E:\北京师范大学\Oracle程序\Tcsoft')
        conf.write(open('./settings.ini', 'a', encoding='utf-8'))
    try:
        conf.read('./settings.ini', encoding='utf-8')
    except:
        conf.read('./settings.ini', encoding='utf-8-sig')
    item = dict(conf.items('section0'))
    item0 = dict(conf.items('section1'))
    item['本地目录'] = item0['本地目录']
    return item


def get_serverfile_md5(file):  # 计算文件md5值
    global dict_file, settings
    file = file.replace(settings['根目录'], 'D:\\Tcsoft\\')
    file_md5 = dict_file[file]
    return file_md5


def get_file_md5(file):  # 计算文件md5值
    m = hashlib.md5()  # 创建md5对象
    with open(file, 'rb') as fobj:
        while True:
            data = fobj.read(1048576)
            if not data:
                break
            m.update(data)  # 更新md5对象
    return m.hexdigest()


def get_dir_files(dir):  # 获取文件夹目录
    return os.listdir(dir)


def equal_file(file1, file2):  # 判断文件是否相同
    if not os.path.exists(file1):
        shutil.copy(file2, file1)
        with open('./log.txt', 'a', encoding='utf-8') as f:
            f.writelines(file1 + '\t' + file2 + '\n')
    elif get_serverfile_md5(file2) != get_file_md5(file1):
        shutil.copy(file2, file1)
        with open('./log.txt', 'a', encoding='utf-8') as f:
            f.writelines(file1 + '\t' + file2 + '\n')


def remove_file():  # 移动文件
    global des_dir
    global rsc_dir
    files_name = rsc_dir.split('\\')[-1]
    des_dir = os.path.join(des_dir, files_name)
    if not os.path.exists(des_dir):
        os.mkdir(des_dir)
    if not get_dir_files(rsc_dir):
        rsc_dir = os.path.abspath(os.path.join((rsc_dir), os.path.pardir))
        des_dir = os.path.abspath(os.path.join((des_dir), os.path.pardir))
    else:
        for i in get_dir_files(rsc_dir):
            print(os.path.join(rsc_dir, i))
            if os.path.isfile(os.path.join(rsc_dir, i)):
                rsc_file = os.path.join(rsc_dir, i)
                des_file = os.path.join(des_dir, i)
                equal_file(des_file, rsc_file)
            elif os.path.isdir(os.path.join(rsc_dir, i)):
                rsc_dir = os.path.join(rsc_dir, i)
                remove_file()
            if i == get_dir_files(rsc_dir)[-1]:
                rsc_dir = os.path.abspath(os.path.join((rsc_dir), os.path.pardir))
                des_dir = os.path.abspath(os.path.join((des_dir), os.path.pardir))


if __name__ == '__main__':  # main函数
    settings = {}
    dict_program = {}
    count = 0
    rsc_list = []
    settings = get_settings()
    des_dir = settings['本地目录']
    settings.pop('本地目录')
    print(des_dir)
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
    #print(rsc_list)
    md5_file = os.path.join(settings['根目录'], 'update\\md5.txt')
    with open(md5_file, 'r', encoding='utf-8') as f:
        list = f.read().split('\n')
        dict_file = {}
        for i in list:
            if i:
                file = i.split('\t')[0]
                md5 = i.split('\t')[1]
                dict_file[file] = md5
    for i in rsc_list:
        rsc_dir = i
        time1 = time.perf_counter()
        remove_file()
        time2 = time.perf_counter()
        print('程序运行时间：%s 秒' % (time2 - time1))
    os.system('pause')
