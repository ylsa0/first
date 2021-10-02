# -*- coding: utf-8 -*-
import os
import time

import pyautogui


pyautogui.PAUSE = 1
pyautogui.FAILSAFE = True

if __name__ == '__main__':
    dir_zhangwu = r'E:\北京师范大学\Oracle程序\Tcsoft\高校财务信息化管理平台V6.0(账务)'
    try:
        os.system('start /d '+dir_zhangwu+' zwmain.exe')
        time.sleep(1)
    except Exception as e:
        print(e)
    pyautogui.press('altleft''tab')
    pyautogui.typewrite('000')
    pyautogui.press('enter')
    pyautogui.typewrite('80135')
    pyautogui.press('enter')
    pyautogui.press('enter')
    pyautogui.press('enter')
    pyautogui.click(10, 50)
    time.sleep(2)
    pyautogui.press('4')
    pyautogui.click(150, 30)
    pyautogui.click(150, 75)
    pyautogui.typewrite('03202109200001')
    time.sleep(2)
    os.system('TASKKILL /F /IM zwmain.exe /T')
