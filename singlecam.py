import numpy as np
import cv2
from collections import Counter
from time import time
import logging
import sys
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

    cap_1 = cv2.VideoCapture(CAM_INDEXES[0], cv2.CAP_V4L2)

    cap_1.set(cv2.CAP_PROP_FPS, fps_cam)
    cap_1.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_width)
    cap_1.set(cv2.CAP_PROP_FRAME_WIDTH, frame_height)

    video_output_1 = '{}/{}_cam1.avi'.format(ruta_carpeta, nombre_carpeta)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(ruta_carpeta+'/' +nombre_carpeta+'_'+r'log.txt')
    logger.addHandler(logging.StreamHandler(sys.stdout))
    logger.addHandler(fh)

    logger.info("ruta de la carpeta que guardara el archivo:")
    logger.info(ruta_carpeta)
    logger.info("cap_1 al inicio del programa: " + str(cap_1.get(cv2.CAP_PROP_FPS)))


    out1 = cv2.VideoWriter(video_output_1, cv2.VideoWriter_fourcc('M','J','P','G'),fps_vid,(frame_width,frame_height),True)

    cont = 0
    #depuracion de tasa de fallos por camara
    rets = dict()
    rets[CAM_INDEXES[0]] = list()

    t0 = time()
    while True:
        # Capture frame-by-frame
        ret1, frame1 = cap_1.read()
        rets[CAM_INDEXES[0]].append(ret1)


        if ret1==True:
            # Display the resulting frame
            cv2.namedWindow('Camera1',cv2.WINDOW_NORMAL)
            cv2.resizeWindow('Camera1', (screen_width,screen_height))
            if DISPLAY_CAMS:
                cv2.imshow('Camera1', frame1)
            out1.write(frame1)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if cv2.waitKey(1) & 0xFF == ord('a'):
            logger.info('foto!')
            cv2.imwrite('F1-'+str(cont)+'.jpg',frame1)
            cv2.imwrite('F2-'+str(cont)+'.jpg',frame2)
            cont = cont + 1
    t1 = time()

    logger.info("al terminar el programa: cap_1.CAP_PROP_FPS: {}".format(cap_1.get(cv2.CAP_PROP_FPS)))

    t_grabacion = t1-t0

    frames_totales = len(rets[CAM_INDEXES[0]])

    logger.info("frames capturados: " + str(frames_totales))
    logger.info("tiempo de grabacion (segundos): " + str(t_grabacion))
    logger.info("fps empirico:" + str(frames_totales/t_grabacion))
    logger.info("Cantidades finales de frames capturados por camara:")
    logger.info({k:Counter(R) for k,R in rets.items()})


    # When everything is done, release the capture
    cap_1.release()

    #close all the frames
    cv2.destroyAllWindows()


if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        main()