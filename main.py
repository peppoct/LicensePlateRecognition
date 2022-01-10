# Importing all necessary libraries
import csv
import cv2
import imutils
import numpy as np
import pytesseract
import pandas
import os
import tkinter as tk
#################
#from picamera.array import PiRGBArray
#from picamera import PiCamera
#################
from PIL import Image


def get_picture_from_camera():
    camera = "" #PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 30
    rawCapture = "" #PiRGBArray(camera, size=(640, 480))
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array
        cv2.imshow("Frame", image)
        key = cv2.waitKey(1) & 0xFF
        rawCapture.truncate(0)
        if key == ord("s"):
            #take image. image is the last frame before the key "s" is pressed
            try:

                # creating a folder named data
                if not os.path.exists('capture'):
                    os.makedirs('capture')

            # if not created then raise error
            except OSError:
                print('Error: Creating directory of data')

            name = './capture/frame.jpg'
            cv2.imwrite(name, image)
            break
        
    camera.close()       
    cv2.destroyAllWindows()
            

def frame_from_video(path, rate):
    cam = cv2.VideoCapture(path)

    try:

        # creating a folder named data
        if not os.path.exists('data'):
            os.makedirs('data')

    # if not created then raise error
    except OSError:
        print('Error: Creating directory of data')

    # frame
    currentframe = 0

    while (True):

        # reading from frame
        ret, frame = cam.read()

        if ret:
            # if video is still left continue creating images
            name = './data/frame' + str(int(currentframe/rate)) + '.jpg'
            # writing the extracted images
            if(currentframe%rate == 0):
                cv2.imwrite(name, frame)
                print('Creating...' + name)
            # increasing counter so that it will
            # show how many frames are created
            currentframe += 1
        else:
            break

    # Release all space and windows once done
    cam.release()
    cv2.destroyAllWindows()
    return int(currentframe/rate)


def detect_plate(photo_path, show):
    
    img = cv2.imread(photo_path, cv2.IMREAD_COLOR)
    img = cv2.resize(img, (620, 480))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # convert to grey scale
    gray = cv2.bilateralFilter(gray, 11, 17, 17)  # Blur to reduce noise
    edged = cv2.Canny(gray, 30, 200)  # Perform Edge detection

    # find contours in the edged image, keep only the largest
    # ones, and initialize our screen contour
    cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]
    screenCnt = None

    # loop over our contours
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)

        # if our approximated contour has four points, then
        # we can assume that we have found our screen
        if len(approx) == 4:
            screenCnt = approx
            break

    if screenCnt is None:
        detected = 0
        print
        "No contour detected"
        return "", 0
    else:
        detected = 1

    if detected == 1:
        cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)

    # Masking the part other than the number plate
    mask = np.zeros(gray.shape, np.uint8)
    new_image = cv2.drawContours(mask, [screenCnt], 0, 255, -1, )
    new_image = cv2.bitwise_and(img, img, mask=mask)

    # Now crop
    (x, y) = np.where(mask == 255)
    (topx, topy) = (np.min(x), np.min(y))
    (bottomx, bottomy) = (np.max(x), np.max(y))
    Cropped = gray[topx:bottomx + 1, topy:bottomy + 1]

    # Read the number plate
    #### this part is for windows only
    pytesseract.pytesseract.tesseract_cmd = r'C:\Users\andre\Desktop\songs\tesseract\tesseract.exe'

    text = pytesseract.image_to_data(Cropped, output_type='data.frame', config='--psm 6')
    text = text[text.conf != -1]
    text.head()

    textResult = ""
    count = 1
    confResult = 0
    if(text.size > 0):
        for textPart in (text.text[:].values):
            textResult = textResult + str(textPart)
        count = 0
        for confPart in (text.conf[:].values):
            count = count +1
            confResult = confResult + confPart
    if show == 1:
        cv2.imshow('image', img)
        cv2.imshow('Cropped', Cropped)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    if(text[:]['text'].values.size == 0):
        return "", 0
    return textResult, confResult/count


def detect_plate_video(video_path, rate):
    lastFrame = 0
    lastFrame = frame_from_video(video_path,rate)
    count = 0
    array = []
    for i in range(lastFrame):
        name = "data/frame" + str(i) + ".jpg"  ## remove .0
        text, conf = detect_plate(name,0)
        if(conf > 0):
            text = ''.join([c for c in str(text) if c.isupper() or c.isdigit()])
            if (not str(text).isnumeric() and  len(str(text)) > 6 and len(str(text)) < 9):
                array.append([text, conf, count])

        count = count+1

    conf = 0
    best = ""
    picture = 0
    for arrayValue in array:
        if(conf < arrayValue[1]):
            best = arrayValue[0]
            conf = arrayValue[1]
            picture = arrayValue[2]
    print(conf, ": ", best,":", picture)
    detect_plate("data/frame" + str(picture) + ".jpg",1)
    return best, conf
            
