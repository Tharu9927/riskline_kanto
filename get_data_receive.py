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
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
#import cv2
import sys
import configparser
# log
from logzero import logger
import logzero
import logging
import traceback

# 引数読み込み
args = sys.argv

# 設定ファイル読み込み
config = configparser.ConfigParser()
config.read('settingS.ini','UTF-8')

# ログイン情報
section1 = 'login'
# プロキシ情報
section2 = 'preference'
# 地方情報
section3 = 'region'
# 一覧ファイル・結果ファイル
section4 = 'suikei'
# メール情報
section5 = 'mail'
# メイン情報
section6 = 'main'
# ログ情報

section7 = 'log_setting_area'
if args[1] == '1':
    wk_logfile = config.get(section7, 'file_result_suikei1')
elif args[1] == '2':
    wk_logfile = config.get(section7, 'file_result_suikei2')
elif args[1] == '3':
    wk_logfile = config.get(section7, 'file_result_suikei3')
elif args[1] == '4':
    wk_logfile = config.get(section7, 'file_result_suikei4')
elif args[1] == '5':
    wk_logfile = config.get(section7, 'file_result_suikei5')
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
url = config.get(section6, 'url_suikei')
url_top = config.get(section6, 'url_top')
url_path = config.get(section6, 'path')

logger.info('■処理開始■■■■■■')

# -----------------------------------
# ログイン処理
# -----------------------------------
try:
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
    
    # 実行日時退避(遅延考慮し30分前の情報が対象)→20分前にしてみる。
    start_date_time = datetime.datetime.now() - datetime.timedelta(minutes = 20)
    # 誤差考慮し0分単位に切捨て
    start_date_time = datetime.datetime(start_date_time.year, start_date_time.month, start_date_time.day, start_date_time.hour, round(start_date_time.minute,-1), 0)
    # デバッグ時
    # start_date_time = datetime.datetime(start_date_time.year, start_date_time.month, start_date_time.day, start_date_time.hour, 0, 0)
    logger.info(start_date_time)

    # フォルダ作成（引数により地方を分ける）
    main_dir = config.get(section4, 'result')
    date_dir = start_date_time.strftime('%Y%m%d')
    if args[1] == '1':
        region_name = config.get(section3, 'region_1_name')
        df_inp = pd.read_csv(config.get(section4, 'suikei_1_list'), encoding='cp932')
        region_dir = config.get(section3, 'region_1')
    elif args[1] == '2':
        region_name = config.get(section3, 'region_2_name')
        df_inp = pd.read_csv(config.get(section4, 'suikei_2_list'), encoding='cp932')
        region_dir = config.get(section3, 'region_2')
    elif args[1] == '3':
        region_name = config.get(section3, 'region_3_name')
        df_inp = pd.read_csv(config.get(section4, 'suikei_3_list'), encoding='cp932')
        region_dir = config.get(section3, 'region_3')
    elif args[1] == '4':
        region_name = config.get(section3, 'region_4_name')
        df_inp = pd.read_csv(config.get(section4, 'suikei_4_list'), encoding='cp932')
        region_dir = config.get(section3, 'region_4')
    elif args[1] == '5':
        region_name = config.get(section3, 'region_5_name')
        df_inp = pd.read_csv(config.get(section4, 'suikei_5_list'), encoding='cp932')
        region_dir = config.get(section3, 'region_5')
    else:
        logger.error('パラメータ不正：' + args[1])
        sys.exit()
    
    #print(main_dir,date_dir, region_name,df_inp, region_dir)

    suikei_names = df_inp['suikei_name'].values 
    suikei_codes = df_inp['suikei_code'].values 
    
    if not os.path.exists(os.path.join(os.getcwd(),main_dir,region_dir)):
        os.mkdir(os.path.join(os.getcwd(),main_dir,region_dir))
    if not os.path.exists(os.path.join(os.getcwd(),main_dir,region_dir,date_dir)):
        os.mkdir(os.path.join(os.getcwd(),main_dir,region_dir,date_dir))

    path1 = os.path.join(url_path,main_dir,region_dir,date_dir)

    if not os.path.exists(path1):
        os.makedirs(path1)
    
    # 0:デスクトップ、1:システム規定のフォルファ、2:ユーザ定義フォルダ
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
    #driver = webdriver.Firefox(firefox_profile=fp, firefox_options=options, log_path=os.path.devnull)
    driver = webdriver.Firefox(firefox_profile=fp, firefox_options=options, log_path='./geckodriver.log')
    driver.implicitly_wait(DEFAULT_WAITIME)
    
