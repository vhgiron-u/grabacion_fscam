"""
Funciones para determinar el numero de frames de un archivo
"""



import cv2
import sys
from collections import Counter

def leer_intensivo(cap):
	"""adaptacion de https://stackoverflow.com/a/19082750"""
	contador_flags = Counter()
	contador_frames = 0
	pos_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
	while True:
		try:
			flag, frame = cap.read()
			if flag:
				# The frame is ready and already captured
				#cv2.imshow('video', frame)
				pos_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
				#print(str(pos_frame)+" frames")
				contador_frames += 1
				contador_flags[flag] += 1
			else:
				# The next frame is not ready, so we try to read it again if it hasnt finished yet
				if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
					# If the number of captured frames is equal to the total number of frames,
					# we stop
					break
				else:
					cap.set(cv2.CAP_PROP_POS_FRAMES, pos_frame-1)
					print( "frame is not ready")
					# It is better to wait for a while for the next frame to be ready
					cv2.waitKey(10)
				pass #:deb:
			if cv2.waitKey(10) == 27:
				break
		except:
			print("total frames:", contador_frames)
			print("flags:", contador_flags)
			raise
	return contador_flags, contador_frames

def contar_frames(ruta = None, intensive=False):
	if not ruta:
		import seleccionar_archivo
		ruta = seleccionar_archivo.seleccionar_archivo("Seleccionar archivo")
	cap = cv2.VideoCapture(ruta)

	if intensive: #contamos uno por uno leyendo el archivo
		print()
		print("Se contara el total de frames leyendo uno por uno, esto tomara algo de tiempo")
		contador_flags, length = leer_intensivo(cap)
		print("total frames:", length)
		print("flags:", contador_flags)
		cap.release()
		#return length
	else:
		length = cap.get(cv2.CAP_PROP_FRAME_COUNT)
		print("total frames:", length )
		#return length
	ruta_sin_extension = ruta.split('.')[0]
	with open(ruta_sin_extension+"_totframes.txt","w") as f:
		f.write(str(length))
	return length


if __name__ == "__main__":

	if len(sys.argv)==1:
		tot_frames = contar_frames()
	elif len(sys.argv)==2:
		tot_frames = contar_frames(sys.argv[1])
	elif len(sys.argv)==3:
		tot_frames = contar_frames(sys.argv[1], bool('' if not sys.argv[2].strip().lower().startswith('intens') else 'True'))
	else:
		raise ValueError("Solo se debe ingresar un maximo de dos argumentos")


	
	#main()