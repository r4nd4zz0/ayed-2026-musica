from pathlib import Path
from src.excepciones import ArchivoInvalidoError
RAIZ = Path(__file__).resolve().parents[2]
DATA = RAIZ / "data"
def cargar_csv(ruta):
    """Lee un .txt/.csv secuencial y devuelve una LISTA DE DICTS, uno por registro.
    Si el archivo no existe o una línea tiene más/menos campos que el encabezado,
    lanza ArchivoInvalidoError."""
    ruta = Path(ruta)
    if not ruta.exists():
        raise ArchivoInvalidoError(f"No existe el archivo: {ruta}")
    filas = []
    with ruta.open("r", encoding="utf-8") as archivo:
        primera_linea = archivo.readline().strip()
        if not primera_linea:
            raise ArchivoInvalidoError(f"El archivo está vacío: {ruta}")  
        encabezado = primera_linea.split(",")
        for linea in archivo:
            linea = linea.strip()
            if not linea:  # línea vacía al final del archivo
                continue
            valores = linea.split(",")
            if len(valores) != len(encabezado):
                raise ArchivoInvalidoError(
                    f"Línea con {len(valores)} campos "
                    f"(se esperaban {len(encabezado)}): {linea}"
                )
            fila = dict(zip(encabezado, valores))
            filas.append(fila)
    return filas
def guardar_csv(ruta, filas, encabezados):
    """Escribe el catálogo en texto: encabezado + un registro por línea."""
    ruta = Path(ruta)
    with ruta.open("w", encoding="utf-8", newline="") as archivo:
        archivo.write(",".join(encabezados) + "\n")
        for fila in filas:
            campos = [str(fila[clave]) for clave in encabezados]
            archivo.write(",".join(campos) + "\n")