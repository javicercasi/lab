import time
import os
import asyncio
from pedido import argumentos
args = argumentos()


async def registro(addr):
    print("Direccion: "+str(addr)+" Fecha de acceso: " + time.strftime("%d/%m/%y")+", "+time.strftime("%H:%M:%S"))
    destino.write("Direccion: "+str(addr)+" Fecha de acceso: "+time.strftime("%d/%m/%y")+", "+time.strftime("%H:%M:%S")+"\n")
    destino.flush()     # vacia el búfer interno del archivo.


async def handle_echo(reader, writer):

    dic = {"txt": " text/plain", "jpg": " image/jpeg", "ppm": " image/x-portable-pixmap", "html": " text/html", "pdf": " application/pdf", "ico": "image/x-icon"}
    data = await reader.read(100)
    encabezado = data.decode().splitlines()[0]  # GET /imagen.jpg
    archivo = args.documentroot + encabezado.split()[1].split("?")[0]
    addr = writer.get_extra_info('peername')

    if encabezado.split()[1].split("?")[0] != "/favicon.ico":
        await registro(addr)

    if archivo == (args.documentroot + "/"):
        archivo = args.documentroot + '/index.html'

    if os.path.isfile(archivo) is False:
        archivo = args.documentroot + '/400error.html'
        codigo = "HTTP/1.1 400 File Not Found"
        extension = "html"

    elif len(encabezado.split()[1].split("?")) != 1:
        archivo = args.documentroot + '/500error.html'
        codigo = "HTTP/1.1 500 Internal Server Error"
        extension = "html"

    else:
        extension = archivo.split('.')[1]
        codigo = "HTTP/1.1 200 OK"

    header = bytearray(codigo + "\r\nContent-type:" +
                       dic[extension] + "\r\nContent-length:"+str((os.path.getsize(archivo)))+"\r\n\r\n", 'utf8')
    writer.write(header)

    fd = os.open(archivo, os.O_RDONLY)
    fin = True
    while fin is True:
        body = os.read(fd, args.size)
        writer.write(body)
        if (len(body) != args.size):
            os.close(fd)
            await writer.drain()
            fin = False
    writer.close()


async def main():

    server = await asyncio.start_server(
        handle_echo, ['::1', '127.0.0.1'], args.port)

    addr = server.sockets[0].getsockname()
    print("\nServidor en:", addr)

    async with server:
        await server.serve_forever()

destino = open("registo.txt", "w")
asyncio.run(main())

#   python3 tp4.py -p 5000 -s 10000 -d $(pwd)
