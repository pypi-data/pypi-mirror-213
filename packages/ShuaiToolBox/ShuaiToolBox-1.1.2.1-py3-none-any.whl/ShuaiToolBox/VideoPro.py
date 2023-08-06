from .cv_plugin import *
from .cv_vdopro import *
from .FindContours import *
from .opencv_Functions import GetIndex,cv_GenImage

# 根据颜色上下限对图像进行二值化处理
def color_seperate(image, lower_hsv, upper_hsv):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)  # 对目标图像进行色彩空间转换
    # 依据设定的上下限对目标图像进行二值化转换,在区间内的为1，不在区间内的为0
    mask = cv2.inRange(hsv, lowerb=lower_hsv, upperb=upper_hsv)
    # dst = cv.bitwise_and(image, image, mask=mask)    #将二值化图像与原图进行“与”操作；实际是提取前两个frame 的“与”结果，然后输出mask 为1的部分
    # 注意：括号中要写mask=xxx
    return mask

def FindContours(image):
    target_contour = ContoursFilterByMouse(image)
    mask = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)
    cv2.drawContours(mask, target_contour, -1, 255, cv2.FILLED)

    return mask

def Separate_Seq(frame, Phase):
    Phase_frames = []
    Blank = np.zeros((frame.shape[0], frame.shape[1]), dtype=np.uint8) + 255
    # Blank=np.stack((Blank,)*3,axis=-1)
    for temp_p in Phase:
        right = False
        Add = False
        Miner = False
        Plus = False
        res = Blank
        res_frame = frame
        for s in temp_p.PhaseSequence:
            if right:
                if s.isdigit():
                    hsv = np.array(temp_p.subPhase[int(s)])
                    if Add:
                        res = cv2.bitwise_and(res, color_seperate(res_frame, hsv[0], hsv[1]))
                        res_frame = cv2.bitwise_and(res_frame, res_frame, res)
                        Add = False
                    elif Miner:
                        res = bitwise_miner(res, color_seperate(res_frame, hsv[0], hsv[1]))
                        res_frame = cv2.bitwise_and(res_frame, res_frame, res)
                        Miner = False
                    elif Plus:
                        res = bitwise_plus(res, color_seperate(res_frame, hsv[0], hsv[1]))
                        res_frame = cv2.bitwise_and(res_frame, res_frame, res)
                        Plus = False
                    else:
                        res = color_seperate(res_frame, hsv[0], hsv[1])
                        res_frame = cv2.bitwise_and(res_frame, res_frame, res)
                if s == "*":
                    Add = True
                if s == "-":
                    Miner = True
                if s == "+":
                    Plus = True
            else:
                if s == "=":
                    right = True
        Phase_frames.append(res)
    return Phase_frames


