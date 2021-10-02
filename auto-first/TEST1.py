# coding=utf-8
import configparser
import os


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
    conf.read('./settings.ini', encoding='utf-8')
    item = dict(conf.items('section0'))
    item0 = dict(conf.items('section1'))
    item['本地目录'] = item0['本地目录']
    return item

item=get_settings()
print(item)
