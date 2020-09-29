import argparse
import multiprocessing as mp
from itertools import islice
import sys
import matplotlib.pyplot as plt


def padre(args, hijo_rojo, hijo_verde, hijo_azul):
    j = 0
    fin = True
    header = []
    path = __file__.replace(sys.argv[0], "")

    try:
        archivo = open(path + args.file, 'r')
    except IOError:
        print("\nSu nombre de archivo es incorrecto\n")
        exit()

    recorte = islice(archivo, 0, None)

    # Creo un iterador dado por islice, que me toma los elementos del archivo
    # desde la fila 0 hasta que se encuentre con el numero 255.

    for linea in recorte:
        j += len(linea)
        texto = linea.replace("\n", "")
        texto = texto.replace("P6", "P3")
        lista = texto.splitlines()
        header += lista
        if ('255' in header) and (len(texto) == 3):
            cola_r.put(header)
            cola_v.put(header)
            cola_a.put(header)
            archivo.close()
            break

    # Abro el archivo y muevo el puntero despues del encabezado
    archivo = open(path + args.file, 'r')
    archivo.seek(j)

    # Leo el archivo ppm por bloques de n bytes, luego envio ese bloque
    # ya convertido en lista, a cada hijo para que pueda empezar a ejercutar.
    # Una vez finalizado el envio de la lista, el bucle while vuelve a empezar
    # y mueve el puntero hasta el ultimo byte anterior leido.

    while fin is True:

        archivo.seek(archivo.tell())
        texto = archivo.read(args.size)
        pixels = []

        for linea in texto:
            pixels.append(ord(linea))
            if (len(texto) != args.size):
                fin = False

        cola_r.put(pixels)
        cola_v.put(pixels)
        cola_a.put(pixels)

    hijo_rojo.start()
    hijo_verde.start()
    hijo_azul.start()

    hijo_rojo.join()
    hijo_verde.join()
    hijo_azul.join()

    print("\nSe generaron correctamente los 3 filtos\n")


def separador(q, primer, segundo, tercero, nombre):
    control = 0
    histograma = []

    path = __file__.replace(sys.argv[0], "")

    fichero = open(path + nombre, 'w')

    # Escribo en el archivo primero el encabezado
    encabezado = q.get()
    for i in range(len(encabezado)):
        fichero.write(str(encabezado[i])+"\n")

    # Escribo los elementos desde el primer pixel, ya sin el encabezado
    while True:

        # Utilizo una variable de control inicializada en 0, que se
        # aumentara en 1 cuando recorra cada valor del pixel y luego
        # se reiniciara otra vez en 0 al llegar al tercer valor del pixel.

        leido = q.get()

        for x in range(len(leido)):

            if (control == 0):
                control += 1
                rojo = int(leido[x] * primer)
                if rojo > 255:
                    rojo = 255
                if rojo != 0:
                    histograma.append(rojo)

                fichero.write(str(rojo) + ' ')

            elif (control == 1):
                control += 1
                verde = int(leido[x] * segundo)
                if verde > 255:
                    verde = 255
                if verde != 0:
                    histograma.append(verde)
                fichero.write(str(verde) + ' ')
            else:
                control += 1
                azul = int(leido[x] * tercero)
                if azul > 255:
                    azul = 255
                if azul != 0:
                    histograma.append(azul)
                fichero.write(str(azul) + ' ')

                if control == 3:
                    fichero.write("\n")
                    control = 0
        if q.empty():
            fichero.close()
            break

    plt.hist(histograma, rwidth=0.9, bins=50)
    plt.xlabel('Valor de pixel')
    plt.ylabel('Frecuencia')
    plt.title('Histograma de valores de: ' + nombre)
    plt.show()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(usage="\ntp1.py [-h] [-r RED] [-g GREEN] [-b BLUE] -s SIZE -f FILE")
    parser.add_argument('-r', '--red', metavar='RED', type=float,
                        help="Escala para rojo", default=1)
    parser.add_argument('-g', '--green', metavar='GREEN', type=float,
                        default=1, help="Escala para verde")
    parser.add_argument('-b', '--blue', metavar='BLUE', type=float,
                        default=1, help="Escala para azul")
    parser.add_argument('-s', '--size', metavar='SIZE', type=int,
                        default=1024, help="Bloque de lectura")
    parser.add_argument('-f', '--file', metavar='FILE', type=str,
                        help="archivo a procesar")
    args = parser.parse_args()
    # args.size += 10

    try:
        if not args.file:
            raise NameError
        if (args.file).split(".")[1] != 'ppm':
            raise NameError
    except NameError:
        print("\nDebe ingresar el nombre de la imagen.ppm\n")
        exit()

    try:
        if (args.red < 0) or (args.green < 0) or (args.blue < 0) or (args.size < 0):
            raise ValueError
    except ValueError:
        print("\nDebe ingresar multiplos de positivos\n")
        exit()

    # Defino 3 colas por separado, y defino la funcion y argumentos a ejecutar
    # por cada proceso hijo

    cola_r = mp.Queue()
    cola_v = mp.Queue()
    cola_a = mp.Queue()

    hijo_verde = mp.Process(target=separador, args=(cola_v, 0, args.green, 0, 'g_'+args.file,))
    hijo_rojo = mp.Process(target=separador, args=(cola_r, args.red, 0, 0, 'r_'+args.file,))
    hijo_azul = mp.Process(target=separador, args=(cola_a, 0, 0, args.blue, 'b_'+args.file,))

    padre(args, hijo_rojo, hijo_verde, hijo_azul)
