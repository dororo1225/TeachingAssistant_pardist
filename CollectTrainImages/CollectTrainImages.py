# coding:utf-8
__author__ = 'yamamoto'

import cv2
import numpy as np
import pandas as pd
import os
import shutil
import datetime

CD = os.getcwd()

# ビデオの読み込み・プロパティの取得
Name = "KOTAYU"
Date = "150608"
Num = "1"

TrainDataNum = 750

video = Name + Date + "_" + Num + ".mp4"
# video = "inokei.mp4"
cap = cv2.VideoCapture(video) # Read Video File

FrameNum_Total = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))

# CTI_dir = os.getcwd()  # 現在のディレクトリを取得

if TrainDataNum > FrameNum_Total:
    print '----------------------------------------------------------'
    print 'Number of Training Data is larger than total frame number'
    print 'Check Number of Training Data'
    print '----------------------------------------------------------'
else:

    os.chdir('..\\material')

    if os.path.isdir('images'):
        print '----------------------------------'
        print 'Folder "images" is already exited'
        print 'Check content of folder "images"'
        print '----------------------------------'

    else:
        os.mkdir('images')  # 顔検出画像の保存ディレクトリの作成
        Choose = np.random.choice(range(0, FrameNum_Total), TrainDataNum, replace=False)
        df = pd.DataFrame({'VideoName': np.repeat(video, len(Choose)),
                            'FrameNum': Choose,
                            'Name': np.repeat(Name, len(Choose)),
                            'Date': np.repeat(Date, len(Choose))
                            })
        df = df.sort('FrameNum')
        df.index = range(0, df.shape[0])
        df = df[['VideoName', 'FrameNum', 'Name', 'Date']] # 列の並び替え

        FileName = []
        for idx in df.index:
            FrameNum = df.ix[idx, 'FrameNum']
            cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, FrameNum)
            ret, im = cap.read()
            if ret:
                # cv2.imshow('Video Stream', im)  # Check Detected 'Face'
                im = cv2.resize(im, (im.shape[1] * 5 / 12, im.shape[0] * 5 / 12))  # resize image
                # 画像の書き出し
                file_name = 'id' + str(idx + 1).zfill(5) + '_' + Name + Date + '_' + str(idx + 1) + '.jpg'
                file_path = 'images\\' + file_name
                cv2.imwrite(file_path, im)

                FileName.append(file_name)
        cap.release()

        df.insert(0, 'id', range(1, len(Choose) + 1))
        df.insert(5, 'img_id', range(1, len(Choose) + 1))
        df['FileName'] = FileName # ファイル名のカラムを追加
        df['Datetime'] = np.repeat(datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"), len(Choose))  # 更新日時
        df.ix[:, 'FrameNum'] += 1
        print df
        df.to_csv('TrainData.csv', index=False)

        # 読み込んだ動画ファイルをmaterial\\video移動
        if not os.path.isdir('videos'):
            os.mkdir('videos')

        dst = os.getcwd() + "\\videos"
        os.chdir(CD)
        src = os.getcwd() + '\\' + video
        print src
        print dst
        shutil.move(src, dst)