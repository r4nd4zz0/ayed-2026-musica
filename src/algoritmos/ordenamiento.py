def ordenar_seleccion(coleccion, obtener_clave):
    """Ordenamiento por selección. NO es estable. Complejidad O(n^2). Busca el mínimo de lo que queda y lo ubica al principio."""
    n = len(coleccion)
    for i in range(n - 1):
        pos_min = i
        for j in range(i + 1, n):
            if obtener_clave(coleccion[j]) < obtener_clave(coleccion[pos_min]):
                pos_min = j
        coleccion[i], coleccion[pos_min] = coleccion[pos_min], coleccion[i]
    return coleccion
def ordenar_insercion(coleccion, obtener_clave):
    """Ordenamiento por inserción. SÍ es estable. Complejidad O(n^2) peor caso. Toma cada elemento y lo empuja hacia atrás hasta su posición correcta."""
    for i in range(1, len(coleccion)):
        actual = coleccion[i]
        j = i - 1
        while j >= 0 and obtener_clave(coleccion[j]) > obtener_clave(actual):
            coleccion[j + 1] = coleccion[j]
            j -= 1
        coleccion[j + 1] = actual
    return coleccion