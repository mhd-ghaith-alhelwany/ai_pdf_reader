import cv2

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

def getLargestAreas(areas, count):
    return [areas.tolist().index(s.tolist()) for s in sorted(areas, key=lambda x: x[2] * x[3], reverse=True)[:count]] if len(areas) else None
def sortedCountours(contours):
    return sorted(contours, key = cv2.contourArea, reverse=True)

def getEyeLocation(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img_gray = cv2.equalizeHist(img_gray)
    img_gray = cv2.GaussianBlur(img_gray, (3, 3), 5)
    _, img_thres = cv2.threshold(img_gray, 20, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(img_thres, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) < 2:
        return None
    contours = sortedCountours(contours)
    M = cv2.moments(contours[1])
    return None if M["m00"] == 0 else int(M["m01"] / M["m00"])

def getEyesLocation(img, winname='frame'):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    if len(faces):
        (x, y, w, h) = faces[getLargestAreas(faces, 1)[0]]
        face_frame = img[y:y+w, x:x+h]

        right_eye_frame = img[y+int(w/4):y+int(w/2), x+int(5*h/8):x+int(7*h/8)]
        right_eye_cY = getEyeLocation(right_eye_frame)
        if right_eye_cY:
            right_eye_cY_on_frame = right_eye_cY + int(w/4)
            face_frame = cv2.line(face_frame, (0, right_eye_cY_on_frame), (face_frame.shape[1], right_eye_cY_on_frame), (0, 255, 0))
            return right_eye_cY / right_eye_frame.shape[0] - 0.5
    return 0

def atLeastOneEyeOpen(img):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    if not len(faces):
        return False
    (x, y, w, h) = faces[getLargestAreas(faces, 1)[0]]
    gray = gray[y:y+w, x:x+h]
    eyes = eye_cascade.detectMultiScale(gray, 1.1, 4)
    return len(eyes) == 0

