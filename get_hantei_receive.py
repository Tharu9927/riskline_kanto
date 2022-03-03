# coding: utf-8
import os
import time
import datetime
from pathlib import Path
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.alert import Alert
#import cv2
import sys
import configparser
# log
from logzero import logger
import logzero
import logging
# requests,json
import json
import requests
import shutil

# 引数読み込み
args = sys.argv

# 設定ファイル読み込み
config = configparser.ConfigParser()
config.read('setting.ini','UTF-8')
# ログイン情報
section1 = 'login'
# プロキシ情報
section2 = 'preference'
# 地方情報
section3 = 'region'
# 一覧ファイル・結果ファイル
section4 = 'receive'
# メール情報
section5 = 'mail'
# メイン情報
section6 = 'main'
# ログ情報
section7 = 'log_setting_area'
if args[1] == '1':
    wk_logfile = config.get(section7, 'file_result_receive1')
elif args[1] == '2':
    wk_logfile = config.get(section7, 'file_result_receive2')
elif args[1] == '3':
    wk_logfile = config.get(section7, 'file_result_receive3')
elif args[1] == '4':
    wk_logfile = config.get(section7, 'file_result_receive4')
elif args[1] == '5':
    wk_logfile = config.get(section7, 'file_result_receive5')
else:
    logger.error('パラメータ不正：' + args[1])
    sys.exit()

logger = logzero.setup_logger(
    name='logzero',                                                                         # loggerの名前、複数loggerを用意するときに区別できる
    logfile=config.get(section7, 'dir')+'\\'+wk_logfile,                                    # ログファイルの格納先
    level=config.getint(section7, 'level'),                                                 # 標準出力のログレベル
    formatter=logging.Formatter('[%(asctime)s]'+' %(levelname)s '+' - %(message)s'),        # ログのフォーマット
    maxBytes=config.getint(section7, 'max_byte'),                                           # ログローテーションする際のファイルの最大バイト数
    backupCount=config.getint(section7, 'backup_count'),                                    # ログローテーションする際のバックアップ数
    fileLoglevel=config.getint(section7, 'level_file'),                                     # ログファイルのログレベル
    disableStderrLogger=False                                                               # 標準出力するかどうか
    )

# URL情報
url_top = config.get(section6, 'url_top')

logger.info('■処理開始■■■■■■')

# -----------------------------------
# ログイン処理
# -----------------------------------
DEFAULT_WAITIME = 1.5
if args[1] == '1':
    user = config.get(section1, 'id_1')
    password = config.get(section1, 'pass_1')
elif args[1] == '2':
    user = config.get(section1, 'id_2')
    password = config.get(section1, 'pass_2')
elif args[1] == '3':
    user = config.get(section1, 'id_3')
    password = config.get(section1, 'pass_3')
elif args[1] == '4':
    user = config.get(section1, 'id_4')
    password = config.get(section1, 'pass_4')
elif args[1] == '5':
    user = config.get(section1, 'id_5')
    password = config.get(section1, 'pass_5')
else:
    logger.error('パラメータ不正：' + args[1])
    sys.exit()

fp = webdriver.FirefoxProfile()
fp.set_preference("network.proxy.type", config.getint(section2, 'type'))
fp.set_preference("network.proxy.http", config.get(section2, 'http'))
fp.set_preference("network.proxy.http_port", config.getint(section2, 'http_port'))

# 実行日時退避(遅延考慮し20分前の情報が対象)
start_date_time = datetime.datetime.now() - datetime.timedelta(minutes = 20)
# 誤差考慮し0分単位に切捨て
start_date_time = datetime.datetime(start_date_time.year, start_date_time.month, start_date_time.day, start_date_time.hour, round(start_date_time.minute,-1), 0)
#start_date_time = datetime.datetime(2021 , 9 , 3 , 22, 20) #デバッグ等で使用
# 時刻設定
tm = start_date_time
logger.info(start_date_time)

# 0:デスクトップ、1:システム規定のフォルダ、2:ユーザ定義フォルダ
fp.set_preference("browser.download.folderList",2)
# 上記で2を選択したのでファイルのダウンロード場所を指定
fp.set_preference("browser.download.dir", os.getcwd())
# ダウンロード完了時にダウンロードマネージャウィンドウを表示するかどうかを示す真偽値。
fp.set_preference("browser.download.manager.showWhenStarting",False)
# mimeタイプを設定
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/zip, application/octet-stream")
# headless
options = Options()
options.add_argument('-headless')

