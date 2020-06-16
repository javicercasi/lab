# COMPUTACION II


## TP2

Fecha de entrega: 16/06/2020


### Problema

Se necesita una desarrollar una aplicación que implemente esteganografía, utilizando una imágen con formato portátil pixmap (ppm) indicado por la opcion "-f archivo" o "--file archivo" como portador o contenedor. 

El mensaje esteganográfico se debe leer desde el archivo con formato ascii indicado por la opción "-m archivo" o "--message archivo".

La aplicación deberá implementar el algoritmo esteganográfico que se describe a continuación y guardar el resultante en un archivo indicado por la opción "-o archivo" o "--output archivo" que será el archivo de salida o estego-mensaje.

En primer lugar se debe modificar el encabezado del archivo original, adicionando como primera linea de comentario la siguiente:

#UMCOMPU2 OFFSET INTERLEAVE L_TOTAL

Esto permitirá poder recuperar el mensaje esteganográfico en el futuro.

El método esteganográfico a usar es LSB (Least Significant Bit). Donde OFFSET indica el primer pixel desde donde se aplicará el método, INTERLEAVE cada cuantos pixeles se aplica y L_TOTAL el tamaño total (en bytes) del mensaje esteganográfico.

El algoritmo LSB se aplicará ciclicamente para los bytes R G o B del pixel que corresponda modificar, comenzando desde el byte correspondiente a Red del pixel OFFSET, contando desde el inicio del raster de la imagen portadora.

La aplicación debe ir leyendo la imagen por bloques de n bytes indicadas por la opcion "-s valor" o "--size valor", y modificar el bit menos significativo (LSB) de los bytes correspondientes, segun el algoritmo descripto. Una vez modificado ese bloque, almacenarlo en el archivo especificado por la opción -o y volver a leer otro bloque, hasta finalizar.

Para mejorar el rendimiento, se exige implementar la solución creando 3 hilos adicionales (uno por cada color) que trabajarán de manera concurrente y éstos serán los que hagan la modificación del archivo portador para obtener el archivo de salida.

Una vez finalizado proceso de creación del estego-mensaje deben terminar los hilos adicionales, y el proceso debe mostrar un mensaje con el tiempo que demoró el proceso.

Los valores de OFFSET e INTERLEAVE se proveerán con las siguientes opciones "-f pixels" o "--offset pixels" y "-i pixels"  o "--interleave pixels" respectivamente. 

Finalmente se pide validar INTERLEAVE, en función del tamaño del raster del portador y el largo del mensaje esteganográfico.


### Requerimientos

* La aplicación debe contener como mínimo 3 funciones, en archivos independientes.
* Debe procesar las opciones con getopt (agregar una opcion de ayuda) o con argparse.
* Debe usar el modulo multithreading o concurrent.futures.
* No se deberá usar otro tipo de módulos o bibliotecas de gestión gráfica o de encriptación o esteganográfica.
* Debe manejar los errores.


#### Ejemplo modo de uso

~~~~~~~~~~~~~~~~~~~
$ ./tp2.py -h
usage: tp2.py [-h] -s SIZE -f FILE -m FILE -f PIXELS -i PIXELS -o FILE2

Tp2 - procesa ppm

optional arguments:
  -h, --help          	    	show this help message and exit
  -s SIZE, --size SIZE		bloque de lectura
  -f FILE, --file FILE    	archivo portador
  -m FILE, --message FILE 	mensaje esteganográfico
  -f PIXS, --offset PIXS  	offset en pixels del inicio del raster
  -i PIXS, --interleave PIXS  	interleave de modificacion en pixel
  -o FILE, --output FILE  	estego-mensaje


$ ./tp2.py -s 10240 -f dog.ppm -m saludo.txt -f 5 -i 200 -o mensaje_oculto.ppm

Se genero correctamente
Tiempo de corrida: 0.31 segundos 

~~~~~~~~~~~~~~~~~~~


### Objetivos

* Manejo de archivos (apertura, escritura y cierre).
* Creación de Hilos.
* Uso de mecanismos de Sincronización

### Referencias
man ppm

http://netpbm.sourceforge.net/doc/ppm.html

https://itnext.io/steganography-101-lsb-introduction-with-python-4c4803e08041

### Bonus Track
Realizar una aplicación que pueda extraer el mensage oculto en la imagen portadora.
