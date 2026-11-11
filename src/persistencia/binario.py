import struct
from pathlib import Path
from src.excepciones import ArchivoInvalidoError
from src.dominio.cancion import Cancion
from src.tads.lista_enlazada import ListaEnlazada

# Layout Música: id(I=4B), titulo(30B), artista(25B), album(30B), genero(12B), anio(H=2B), duracion_seg(H=2B) -> 105 bytes
FORMATO = struct.Struct("<I 30s 25s 30s 12s 2H")
# Header: magia(4s), tema(1s), cantidad(I) -> 9 bytes
HEADER = struct.Struct("<4s 1s I")
TEMA = b"M"
def _a_bytes(texto: str, ancho: int) -> bytes:
    """Convierte texto a bytes UTF-8 de 'ancho' exacto: recorta o rellena con \\x00."""
    return str(texto).encode("utf-8")[:ancho].ljust(ancho, b"\x00")
def _a_texto(datos: bytes) -> str:
    """Convierte bytes a texto quitando los \\x00 del final."""
    return datos.rstrip(b"\x00").decode("utf-8", errors="replace")
def _item_a_tupla(c) -> tuple:
    """Convierte un objeto Cancion (o dict) en una tupla lista para FORMATO.pack."""
    if isinstance(c, dict):
        c = Cancion.from_dict(c)
    return (
        int(c.id),
        _a_bytes(c.titulo, 30),
        _a_bytes(c.artista, 25),
        _a_bytes(c.album, 30),
        _a_bytes(c.genero, 12),
        int(c.anio),
        int(c.duracion_seg),
    )
def _tupla_a_item(t: tuple) -> Cancion:
    """Convierte la tupla desempaquetada por struct en un objeto Cancion."""
    return Cancion(
        id=t[0],
        titulo=_a_texto(t[1]),
        artista=_a_texto(t[2]),
        album=_a_texto(t[3]),
        genero=_a_texto(t[4]),
        anio=t[5],
        duracion_seg=t[6],
    )
def _cantidad_items(items) -> int:
    """Obtiene la cantidad de elementos ya sea ListaEnlazada o list."""
    if hasattr(items, "tamanio"):
        return items.tamanio()
    return len(items)
def guardar_binario(ruta, items):
    """Escribe el archivo binario completo: header + registros de longitud fija."""
    ruta = Path(ruta)
    cantidad = _cantidad_items(items)
    with open(ruta, "wb") as archivo:
        archivo.write(HEADER.pack(b"AYED", TEMA, cantidad))
        for item in items:
            archivo.write(FORMATO.pack(*_item_a_tupla(item)))
def cargar_binario(ruta) -> ListaEnlazada:
    """Lee el archivo binario validando header y tamaño. Devuelve ListaEnlazada de Cancion."""
    ruta = Path(ruta)
    if not ruta.exists():
        raise ArchivoInvalidoError(f"No existe el archivo binario: {ruta}")
    with open(ruta, "rb") as archivo:
        cabecera = archivo.read(HEADER.size)
        if len(cabecera) < HEADER.size:
            raise ArchivoInvalidoError("Binario truncado: ni siquiera tiene header completo.")
        magia, tema, cantidad = HEADER.unpack(cabecera)
        if magia != b"AYED":
            raise ArchivoInvalidoError("Magia incorrecta: este archivo no es de este TP.")
        if tema != TEMA:
            raise ArchivoInvalidoError(f"El tema del archivo ({tema!r}) no coincide con Música ({TEMA!r}).")
        catalogo = ListaEnlazada()
        for _ in range(cantidad):
            datos = archivo.read(FORMATO.size)
            if len(datos) < FORMATO.size:
                raise ArchivoInvalidoError(
                    "Binario truncado: el header indica más registros de los que hay."
                )
            try:
                tupla = FORMATO.unpack(datos)
                catalogo.insertar_al_final(_tupla_a_item(tupla))
            except Exception as exc:
                raise ArchivoInvalidoError(f"Registro binario corrupto: {exc}") from exc
    return catalogo
def actualizar_registro(ruta, posicion: int, item):
    """Pisa SOLO el registro en 'posicion' (0-based) con acceso directo O(1) usando seek."""
    ruta = Path(ruta)
    if not ruta.exists():
        raise ArchivoInvalidoError(f"No existe el archivo binario: {ruta}")
    if posicion < 0:
        raise ArchivoInvalidoError(f"Posición inválida: {posicion}")
    with open(ruta, "r+b") as archivo:
        cabecera = archivo.read(HEADER.size)
        if len(cabecera) < HEADER.size:
            raise ArchivoInvalidoError("Binario truncado: header incompleto.")
        magia, tema, cantidad = HEADER.unpack(cabecera)
        if magia != b"AYED" or tema != TEMA:
            raise ArchivoInvalidoError("Header binario inválido.")
        if posicion >= cantidad:
            raise IndexError(f"Posición {posicion} fuera de rango (cantidad={cantidad}).")
        archivo.seek(HEADER.size + posicion * FORMATO.size)
        archivo.write(FORMATO.pack(*_item_a_tupla(item)))
def alta_binario(ruta, item):
    """Agrega un registro al final del archivo binario y actualiza el contador del header."""
    ruta = Path(ruta)
    if not ruta.exists():
        catalogo = ListaEnlazada()
        catalogo.insertar_al_final(item)
        guardar_binario(ruta, catalogo)
        return
    with open(ruta, "r+b") as archivo:
        cabecera = archivo.read(HEADER.size)
        if len(cabecera) < HEADER.size:
            raise ArchivoInvalidoError("Binario truncado: header incompleto.")
        magia, tema, cantidad = HEADER.unpack(cabecera)
        if magia != b"AYED" or tema != TEMA:
            raise ArchivoInvalidoError("Header binario inválido.")
        archivo.seek(0, 2)  # Salta al final del archivo
        archivo.write(FORMATO.pack(*_item_a_tupla(item)))
        archivo.seek(0)     # Vuelve al inicio para actualizar la cantidad
        archivo.write(HEADER.pack(magia, tema, cantidad + 1))
def baja_binario(ruta, posicion: int):
    """Quita el registro en 'posicion': relee, elimina ese registro y reescribe el archivo."""
    ruta = Path(ruta)
    if not ruta.exists():
        raise ArchivoInvalidoError(f"No existe el archivo binario: {ruta}")
    with open(ruta, "r+b") as archivo:
        cabecera = archivo.read(HEADER.size)
        if len(cabecera) < HEADER.size:
            raise ArchivoInvalidoError("Binario truncado: header incompleto.")
        magia, tema, cantidad = HEADER.unpack(cabecera)
        if magia != b"AYED" or tema != TEMA:
            raise ArchivoInvalidoError("Header binario inválido.")
        if posicion < 0 or posicion >= cantidad:
            raise IndexError(f"Posición {posicion} fuera de rango (cantidad={cantidad}).")
        registros = [archivo.read(FORMATO.size) for _ in range(cantidad)]
        del registros[posicion]
        archivo.seek(0)
        archivo.truncate()
        archivo.write(HEADER.pack(magia, tema, len(registros)))
        for datos in registros:
            archivo.write(datos)