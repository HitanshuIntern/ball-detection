'''import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cap1 = cv2.VideoCapture(1)

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))


size = (frame_width, frame_height)

out = cv2.VideoWriter('test3.mp4', 
                         cv2.VideoWriter_fourcc(*'XVID'),
                         15, size)
while(cap.isOpened()):

    ret, frame = cap.read()
    ret1, frame1 = cap1.read()
    if ret == True: 

        both = np.concatenate((frame, frame1), axis=1)


        cv2.imshow('Frame', both)
        out.write(both)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    else: 
        break

cap.release()
out.release()


cv2.waitKey(0)
cv2.destroyAllWindows()'''


import cv2
import threading

class camThread(threading.Thread):
    def __init__(self, previewName, camID):
        threading.Thread.__init__(self)
        self.previewName = previewName
        self.camID = camID
    def run(self):
        print ("Starting " + self.previewName)
        camPreview(self.previewName, self.camID)

def camPreview(previewName, camID):
    cv2.namedWindow(previewName)
    cam = cv2.VideoCapture(camID)
    if cam.isOpened():  # try to get the first frame
        rval, frame = cam.read()
    else:
        rval = False

    while rval:
        cv2.imshow(previewName, frame)
        rval, frame = cam.read()
        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break
    cv2.destroyWindow(previewName)

# Create two threads as follows
thread1 = camThread("Camera 1", 0)
thread2 = camThread("Camera 2", 1)
thread1.start()
thread2.start()