from itertools import islice
from concurrent import futures
size = 0
original = []


def encabezado(path):
    header = []
    head = ''
    j = 0
    origen = open(path, "r")
    recorte = islice(origen, 0, None)

    for linea in recorte:
        j += len(linea)
        linea = str(linea)
        texto = linea.replace("\n", "")
        texto = texto.replace("P6", "P3")
        lista = texto.splitlines()
        header += lista
        if ('255' in header) and (len(texto) == 3):
            origen.close()
            break

    for elemento in header:
        head += str(elemento) + "\n"
    lectura(j, path)
    return(bytearray(head, "utf-8"))


def lectura(j, path):
    global original
    archivo = open(path, "rb")
    archivo.seek(j)
    read = list(archivo)
    for elemento in read:
        for num in elemento:
            original.append((num))
    archivo.close()


def hilos(offset):

    control = 0
    out = ''
    global a, b, c, size

    for x in range(offset, offset+size):

        try:
            if (control == 0):
                control += 1
                rojo = int(original[x] * a)
                if rojo > 255:
                    rojo = 255

            elif (control == 1):
                control += 1
                verde = int(original[x] * b)
                if verde > 255:
                    verde = 255

            else:
                control += 1
                azul = int(original[x] * c)
                if azul > 255:
                    azul = 255

                if control == 3:
                    out += str(int(rojo))+" " + str(int(verde)) + " " + str(int(azul)) + "\n"
                    control = 0

        except IndexError:
            pass
    return(out)


def negro(offset):
    global a, size
    control = 0
    out = ''

    for x in range(offset, offset+size):

        try:
            if (control == 0):
                control += 1
                negro = int(original[x])

            elif (control == 1):
                control += 1
                negro += int(original[x])
            else:
                control += 1
                negro += int(original[x])
                negro = int((negro/3) * a)
                if negro > 255:
                    negro = 255

                out += str(int(negro))+" " + str(int(negro)) + " " + str(int(negro)) + "\n"
                if control == 3:
                    control = 0
        except IndexError:
            pass
    return(out)


def main(color, escala, path, argsize):

    global a, b, c, size
    funcion = hilos
    size = argsize
    x = encabezado(path)
    while size % 3 != 0:
        size += 1
    parseo = len(original)/size
    if isinstance(parseo, float):
        if int(parseo) < parseo:
            nuevo = int(parseo) + 1
        else:
            nuevo = int(parseo)
    if color == "W":
        funcion = negro
        a = escala
    if color == "B":
        a, b, c = (0, 0, escala)
    if color == "R":
        a, b, c = (escala, 0, 0)
    if color == "G":
        a, b, c = (0, escala, 0)
    hilo = futures.ThreadPoolExecutor(max_workers=nuevo)
    resultado_a_futuro = hilo.map(funcion, range(0, len(original), size))
    return(x, resultado_a_futuro)
