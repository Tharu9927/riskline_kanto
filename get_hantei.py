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
from selenium.common.exceptions import NoSuchElementException
import cv2
import sys
import configparser
# log
from logzero import logger
import logzero
import logging

# 引数読み込み
args = sys.argv

# 設定ファイル読み込み
config = configparser.ConfigParser()
config.read('settingJ.ini','UTF-8')
# ログイン情報
section1 = 'login'
# プロキシ情報
section2 = 'preference'
# 地方情報
section3 = 'region'
# 一覧ファイル・結果ファイル
section4 = 'judan'
# メール情報
section5 = 'mail'
# メイン情報
section6 = 'main'
# ログ情報
section7 = 'log_setting_area'
#保存フォルダ
if args[1] == '1':
    wk_logfile = config.get(section7, 'file_result1')
elif args[1] == '2':
    wk_logfile = config.get(section7, 'file_result1')
elif args[1] == '3':
    wk_logfile = config.get(section7, 'file_result1')
elif args[1] == '4':
    wk_logfile = config.get(section7, 'file_result1')
elif args[1] == '5':
    wk_logfile = config.get(section7, 'file_result1')
elif args[1] == '6':
    wk_logfile = config.get(section7, 'file_result1')
elif args[1] == '7':
    wk_logfile = config.get(section7, 'file_result1')
elif args[1] == '8':
    wk_logfile = config.get(section7, 'file_result1')
elif args[1] == '9':
    wk_logfile = config.get(section7, 'file_result1')
elif args[1] == '10':
    wk_logfile = config.get(section7, 'file_result1')
elif args[1] == '11':
    wk_logfile = config.get(section7, 'file_result1')
elif args[1] == '12':
    wk_logfile = config.get(section7, 'file_result1')
elif args[1] == '13':
    wk_logfile = config.get(section7, 'file_result1')
elif args[1] == '14':
    wk_logfile = config.get(section7, 'file_result1')
elif args[1] == '15':
    wk_logfile = config.get(section7, 'file_result1')
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
url_path = config.get(section6, 'path')

logger.info('■処理開始■■■■■■')

# -----------------------------------
# ログイン処理
# -----------------------------------
DEFAULT_WAITIME = 10
if args[1] == '1':
    user = config.get(section1, 'id_1')
    password = config.get(section1, 'pass_1')
elif args[1] == '2':
    user = config.get(section1, 'id_1')
    password = config.get(section1, 'pass_1')
elif args[1] == '3':
    user = config.get(section1, 'id_1')
    password = config.get(section1, 'pass_1')
elif args[1] == '4':
    user = config.get(section1, 'id_1')
    password = config.get(section1, 'pass_1')
elif args[1] == '5':
    user = config.get(section1, 'id_1')
    password = config.get(section1, 'pass_1')
elif args[1] == '6':
    user = config.get(section1, 'id_1')
    password = config.get(section1, 'pass_1')
elif args[1] == '7':
    user = config.get(section1, 'id_1')
    password = config.get(section1, 'pass_1')
elif args[1] == '8':
    user = config.get(section1, 'id_1')
    password = config.get(section1, 'pass_1')
elif args[1] == '9':
    user = config.get(section1, 'id_1')
    password = config.get(section1, 'pass_1')
elif args[1] == '10':
    user = config.get(section1, 'id_1')
    password = config.get(section1, 'pass_1')
elif args[1] == '11':
    user = config.get(section1, 'id_1')
    password = config.get(section1, 'pass_1')
elif args[1] == '12':
    user = config.get(section1, 'id_1')
    password = config.get(section1, 'pass_1')
elif args[1] == '13':
    user = config.get(section1, 'id_1')
    password = config.get(section1, 'pass_1')
elif args[1] == '14':
    user = config.get(section1, 'id_1')
    password = config.get(section1, 'pass_1')
