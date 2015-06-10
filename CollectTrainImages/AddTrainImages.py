# coding:utf-8
__author__ = 'yamamoto'

import cv2
import cv2.cv
import numpy as np
import pandas as pd
import os
import sys
import shutil
import datetime

CD = os.getcwd()

# ビデオの読み込み・プロパティの取得
Name = "KOTAYU"
Date = "150608"
Num = "2"

TrainDataNum = 750

video = Name + Date + "_" + Num + ".mp4"
# video = "visionface.avi"
cap = cv2.VideoCapture(video) # Read Video File
FrameNum_Total = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))


os.chdir('..\\material')

# 過去のTrainDataの読み込み
if not os.path.isfile('TrainData.csv'):
    print '-------------------------------------'
    print 'File "TrainData" is not exited'
    print '-------------------------------------'
else:
    df_Old = pd.read_csv('TrainData.csv')
    Total_Old = df_Old.ix[(len(df_Old) - 1), 'id']
    print Total_Old

if TrainDataNum > FrameNum_Total:
    print '----------------------------------------------------------'
    print 'Number of Training Data is larger than total frame number'
    print 'Check Number of Training Data'
    print '----------------------------------------------------------'
else:
    if not os.path.isdir('images'):
        print '-------------------------------------'
        print 'Folder "images" is not exited'
        print 'Run "CollectTrainData.py" first'
        print '-------------------------------------'
    else:
        Choose = np.random.choice(range(0, FrameNum_Total), TrainDataNum, replace=False)
        df = pd.DataFrame({'VideoName': np.repeat(video, len(Choose)),
                           'FrameNum': Choose,
                           'Name': np.repeat(Name, len(Choose)),
                           'Date': np.repeat(Date, len(Choose))
                           })
        df = df.sort('FrameNum')
        df.index = range(0, df.shape[0])
        df = df[['VideoName', 'FrameNum', 'Name', 'Date']]

        FileName = []
        for idx in df.index:
            FrameNum = df.ix[idx, 'FrameNum']
            cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, FrameNum)
            ret, im = cap.read()
            if ret:
                # cv2.imshow('Video Stream', im)  # Check Detected 'Face'
                im = cv2.resize(im, (im.shape[1] * 5 / 12, im.shape[0] * 5 / 12))  # resize image
                # 画像の書き出し
                file_name = 'id' + str(Total_Old + idx + 1).zfill(5) + '_' + Name + Date + '_' + str(idx + 1) + '.jpg'
                file_path = 'images\\' + file_name
                cv2.imwrite(file_path, im)

                FileName.append(file_name)
        cap.release()

        df.insert(0, 'id', range(Total_Old + 1, Total_Old + len(Choose) + 1))
        df.insert(5, 'img_id', range(1, len(Choose) + 1))
        df['FileName'] = FileName  # ファイル名をカラムに追加
        df['Datetime'] = np.repeat(datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"), len(Choose))  # 更新日時をカラムに追加
        df.ix[:, 'FrameNum'] += 1
        df = pd.concat([df_Old, df])
        print df
        df.to_csv('TrainData.csv', index=False)  # TrainDataを更新

        # 読み込んだ動画ファイルをmaterial\\video移動
        if not os.path.isdir('videos'):
            os.mkdir('videos')

        dst = os.getcwd() + "\\videos"
        os.chdir(CD)
        src = os.getcwd() + '\\' + video
        print src
        print dst
        shutil.move(src, dst)


