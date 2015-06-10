# coding:utf-8
__author__ = 'yamamoto'

import cv2

NameID = "KOTAYU"
Date = "150525"
Num = "4"


# ビデオの読み込み・プロパティの取得
video = NameID + Date + "_" + Num + ".mp4"
cap = cv2.VideoCapture(video) # Read Video File

FrameNum_Total = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
print FrameNum_Total