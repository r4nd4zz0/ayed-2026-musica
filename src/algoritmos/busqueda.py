def busqueda_lineal(coleccion, clave, obtener_clave=None):
    """Búsqueda lineal propia. Recorre uno por uno (O(n)). Prohibido usar 'in' o '.index()'."""
    for elemento in coleccion:
        if obtener_clave is None:
            if elemento == clave:
                return elemento
        else:
            if obtener_clave(elemento) == clave:
                return elemento
    return None
def busqueda_binaria(coleccion, clave, obtener_clave):
    """Búsqueda binaria propia. Corta a la mitad en cada paso (O(log n)).Prohibido usar 'bisect'. REQUIERE que la colección esté ordenada."""
    izq = 0
    der = len(coleccion) - 1
    while izq <= der:
        medio = (izq + der) // 2
        valor = obtener_clave(coleccion[medio])
        if valor == clave:
            return coleccion[medio]
        elif valor < clave:
            izq = medio + 1 
        else:
            der = medio - 1          
    return None