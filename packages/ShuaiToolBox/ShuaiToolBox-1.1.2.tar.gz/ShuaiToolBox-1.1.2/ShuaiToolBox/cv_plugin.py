import cv2
import numpy as np

def cv_imread(img_path):
    cv_img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), -1)
    #cv_img = cv2.cvtColor(cv_img, cv2.COLOR_RGB2BGR)
    return cv_img

def cv_imsave(image, img_path, img_ext):
    # img_ext: .jpg/.png
    cv2.imencode(img_ext, image)[1].tofile(img_path + img_ext)

    # 白色区域(1)相减
def bitwise_miner(src1, src2):
    return cv2.bitwise_and(src1, cv2.bitwise_not(src2))


def bitwise_plus(src1, src2):
    return cv2.add(src1, src2)


# img1=cv2.imread(r'D:\OneDrive - pku.edu.cn\000 Doing\DataFlux\Test\EOR\Video1.mp4 VideoPro\Clip 1\Clip 1_1-0-0\1-0-0.jpg')
# img2=cv2.imread(r'D:\OneDrive - pku.edu.cn\000 Doing\DataFlux\Test\EOR\Video1.mp4 VideoPro\Clip 1\Clip 1_1-0-0\1-0-01.jpg')
#
# #gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
# #ret, img2 = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
#
# #img=cv2.bitwise_and(img1, img1,mask=img2)
# img=cv2.bitwise_and(img1, img2)
#
# cv2.imshow('1',img)
# cv2.waitKey(0)