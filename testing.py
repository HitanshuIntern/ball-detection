import cv2
import threading
import numpy as np


# Camera Thread run camera simultaneously
class camThread(threading.Thread):
    def __init__(self, previewName, camID):
        threading.Thread.__init__(self)
        self.previewName = previewName
        self.camID = camID
    def run(self):
        print ("Starting " + self.previewName)
        camPreview(self.previewName, self.camID) #Calling Function camPreview which is head of this Script all Decision done here.

#Head of Script..
def camPreview(previewName, camID):
    net = cv2.dnn.readNetFromDarknet('yolov4_tiny.cfg', 'yolov4_tiny.weights') #Loading of weights and configuration file

    #Read Class Name from txt file
    classes = []
    with open("classes.txt", "r") as f:
        classes = f.read().splitlines()
        font = cv2.FONT_HERSHEY_PLAIN
        colors = np.random.uniform(0, 255, size=(100, 3))

    cv2.namedWindow(previewName)
    cap = cv2.VideoCapture(camID) #Capturing the Video from camera with Camera id start with 0-> WebCam 1....n -> Extrenal Cam
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))


    size = (frame_width, frame_height)

    result = cv2.VideoWriter('testing1.avi', 
                         cv2.VideoWriter_fourcc(*'MJPG'),
                         30, size) #Saving File just for testing purpose

    while True:
        _, img = cap.read()
        height, width, _ = img.shape

        blob = cv2.dnn.blobFromImage(img, 1/255, (416, 416), (0,0,0), swapRB=True, crop=False) #convert image to a blog object for fast calculations
        net.setInput(blob) #Feed Frame in Neural Network
        output_layers_names = net.getUnconnectedOutLayersNames() #output layer
        layerOutputs = net.forward(output_layers_names) #layer Names

        boxes = []
        confidences = []
        class_ids = []
        for output in layerOutputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id] #check Confidence
                if confidence > 0.2: #threshold of condition
                    center_x = int(detection[0]*width)
                    center_y = int(detection[1]*height)
                    w = int(detection[2]*width)
                    h = int(detection[3]*height)

                    x = int(center_x - w/2)
                    y = int(center_y - h/2)

                    boxes.append([x, y, w, h])
                    confidences.append((float(confidence)))
                    class_ids.append(class_id)
                    result.write(img) #stiching of Frames in future it will become streaming funtion here....... Note it's Important

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.2, 0.4)
        
        # Fancy stuff Box and Text overlay
        if len(indexes)>0:
            for i in indexes.flatten():
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                confidence = str(round(confidences[i],2))
                color = colors[i]
                cv2.rectangle(img, (x,y), (x+w, y+h), color, 2)
                cv2.putText(img, label + " " + confidence, (x, y+20), font, 2, (0,0,255), 2)

        cv2.imshow(previewName, img)
        key = cv2.waitKey(1)
        if key==27:
            break


    
    cv2.destroyWindow(previewName)
    result.release()

thread1 = camThread("Camera 1", 0) #webCam
thread2 = camThread("Camera 2", 1) #External Cam
thread1.start()
thread2.start()
