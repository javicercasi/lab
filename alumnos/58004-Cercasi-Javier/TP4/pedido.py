import argparse
import os


def argumentos():

    parser = argparse.ArgumentParser(usage="\ntp4.py [-h] -d DIR -p PUERTO -s SIZE")

    parser.add_argument('-s', '--size', metavar='SIZE', type=int, default=10000,
                        help="Bloque de lectura maxima para los documentos")

    parser.add_argument('-p', '--port', metavar='PORT', type=int,
                        help="Puerto en donde espera conexiones nuevas",
                        default=5000)

    parser.add_argument('-d', '--documentroot', metavar='DIR', type=str,
                        help="Directorio donde estan los documentos web")

    args = parser.parse_args()

    try:
        if not args.port:
            raise NameError
        if args.port < 1024 or args.port > 65535:
            raise NameError
    except NameError:
        print("\nDebe ingresar un puerto valido.\n")
        exit()

    try:
        if not args.documentroot or os.path.isdir(args.documentroot) is False:
            raise NameError
    except NameError:
        print("\nDebe ingresar un directorio valido.\n")
        exit()

    try:
        if (args.size < 10000):
            raise ValueError
    except ValueError:
        print("\nDebe ingresar un size mayor a 10kB.\n")
        exit()
    return(args)
