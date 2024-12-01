# api/send_email.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json

def handler(request):
    # 邮件发送者和接收者
    sender_email = 'wangyanjun13@qq.com'
    receiver_email = 'wangyanjun13@foxmail.com'
    password = 'xoxawdmnfpzvdbid'  # 使用授权码而不是QQ密码

    # 解析请求体
    request_body = json.loads(request.get('body', '{}'))
    subject = request_body.get('subject', '默认主题')
    body = request_body.get('body', '默认内容')

    # 创建MIMEText对象
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # 连接到SMTP服务器
        server = smtplib.SMTP('smtp.qq.com', 587)  # QQ邮箱SMTP服务器
        server.starttls()  # 启用TLS加密
        server.login(sender_email, password)  # 登录邮箱
        server.sendmail(sender_email, receiver_email, msg.as_string())  # 发送邮件
        return {
            'statusCode': 200,
            'body': json.dumps({'status': 'success', 'message': '邮件发送成功！'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'status': 'error', 'message': str(e)})
        }
    finally:
        server.quit()  # 关闭连接