import argparse


def pedido():

    parser = argparse.ArgumentParser(usage="\ntp2.py [-h] -s SIZE -f FILE -m FILE -f PIXELS -i PIXELS -o FILE2")

    parser.add_argument('-s', '--size', metavar='SIZE', type=int,
                        default=1024, help="Bloque de lectura")

    parser.add_argument('-f', '--file', metavar='FILE', type=str,
                        help="Archivo portador")

    parser.add_argument('-m', '--message', metavar='FILE', type=str,
                        help="Mensaje esteganografico")

    parser.add_argument('-ff', '--offset', metavar='PIXS', type=int,
                        help="Offset en pixels del inicio del raster", default=1)

    parser.add_argument('-i', '--interleave', metavar='PIXS', type=int,
                        help="Interleave de modificacion de pixel", default=1)

    parser.add_argument('-o', '--output', metavar='FILE', type=str,
                        help="Estego mensaje")

    args = parser.parse_args()

    try:
        if not args.file or not args.output:
            raise NameError
        if ((args.file).split(".")[1] != 'ppm') or ((args.output).split(".")[1] != 'ppm'):
            raise NameError
    except NameError:
        print("\nEl archivo de origen y destino deben ser una imagen.ppm\n")
        exit()

    try:
        if not args.message:
            raise NameError
        if (args.message).split(".")[1] != 'txt':
            raise NameError
    except NameError:
        print("\nEl archivo del Mensaje esteganografico debe ser un archivo.txt\n")
        exit()

    try:
        if (args.size < 1):
            raise ValueError
    except ValueError:
        print("\nDebe ingresar un size mayor a 0.\n")
        exit()

    try:
        if (args.offset < 1) or (args.interleave < 1):
            raise ValueError
    except ValueError:
        print("\nDebe ingresar un Offset y un Interleave mayor a 0.\n")
        exit()

    return(args)
