import cv2
import imageio
#import ffmpeg
import numpy as np
import copy
from cv_plugin import *


def GetIndex(Framelist,Clip,space):

    _start=Clip[0]
    _end=Clip[1]
    _startInd=Clip[2]
    _endInd=Clip[3]

    _totalFrame = 0
    for i in list(range(_start,_end+1)):
        if i==_end: _totalFrame+=_endInd+1
        elif i==_start: _totalFrame+=Framelist[i]-_startInd
        else: _totalFrame+=Framelist[i]

    _Framelist=copy.copy(Framelist)
    for i in range(0,_start):
        _Framelist[i]=0

    cumFrame=np.cumsum(np.array(_Framelist))
    cumFrame=np.insert(cumFrame,0,0)
    print(cumFrame)

    Frameindex=np.arange(_startInd,_totalFrame+1,space)

    Videoindex=[]
    FrameindexInVideo=[]
    Ind=0
    for i in range(_start,_end+1):
        to_Ind=Ind+np.sum(Frameindex>=cumFrame[i])-np.sum(Frameindex>cumFrame[i+1]-1)
        Videoindex.append(i)
        frames=Frameindex[Ind:to_Ind]-cumFrame[i]

        FrameindexInVideo.append(frames.tolist())
        Ind=to_Ind

    return Videoindex,FrameindexInVideo

def cv_ExplodeVideo(path):
    cap=cv2.VideoCapture(path)
    frames=[]
    while(cap.isOpened()):
        ret, frame=cap.read()
        if ret==False:
            break
        else:
            frames.append(frame)
    cap.release()
    return frames

def cv_toVideo(frames,path,fps,format='.mp4',space=1):
    if len(frames)!=0:
        # 识别frame的数据类型，判断其为图片地址还是图片
        isDir=0
        if isinstance(frames[0],str):
            isDir=1
            frame=cv_imread(frames[0])
            size = (frame.shape[1], frame.shape[0])
        else:
            isDir=0
            size = (frames[0].shape[1], frames[0].shape[0])
        # 判断输出格式
        # if format=='.gif' or '.GIF':# imageio package in Python
        #     imageio.mimsave(path,frames,'GIF')
        #     return True
        # else:
        #video = cv_VideoWriter(path, format, fps, size)
        video =cv2.VideoWriter(path, cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), fps, size, isColor=True)
        if isDir:# if the input is path
            print('Writing video from dictories.')
            for dir in frames:
                frame = cv_imread(dir)
                video.write(frame)
        else: # if the input is image
            print('Writing video from image list.')
            for i in list(range(0,len(frames),space)):
            #for i in frames:
                video.write(frames[i])
        video.release()
        return True
    else:
        return False


