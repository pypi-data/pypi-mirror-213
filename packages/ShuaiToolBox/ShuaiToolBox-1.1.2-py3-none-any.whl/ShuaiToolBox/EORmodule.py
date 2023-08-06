import math
import pandas as pd
from openpyxl import load_workbook
import re
import matplotlib.pyplot as plt
import matplotlib.cm as mplcm
import matplotlib.colors as mplcolors
import codecs

from .cv_plugin import *
from .VideoPro import *
from .py_plugin import *


class EOR():
    def __init__(self):

        #initialization Data
        self.dir = ''
        self.opendir='/'
        self.OutDir = ''
        self.subPhaseNum = 0

        self.Crop=[]

        # Color Separate algorithm parameters
        self.isColorSeparateAlgo = False

        self.Phase = []
        self.HSVs = []
        self.Cliplist = []
        self.le_Cliplist=[]
        self.ColorPhase_i = 0

        self.org_seq=[]
        self.PhasesNum = 1

        # Find Contours Algorithm
        self.isFindContourAlgo=False

        # ColorFrame
        self.isColorFrame = False
        self.colorbar=[]
        self.ColorbarTitle=''

        self.ImportPathRecord=os.path.join(os.curdir,'temp')
        self.ExportPathRecord=os.path.join(os.curdir,'temp')

    def EOR_Process(self):
        self.PhaseSeqPro()
        # Check the Files
        FileType=1

        print('------------ Geting Frame ------------------')
        if FileType==0: #Image
            _, Captures =Image2Capture(self.dir)
        elif FileType==1: # Video
            EORVideos = []
            for temp in self.dir:
                EORVideos.append(Video(temp))
            _, Captures = GetFrameIndex2(self.Cliplist, EORVideos, self.Frame_Space)

        print('----------------Process start---------------')
        self.CaptureProcess(Captures, self.Phase,Crop=self.Crop)
        self.ColorFrame(Captures,self.ColorPhase_i)
        self.WriteExcel(Captures)
        print('Excel Export Complete.')

    def ReadPara(self):
        # Read HSV data
        self.HSVs=[]
        HSVstr=qListw_GetItems(self.Listw_HSV)
        for ihsv in HSVstr:
            temp=re.split(": ",ihsv)
            temp=eval(temp[1])
            self.Echo(str(temp))
            self.HSVs.append(temp)

    def PhaseSeqPro(self):
        self.PhasesNum = len(self.org_seq)
        self.Phase.clear()
        for line in self.org_seq:
            equation=re.split("=",line)
            name=equation[0]
            name = name.strip()

            seq='='+equation[1]
            seq = re.split(r"(\D)", seq)
            seq=remove(seq,'')
            seq=remove(seq,' ')
            temp_p = Phases()
            temp_p.name=name
            temp_p.subPhase = self.HSVs
            temp_p.PhaseSequence = seq
            self.Phase.append(temp_p)

    def CaptureProcess(self, Captures, Phase, Crop=[]):
        TotalFrame = len(Captures)
        cmap = mplcm.get_cmap("rainbow", TotalFrame)

        # For Echo processing bar
        count = 1
        rate = 0
        print('{}% processing, {}th in total {} frams'.format(rate, 0, TotalFrame))

        for Capture in Captures:
            # output the progress rate
            if math.floor((count * 100) / TotalFrame) != rate:
                rate = math.floor((count * 100) / TotalFrame)
                print('{}% processing, {}th in total {} frams'.format(rate, count, TotalFrame))

            # Locate the video
            # if Capture.iVideo != videoi:
            #     if count == 1:
            #         videoi = videoi + 1
            #         Video = next(it)
            #         VdoCap = cv2.VideoCapture(Video.path)
            #     else:
            #         videoi = videoi + 1
            #         VdoCap.release()
            #         Video = next(it)
            #         VdoCap = cv2.VideoCapture(Video.path)
            # #VdoCap = cv2.VideoCapture(Video.path)
            # VdoCap.set(cv2.CAP_PROP_POS_FRAMES, Capture.iFrame)
            # ret, frame = VdoCap.read()

            if len(Crop) != 0:
                Capture.frame = Capture.frame[Crop[2]:Crop[3], Crop[0]:Crop[1]]  # y1:y2,x1:x2

            #Capture.GetFrame(frame)

            if self.isColorSeparateAlgo:
                Capture.Separate(Phase)
            elif self.isFindContourAlgo:
                Capture.FindContours()

            Capture.CalArea()
            Capture.WriteFile(self.OutDir)

            count = count + 1

        # VdoCap.release()


    def ColorFrame(self,Captures,ColorPhase_i):

        if len(Captures)!=0:
            count=1
            TotalFrame=len(Captures)
            cmap = mplcm.get_cmap("rainbow", TotalFrame)

            size=(Captures[0].frame.shape[0], Captures[0].frame.shape[1])
            # Initial base image
            Final = np.zeros(size, dtype=np.uint8)
            Final = np.stack((Final,) * 3, axis=-1)
            pre_mask = np.zeros(size, dtype=np.uint8) + 0
            for Capture in Captures:

                if self.isColorFrame:
                    Capture.ColorFrame(Capture.Phase_frames[ColorPhase_i], cmap(count / TotalFrame), pre_mask)
                    pre_mask = Capture.Phase_frames[ColorPhase_i]
                    Final = cv2.add(Final, Capture.colorframe)
                    cv2.imshow(str(count),Capture.colorframe)
                    # cv2.imshow(str(i),Final)
                count+=1


            # Sturation Calculation
            # if self.isColorFrame:
            #     max_Area=Captures[-1].PhaseArea[0]
            #     i=1
            #     for Capture in Captures:
            #         if i == 1:
            #             pre_mask = np.zeros((frame.shape[0], frame.shape[1]), dtype=np.uint8) + 0
            #             Capture.ColorFrame(Capture.Phase_frames[ColorPhase_i], cmap(Capture.PhaseArea[0] / max_Area), pre_mask)
            #
            #             pre_mask = Capture.Phase_frames[ColorPhase_i]
            #
            #             Final = np.zeros((Capture.frame.shape[0], Capture.frame.shape[1]), dtype=np.uint8)
            #             Final = np.stack((Final,) * 3, axis=-1)
            #
            #         else:
            #             Capture.ColorFrame(Capture.Phase_frames[ColorPhase_i], cmap(Capture.PhaseArea[0] / max_Area), pre_mask)
            #             pre_mask = Capture.Phase_frames[ColorPhase_i]
            #
            #         Final = cv2.add(Final, Capture.colorframe)
            #         i+=1


            if self.isColorFrame:
                Final = cv2.cvtColor(Final, cv2.COLOR_BGR2RGB)

                fig, ax = plt.subplots(1, 1, constrained_layout=True, sharey=True)  # ,figsize=(6, 2)
                cmap1 = plt.get_cmap("rainbow")
                #colors = cmap(np.linspace(0, 1, cmap.N))

                ax.imshow(Final)
                ax.set_xticks([])
                ax.set_yticks([])

                norm = mplcolors.Normalize(vmin=self.colorbar[0], vmax=self.colorbar[1])
                sm = mplcm.ScalarMappable(norm=norm, cmap=cmap)
                sm.set_array([])
                fig.colorbar(sm, ax=ax, orientation='vertical', label=self.ColorbarTitle)
                plt.show()



    def WriteExcel(self, Captures):
        name, npdata = Cap2List(Captures)
        ExcelPath=os.path.join(self.OutDir,'Data.xlsx')
        if os.path.exists(ExcelPath):
            os.remove(ExcelPath)

        ### 对data操作

        # np.save("npdata.npy",npdata)
        # npdata=np.load("npdata.npy")

        # 读取压力数据 CC3 file
        # CCdata=ReadCCdata(str(r'H:\SDS-3AP\模型驱油实验\2021.2.3 亲油模型驱油实验\New_Measure_03-02-2021.csv'))

        # 提取和Clip相同时刻的压力
        # findindex = lambda self,i,value:sorted(self,key=lambda x:x[i]!=value)[0]
        # Clip_Pre=np.empty(npdata.shape[1],dtype=float)
        # i=0
        # for x in np.nditer(npdata[3]):
        #    a=findindex(CCdata,1,x)
        #    Clip_Pre[i]=float(a[3])
        #    i+=1

        # 得到PV数据
        np_PV = np.cumsum(npdata[2].astype(float))
        # 得到油采收率
        # Oil_Ref=npdata[5][0]
        # Rec=100-(npdata[5].astype(float))/float(Oil_Ref)*100
        # 得到水和CO2的注入速率
        # WaterInjectionList=[0.5]
        # CO2InjectionList=[1.0,2.0]
        # Inj_Water=[]
        # Inj_CO2=[]
        # i=0
        # for x in np.nditer(npdata[2]):
        #    if float(x) in WaterInjectionList:
        #        #print("x:  ",x,"    float_x:  ",float(x))
        #        Inj_Water.append(str(x))
        #        Inj_CO2.append('')
        #    elif float(x) in CO2InjectionList:
        #        Inj_Water.append('')
        #        Inj_CO2.append(str(x))
        #    else:
        #        Inj_Water.append('')
        #        Inj_CO2.append('')
        #    i+=1

        # 把处理后的数据插入至npdata
        # name=['ClipNum','VideoNum','PV=1','InjRate','Inj_Water','Inj_CO2','Time','Pillar','Oil','Recovery','Water','Pressure']
        # npdata=np.insert(npdata,2,values=np_PV,axis=0)
        # npdata=np.insert(npdata,4,values=Inj_Water,axis=0)
        # npdata=np.insert(npdata,5,values=Inj_CO2,axis=0)
        # npdata=np.insert(npdata,9,values=Rec,axis=0)
        # npdata=np.insert(npdata,11,values=Clip_Pre,axis=0)

        data = (np.transpose(npdata)).tolist()

        # np.save('dataRecord',data)
        # d=[]
        # for i in data:
        #    d.append(i[2])

        # f=()
        # for i in d:
        #    f.append(datetime(2021,2,1,1,1,1,30000))
        # df = pd.DataFrame([datetime(2014, 9, 18, 12, 30, 5, 60000)])

        # 将数据写入Excel中，并绘图
        pddata = pd.DataFrame(data, index=None, columns=name)  # ,columns=name
        # pddata[['ClipNum','VideoNum']]=pddata[['ClipNum','VideoNum']].apply(pd.to_numeric, errors='ignore')
        # pddata[['PV=1','InjRate','Inj_Water','Inj_CO2','Pillar','Oil','Recovery','Water','Pressure']]=pddata[['PV=1','InjRate','Inj_Water','Inj_CO2','Pillar','Oil','Recovery','Water','Pressure']].apply(pd.to_numeric, errors='ignore')
        #pddata['Time'] = pd.to_datetime(pddata['Time'], format="%I:%M:%S")

        # pdCCdata=pd.DataFrame(CCdata,index=None,columns=['Date','Time','ms','Pressure'],dtype=float)
        # pdCCdata['Time']=pd.to_datetime(pdCCdata['Time'],format="%I:%M:%S")

        writer = pd.ExcelWriter(ExcelPath, engine='xlsxwriter', datetime_format='hh:mm:ss')
        pddata.to_excel(writer, index=None, columns=name, sheet_name='Sheet1')  # ,columns=name
        # pdCCdata.to_excel(writer,index=None,columns=['Date','Time','ms','Pressure'],sheet_name='Sheet2')

        #insertLoc = 'N2'

        workbook = writer.book
        writer.save()  ###
    # Assistant Functions

