import win32com.client
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formatdate

def send_email(path, result, runtime):
    from_address = 'taruka-vijayaratana@ctie.co.jp'
    charset = "UTF-8"
    subject = "【タスクスケジューラエラー】" 
    message = f"\nスケジューラ{path}でエラーが発生\n\n Last Run    : {runtime}\n Last Result  : {result}" 

    msg = MIMEText(message, 'plain', charset)
    msg['Subject'] = subject
    send_name = "水害リスクライン自動チェック"
    send_addr = from_address
    msg['From'] = '%s <%s>'%(Header(send_name.encode(charset), charset).encode(), send_addr)
    msg['To'] = from_address
    msg['Date'] = formatdate(localtime=True)

    smtp = smtplib.SMTP('smtp.tokyo.ctie.co.jp')
    smtp.sendmail(from_address, from_address, msg.as_string())
    smtp.quit()

if __name__ == '__main__':
    TASK_ENUM_HIDDEN = 1
    TASK_STATE = {0: 'Unknown',
              1: 'Disabled',
              2: 'Queued',
              3: 'Ready',
              4: 'Running'}

    scheduler = win32com.client.Dispatch('Schedule.Service')
    scheduler.Connect()

    folders = [scheduler.GetFolder('\\')]
    while folders:
        folder = folders.pop(0)
        folders += list(folder.GetFolders(0))
        tasks = list(folder.GetTasks(TASK_ENUM_HIDDEN))
        for task in tasks:
            settings = task.Definition.Settings
            if task.path =='\水系':
                file = '水系'
                result = task.LastTaskResult
                runtime = task.LastRunTime
                if result == 1:
                    send_email(file, result, runtime)
            if task.path =='\縦断':
                file = '縦断'
                result = task.LastTaskResult
                runtime = task.LastRunTime
                if result == 1:
                    send_email(file, result, runtime)