fp.update_preferences()
driver = webdriver.Firefox(firefox_profile=fp, firefox_options=options, log_path=os.path.devnull)
driver.implicitly_wait(DEFAULT_WAITIME)

# フォルダ作成（引数により地方を分ける）
main_dir = config.get(section4, 'result')
date_dir = start_date_time.strftime('%Y%m%d')
datetime_dir = start_date_time.strftime('%Y%m%d%H%M')

# 引数チェックと設定
if args[1] == '1':
    region_name = config.get(section3, 'region_1_name')
    df_inp = pd.read_csv(config.get(section4, 'receive_1_list'), encoding='cp932')
    region_dir = config.get(section3, 'region_1')
elif args[1] == '2':
    region_name = config.get(section3, 'region_2_name')
    df_inp = pd.read_csv(config.get(section4, 'receive_2_list'), encoding='cp932')
    region_dir = config.get(section3, 'region_2')
elif args[1] == '3':
    region_name = config.get(section3, 'region_3_name')
    df_inp = pd.read_csv(config.get(section4, 'receive_3_list'), encoding='cp932')
    region_dir = config.get(section3, 'region_3')
elif args[1] == '4':
    region_name = config.get(section3, 'region_4_name')
    df_inp = pd.read_csv(config.get(section4, 'receive_4_list'), encoding='cp932')
    region_dir = config.get(section3, 'region_4')
elif args[1] == '5':
    region_name = config.get(section3, 'region_5_name')
    df_inp = pd.read_csv(config.get(section4, 'receive_5_list'), encoding='cp932')
    region_dir = config.get(section3, 'region_5')
else:
    logger.error('パラメータ不正：' + args[1])
    sys.exit()

# フォルダ作成
if not os.path.exists(os.path.join(os.getcwd(),main_dir,region_dir)):
    os.mkdir(os.path.join(os.getcwd(),main_dir,region_dir))
if not os.path.exists(os.path.join(os.getcwd(),main_dir,region_dir,date_dir)):
    os.mkdir(os.path.join(os.getcwd(),main_dir,region_dir,date_dir))
if not os.path.exists(os.path.join(os.getcwd(),main_dir,region_dir,date_dir,datetime_dir)):
    os.mkdir(os.path.join(os.getcwd(),main_dir,region_dir,date_dir,datetime_dir))

# 一覧読み込み
urls = df_inp['url'].values
suikei_names = df_inp['suikei_name'].values
river_names = df_inp['river_name'].values

stat_receives = []
error_msg = ''

# ログイン画面
driver.get(url_top)
#logger.info('ログイン処理開始')
time.sleep(3)
driver.find_element_by_xpath('//*[@id="user_id"]').send_keys(user)
driver.find_element_by_xpath('//*[@id="password"]').send_keys(password)
driver.find_element_by_xpath('/html/body/div[2]/form/div[2]/button').click()
time.sleep(5)
#logger.info('ログイン処理終了')

# リクエスト
session = requests.session()
for cookie in driver.get_cookies():
    session.cookies.set(cookie["name"], cookie["value"])

# 一時フォルダ削除/作成
#if os.path.isdir('./json/'):
#    shutil.rmtree('./json/')
#os.mkdir('./json/')

# メイン処理
for cnt, (url, suikei_name, river_name) in enumerate(zip(urls, suikei_names, river_names)):
    result_flg = 0
    try:
        logger.info("■"+suikei_name+" "+river_name+' start')
        # ファイル保存
        url = url + tm.strftime('%Y') + '/' + tm.strftime('%m') + '/' + tm.strftime('%d') + '/' + tm.strftime('%H') + '/' + tm.strftime('%M') + '.json'
        logger.info("　"+url)
        result = session.post(url)
        file_name = os.path.join(os.getcwd(),main_dir,region_dir,date_dir,datetime_dir,suikei_name + '_' + river_name + '.json')
        with open(file_name, "w") as f:
            f.write(result.text)
        
        # JSON読み込み
        with open(file_name, "r") as f:
            jsn = json.load(f)
        
        # 未受信判定
        if ((jsn["dangerousness_r"][1][0][2]) == -9999):
            logger.warning("　予測データ未受信")
            stat_receives.append("予測データ未受信")
            error_msg = error_msg + suikei_name + " " + river_name + ",予測データ未受信\r\n"
        else:
            logger.info("　正常")
            stat_receives.append("正常")
        
    except:
        logger.error('エラー発生', exc_info=True)
        stat_receives.append('networkerror')

        # エラーメッセージに追加する
        error_msg = error_msg + suikei_name + " " + river_name + ",チェックエラー\r\n"

    #logger.info("■"+suikei_name+" "+river_name+' end')