######################################################################################################################
def ReadCCdata(path):
    out_path = os.path.dirname(path)
    f = open(path)
    lines = f.readlines()
    pdata = []

    num = 1
    flag = True
    for line in lines:
        if num < 6:
            num += 1
            continue
        else:
            data = re.split(" |\t|PM\.|\n|AM.|;", line)
            if flag:
                flag = False
                t0 = data[1]
            if len(data) > 3:
                del data[5:12]
                del data[2]
                t1 = data[1]
                if t0 == t1:
                    continue
                else:
                    t0 = t1
                    pdata.append(data)
    pdata.pop()
    pdata.pop()
    return pdata

def Cap2List(Capture):
    names = ['ClipNum', 'VideoNum', 'InjRate', 'Time']
    for i in Capture[0].Phase_frames_names:
        names.append(i)

    Dat_ClipNum_List = []
    Dat_VideoNum_List = []
    Dat_Time_List = []
    Dat_PhaseArea_List = []
    Dat_PhaseRate_List = []
    for cap in Capture:
        Dat_ClipNum_List.append(cap.iClip)
        Dat_VideoNum_List.append(cap.iVideo)
        Dat_PhaseRate_List.append(cap.InjRate)
        Dat_Time_List.append('%d:%02d:%02d' % (int(cap.time[0]), int(cap.time[1]), int(cap.time[2])))

        temp_AreaList = []
        for i in range(cap.PhaseNum):
            temp_AreaList.append(cap.PhaseArea[i])
        Dat_PhaseArea_List.append(temp_AreaList)

    data = [Dat_ClipNum_List, Dat_VideoNum_List, Dat_PhaseRate_List, Dat_Time_List]
    npdata = np.array(data)
    npdata = np.concatenate((npdata, np.transpose(np.array(Dat_PhaseArea_List))), axis=0)
    # data=(np.transpose(npdata)).tolist()
    return names, npdata