def VideoCombine(VdoPathList,path,format='.mp4',space=1):
    if len(VdoPathList)!=0:
        # Get FPS
        Vdo = cv2.VideoCapture(VdoPathList[0])
        fps = Vdo.get(cv2.CAP_PROP_FPS)
        size = (int(Vdo.get(cv2.CAP_PROP_FRAME_WIDTH)),int(Vdo.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        Vdo.release()

        # Get Format
        video = cv_VideoWriter(path, format, fps, size)

        for VdoPath in VdoPathList:
            Vdo=cv2.VideoCapture(VdoPath)
            VdoLength=int(Vdo.get(cv2.CAP_PROP_FRAME_COUNT))
            for i in list(range(0,VdoLength,space)):
                Vdo.set(cv2.CAP_PROP_POS_FRAMES, i)
                ret, frame = Vdo.read()
                video.write(frame)
            Vdo.release()

        video.release()
    else:
        return False

def RegularVideo(VdoPathList,OutPath,times,format='.mp4',fps=0):
    if len(VdoPathList)!=0:
        _vdo = cv2.VideoCapture(VdoPathList[0])
        if fps==0:
            fps = _vdo.get(cv2.CAP_PROP_FPS)
        size = (int(_vdo.get(cv2.CAP_PROP_FRAME_WIDTH)), int(_vdo.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        space=times
        _vdo.release()

        # Get Format
        video = cv_VideoWriter(OutPath, format, int(fps), size)

        # from video get Framelist
        Framelist=[]
        for temp_vdo in VdoPathList:
            temp_Vdocap=cv2.VideoCapture(temp_vdo)
            Frame_Count = int(temp_Vdocap.get(cv2.CAP_PROP_FRAME_COUNT))
            Framelist.append(Frame_Count)
            temp_Vdocap.release()

        # Construct Clip
        temp_Vdocap=cv2.VideoCapture(VdoPathList[-1])
        _endIndofLastVideo=int(temp_Vdocap.get(cv2.CAP_PROP_FRAME_COUNT))-1
        temp_Vdocap.release()
        Clip=[0,len(VdoPathList)-1,0,_endIndofLastVideo]

        # Get Index
        VideoInd,FrameInd=GetIndex(Framelist,Clip,space)
        for i in VideoInd:
            Vdocap=cv2.VideoCapture(VdoPathList[i])
            for fr in FrameInd[i]:
                Vdocap.set(cv2.CAP_PROP_POS_FRAMES,fr)
                ret,frame=Vdocap.read()
                if ret: video.write(frame)
            Vdocap.release()

        video.release()

    else:
        return False

def cv_VideoWriter(path,format,fps,size):
    # Get Format
    if format == '.mp4':
        video = cv2.VideoWriter(path, cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), fps, size, isColor=True)  #
    elif format == '.flv':  # Doesn't work
        video = cv2.VideoWriter(path, cv2.VideoWriter_fourcc('F', 'L', 'V', 'i'), fps, size)
    elif format == '.org':  # Doesn't work
        video = cv2.VideoWriter(path, cv2.VideoWriter_fourcc('T', 'H', 'E', 'O'), fps, size)
    elif format == '.avi-YUV':
        video = cv2.VideoWriter(path, cv2.VideoWriter_fourcc('I', '4', '2', '0'), fps, size)
    elif format == '.avi-1':  # Doesn't work
        video = cv2.VideoWriter(path, cv2.VideoWriter_fourcc('P', 'I', 'M', 'I'), fps, size)
    elif format == '.avi':
        video = cv2.VideoWriter(path, cv2.VideoWriter_fourcc('X', 'V', 'I', 'D'), fps, size)

    return video



# import ffmpeg
# import numpy
# import cv2
# import sys
# import random
#
# def read_frame_as_jpeg(in_file, frame_num):
#     """
#     指定帧数读取任意帧
#     """
#     out, err = (
#         ffmpeg.input(in_file)
#               .filter('select', 'gte(n,{})'.format(frame_num))
#               .output('pipe:', vframes=1, format='image2', vcodec='mjpeg')
#               .run(capture_stdout=True)
#     )
#     return out
#
#
# def get_video_info(in_file):
#     """
#     获取视频基本信息
#     """
#     try:
#         probe = ffmpeg.probe(in_file)
#         video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
#         if video_stream is None:
#             print('No video stream found', file=sys.stderr)
#             sys.exit(1)
#         return video_stream
#     except ffmpeg.Error as err:
#         print(str(err.stderr, encoding='utf8'))
#         sys.exit(1)
#
#
# if __name__ == '__main__':
#     file_path = './Test/EOR/video2.mp4'
#     video_info = get_video_info(file_path)
#     total_frames = int(video_info['nb_frames'])
#     print('总帧数：' + str(total_frames))
#     random_frame = random.randint(1, total_frames)
#     print('随机帧：' + str(random_frame))
#     out = read_frame_as_jpeg(file_path, random_frame)
#     image_array = numpy.asarray(bytearray(out), dtype="uint8")
#     image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
#     cv2.imshow('frame', image)
#     cv2.waitKey()


'''
Test functions
'''

# 随机生成一张图片
def cv_RandomImg(h,v):
    frame= np.random.rand(v,h,3)
    frame = np.uint8(255 * frame)
    return frame

def cv_GenImage(img):
    Blank = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8) + 255
    Blank = np.stack((Blank,) * 3, axis=-1)
    return Blank

#cv2.imshow('1',img)
#cv2.waitKey(0)

#fr=cv_ExplodeVideo()
#imglist=['D:/DCIM/1/2.mp4','D:/DCIM/1/3.mp4']
#VideoCombine(imglist,'4.mp4',format='.mp4',space=1)