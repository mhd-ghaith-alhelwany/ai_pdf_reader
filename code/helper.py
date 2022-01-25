import cv2
import numpy as np

def change_background_color(path, bg, fg):
    img = cv2.imread(path)
    _, bgthresh = cv2.threshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 240, 255, cv2.THRESH_BINARY)
    _, fgthresh = cv2.threshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 50, 255, cv2.THRESH_BINARY_INV)
    img[bgthresh>0]=bg
    img[fgthresh>0]=fg
    cv2.imwrite(path, img)

def eye_comfort(file):
    img = cv2.imread(file)
    BLUT = np.interp(np.arange(0, 256), np.array([0, 128, 255]), np.array([0, 64, 192]))
    RLUT = np.interp(np.arange(0, 256), np.array([0, 128, 255]), np.array([0, 192, 255]))
    B, G, R = cv2.split(img)
    cv2.imwrite(file, cv2.merge([np.uint8(cv2.LUT(B, BLUT)), G, np.uint8(cv2.LUT(R, RLUT))]))