# 根据起始时间和间隔秒，计算当前时间 [hour,min,sec]
def TimeCal(t1, sec):
    t2 = t1.copy()
    t2[2] = (t1[2] + sec) % 60
    t2[1] = ((t1[2] + sec) // 60 + t1[1]) % 60
    t2[0] = ((t1[2] + sec) // 60 + t1[1]) // 60 + t1[0]
    if t2[0] > 12:
        t2[0] -= 12
    return t2


class Phases():
    def __init__(self):
        self.name=''
        self.subPhase = []
        self.PhaseSequence = ''


# 视频采集frame
class Capture:
    def __init__(self, iClip, iVideo, iFrame, Capture_time, InjRate):

        self.iClip = iClip + 1
        self.iVideo = iVideo
        self.iFrame = iFrame
        self.time = Capture_time
        self.InjRate = InjRate

        self.Phase_frames = []

        #self.name = '{}-{}-{}'.format(int(self.time[0]), int(self.time[1]), int(self.time[2]))
        self.name='{}-{}-{}'.format(iVideo,iClip,iFrame)

        # Define the path ouput the files
        # self.path_out = './VideoProcess3/Clip {}/Clip {}_{}'.format(self.iClip, self.iClip, self.name)
        # isExist = os.path.exists(self.path_out)
        # if not isExist:
        #    os.makedirs(self.path_out)

    def GetFrame(self, frame):
        self.frame = frame

    def Separate(self, Phase):
        self.PhaseNum = len(Phase)
        self.Phase_frames = Separate_Seq(self.frame, Phase)
        self.Phase_frames_names=[i.name for i in Phase]

    def FindContours(self):
        self.PhaseNum = 1
        self.Phase_frames.append(FindContours(self.frame))
        self.Phase_frames_names=['1']

    def CalArea(self):
        Capture_Size = (self.frame.shape[0]) * (self.frame.shape[1])
        self.PhaseArea = []
        for i in range(self.PhaseNum):
            self.PhaseArea.append(cv2.countNonZero(self.Phase_frames[i]))

    def ColorFrame(self, binary_image, c, mask):
        Phase2 = bitwise_miner(binary_image, mask)
        Phase2 = np.stack((Phase2,) * 3, axis=-1)
        b, g, r = cv2.split(Phase2)

        ret1, b = cv2.threshold(b, 0, c[2] * 255, cv2.THRESH_BINARY)
        ret2, g = cv2.threshold(g, 0, c[1] * 255, cv2.THRESH_BINARY)
        ret3, r = cv2.threshold(r, 0, c[0] * 255, cv2.THRESH_BINARY)
        dst = cv2.merge((b, g, r))

        self.colorframe = dst

    # Write the image to the file
    def WriteFile(self, path):
        path_out = os.path.join(path, 'Clip {}'.format(self.iClip), 'Clip {}_{}'.format(self.iClip, self.name))
        isExist = os.path.exists(path_out)
        if not isExist:
            os.makedirs(path_out)

        # Write the separated image to the Sub Dir.
        cv_imsave(self.frame, os.path.join(path_out, self.name), '.jpg')
        i = 1
        for i in range(len(self.Phase_frames)):
            cv_imsave(self.Phase_frames[i], os.path.join(path_out , self.name + self.Phase_frames_names[i]), '.jpg')
            i += 1

    # Delete the image from memory
    def _destory(self):
        del self.frame
        del self.Phase_frames


# 定义视频片段类
class Clip:
    def __init__(self, start_min, start_sec, start_videoIndex, end_min, end_sec, end_videoIndex, InjRate):
        self.start_min = start_min
        self.start_sec = start_sec
        self.start_i = start_videoIndex
        self.end_min = end_min
        self.end_sec = end_sec
        self.end_i = end_videoIndex
        self.InjRate = InjRate



def GetFrameIndex2(Cliplist,Videos,FrameSpace):
    Captures = []
    Frames = []

    # Process Video
    _FrameCount=[]
    for v in Videos:
        _FrameCount.append(v.Frame_Count)

    # process the Cliplist & Videos
    iclip=0
    for c in Cliplist:
        # Get Index
        _from=c.start_i
        _to=c.end_i
        _IndexFrom=Videos[_from].FPS*(c.start_min*60+c.start_sec)
        _IndexTo = Videos[_to].FPS * (c.end_min * 60 + c.end_sec)
        _clip=[_from,_to,_IndexFrom,_IndexTo]
        _VideoIndex,_FrameIndex=GetIndex(_FrameCount,_clip,FrameSpace)

        Clip_Cap = []
        Clip_frames = []

        for i in range(len(_VideoIndex)):
            vdo=Videos[_VideoIndex[i]]
            VdoCap=cv2.VideoCapture(vdo.path)

            frame_num=0
            for fr in _FrameIndex[i]:
                temp_capture = Capture(iclip, _VideoIndex[i], fr, TimeCal(vdo.start_time, fr / vdo.FPS),
                                       c.InjRate)
                VdoCap.set(cv2.CAP_PROP_POS_FRAMES, fr)
                print(fr)
                ret,frame=VdoCap.read()
                # cv2.namedWindow('1',0)
                # cv2.imshow('1', frame[1054:1357,1158:1569])
                # cv2.waitKey(0)
                if ret:
                    Clip_frames.append(frame)
                    temp_capture.GetFrame(frame)
                    record_frame=frame
                else:
                    print('------------Lost one frame at No. '+str(frame_num)+'/'+str(len(_FrameIndex[i]))+'-------------')
                    blank=cv_GenImage(record_frame)
                    Clip_frames.append(blank)
                Clip_Cap.append(temp_capture)
                frame_num=frame_num+1

            VdoCap.release()
        Frames.extend(Clip_frames)
        Captures.extend(Clip_Cap)
        iclip+=1

    return Frames,Captures

# 对于给定的视频序列，根据起始时间列表确定要捕捉的画面
def GetFrameIndex(Cliplist, Videos, FrameSpace):
    Captures = []
    Frames=[]

    IsOver = False
    IsNextvideo = False
    IsNextClip = False

    n = 0
    ivideo = 0
    for video in Videos:
        ivideo = ivideo + 1
        # Read video frame
        VdoCap = cv2.VideoCapture(video.path)
        while not IsNextClip:
            # 确定当前clip是否在范围内，不在该视频中，跳到下一个视频
            if (Cliplist[n].start_i < (ivideo) and Cliplist[n].end_i < (ivideo)) or (
                    Cliplist[n].start_i > (ivideo) and Cliplist[n].end_i > (ivideo)):
                # IsNextvideo=True
                break
            # 在该视频范围内，分为三种情况：1.不跨视频截图；2.跨一个视频截图3.跨多个视频
            else:
                if Cliplist[n].start_i == Cliplist[n].end_i:  # 1
                    start_min = Cliplist[n].start_min
                    start_sec = Cliplist[n].start_sec
                    end_min = Cliplist[n].end_min
                    end_sec = Cliplist[n].end_sec
                    IsNextClip = True
                elif Cliplist[n].start_i == ivideo:  # 2-1
                    start_min = Cliplist[n].start_min
                    start_sec = Cliplist[n].start_sec
                    end_min = 0
                    end_sec = 0
                    IsNextvideo = True
                elif Cliplist[n].end_i == ivideo:  # 2-2
                    start_min = 0
                    start_sec = 0
                    end_min = Cliplist[n].end_min
                    end_sec = Cliplist[n].end_sec
                    IsNextClip = True
                elif Cliplist[n].start_i < ivideo < Cliplist[n].end_i:  # 3
                    start_min = 0
                    start_sec = 0
                    end_min = 0
                    end_sec = 0
                    IsNextvideo = True

                FramesIndex = video.GetCaptures(FrameSpace, Sm=start_min, Ss=start_sec, Em=end_min, Es=end_sec)

                # Initial list size
                VdoCap.set(cv2.CAP_PROP_POS_FRAMES,0)
                ret, Video_Frame = VdoCap.read()
                temp_list_Frame=[Video_Frame]*len(FramesIndex)
                frame_i=0
                temp_list_Cap=[None]*len(FramesIndex)
                for iframe in FramesIndex:
                    temp_capture = Capture(n, ivideo, iframe, TimeCal(video.start_time, iframe / video.FPS), Cliplist[n].InjRate)
                    VdoCap.set(cv2.CAP_PROP_POS_FRAMES, iframe)
                    ret, Video_Frame = VdoCap.read()
                    if ret:
                        temp_capture.frame=Video_Frame
                        #Frames.append(Video_Frame)
                        #Captures.append(temp_capture)
                        temp_list_Frame[frame_i]=Video_Frame
                        temp_list_Cap[frame_i]=temp_capture
                        frame_i+=1
                    else:
                        print(iframe)
                # num_processes=mp.cpu_count()
                # p=mp.Pool(num_processes)
                # p.apply_async(func=GetFrames_multi, arg=(VdoCap,video,))

                Frames.extend(temp_list_Frame)
                Captures.extend(temp_list_Cap)

                if IsNextvideo:
                    IsNextvideo = False
                    break

                if IsNextClip:
                    IsNextClip = False
                    n += 1
                    if n == len(Cliplist):
                        IsOver = True
                        break
        VdoCap.release()
        if IsOver:
            break
    return Frames,Captures

def GetFrames_multi(_Video,video,FramesIndex,n,ivideo,Cliplist):

    temp_capture = Capture(n, ivideo, FramesIndex, TimeCal(video.start_time, FramesIndex / video.FPS), Cliplist[n].InjRate)
    _Video.set(cv2.CAP_PROP_POS_FRAMES, FramesIndex)
    ret, Video_Frame = _Video.read()
    temp_capture.frame = Video_Frame

    return Video_Frame,temp_capture

def ExtractFromVideos(Videos,TimeSpace=0,Sm=0, Ss=0, Em=0, Es=0):
    if len(Videos)!=0:
        VdoCap = cv2.VideoCapture(Videos[0])
        FPS = VdoCap.get(cv2.CAP_PROP_FPS)
        FrameSpace=TimeSpace*FPS
        Cliplist=[Clip(Sm,Ss,0,Em,Es,len(Videos)-1,0)]
        Frames,_=GetFrameIndex(Cliplist,Videos,FrameSpace)
        return Frames
    else:
        return False


def Image2Capture(Imagepaths):
    Captures=[]
    Frames=[]
    TotalImg=len(Imagepaths)
    if TotalImg!=0:
        i=0
        for path in Imagepaths:
            img=cv_imread(path)
            temp_capture = Capture(1, 0, i, GetCreatTime(path), 0)
            temp_capture.frame=img
            Captures.append(temp_capture)
            Frames.append(img)

    return Frames,Captures

def Img2Video(path,fps,crop=0):
    #path = r'M:\高压\Co2 Flooding\Part1'
    path_list = os.listdir(path)
    # Sort by time
    path_list = sorted(path_list, key=lambda x: os.path.getmtime(os.path.join(path, x)))
    # Default output name
    videooutpath = os.path.dirname(path + '/' + path_list[0]) + '\\Video.mp4'
    # Get the frame size
    img = cv2.imdecode(np.fromfile(path + "/" + path_list[0], dtype=np.uint8), -1)
    size = (int(img.shape[1]), int(img.shape[0]))
    video = cv2.VideoWriter(videooutpath, cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), fps, size, isColor=True)
    for p in path_list:
        f = cv2.imdecode(np.fromfile(path + "/" + p, dtype=np.uint8), -1)
        video.write(f)
    video.release()