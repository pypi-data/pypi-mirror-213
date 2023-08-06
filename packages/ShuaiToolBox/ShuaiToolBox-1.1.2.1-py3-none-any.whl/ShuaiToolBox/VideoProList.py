import sys,os
sys.path.append(r"D:\OneDrive - pku.edu.cn\000 Doing\DataFlux")

import cv2
import paddlehub as hub
from .VideoPro import *
import imageio
from .opencv_Functions import *

class process():
    def __init__(self,_path,_videos,_Times,_Cliplist):
        self.path=_path
        self.videos=_videos
        self.Times=_Times
        self.Cliplist=_Cliplist

def Speed_Fig(images,paths,Times,Space,output_dir):
    if (images!=None)&(paths!=None):
        print("input error! only one item should be specified.")
    elif images!=None: # images input
        videooutpath = output_dir + '\\X' + str(Times) + '.mp4'
        fps = _vdo.get(cv2.CAP_PROP_FPS)
        size = (int(_vdo.get(cv2.CAP_PROP_FRAME_WIDTH)), int(_vdo.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        video = cv2.VideoWriter(videooutpath, cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), fps, size, isColor=True)
        print("Start processing")
        for img in images:
            video.write(img)
        video.release()
        print("Output complete!")
    elif paths!=None: # paths input
        print(paths)
        pass
    else:
        print("input error!")

def Speed_Vdo(videos,paths,Times,Cliplist,output_dir,visualization=False):
    isProcess=False
    if(videos!=None)&(paths!=None):
        print("input error! only one item should be specified.")
    elif videos!=None:
        isProcess=True
    elif paths!=None:
        videoList=[]
        for p in paths:
            videoList.append(Video(p))
        isProcess=True
    else:
        print("input error!")

    if isProcess:
        frames, _ = GetFrameIndex2(Cliplist, videos, Times)
        videooutpath = output_dir + '\\X' + str(Times) + '.mp4'
        _vdo = cv2.VideoCapture(path[0])
        fps = _vdo.get(cv2.CAP_PROP_FPS)
        size = (int(_vdo.get(cv2.CAP_PROP_FRAME_WIDTH)), int(_vdo.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        _vdo.release()
        video = cv2.VideoWriter(videooutpath, cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), fps, size, isColor=True)
        if visualization:
            i=0
            makedir(output_dir + '\\Visualizaiton\\')
            for fr in frames:
                cv_imsave(fr, output_dir + '\\Visualizaiton\\'+str(i), '.jpg')  #
                video.write(fr)
                i=i+1
        else:
            for fr in frames: video.write(fr)
        video.release()

def Speed(path,videos,Times,Cliplist):
    print('start')
    frames, _ = GetFrameIndex2(Cliplist, videos, Times)
    videooutpath = os.path.dirname(path[0]) + '\\X' + str(Times) + '.mp4'
    # outpath=os.path.dirname(path[0])+'\\Capture\\'#
    _vdo = cv2.VideoCapture(path[0])
    fps = _vdo.get(cv2.CAP_PROP_FPS)
    size = (int(_vdo.get(cv2.CAP_PROP_FRAME_WIDTH)), int(_vdo.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    _vdo.release()
    video = cv2.VideoWriter(videooutpath, cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), fps, size, isColor=True)
    print('output')
    i = 0
    for fr in frames:
        video.write(fr)
        # cv_imsave(fr,outpath+str(i),'.jpg')#
        i += 1

    video.release()

def GetCapture(path,videos,Times,Cliplist):
    frames, _ = GetFrameIndex2(Cliplist, videos, Times)
    #frames, _ = GetFrameIndex2(Cliplist, videos, 25*60*Times)
    #frames, _ = GetFrameIndex2(Cliplist, videos, 25*Times)
    outpath = os.path.dirname(path[0]) + '\\Capture\\'
    #outpath=r'G:\ConvecDiss in CloseSys\Test\2022.11.18 WaterBulk\Capture\\'
    if not os.path.exists(outpath):
        os.makedirs(outpath)
    i = 0
    for fr in frames:
        #cv2.imwrite(outpath+'t='+str(i*Times)+' min.jpg',fr)
        cv_imsave(fr,outpath+'t='+str(i*Times)+' s','.jpg')#
        i += 1

def GetCapture(path,videos,Times,Cliplist):
    frames, _ = GetFrameIndex2(Cliplist, videos, Times)
    #frames, _ = GetFrameIndex2(Cliplist, videos, 25*60*Times)
    #frames, _ = GetFrameIndex2(Cliplist, videos, 25*Times)
    outpath = os.path.dirname(path[0]) + '\\Capture\\'
    #outpath=r'G:\ConvecDiss in CloseSys\Test\2022.11.18 WaterBulk\Capture\\'
    if not os.path.exists(outpath):
        os.makedirs(outpath)
    i = 0
    for fr in frames:
        #cv2.imwrite(outpath+'t='+str(i*Times)+' min.jpg',fr)
        cv_imsave(fr,outpath+'t='+str(i*Times)+' s','.jpg')#
        i += 1

def CaptureCrop(pathlist,crop):
    (path,filename)=os.path.split(pathlist[0])
    makedir(path+'\\Capture Crop\\')
    for p in pathlist:
        (path,filename)=os.path.split(p)
        (filename,ext)=os.path.splitext(filename)
        im=cv_imread(p)
        cv_imsave(im[crop[0]:crop[1],crop[2]:crop[3]],path+'\\Capture Crop\\'+filename,'.png')

def MakeDyImg(pathlist,loc,width,dir='x'):
    im=cv_imread(pathlist[0])
    if dir=='x':
        c=im[loc-width:loc+width,:]
        for p in pathlist[1:-1]:
            im=cv_imread(p)
            f=im[loc-width:loc+width,:]
            c = np.concatenate((c,f), axis = 0)
    if dir=='y':
        c=im[:,loc-width:loc+width]
        for p in pathlist[1:-1]:
            im=cv_imread(p)
            f=im[:,loc-width:loc+width]
            c = np.concatenate((c,f), axis = 1)
    (path,filename)=os.path.split(pathlist[0])
    cv_imsave(c,path+'\\Dyna-'+dir+'='+str(loc)+',width='+str(width)+',Num='+str(len(pathlist)),'.bmp')



ProcessSeq=[]



# path=r'I:\Water Hele-shaw\Water+1MPa\0.5mm'
# pathlist = GetFiles(path,'*.tiff')
# #CaptureCrop(pathlist,[209,1809,465,2045])
# MakeDyImg(pathlist[0:200],560,3,dir='x')

# path=r'I:\Water Hele-shaw\Water+1MPa\bulk\Capture'
# pathlist = GetFiles(path,'*.tiff')
# CaptureCrop(pathlist,[547,625,955,1069])


#pathlist=pathlist[0:300]
#cvFun.cv_toVideo(pathlist,path+'\\000.mp4',25)





# N=50
# img=[]
# i=0
# for p in pathlist:
#     if i%N==0:
#         img.append(imageio.imread(p))
#     i=i+1
# print(len(img))
# imageio.mimsave(path+"\\test.gif",img,fps=25)




# videos=[]
# path=r'I:\Water Porous(Repaired-指示剂更正)\Water 1mm(40ml瓶×2)-2'
# pathlist= GetFiles(path,'*.MTS')
# #pathlist=[r'Q:\孔尺度观察\1mm Pore\1MPa+1mm+玻璃模型+高速相机.mp4']
# VideoNumber=len(pathlist)
# for p in pathlist:
#     videos.append(Video(p))
# Cliplist=[Clip(0,0,0,3,0,2,0)]
# ProcessSeq.append(process(pathlist,videos,50,Cliplist))


# for i in range(len(ProcessSeq)):
#     Speed(ProcessSeq[i].path, ProcessSeq[i].videos, ProcessSeq[i].Times, ProcessSeq[i].Cliplist)
#     #GetCapture(ProcessSeq[i].path,ProcessSeq[i].videos,ProcessSeq[i].Times,ProcessSeq[i].Cliplist)

# path=r'I:\Water Hele-shaw\Water+1MPa\1mm'
# pathlist = GetFiles(path,'*.tiff')
# pathlist=pathlist[0:500]
# cvFun.cv_toVideo(pathlist,path+'\\000.mp4',25)




# path=r'I:\Water Hele-shaw\Water+1MPa\bulk\Capture'
# pathlist = GetFiles(path,'*.jpg')
# Crl_para=open(path+'\\'+'1crop.txt')
# Crl=[int(Crl_para.readline()),int(Crl_para.readline()),int(Crl_para.readline()),int(Crl_para.readline())]
# CaptureCrop(pathlist,[Crl[0],Crl[1],Crl[2],Crl[3]])
# cvFun.cv_toVideo(pathlist,path+'\\000.mp4',25)

# path=r'D:\img'
# pathlist = GetFiles(path,'*.png')

# module_name='falsr_c'
# sr_model = hub.Module(name='falsr_c')
# # path=r'F:\Ca(OH)2 Micromodel\Ca(OH)2+1MPa+NoPH\01-1s'
# # pathlist = GetFiles(path,'*.tiff')
# # pathlist=pathlist[0:1]
# res = sr_model.reconstruct(
#     images=None,
#     paths=pathlist,
#     use_gpu=False,
#     visualization=True,
#     output_dir=r'D:\img'
# )



videos=[]
# 多个视频
path=r'I:\Water Porous(Repaired-指示剂更正)\Water 1mm(40ml瓶×2)-2'
pathlist= GetFiles(path,'*.MTS')
# 单个视频
#pathlist=[r'Q:\孔尺度观察\1mm Pore\1MPa+1mm+玻璃模型+高速相机.mp4']
VideoNumber=len(pathlist)
for p in pathlist:
    videos.append(Video(p))
# 分 秒 视频序号 分 秒 视频序号 0
Cliplist=[Clip(0,0,0,3,0,2,0)]
ProcessSeq.append(process(pathlist,videos,50,Cliplist))
# 若为视频加速，为视频倍数（倍数即为隔多少帧取图像）输出视频与原视频帧率一致
# 若为提取图像，为隔多少帧取图像

for i in range(len(ProcessSeq)):
    # 视频加速
    Speed(ProcessSeq[i].path, ProcessSeq[i].videos, ProcessSeq[i].Times, ProcessSeq[i].Cliplist)
    # 提取图片
    GetCapture(ProcessSeq[i].path,ProcessSeq[i].videos,ProcessSeq[i].Times,ProcessSeq[i].Cliplist)



path=r'F:\Ca(OH)2 Sensitive Experiments\5MPa\5MPa+3mm-1'
pathlist = GetFiles(path,'*.tiff')
# 图片转视频
cvFun.cv_toVideo(pathlist,path+'\\000.mp4',25)
# 图片裁剪
CaptureCrop(pathlist,[547,625,955,1069])

