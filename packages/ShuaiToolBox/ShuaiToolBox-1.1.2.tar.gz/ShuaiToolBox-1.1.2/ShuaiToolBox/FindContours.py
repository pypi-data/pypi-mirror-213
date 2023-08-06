import cv2
import copy
import time

def ContoursFilterByMouse(images):
    # Get image
    image = copy.copy(images)
    # init the window
    WindowName = 'Image'
    cv2.namedWindow(WindowName)
    cv2.imshow(WindowName, image)
    target_contour = []

    # opencv轮廓检测
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    _, contours, _ = cv2.findContours(binary, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    FilterContours = contours
    # for i in range(len(contours)):
    #    if len(contours[i])>200:
    #        #print(cv2.contourArea(contours[i]))
    #        #print()
    #        if 5000<cv2.contourArea(contours[i]):
    #            FilterContours.append(contours[i])
    #            #cv2.drawContours(img,contours,i,(0,0,255),3)

    cv2.drawContours(image, FilterContours, -1, (0, 0, 255), 3)
    cv2.imshow(WindowName, image)

    def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            if len(FilterContours)>0:
                cv2.circle(image, (x, y), 1, (255, 0, 0), thickness=-1)
                dist = []
                for i in range(len(FilterContours)):
                    flag = cv2.pointPolygonTest(FilterContours[i], (x, y), True)
                    dist.append(flag)
                dist = list(map(abs, dist))
                target_index = dist.index(min(dist))
                target_contour.append(FilterContours[target_index])
                cv2.drawContours(image, FilterContours, target_index, (0, 255, 0), 3)
                cv2.imshow(WindowName, image)
                #cv2.waitKey(0)
                # if cv2.getWindowProperty(WindowName, 0) == -1:
                #time.sleep(0.5)
                # cv2.destroyWindow(WindowName)

    cv2.setMouseCallback(WindowName, on_EVENT_LBUTTONDOWN)
    while True:
        # if target_contour[0] is not 0:
        # cv2.destroyWindow(WindowName)
        # cv2.waitKey(1)
        #    break
        if (cv2.waitKey() == 13): # Enter
            cv2.destroyWindow(WindowName)
            break
    #cv2.destroyWindow(WindowName)
    return target_contour

# target_contour=ContoursFilterByMouse(img)
# cv2.drawContours(img,target_contour,0,(0,0,255),3)
# mask=np.zeros((img.shape[0],img.shape[1]),dtype=np.uint8)
# cv2.drawContours(mask,target_contour,-1,255,cv2.FILLED)
# cv2.imshow('im',mask)
#
#
# cv2.waitKey(0)
# cv2.destroyAllWindows()