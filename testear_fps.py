
#python2 
import cv2
import time
import numpy as np

ix_cam = 2
cam_fps = 120

NUM_EXPS = 10 #number of experiments
FPS_PER_EXP = [] #list of measured fps

width =  480 #3840 #con 4K UHD de hecho cambia el fps
height = 360 #2160 

video = cv2.VideoCapture(ix_cam)
video.set(cv2.CAP_PROP_FPS, cam_fps)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, width)
video.set(cv2.CAP_PROP_FRAME_WIDTH, height)
video.release()

def main():
    print(ix_cam)
    print(cam_fps)
    # Start default camera
    video = cv2.VideoCapture(ix_cam)
    video.set(cv2.CAP_PROP_FPS, cam_fps)
    video.set(cv2.CAP_PROP_FRAME_HEIGHT, width)
    video.set(cv2.CAP_PROP_FRAME_WIDTH, height)     
    # Find OpenCV version
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
     
    # With webcam get(CV_CAP_PROP_FPS) does not work.
    # Let's see for ourselves.
     
    if int(major_ver)  < 3 :
        fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
        print ("Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps))
    else :
        fps = video.get(cv2.CAP_PROP_FPS)
        print ("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))
     
 
    # Number of frames to capture
    num_frames = 120
     
     
    print ("Capturing {0} frames".format(num_frames))
 
    # Start time
    start = time.time()
     
    # Grab a few frames
    #for i in xrange(0, num_frames) :
    for i in range(0, num_frames) :
        ret, frame = video.read()
        #   cv2.imshow('Cam ix:{}'.format(ix_cam), frame)
 
     
    # End time
    end = time.time()
 
    # Time elapsed
    seconds = end - start
    print( "Time taken : {0} seconds".format(seconds))
 
    # Calculate frames per second
    fps  = num_frames / seconds
    print( "Estimated frames per second : {0}".format(fps))
    FPS_PER_EXP.append(fps)
 
    # Release video
    video.release()
    


if __name__ == '__main__' :
    print("TOTAL EXPERIMENTS:",NUM_EXPS)
    for i in range(NUM_EXPS):
        print("exp:",i)
        main()
        print()
    print("\n\n")
    print("Average fps: {}, std: {}".format(np.mean(FPS_PER_EXP), np.std(FPS_PER_EXP)))
    