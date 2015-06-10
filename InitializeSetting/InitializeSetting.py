# coding:utf-8
__author__ = 'yamamoto'

import os
import shutil

#  作業ディレクトリをTeachingAssistantにする
os.chdir('..')

#  Dropbox\\teachers内のDBファイルを消去する
#  DBファイルの場所としてDropboxのpathを取得
data_path = os.getenv("HOMEDRIVE") + \
            os.getenv("HOMEPATH") +  \
            "\\Dropbox\\teachers"

if os.path.isdir(data_path):
    shutil.rmtree(data_path)

#  CollectTrainImages\imagesを消去する
if os.path.isdir('CollectTrainImages\\images'):
    shutil.rmtree('CollectTrainImages\\images')

# CollectTrainImages\\TrainData.csvを消去する
if os.path.isfile('CollectTrainImages\\TrainData.csv'):
    os.remove('CollectTrainImages\\TrainData.csv')

# DBOutput\\bg.txtを消去する
if os.path.isfile('DBOutput\\bg.txt'):
    os.remove('DBOutput\\bg.txt')

# DBOutput\\info.datを消去する
if os.path.isfile('DBOutput\\info.dat'):
    os.remove('DBOutput\\info.dat')


# DBOutput\\TeacherData.csvを消去する
if os.path.isfile('DBOutput\\TeacherData.csv'):
    os.remove('DBOutput\\TeacherData.csv')


# DBOutput\\progress.csvを消去する
if os.path.isfile('DBOutput\\progress.csv'):
    os.remove('DBOutput\\progress.csv')