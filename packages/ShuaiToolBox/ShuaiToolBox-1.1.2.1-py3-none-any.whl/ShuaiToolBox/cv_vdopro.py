from .py_plugin import *

import operator
import cv2
import time
import os


# 获取视频文件的创建时间 [hour,min,sec]
def GetCreatTime(path):
    t = os.path.getctime(path)
    timeStruct = time.localtime(t)
    fina = [timeStruct.tm_hour, timeStruct.tm_min, timeStruct.tm_sec]
    return fina

# Define the Video Class
class Video:
    def __init__(self, path, start_time=[0, 0, 0]):
        self.Vdo = cv2.VideoCapture(path)
        self.path = path
        self.FPS = self.Vdo.get(cv2.CAP_PROP_FPS)
        self.Frame_Count = int(self.Vdo.get(cv2.CAP_PROP_FRAME_COUNT))
        if operator.eq(start_time, [0, 0, 0]):
            self.start_time = GetCreatTime(path)
        else:
            self.start_time = start_time

        self.Vdo.release()

    # 对于给定的视频，根据起止时间确定要捕捉的 Frame 索引
    #
    def GetCaptures(self, Space, Sm=0, Ss=0, Em=0, Es=0):
        # Start & End Frame index
        # From start frame of the Start_sec TO end frame of the End_sec
        if Sm == Ss == 0:
            Start_frame = 0
        else:
            Start_frame = self.FPS * (Sm * 60 + Ss)

        if Em == Es == 0:
            End_frame = self.Frame_Count - 1
        else:
            End_frame = self.FPS * (Em * 60 + Es + 1) if self.FPS * (
                        Em * 60 + Es + 1) < self.Frame_Count else self.Frame_Count - 1

        # Get Frames
        Frames = orange(int(Start_frame), int(End_frame), int(Space))
        return Frames


def GetCaptures(FPS, Frame_Count,Space, Sm=0, Ss=0, Em=0, Es=0):
    # Start & End Frame index
    # From start frame of the Start_sec TO end frame of the End_sec
    if Sm == Ss == 0:
        Start_frame = 0
    else:
        Start_frame = FPS * (Sm * 60 + Ss)

    if Em == Es == 0:
        End_frame = Frame_Count - 1
    else:
        End_frame = FPS * (Em * 60 + Es + 1) if FPS * (
                    Em * 60 + Es + 1) < Frame_Count else Frame_Count - 1

    # Get Frames
    Frames = orange(int(Start_frame), int(End_frame), int(Space))
    return Frames