except:
    logger.error(traceback.format_exc())

dates = []
times = []
stat_actuals = []
stat_predicts = []
error_msg = ''

# ログイン画面
driver.get(url)
logger.info('ログイン処理開始')
time.sleep(3)
driver.find_element_by_xpath('//*[@id="user_id"]').send_keys(user)
driver.find_element_by_xpath('//*[@id="password"]').send_keys(password)
driver.find_element_by_xpath('/html/body/div[2]/form/div[2]/button').click()
time.sleep(5)
# png_name = start_date_time.strftime('%Y%m%d%H%M')+'_login.png'
# png_path = os.path.join(main_dir,region_dir,date_dir,png_name)
# driver.save_screenshot(png_path)
logger.info('ログイン処理終了')

for cnt, (suikei_name, suikei_code) in enumerate(zip(suikei_names, suikei_codes)):
    logger.info("■"+suikei_name+' start')
    try:
        try:
            # 水系選択
            logger.info('  水系プルダウン')
            driver.find_element_by_id('river-system-btn').click()
            time.sleep(2)
            logger.info('  水系選択')

            # 要素が重なっている場合があるためJavaScriptでクリックする。
            target = driver.find_element_by_id(suikei_code)
            driver.execute_script("arguments[0].click();", target)
            time.sleep(2)
            # 固定ロジック(淀川の場合だけ2回、水系を選択する)
            # if suikei_name == '淀川水系':
            #     logger.info(suikei_name+' 水系選択(2回目)')
            #     driver.execute_script("arguments[0].click();", target)
            #     time.sleep(2)
            # 全水系で２回水系を選択する。
            logger.info(suikei_name+' 水系選択(2回目)')
            driver.execute_script("arguments[0].click();", target)
            time.sleep(2)

            # 履歴表示
            # 利根川の場合描画が遅いので追加でsleep
            time.sleep(10)
            driver.find_element_by_id('layertype-btn').click()
            logger.info('  ＞情報ボタンクリック')
            time.sleep(2)

            # 履歴選択
            # オプション
            driver.find_element_by_id('radio-lt-history').click()
            logger.info('  履歴選択')

            # 固定ロジック(淀川の場合だけ2回、水系を選択する)
            if suikei_name == '淀川水系':
                time.sleep(8)
            else:
                time.sleep(2)

            # 年
            driver.find_element_by_xpath("//select[@id='history_year']/option[@value='" + start_date_time.strftime('%Y') + "']").click()
            logger.info('  年選択')
            time.sleep(1)
            # 月
            driver.find_element_by_xpath("//select[@id='history_month']/option[@value='" + start_date_time.strftime('%m') + "']").click()
            logger.info('  月選択')
            time.sleep(1)
            # 日
            driver.find_element_by_xpath("//select[@id='history_day']/option[@value='" + start_date_time.strftime('%d') + "']").click()
            logger.info('  日選択')
            time.sleep(1)
            # 時
            driver.find_element_by_xpath("//select[@id='history_hour']/option[@value='" + start_date_time.strftime('%H') + "']").click()
            logger.info('  時選択')
            time.sleep(1)
            # 分
            driver.find_element_by_xpath("//select[@id='history_minute']/option[@value='" + start_date_time.strftime('%M') + "']").click()
            logger.info('  分選択')
            time.sleep(1)
            # 表示
            driver.find_element_by_id('show-history').click()
            logger.info('  表示ボタンクリック')
            time.sleep(3)

            dates.append(driver.find_element_by_xpath('//*[@id="latest-date-value"]').text)
            times.append(driver.find_element_by_xpath('//*[@id="latest-time-value"]').text)
            stat_actuals.append(driver.find_element_by_xpath('//*[@id="stat-actual"]').text)
            stat_predicts.append(driver.find_element_by_xpath('//*[@id="stat-predict"]').text)

            # 未受信状況取得
            logger.info('  未受信チェック')
            # 観測水位は無視する
            # a = driver.find_element_by_xpath('//*[@id="stat-actual"]').text
            a = ''
            b = driver.find_element_by_xpath('//*[@id="stat-predict"]').text

            if a != '' :
                if b != '' :
                    error_msg = error_msg + suikei_name + "," + a + "," + b + "\r\n"
                    logger.warning(a + "," + b)
                else :
                    error_msg = error_msg + suikei_name + "," + a + "\r\n"
                    logger.warning(a)
            else :
                if b != '' :
                    error_msg = error_msg + suikei_name + "," + b + "\r\n"
                    logger.warning(b)
                else:
                    logger.info('  正常')

        except:

            dates.append('networkerror')
            times.append('networkerror')
            stat_actuals.append('networkerror')
            stat_predicts.append('networkerror')

            # エラーメッセージに追加する
            ## 一旦対象外としておく
            error_msg = error_msg + suikei_name + "," + '自動チェックエラー' + "\r\n"
            print(error_msg)

            logger.warning(' 自動チェックエラー', exc_info=True)

    except:
        logger.warning(' その他エラー', exc_info=True)

    logger.info("■"+suikei_name+' end')
    # ログイン状態で画面リロード
    driver.get(url)
    time.sleep(3)

