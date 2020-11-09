import threading
import cv2
import os
import time
import numpy as np
from ProducerConsumer import ProducerConsumer
from threading import Thread

#file
fileName = 'clip.mp4'


inputQueue = ProducerConsumer() #Queue for images
outputQueue = ProducerConsumer() #Queue for gray scale images

#Extract frames and convert to images and saves it to the queue
def extractFrames(fileName, inputQueue):
    count = 0
    # open the video clip
    vidcap = cv2.VideoCapture(fileName)

    # read one frame
    success,image = vidcap.read()
    print(f'Reading frame {count} {success}')

    #adding images to the queue
    while success :
        success, jpgImage = cv2.imencode('.jpg', image)
        inputQueue.putFrame(jpgImage)
        success,image = vidcap.read()
        print(f'Reading frame {count}')
        count += 1
    print("Extraction Complete")
    inputQueue.putFrame(None) #add a None at the end of the queue

#Convert images from one queue into gray and saves it to the new queue
def convertToGray(inputQueue, outputQueue):
    count = 0

    #Gets 1st image of the queue
    inputFrames = inputQueue.getFrame()

    #Takes images from original queue then converrt it into gray then it save it into the new queue
    while inputFrames is not None :
        print(f'Converting frame {count}')
        inputFrames = np.asarray(bytearray(inputFrames), dtype = np.uint8)
        image = cv2.imdecode(inputFrames, cv2.IMREAD_UNCHANGED)

        # convert the image to grayscale
        grayscaleFrame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        success, jpgImage = cv2.imencode('.jpg', grayscaleFrame)
        #add image to the new queue
        outputQueue.putFrame(jpgImage)
        count += 1
        #it grabes another frame from old queue
        inputFrames = inputQueue.getFrame()
    outputQueue.putFrame(None) #add a None at the end of the queue

#Display image of the grayscale queue
def displayFrames(outputQueue):
    count = 0
    #Gets 1st image of the queue
    frame = outputQueue.getFrame()

    #display image
    while frame is not None:
        print(f'Displaying frame {count}')

        #display image
        frame = np.asarray(bytearray(frame), dtype = np.uint8)
        image = cv2.imdecode(frame, cv2.IMREAD_UNCHANGED)
        cv2.imshow('Video', image)

        if cv2.waitKey(42) and 0xFF == ord("q"):
            break

        count += 1
        #it grabes another frame from queue
        frame = outputQueue.getFrame()

    print('Finished displaying all frames')
    # cleanup the windows
    cv2.destroyAllWindows()

#Create Threads
extractThread = Thread(target = extractFrames, args = (fileName, inputQueue ))
greyFramesThread = Thread(target = convertToGray, args = (inputQueue , outputQueue))
displayThread = Thread(target = displayFrames, args = (outputQueue,))

#start Threads
extractThread.start()
greyFramesThread .start()
displayThread.start()
