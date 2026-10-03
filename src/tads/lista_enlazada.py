from src.excepciones import ItemNoEncontradoError
from src.tads.nodo import Nodo


class ListaEnlazada:
    """TAD lista enlazada simple sin usar list de Python como estructura interna."""

    def __init__(self):
        self._cabeza = None
        self._longitud = 0

    def esta_vacia(self):
        return self._cabeza is None

    def tamanio(self):
        return self._longitud

    def insertar_al_inicio(self, dato):
        nuevo = Nodo(dato, self._cabeza)
        self._cabeza = nuevo
        self._longitud += 1

    def insertar_al_final(self, dato):
        if self.esta_vacia():
            self.insertar_al_inicio(dato)
            return

        actual = self._cabeza
        while actual.siguiente is not None:
            actual = actual.siguiente

        actual.siguiente = Nodo(dato)
        self._longitud += 1

    def insertar_ordenado(self, dato, clave):
        if self.esta_vacia() or clave(dato) <= clave(self._cabeza.dato):
            self.insertar_al_inicio(dato)
            return

        actual = self._cabeza
        while actual.siguiente is not None and clave(actual.siguiente.dato) < clave(dato):
            actual = actual.siguiente

        nuevo = Nodo(dato, actual.siguiente)
        actual.siguiente = nuevo
        self._longitud += 1

    def eliminar(self, dato):
        if self.esta_vacia():
            raise ItemNoEncontradoError(f"El elemento {dato} no existe en la lista.")

        if self._cabeza.dato == dato:
            self._cabeza = self._cabeza.siguiente
            self._longitud -= 1
            return

        actual = self._cabeza
        while actual.siguiente is not None and actual.siguiente.dato != dato:
            actual = actual.siguiente

        if actual.siguiente is None:
            raise ItemNoEncontradoError(f"El elemento {dato} no existe en la lista.")

        actual.siguiente = actual.siguiente.siguiente
        self._longitud -= 1

    def buscar(self, dato):
        actual = self._cabeza
        while actual is not None:
            if actual.dato == dato:
                return actual.dato
            actual = actual.siguiente
        return None

    def __iter__(self):
        actual = self._cabeza
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente
    
    def ver_primero(self):
        if self.esta_vacia():
            return None
        return self._cabeza.dato