# ログアウト
try:
    # ログイン状態でトップ画面
    logger.info('ログアウト処理開始')
    driver.get(url_top)
    time.sleep(2)
    driver.find_element_by_xpath('/html/body/div[1]/div/span/button/img').click()
    time.sleep(1)
    Alert(driver).accept()
    time.sleep(1)
#     png_name = start_date_time.strftime('%Y%m%d%H%M')+'_logout.png'
#     png_path = os.path.join(main_dir,region_dir,date_dir,png_name)
#     driver.save_screenshot(png_path)
    logger.info('ログアウト処理完了')
except:
    logger.error(' ログアウトエラー', exc_info=True)

driver.quit()
# 結果出力
out = pd.DataFrame({'suikei_name': df_inp.iloc[:, 0],
                    'url': url_top,
                    'date': dates,
                    'time': times,
                    'stat_actual': stat_actuals,
                    'stat_predict': stat_predicts})[['suikei_name', 'url', 'date', 'time', 'stat_actual', 'stat_predict']]
csv_name = main_dir+"_"+start_date_time.strftime('%Y%m%d%H%M')+".csv"
# out.to_csv(os.path.join(main_dir,region_dir,date_dir,csv_name),encoding='utf_8_sig')
out.to_csv(os.path.join(url_path,main_dir,region_dir,date_dir,csv_name),encoding='utf_8_sig')

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
        subject = "【自動送信："+region_name+"洪水予測】" + start_date_time.strftime('%Y/%m/%d %H:%M') + "のチェックで予測未連携水系もしくはエラーが発生"
        message = "各位" + "\r\n\r\n"
        message = message + start_date_time.strftime('%Y/%m/%d %H:%M') + "計算結果の自動チェックにて予測未連携水系もしくは自動チェックエラーが発生しております。" + "\r\n"
        message = message + "対象は以下のとおりです。" + "\r\n==================================\r\n" + error_msg + "\r\n=========================\r\n"
        message = message + "以下URLにて確認可能です。" + "\r\n" + "https://frlg.river.go.jp"

        message = message + "\r\n\r\n"+"結果ファイルは以下に保存されてます。"
        message = message + "\r\n"+os.path.join(config.get(section6, 'path'),main_dir,region_dir,date_dir)
        message = message + "\r\n"+csv_name

        message = message + "\r\n\r\n"
        message = message + "\r\n"+config.get(section5, 'message_suikei1')
        #message = message + "\r\n"+config.get(section5, 'message_suikei2')
        #message = message + "\r\n"+config.get(section5, 'message_suikei3')
        #message = message + "\r\n"+config.get(section5, 'message_suikei4')
        #message = message + "\r\n"+config.get(section5, 'message_suikei5')
        #message = message + "\r\n"+config.get(section5, 'message_suikei6')

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