elif args[1] == '15':
    user = config.get(section1, 'id_1')
    password = config.get(section1, 'pass_1')
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
# start_date_time = datetime.datetime(start_date_time.year, start_date_time.month, start_date_time.day, start_date_time.hour, round(start_date_time.minute,-1), 0)
start_date_time = datetime.datetime(start_date_time.year, start_date_time.month, start_date_time.day, start_date_time.hour, ((start_date_time.minute//20)*20), 0)
#start_date_time = datetime.datetime(2021 , 8 , 13 , 10)

# デバッグ時
# start_date_time = datetime.datetime(start_date_time.year, start_date_time.month, start_date_time.day, start_date_time.hour, 0, 0)
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
# driver = webdriver.Firefox(executable_path='./geckodriver.exe', firefox_options=options)
driver.implicitly_wait(DEFAULT_WAITIME)

# フォルダ作成（引数により地方を分ける）
main_dir = config.get(section4, 'result')
date_dir = start_date_time.strftime('%Y%m%d')
datetime_dir = start_date_time.strftime('%Y%m%d%H%M')

if args[1] == '1':
    region_name = config.get(section3, 'region_1_name')
    df_inp = pd.read_csv(config.get(section4, 'judan_1_list'), encoding='cp932')
    region_dir = config.get(section3, 'region_1')
elif args[1] == '2':
    region_name = config.get(section3, 'region_1_name')
    df_inp = pd.read_csv(config.get(section4, 'judan_2_list'), encoding='cp932')
    region_dir = config.get(section3, 'region_1')
elif args[1] == '3':
    region_name = config.get(section3, 'region_1_name')
    df_inp = pd.read_csv(config.get(section4, 'judan_3_list'), encoding='cp932')
    region_dir = config.get(section3, 'region_1')
elif args[1] == '4':
    region_name = config.get(section3, 'region_1_name')
    df_inp = pd.read_csv(config.get(section4, 'judan_4_list'), encoding='cp932')
    region_dir = config.get(section3, 'region_1')
elif args[1] == '5':
    region_name = config.get(section3, 'region_1_name')
    df_inp = pd.read_csv(config.get(section4, 'judan_5_list'), encoding='cp932')
    region_dir = config.get(section3, 'region_1')
elif args[1] == '6':
    region_name = config.get(section3, 'region_1_name')
    df_inp = pd.read_csv(config.get(section4, 'judan_6_list'), encoding='cp932')
    region_dir = config.get(section3, 'region_1')
elif args[1] == '7':
    region_name = config.get(section3, 'region_2_name')
    df_inp = pd.read_csv(config.get(section4, 'judan_7_list'), encoding='cp932')
    region_dir = config.get(section3, 'region_2')
elif args[1] == '8':
    region_name = config.get(section3, 'region_2_name')
    df_inp = pd.read_csv(config.get(section4, 'judan_8_list'), encoding='cp932')
    region_dir = config.get(section3, 'region_2')
elif args[1] == '9':
    region_name = config.get(section3, 'region_2_name')
    df_inp = pd.read_csv(config.get(section4, 'judan_9_list'), encoding='cp932')
    region_dir = config.get(section3, 'region_2')
elif args[1] == '10':
    region_name = config.get(section3, 'region_1_name')
    df_inp = pd.read_csv(config.get(section4, 'judan_10_list'), encoding='cp932')
    region_dir = config.get(section3, 'region_1')
elif args[1] == '11':
    region_name = config.get(section3, 'region_1_name')
    df_inp = pd.read_csv(config.get(section4, 'judan_11_list'), encoding='cp932')
    region_dir = config.get(section3, 'region_1')
elif args[1] == '12':
    region_name = config.get(section3, 'region_1_name')
    df_inp = pd.read_csv(config.get(section4, 'judan_12_list'), encoding='cp932')
    region_dir = config.get(section3, 'region_1')
elif args[1] == '13':
    region_name = config.get(section3, 'region_2_name')
    df_inp = pd.read_csv(config.get(section4, 'judan_13_list'), encoding='cp932')
    region_dir = config.get(section3, 'region_2')
elif args[1] == '14':
    region_name = config.get(section3, 'region_1_name')
    df_inp = pd.read_csv(config.get(section4, 'judan_14_list'), encoding='cp932')
    region_dir = config.get(section3, 'region_1')
elif args[1] == '15':
    region_name = config.get(section3, 'region_2_name')
    df_inp = pd.read_csv(config.get(section4, 'judan_15_list'), encoding='cp932')
    region_dir = config.get(section3, 'region_2')

else:
    logger.error('パラメータ不正：' + args[1])
    sys.exit()
    

if not os.path.exists(os.path.join(os.getcwd(),main_dir,region_dir)):
    os.mkdir(os.path.join(os.getcwd(),main_dir,region_dir))
if not os.path.exists(os.path.join(os.getcwd(),main_dir,region_dir,date_dir)):
    os.mkdir(os.path.join(os.getcwd(),main_dir,region_dir,date_dir))
if not os.path.exists(os.path.join(os.getcwd(),main_dir,region_dir,date_dir,datetime_dir)):
    os.mkdir(os.path.join(os.getcwd(),main_dir,region_dir,date_dir,datetime_dir))
if not os.path.exists(os.path.join(os.getcwd(),main_dir,region_dir,date_dir,datetime_dir,args[1])):
    os.mkdir(os.path.join(os.getcwd(),main_dir,region_dir,date_dir,datetime_dir,args[1]))

path1 = os.path.join(url_path,main_dir,region_dir,date_dir,datetime_dir,args[1])

if not os.path.exists(path1):
    os.makedirs(path1)

flag_rights_black = []
flag_lefts_black = []
flag_rights_red = []
flag_lefts_red = []
flag_rights_orange = []
flag_lefts_orange = []
flag_rights_yellow = []
flag_lefts_yellow = []
urls = df_inp['url'].values
suikei_names = df_inp['suikei_name'].values
river_names = df_inp['river_name'].values
error_msg = ''
black_flg_cnt = 0
red_flg_cnt = 0
orange_flg_cnt = 0
yellow_flg_cnt = 0

# ログイン画面
driver.get(url_top)
print(driver.page_source)
# print(driver.find_element_by_xpath('//*[@id="user_id"]'))
logger.info('ログイン処理開始')
time.sleep(3)
driver.find_element_by_xpath('//*[@id="user_id"]').send_keys(user)
driver.find_element_by_xpath('//*[@id="password"]').send_keys(password)
driver.find_element_by_xpath('/html/body/div[2]/form/div[2]/button').click()
time.sleep(5)
# png_name = 'login.png'
# png_path = os.path.join(main_dir,region_dir,date_dir,datetime_dir,png_name)
# driver.save_screenshot(png_path)
logger.info('ログイン処理終了')

times = []
for cnt, (url, suikei_name, river_name) in enumerate(zip(urls, suikei_names, river_names)):
    result_flg = 0
    black_flg = 0
    red_flg = 0
    orange_flg = 0
    yellow_flg = 0
    try:
        logger.info("■"+suikei_name+" "+river_name+' start')

        # 日時のパラメータをセット
        url = url + "&time=" + tm.strftime('%Y%m%d%H%M00')
        # 画面遷移
        driver.get(url)
        logger.info('  '+url)
        time.sleep(5)
        try:
            # 縦断図スクショ
            png_name = '{0:03d}.png'.format(cnt)
            png_path = os.path.join(main_dir,region_dir,date_dir,datetime_dir,args[1],png_name)
            png_path1 = os.path.join(url_path,main_dir,region_dir,date_dir,datetime_dir,args[1],png_name)
            driver.save_screenshot(png_path)
            driver.save_screenshot(png_path1)
            logger.info('  スクリーンショット取得')
            logger.info('  '+png_path)
        except:
            logger.error('  エラー発生', exc_info=True)

        # スクショから越水判定
        img = cv2.imread(png_path)
        img_right = img[125:130, 73:73+1201]
        img_left = img[155:160, 73:73+1201]

        # black
        res_right = cv2.inRange(img_right, np.array([0,0,0]), np.array([15,15,15]))
        res_left = cv2.inRange(img_left, np.array([0,0,0]), np.array([15,15,15]))
        flag_rights_black.append(np.any(res_right == 255))
        flag_lefts_black.append(np.any(res_left == 255))
        #print('res_right')
        # 判定
        if np.any(res_right == 255) == True or np.any(res_left == 255) == True:
            result_flg = 1
            black_flg = 1
            black_flg_cnt = black_flg_cnt + 1

        # red → purple
        res_right = cv2.inRange(img_right, np.array([150,0,150]), np.array([255,25,255]))
        res_left = cv2.inRange(img_left, np.array([150,0,150]), np.array([255,25,255]))
        flag_rights_red.append(np.any(res_right == 255))
        flag_lefts_red.append(np.any(res_left == 255))
        # 判定
        if np.any(res_right == 255) == True or np.any(res_left == 255) == True:
            result_flg = 1
            red_flg = 1
            red_flg_cnt = red_flg_cnt + 1

        # orange → red
        res_right = cv2.inRange(img_right, np.array([0,0,225]), np.array([50,50,255]))
        res_left = cv2.inRange(img_left, np.array([0,0,225]), np.array([50,50,255]))
        flag_rights_orange.append(np.any(res_right == 255))
        flag_lefts_orange.append(np.any(res_left == 255))
        # 判定
        if np.any(res_right == 255) == True or np.any(res_left == 255) == True:
            result_flg = 1
            orange_flg = 1
            orange_flg_cnt = orange_flg_cnt + 1

        # yellow
        res_right = cv2.inRange(img_right, np.array([0,225,225]), np.array([50,255,255]))
        res_left = cv2.inRange(img_left, np.array([0,225,225]), np.array([50,255,255]))
        flag_rights_yellow.append(np.any(res_right == 255))
        flag_lefts_yellow.append(np.any(res_left == 255))
        # 判定
        if np.any(res_right == 255) == True or np.any(res_left == 255) == True:
            result_flg = 1
            yellow_flg = 1
            yellow_flg_cnt = yellow_flg_cnt + 1

        # message追加
        if black_flg == 1:
            error_msg = error_msg + suikei_name + " " + river_name + "," + "画像：" + png_name + ",（警戒レベル５相当）氾濫している可能性" + "\r\n　" + url + "\r\n"
            logger.warning(' （警戒レベル５相当）氾濫している可能性')
        elif red_flg == 1:
            error_msg = error_msg + suikei_name + " " + river_name + "," + "画像：" + png_name + ",（警戒レベル４相当）氾濫危険水位超過相当" + "\r\n　" + url + "\r\n"
            logger.warning(' （警戒レベル４相当）氾濫危険水位超過相当')
        elif orange_flg == 1:
            error_msg = error_msg + suikei_name + " " + river_name + "," + "画像：" + png_name + ",（警戒レベル３相当）避難判断水位超過相当" + "\r\n　" + url + "\r\n"
            logger.warning(' （警戒レベル３相当）避難判断水位超過相当')
        elif yellow_flg == 1:
            error_msg = error_msg + suikei_name + " " + river_name + "," + "画像：" + png_name + ",（警戒レベル２相当）氾濫注意水位超過相当" + "\r\n　" + url + "\r\n"
            logger.warning(' （警戒レベル２相当）氾濫注意水位超過相当')
        else:
            logger.info('  基準水位超過なし')

        print(f'error message {error_msg}')
    except:
        
        times.append('networkerror')
        flag_rights_black.append('networkerror')
        flag_lefts_black.append('networkerror')
        flag_rights_red.append('networkerror')
        flag_lefts_red.append('networkerror')
        flag_rights_orange.append('networkerror')
        flag_lefts_orange.append('networkerror')
        flag_rights_yellow.append('networkerror')
        flag_lefts_yellow.append('networkerror')
        if river_name != '由良川' and river_name != '円山川':
            error_msg = error_msg + suikei_name + " " + river_name + ",自動チェックエラー" + "\r\n　" + url + "\r\n"
        logger.warning('  自動チェックエラー', exc_info=True)

    logger.info("■"+suikei_name+" "+river_name+' end')

# ログアウト
try:
    # ログイン状態でトップ画面
    logger.info('ログアウト処理開始')
    driver.get(url_top)
    # print(driver.page_source)
    time.sleep(2)
    # driver.find_element_by_xpath('/html/body/div[1]/div/span/button/img').click()
    driver.find_element_by_xpath('/html/body/div[1]/div/span[2]/button').click()
    # print(driver.page_source)
    time.sleep(1)
    Alert(driver).accept()
    time.sleep(1)
#     png_name = 'logout.png'
#     png_path = os.path.join(main_dir,region_dir,date_dir,datetime_dir,png_name)
#     driver.save_screenshot(png_path)
    logger.info('ログアウト処理完了')
except:
    logger.error(' ログアウトエラー', exc_info=True)

driver.quit()

col = ['suikei_name',
       'river_name',
       'url',
       'black_left',
       'black_right',
       'red_left',
       'red_right',
       'orange_left',
       'orange_right',
       'yellow_left',
       'yellow_right']
out = pd.DataFrame({'suikei_name': df_inp.iloc[:, 0],
                    'river_name': df_inp.iloc[:, 1],
                    'url': urls,
                    'black_right': flag_rights_black,
                    'black_left': flag_lefts_black,
                    'red_right': flag_rights_red,
                    'red_left': flag_lefts_red,
                    'orange_right': flag_rights_orange,
                    'orange_left': flag_lefts_orange,
                    'yellow_right': flag_rights_yellow,
                    'yellow_left': flag_lefts_yellow})[col]
csv_name = main_dir+"_"+start_date_time.strftime('%Y%m%d%H%M')+".csv"
out.to_csv(os.path.join(main_dir,region_dir,date_dir,datetime_dir,args[1],csv_name),encoding='utf_8_sig')
out.to_csv(os.path.join(url_path,main_dir,region_dir,date_dir,datetime_dir, args[1],csv_name),encoding='utf_8_sig')

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
            # cc_address = config.get(section5, 'region_1_cc')
        elif args[1] == '2':
            to_address = config.get(section5, 'region_2_to')
            # cc_address = config.get(section5, 'region_2_cc')
        elif args[1] == '3':
            to_address = config.get(section5, 'region_3_to')
            # cc_address = config.get(section5, 'region_3_cc')
        elif args[1] == '4':
            to_address = config.get(section5, 'region_4_to')
            # cc_address = config.get(section5, 'region_4_cc')
        elif args[1] == '5':
            to_address = config.get(section5, 'region_5_to')
            # cc_address = config.get(section5, 'region_5_cc')
        elif args[1] == '6':
            to_address = config.get(section5, 'region_6_to')
            # cc_address = config.get(section5, 'region_2_cc')
        elif args[1] == '7':
            to_address = config.get(section5, 'region_7_to')
            # cc_address = config.get(section5, 'region_3_cc')
        elif args[1] == '8':
            to_address = config.get(section5, 'region_8_to')
            # cc_address = config.get(section5, 'region_4_cc')
        elif args[1] == '9':
            to_address = config.get(section5, 'region_9_to')
            # cc_address = config.get(section5, 'region_5_cc')
        elif args[1] == '10':
            to_address = config.get(section5, 'region_10_to')
            # cc_address = config.get(section5, 'region_2_cc')
        elif args[1] == '11':
            to_address = config.get(section5, 'region_11_to')
            # cc_address = config.get(section5, 'region_3_cc')
        elif args[1] == '12':
            to_address = config.get(section5, 'region_12_to')
            # cc_address = config.get(section5, 'region_4_cc')
        elif args[1] == '13':
            to_address = config.get(section5, 'region_13_to')
            # cc_address = config.get(section5, 'region_5_cc')
        elif args[1] == '14':
            to_address = config.get(section5, 'region_14_to')
            # cc_address = config.get(section5, 'region_4_cc')
        elif args[1] == '15':
            to_address = config.get(section5, 'region_15_to')
            # cc_address = config.get(section5, 'region_5_cc')
        else:
            logger.error('パラメータ不正：' + args[1])
            sys.exit()
        # TOとCC
        # sendToList=to_address.split(',')+cc_address.split(',')
        sendToList=to_address.split(',')

        charset = "UTF-8"
        subject = "【自動送信："+region_name+"洪水予測】" + start_date_time.strftime('%Y/%m/%d %H:%M') 
        message = "各位" + "\r\n\r\n" + start_date_time.strftime('%Y/%m/%d %H:%M')
        if black_flg_cnt > 0:
            subject = subject + "のチェックで洪水の警戒レベル５相当が発生"
            message = message + "計算結果の自動チェックにて警戒レベル５相当が発生しております。" + "\r\n"
        elif red_flg_cnt > 0:
            subject = subject + "のチェックで洪水の警戒レベル４相当が発生"
            message = message + "計算結果の自動チェックにて警戒レベル４相当が発生しております。" + "\r\n"
        elif orange_flg_cnt > 0:
            subject = subject + "のチェックで洪水の警戒レベル３相当が発生"
            message = message + "計算結果の自動チェックにて警戒レベル３相当が発生しております。" + "\r\n"
        elif yellow_flg_cnt > 0:
            subject = subject + "のチェックで洪水の警戒レベル２相当が発生"
            message = message + "計算結果の自動チェックにて警戒レベル２相当が発生しております。" + "\r\n"
        else:
            subject = subject + "のチェックで自動チェックエラーが発生"
            message = message + "計算結果の自動チェックにてエラーが発生しております。" + "\r\n"
        #print(message,'***************')
        message = message + "対象は以下のとおりです。" + "\r\n==================================\r\n" + error_msg + "\r\n=========================\r\n"
        message = message + "以下URLにて確認可能です。" + "\r\n" + url_top

        message = message + "\r\n\r\n"+"結果ファイルは以下に保存されてます。"
        message = message + "\r\n"+os.path.join(config.get(section6, 'path'),main_dir,region_dir,date_dir,datetime_dir,args[1])
        message = message + "\r\n"+csv_name

        message = message + "\r\n\r\n"+"スクリーンショット画像は以下に保存されてます。"
        message = message + "\r\n"+os.path.join(config.get(section6, 'path'),main_dir,region_dir,date_dir,datetime_dir,args[1])

        message = message + "\r\n\r\n"
        message = message + "\r\n"+config.get(section5, 'message_judan1')
        #message = message + "\r\n"+config.get(section5, 'message_judan')
        #message = message + "\r\n"+config.get(section5, 'message_judan3')
        #message = message + "\r\n"+config.get(section5, 'message_judan4')
        #message = message + "\r\n"+config.get(section5, 'message_judan5')
        #message = message + "\r\n"+config.get(section5, 'message_judan6')

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
        #print(from_address,sendToList,subject,message)