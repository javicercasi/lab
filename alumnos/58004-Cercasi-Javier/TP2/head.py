from itertools import islice


def encabezado(file, output, offset, interleave, largo, cota):
    header = []
    j = 0

    destino = open(output, 'w')
    archivo_origen = open(file, "r")
    recorte = islice(archivo_origen, 0, None)

    # Creo un iterador dado por islice, que me toma los elementos del archivo
    # desde la fila 0 hasta que se encuentre con el numero 255.

    for linea in recorte:
        j += len(linea)
        texto = linea.replace("\n", "")
        lista = texto.splitlines()
        header += lista
        if ('255' in header) and (len(texto) == 3):
            archivo_origen.close()
            break

    header.insert(1, "#UMCOMPU2 {} {} {}".format(offset-1, interleave, largo))
    limite = header[-2].split(" ")

    try:
        if (int(limite[0]) * int(limite[1]))*3 < cota:
            raise ValueError
    except ValueError:
        print("El mensaje seleccionado no es valido para el offset e interleave seleccionado.\n")
        exit()

    for elemento in header:
        destino.write(str(elemento)+"\n")
    destino.close()

    return(j)
