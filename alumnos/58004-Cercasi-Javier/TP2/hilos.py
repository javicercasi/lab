import threading
import array
import time
from pedido import pedido
from head import encabezado
from lectura import mensaje

barrera = threading.Barrier(3)
barrera2 = threading.Barrier(3)
original = []


def lectura_ascii(size):
    global original
    original = []
    while size % 3 != 0:
        size += 1

    for elemento in archivo.read(size):
        original.append(elemento)
    return(original)


def hilo_rojo(output, interleave, oculto, primer_bloque, size):

    a = 0
    b = 0
    c = size
    destino = open(output, 'ab')
    fin = True
    offset = 0
    cota_superior = offset + interleave * len(oculto) * 3
    paso = interleave * 3 * 3
    global original

    if c < (cota_superior - offset):
        c = cota_superior - offset

    while fin is True:

        if b == 1:
            for i in range(offset, cota_superior, paso):
                binario = format(original[i], "#b")
                if binario[-1] != oculto[a]:
                    binario = binario[:-1] + oculto[a]
                    original[i] = int(binario, 2)
                a += 3
        b += 1
        barrera2.wait()

        image = array.array('B', original)
        image.tofile(destino)
        lectura_ascii(c)

        barrera.wait()
        if len(original) != c:
            fin = False

    destino.close()


def hilo_verde(interleave, oculto, size):

    b = 0
    c = size
    offset = 4 * interleave
    if interleave != 1:
        offset = offset - (interleave - 1)

    fin = True

    cota_superior = offset + interleave * len(oculto) * 3
    paso = interleave * 3 * 3
    global original

    if c < (cota_superior - offset):
        c = cota_superior - offset

    if len(oculto) % 3 == 1:
        cota_superior = cota_superior - paso
    a = 1

    while fin is True:
        if b == 1:
            for i in range(offset, cota_superior, paso):
                binario = format(original[i], "#b")
                if binario[-1] != oculto[a]:
                    binario = binario[:-1] + oculto[a]
                    original[i] = int(binario, 2)
                a += 3
        barrera2.wait()
        b += 1
        barrera.wait()
        if len(original) != c:
            fin = False


def hilo_azul(interleave, oculto, size):

    b = 0
    c = size
    a = 2
    offset = 8 * interleave

    if interleave != 1:
        offset -= interleave

    fin = True
    cota_superior = offset + interleave * len(oculto) * 3
    paso = interleave * 3 * 3

    if c < (cota_superior - offset):
        c = cota_superior - offset

    global original

    if (len(oculto) % 3 == 2) or (len(oculto) % 3 == 1):
        cota_superior = cota_superior - paso

    while fin is True:
        if b == 1:
            for i in range(offset, cota_superior, paso):

                binario = format(original[i], "#b")
                if binario[-1] != oculto[a]:
                    binario = binario[:-1] + oculto[a]
                    original[i] = int(binario, 2)
                a += 3
        b += 1
        barrera2.wait()
        barrera.wait()
        if len(original) != c:
            fin = False


if __name__ == '__main__':

    comienzo = time.time()
    args = pedido()

    try:
        mensaje_oculto = open(args.message, "r")
        saludo = mensaje_oculto.read()
        oculto = mensaje(saludo)
        mensaje_oculto.close()
    except IOError:
        print("\nSu nombre de archivo archivo.txt es incorrecto\n")
        exit()

    try:
        archivo = open(args.file, "rb")
    except IOError:
        print("\nSu nombre de origen imagen.ppm es incorrecto\n")
        exit()

    cota_superior = args.offset + args.interleave * len(oculto) * 3
    seek = encabezado(args.file, args.output, args.offset, args.interleave,
                      len(saludo), cota_superior)
    archivo.seek(seek)

    x = threading.Thread(target=hilo_rojo, args=(args.output, args.interleave,
                         oculto, lectura_ascii((int(args.offset) - 1) * 3),
                         args.size,))
    y = threading.Thread(target=hilo_verde, args=(args.interleave, oculto, args.size,))
    z = threading.Thread(target=hilo_azul, args=(args.interleave, oculto, args.size,))
    x.start()
    y.start()
    z.start()
    x.join()
    y.join()
    z.join()
    print("\nTiempo de ejecucion: {} seg.\n".format(time.time() - comienzo))
