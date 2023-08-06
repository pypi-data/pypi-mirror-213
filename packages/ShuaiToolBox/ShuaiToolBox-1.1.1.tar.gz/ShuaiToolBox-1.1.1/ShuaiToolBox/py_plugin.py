import numpy as np
import os
import glob
import natsort

def os_linesep():
    if os.linesep=='\r\n':
        return '\n'
    else:
        return os.linesep

def orange(start, stop, space):
    l = np.arange(start, stop, space)
    l = l.tolist()
    l.append(stop)
    return l

def makedir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

def remove(list_i, value):
    j = 0
    for i in range(len(list_i)):
        if list_i[j] == value:
            list_i.pop(j)
        else:
            j += 1
    return list_i

def CheckFilesOpened(FilePath):
    # Define Error Code:
    imageExt=['jpg','png'] # result = 0 'img'
    videoExt=['mp4','mts'] # result = 1 'video'
    ErrorCode=''
    if len(FilePath)!=0:
        isFirst=True
        res=0
        for f in FilePath:
            ext=f.split('.')[-1]
            ext=ext.lower()
            if ext in imageExt: res = 0
            elif ext in videoExt: res=1

            if isFirst:
                res_pre=res
                isFirst=False
            if res!=res_pre:
                ErrorCode='The Files are not uniform'
                break

        # Deal with Error
        if ErrorCode is not '':
            print(ErrorCode)
            return ErrorCode
        # Deal with res
        else:
            return res
    else:
        pass

def GetFiles(path,ext):
    if (ext[0]!='.')&(ext[0]!='*'):
        ext='*.'+ext
    elif (ext[0]!='*'):
        ext='*'+ext
    filter_path = os.path.join(path, ext)
    path_list = natsort.natsorted(glob.glob(filter_path))
    return path_list