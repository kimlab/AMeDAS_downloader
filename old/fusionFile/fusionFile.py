﻿#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        fusionFile.py
# Purpose:      このスクリプトファイルと同じ階層にあるフォルダを走査し、観測データを結合する
#               処理済みファイル数年分のデータ結合に利用可能です。
#               昨年組んだRubyスクリプトよりも利便性が上がったはず。
# Author:      K. Morishita
#
# Created:     22/08/2012
# History:      2013/12/14 現在のCSV保存フォーマットに対応した。
#                           スクリプトの実行フォルダを"Processed HTML"の上にした。
#               2014/1/19   保存ファイルに日付を入れるように変更
#                           1時間毎の観測データに対応
# Copyright:   (c) morishita 2012
# Licence:     MIT
#-------------------------------------------------------------------------------
import os
import re
import glob
import datetime

def get_Date(txt):
    """ 日付の文字列から時刻オブジェクトを作成する
    """
    #print(txt)
    p = re.compile(r'(?P<date>(?P<year>\d{4})_(?P<month>\d{1,2})_(?P<day>\d{1,2}))')    # 日付にマッチするパターン
    matchTest = p.search(txt)
    if matchTest != None:
        #print(matchTest.groups())
        year   = int(matchTest.group('year'))
        month  = int(matchTest.group('month'))
        day    = int(matchTest.group('day'))
        return datetime.datetime(year, month, day, 0, 0, 0, 0)
    else:
        return None
    return

def get_clock(txt):
    """ 時刻を時と分に分けて返す
    """
    #print(txt)
    p = re.compile("(?P<hour>\d{1,2})(?:[:](?P<min>\d\d))?")   # 分は1時間毎のデータで省略される
    matchTest = p.match(txt)
    #print(matchTest)
    hour = None
    minute = None
    if matchTest != None:
        #print(matchTest.groups())
        hour = matchTest.group('hour')
        if hour != None:
            hour = int(hour)
        minute = matchTest.group('min')
        if minute != None:
            minute = int(minute)
        #print(hour, minute)
    return (hour, minute)

def process(dirPath):
    """ 指定されたフォルダの直下にあるフォルダ内を走査し、全てのcsvを結合したテキストデータを保存する
    """
    saveFileName = "fusion.csv"
    savePath = dirPath + "/" + saveFileName
    fw = open(savePath, 'w', encoding='utf-8-sig')
    plist =  os.listdir(dirPath)                # 指定されたフォルダ内を走査する
    #print (plist)
    for men in plist:
        fpath = os.path.join(dirPath, men)
        if os.path.isdir(fpath):                # 直下のフォルダを対象として処理
            fileList =  glob.glob(dirPath + "/" + men + '/*.csv')   # CSVファイルのリストを作成
            for fname in fileList:
                bname = os.path.basename(fname)
                if(bname != saveFileName):
                    with open(fname, 'r', encoding='utf-8-sig') as fr:
                        _txt = fr.readlines()
                        date = get_Date(fname)
                        for i in range(1, len(_txt)):   # 1行目には項目名があることが前提
                            line = _txt[i]
                            if line != "":
                                hour, minute = get_clock(line)
                                if minute == None:
                                    minute = 0
                                #print(date)
                                #print(datetime.timedelta(hours=hour, minutes=minute))
                                _date = date + datetime.timedelta(hours=hour, minutes=minute)
                                #print(str(_date))
                                fw.write(str(_date) + "," + line)
    fw.close()
    return

def main():
    """
    "Processed HTML"内のフォルダを走査し、そのフォルダ内にある全てのcsvファイルを各々結合する
    """
    target_dir = "Processed HTML"
    if os.path.isdir(target_dir):                   # target_dirの存在を確認
        print("'{0}' is founded.".format(target_dir))
        target_dir_path = os.path.join(os.getcwd(), target_dir)
        plist =  os.listdir(target_dir_path)        # target_dir内のファイルとフォルダを走査
        print("target list: ")
        print(plist)
        print("\n")
        for men in plist:
            _each_target_path = os.path.join(target_dir_path, men)
            if os.path.isdir(_each_target_path):    # フォルダ判定
                print("now target: " + men)
                process(_each_target_path)
                print(men + " is fin.")
    else:
        print("there isn't '{0}' dir.".format(target_dir))

if __name__ == '__main__':
    main()
