# coding=utf-8
import datetime
import time
import os
import configparser

import pytesseract
from PIL import Image
from selenium import webdriver
from chinese_calendar import is_workday
from tools import smtp_email


def auto_qd():  # 签到程序
    settings = get_settings()
    driver = webdriver.Chrome()
    driver.get('http://114.115.168.162:8080/wsqdWB/')  # 地址
    time.sleep(1)
    driver.save_screenshot('temp.png')
    driver.find_element_by_xpath('//*[@id="userName"]').send_keys(settings['username'])  # 用户名
    driver.find_element_by_xpath('//*[@id="password"]').send_keys(settings['password'])  # 密码
    img_url = driver.find_element_by_xpath('//*[@id="yzmImg"]')  # 验证码图片
    left = img_url.location['x']
    top = img_url.location['y']
    right = img_url.size['width'] + left
    down = img_url.size['height'] + top
    image = Image.open('temp.png')
    code_image = image.crop((left, top, right, down))
    code_image.save('yzm.png')
    image = Image.open(r'yzm.png')
    text = pytesseract.image_to_string(image)  # ocr识别验证码
    if str(text) == '':
        driver.close()
    driver.find_element_by_xpath('//*[@id="yzm"]').send_keys(str(text))  # 验证码
    time.sleep(1)
    try:
        driver.find_element_by_xpath('//*[@id="submitDiv"]/div/button').click()  # 登录
        time.sleep(1)
    except Exception as e:
        print(e)
    if 'LoginServlet' in driver.current_url:
        driver.find_element_by_xpath('//*[@id="datalistDiv"]/div[1]/div/button').click()  # 签到
        driver.find_element_by_xpath('//*[@id="datalistDiv"]/div/table/tbody/tr[2]/td[6]/input').clear()  # 清空信息
        driver.find_element_by_xpath('//*[@id="datalistDiv"]/div/table/tbody/tr[2]/td[6]/input').send_keys(settings['diqu'])  # 地区
        driver.find_element_by_xpath('//*[@id="datalistDiv"]/div/table/tbody/tr[2]/td[7]/input').clear()  # 清空信息
        driver.find_element_by_xpath('//*[@id="datalistDiv"]/div/table/tbody/tr[2]/td[7]/input').send_keys(settings['xuexiao'])  # 学校
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="datalistDiv"]/div/table/tbody/tr[2]/td[11]/button').click()  # 签到
        driver.close()
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")  # 当天日期
        with open('./log.txt', 'a') as f:
            f.writelines(current_date+'\t签到成功\n')  # 记录日志
        if settings['is_email'] in ('1', '是'):
            msg = current_date+'\t签到成功\n'
            smtp_email(settings['email'], msg)  # 发放邮件
    else:
        driver.quit()
        auto_qd()


def get_settings():  # 配置信息
    settings = {}
    conf = configparser.ConfigParser()  # 初始化
    if os.path.exists('./settings.ini'):  # 存在settings.ini
        conf.read('./settings.ini', encoding='utf-8')
        items = dict(conf.items('section0'))  # 读取配置信息
    else:
        print('初次使用，请完成初始化\n用户名：')
        settings['username'] = input()
        print('登录密码：')
        settings['password'] = input()
        print('签到地点：')
        settings['diqu'] = input()
        print('学校：')
        settings['xuexiao'] = input()
        print('是否启用邮箱推送：0、否；1、是')
        settings['is_email'] = input()
        if settings['is_email'] in ('1', '是'):
            print('邮箱：')
            settings['email'] = input()
        else:
            settings['email'] = ''
        # np.save('settings.npy', settings)
        conf.add_section('section0')
        conf.set('section0', 'username', settings['username'])
        conf.set('section0', 'password', settings['password'])
        conf.set('section0', 'diqu', settings['diqu'])
        conf.set('section0', 'xuexiao', settings['xuexiao'])
        conf.set('section0', 'is_email', settings['is_email'])
        conf.set('section0', 'email', settings['email'])
        conf.write(open('./settings.ini', 'a', encoding='utf-8'))  # 创建配置信息
        items = settings
    return items  # 返回配置信息


if __name__ == '__main__':  # 主程序
    date_now = datetime.date.today()
    if is_workday(date_now):  # 工作日
        auto_qd()
