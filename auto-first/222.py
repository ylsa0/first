# coding=utf-8
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from email.header import Header


def smtp_email(to_addr='15822909392@163.com'):
    from_addr = '15822909392@163.com'  # 准备使用的发件人邮箱账号
    password = 'CPYSOCXEAMCUOKRX'  # 从发件人邮箱获取的授权码
    cc_addr = 'lisi.@163.com'  # 抄送人的邮箱地址

    # SMTP服务器地址,这里使用的是网易
    smtp_server = 'smtp.163.com'  # 需要哪个自己百度(注意企业邮箱服务器地址是不同的)
    # 编写邮件正文
    msg = MIMEMultipart()
    text_part = MIMEText('邮件推送测试', 'plain', 'utf-8')
    msg.attach(text_part)
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Cc'] = cc_addr
    # 使用Header对标题进行编码
    msg['Subject'] = Header('签到推送', 'utf-8').encode()
    # 构建发送服务
    server = smtplib.SMTP(smtp_server, 25)  # SMTP协议默认端口是25
    server.set_debuglevel(1)
    server.login(from_addr, password)  # 登录发件人邮箱，password是授权码！
    # 收件人和抄送人在sendmail方法里都是list类型，中间用+号连接
    server.sendmail(from_addr, [to_addr] + [cc_addr], msg.as_string())  # 收件人是一个list类型
    server.quit()
