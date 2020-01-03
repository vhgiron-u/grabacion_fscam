import subprocess
from seleccionar_archivo import seleccionar_archivo
def get_length(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)

if __name__ == "__main__":
	ruta = seleccionar_archivo("Seleccionar archivo")
	ruta_sin_extension = ruta.split('.')[0]
	duracion = get_length(ruta)
	print("segundos totales: ",duracion)
	with open(ruta_sin_extension+"_duracion.txt","w") as f:
		f.write(str(duracion))