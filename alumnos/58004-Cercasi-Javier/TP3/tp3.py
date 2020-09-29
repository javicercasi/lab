#!/usr/bin/python3
import socketserver
import os
from pedido import argumentos
from filter import main
args = argumentos()


class Pixmap():

    def parseo(self, lista):
        valores = lista.pop(1).split(" ").pop(0).split("&")

        try:
            color = valores[0].split("=")[1]
            c = color.upper()
        except IndexError:
            return(0, 0)
        if (c != "W") and (c != "B") and (c != "R") and (c != "G"):
            return(0, 0)

        try:
            escala = int(valores[1].split("=")[1])
        except Exception:
            escala = 1
            pass
        return(color.upper(), escala)


class Handler(socketserver.BaseRequestHandler):

    def handle(self):
        ppm = Pixmap()
        color, escala = 1, 1
        dic = {"txt": " text/plain", "jpg": " image/jpeg", "ppm": " image/x-portable-pixmap", "html": " text/html", "pdf": " application/pdf", "ico": "image/vnd.microsoft.icon"}
        self.data = self.request.recv(1024)
        encabezado = self.data.decode().splitlines()[0]
        archivo = args.documentroot + encabezado.split()[1].split("?")[0]

        if (len(encabezado.split("?")) != 1) and (archivo.split('.')[1] == "ppm"):
            color, escala = ppm.parseo(encabezado.split("?"))

        if archivo == (args.documentroot + "/"):
            archivo = args.documentroot + '/index.html'

        print(self.client_address)

        if os.path.isfile(archivo) is False:
            archivo = args.documentroot + '/400error.html'
            codigo = "HTTP/1.1 400 File Not Found"
            extension = "html"

        elif color == 0 and escala == 0:
            archivo = args.documentroot + '/500error.html'
            codigo = "HTTP/1.1 500 Internal Server Error"
            extension = "html"

        else:
            extension = archivo.split('.')[1]
            codigo = "HTTP/1.1 200 OK"

        if (extension != "ppm") or (extension == "ppm" and len(encabezado.split("?")) == 1):
            fd = os.open(archivo, os.O_RDONLY)
            body = os.read(fd, os.path.getsize(archivo))
            os.close(fd)
            header = bytearray(codigo + "\r\nContent-type:" + dic[extension] + "\r\nContent-length:"+str(len(body))+"\r\n\r\n",'utf8')
            self.request.sendall(header)
            self.request.sendall(body)

        if extension == "ppm" and color != 1:

            enca, body = main(color, escala, archivo, args.size)
            header = bytearray(codigo + "\r\nContent-type:" + dic[extension] + "\r\nContent-length:"+str((os.path.getsize(archivo))*4)+"\r\n\r\n",'utf8')
            self.request.sendall(header)
            self.request.sendall(enca)
            for lista in (list(body)):
                self.request.sendall(bytearray(lista, "utf-8"))


socketserver.TCPServer.allow_reuse_address = True
server = socketserver.ThreadingTCPServer(("0.0.0.0", args.port), Handler)
server.serve_forever()