# ログアウト
try:
    # ログイン状態でトップ画面
    #logger.info('ログアウト処理開始')
    driver.get(url_top)
    time.sleep(2)
    driver.find_element_by_xpath('/html/body/div[1]/div/span/button/img').click()
    time.sleep(1)
    Alert(driver).accept()
    time.sleep(1)
    #logger.info('ログアウト処理完了')
except:
    logger.error(' ログアウトエラー', exc_info=True)

driver.quit()

# 結果出力
#out = pd.DataFrame({'suikei_name': df_inp.iloc[:, 0],
#                    'kasen_name': df_inp.iloc[:, 1],
#                    'stat_receive': stat_receives})[['suikei_name', 'kasen_name', 'stat_receive']]
#csv_name = main_dir+"_"+start_date_time.strftime('%Y%m%d%H%M')+".csv"
#out.to_csv(os.path.join(main_dir,region_dir,date_dir,csv_name),encoding='utf_8_sig')

# フォルダ削除
if os.path.isdir(os.path.join(os.getcwd(),main_dir,region_dir)):
    shutil.rmtree(os.path.join(os.getcwd(),main_dir,region_dir))


# メール送信
import smtplib
 
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formatdate

if error_msg != '' :
    if __name__ == '__main__':

        # 引数により地方を分ける
        from_address = config.get(section5, 'address')
        if args[1] == '1':
            to_address = config.get(section5, 'region_1_to')
            cc_address = config.get(section5, 'region_1_cc')
        elif args[1] == '2':
            to_address = config.get(section5, 'region_2_to')
            cc_address = config.get(section5, 'region_2_cc')
        elif args[1] == '3':
            to_address = config.get(section5, 'region_3_to')
            cc_address = config.get(section5, 'region_3_cc')
        elif args[1] == '4':
            to_address = config.get(section5, 'region_4_to')
            cc_address = config.get(section5, 'region_4_cc')
        elif args[1] == '5':
            to_address = config.get(section5, 'region_5_to')
            cc_address = config.get(section5, 'region_5_cc')
        else:
            logger.error('パラメータ不正：' + args[1])
            sys.exit()
        # TOとCC
        sendToList=to_address.split(',')+cc_address.split(',')

        charset = "UTF-8"
        subject = "【自動送信："+region_name+"洪水予測】" + start_date_time.strftime('%Y/%m/%d %H:%M') + "の未受信チェックで予測未連携河川もしくはエラーが発生"
        message = "各位" + "\r\n\r\n"
        message = message + start_date_time.strftime('%Y/%m/%d %H:%M') + "未受信チェックにて予測未連携河川もしくはエラーが発生しております。" + "\r\n"
        message = message + "対象は以下のとおりです。" + "\r\n==================================\r\n" + error_msg + "\r\n=========================\r\n"
        message = message + "※メール後に解消されている場合があります。" + "\r\n"
        message = message + "以下URLにて確認可能です。" + "\r\n" + "https://frlg.river.go.jp"

        message = message + "\r\n\r\n"
        message = message + "\r\n"+config.get(section5, 'message_suikei1')
        message = message + "\r\n"+config.get(section5, 'message_suikei2')
        message = message + "\r\n"+config.get(section5, 'message_suikei3')
        message = message + "\r\n"+config.get(section5, 'message_suikei4')
        message = message + "\r\n"+config.get(section5, 'message_suikei5')
        message = message + "\r\n"+config.get(section5, 'message_suikei6')

        msg = MIMEText(message, 'plain', charset)
        msg['Subject'] = subject
        send_name = config.get(section5, 'from')
        send_addr = from_address
        msg['From'] = '%s <%s>'%(Header(send_name.encode(charset), charset).encode(), send_addr)
        msg['To'] = to_address
        msg['Date'] = formatdate(localtime=True)

        smtp = smtplib.SMTP(config.get(section5, 'smtp'))
        smtp.sendmail(from_address, sendToList, msg.as_string())
        smtp.quit()

        logger.info(from_address)
        logger.info(sendToList)
        logger.info(subject)
        logger.info(message)

logger.info('■処理終了')