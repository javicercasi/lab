

def mensaje(saludo):

    oculto = []
    oculto2 = []
    # Realizo la codificacion del saludo.txt:
    for x in saludo:
        bina = format(ord(x), 'b')
        while len(bina) != 8:
            bina = "0" + bina
        oculto.append(bina)
    for subgrupo in oculto:
        for bit in subgrupo:
            oculto2.append(bit)

    return(oculto2)
