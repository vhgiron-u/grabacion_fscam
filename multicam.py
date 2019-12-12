import numpy as np
import cv2


frame_width = 640
frame_height = 480


#para mostrar en pantalla lo que se esta grabando
screen_width = 1920
#screen_width = frame_width
screen_height = 1080
#screen_height = frame_height


fps_cam = 120
fps_vid = 60

#cap_1 = cv2.VideoCapture(0)
#cap_2 = cv2.VideoCapture(1)
cap_1 = cv2.VideoCapture(1)
cap_2 = cv2.VideoCapture(2)
cap_3 = cv2.VideoCapture(3)

cap_1.set(cv2.CAP_PROP_FPS, fps_cam)
cap_2.set(cv2.CAP_PROP_FPS, fps_cam)
cap_3.set(cv2.CAP_PROP_FPS, fps_cam)

cap_1.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_width)
cap_1.set(cv2.CAP_PROP_FRAME_WIDTH, frame_height)
cap_2.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_width)
cap_2.set(cv2.CAP_PROP_FRAME_WIDTH, frame_height)
cap_3.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_width)
cap_3.set(cv2.CAP_PROP_FRAME_WIDTH, frame_height)

video_output_1 = 'cam1.avi'
video_output_2 = 'cam2.avi'
video_output_3 = 'cam3.avi'

ret1, frame1 = cap_1.read()
ret2, frame2 = cap_2.read()
ret3, frame3 = cap_3.read()



out1 = cv2.VideoWriter(video_output_1, cv2.VideoWriter_fourcc('M','J','P','G'),fps_vid,(frame_width,frame_height),True)

out2 = cv2.VideoWriter(video_output_2, cv2.VideoWriter_fourcc('M','J','P','G'),fps_vid,(frame_width,frame_height),True)

out3 = cv2.VideoWriter(video_output_3, cv2.VideoWriter_fourcc('M','J','P','G'),fps_vid,(frame_width,frame_height),True)

cont = 0

while True:
    # Capture frame-by-frame
    ret1, frame1 = cap_1.read()
    ret2, frame2 = cap_2.read()
    ret3, frame3 = cap_3.read()

    if ret1==True:
        # Display the resulting frame
        cv2.namedWindow('Camera1',cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Camera1', (screen_width,screen_height))
        cv2.imshow('Camera1', frame1)
        out1.write(frame1)

    if ret2==True:
        # Display the resulting frame
        cv2.namedWindow('Camera2',cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Camera2', (screen_width,screen_height))
        cv2.imshow('Camera2', frame2)
        out2.write(frame2)

    if ret3==True:
        # Display the resulting frame
        cv2.namedWindow('Camera3',cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Camera3', (screen_width,screen_height))
        cv2.imshow('Camera3', frame3)
        out3.write(frame3)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if cv2.waitKey(1) & 0xFF == ord('a'):
        print('foto!')
        cv2.imwrite('F1-'+str(cont)+'.jpg',frame1)
        cv2.imwrite('F2-'+str(cont)+'.jpg',frame2)
        #cv2.imwrite('F1.jpg',frame1)
        #cv2.imwrite('F2.jpg',frame2)
        cont = cont + 1


# When everything is done, release the capture
cap_1.release()
cap_2.release()

#close all the frames
cv2.destroyAllWindows()
