import numpy as np
import cv2
from collections import Counter
from time import time
import logging
import sys
import datetime
from seleccionar_archivo import seleccionar_carpeta

#Constantes y valores a setear

CONFIGS = {
    "VGA":{
        "frame_width": 640,
        "frame_height": 480,
        "fps_cam": 120,
    },
    "1080P":{
        "frame_width": 1920,
        "frame_height": 1080,
        "fps_cam": 60,
    }
}

DISPLAY_CAMS = True

CAM_INDEXES = [1]

EXPERIMENT_TIME = 30.0#60.0*15 #-1


def main(ruta=None, conf_name = "VGA"):
    if conf_name not in CONFIGS:
        raise ValueError("Nombre de configuracion '{}' no reconocido".format(conf_name))

    if ruta is None:
        ruta_carpeta = seleccionar_carpeta("Seleccionar carpeta")
    else:
        ruta_carpeta = ruta
    nombre_carpeta = ruta_carpeta.split('/')[-1]

    current_config_name = conf_name
    current_config_options = CONFIGS[current_config_name]

    frame_width = current_config_options["frame_width"]
    frame_height = current_config_options["frame_height"]

    #para mostrar en pantalla lo que se esta grabando
    screen_width = frame_width
    screen_height = frame_height

    fps_cam = current_config_options['fps_cam']
    fps_vid = fps_cam


    caps = dict()
    video_outputs = dict()
    for i_,ix in enumerate(CAM_INDEXES):
        vcap = cv2.VideoCapture(CAM_INDEXES[i_], cv2.CAP_V4L2) #:specific_cam:
        vcap.set(cv2.CAP_PROP_FPS, fps_cam) #:specific_cam:
        vcap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_width) #:specific_cam:
        vcap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_height) #:specific_cam:
        caps[ix] = vcap
        video_outputs[ix] = '{}/{}_cam{}.avi'.format(ruta_carpeta, nombre_carpeta,ix) #:specific_cam:
    

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(ruta_carpeta+'/' +nombre_carpeta+'_'+r'log.txt')
    logger.addHandler(logging.StreamHandler(sys.stdout))
    logger.addHandler(fh)

    logger.info("ruta de la carpeta que guardara el archivo:")
    logger.info(ruta_carpeta)
    ahora = datetime.datetime.now()
    logger.info(    "inicio del experimento:       {}"\
                            .format(ahora.strftime("%H:%M:%S, %m/%d/%Y")))
    if EXPERIMENT_TIME > 0:
        logger.info("duracion de grabacion limite: {}s".format(EXPERIMENT_TIME))
        tfin = ahora+datetime.timedelta(seconds=EXPERIMENT_TIME)
        logger.info("fin estimado del experimento: {}"\
                            .format(tfin.strftime("%H:%M:%S, %m/%d/%Y")))
    for ix in CAM_INDEXES:
        logger.info("cap_{} al inicio del programa: ".format(ix) + str(caps[ix].get(cv2.CAP_PROP_FPS))) #:specific_cam:

    outs = dict()
    for ix in CAM_INDEXES:
        outs[ix] = cv2.VideoWriter(video_outputs[ix], cv2.VideoWriter_fourcc('M','J','P','G'),fps_vid,(frame_width,frame_height),True)  #:specific_cam:

    cont = 0
    #depuracion de tasa de fallos por camara
    rets = dict()
    frames = [None]*len(CAM_INDEXES) #frames es una lista indexada en 0
    cam_names = {ix:"Camera{}".format(ix) for ix in CAM_INDEXES}
    for ix in CAM_INDEXES:
        rets[ix] = list() #:specific_cam:
    started = False
    
    while True:
        # Capture frame-by-frame
        for i_, ix in enumerate(CAM_INDEXES):
            ret, frame = caps[ix].read() #:specific_cam:
            rets[ix].append(ret) #:specific_cam:
            frames[i_] = frame

        for i_, ix in enumerate(CAM_INDEXES):
            ret, frame = rets[ix][-1], frames[i_]
            cam_name = cam_names[ix]
            if ret==True: #:specific_cam:
                # Display the resulting frame
                if not started: #iniciamos registro de tiempo desde que devolvemos un frame correcto
                    started = True
                    t0 = time()

                cv2.namedWindow(cam_name,cv2.WINDOW_NORMAL) #:specific_cam:
                cv2.resizeWindow(cam_name, (screen_width,screen_height)) #:specific_cam:
                if DISPLAY_CAMS: #:specific_cam:
                    cv2.imshow(cam_name, frame) #:specific_cam:
                outs[ix].write(frame) #:specific_cam:


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if cv2.waitKey(1) & 0xFF == ord('a'):
            logger.info('foto!')
            for i_, ix in enumerate(CAM_INDEXES):
                cv2.imwrite('F{}-'.format(ix)+str(cont)+'.jpg',frames[i_]) #:specific_cam:
                cont = cont + 1
        if time() - t0 >= EXPERIMENT_TIME:
            break
    t1 = time()
    for ix in CAM_INDEXES:
        
        cap = caps[ix]
        logger.info("al terminar el programa: caps[{}].CAP_PROP_FPS: {}".format(ix,cap.get(cv2.CAP_PROP_FPS)))

    t_grabacion = t1-t0

    frames_totales = len(rets[CAM_INDEXES[0]]) #:specific_cam:

    logger.info("frames capturados: " + str(frames_totales)) #:specific_cam:
    logger.info("tiempo de grabacion (segundos): " + str(t_grabacion))
    logger.info("fps empirico:" + str(frames_totales/t_grabacion)) #:specific_cam:
    logger.info("Cantidades finales de frames capturados por camara:")
    logger.info({k:Counter(R) for k,R in rets.items()})


    # When everything is done, release the capture
    for ix in CAM_INDEXES:
        caps[ix].release() #:specific_cam:

    #close all the frames
    cv2.destroyAllWindows()


if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        main()