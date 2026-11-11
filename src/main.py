import csv
from pathlib import Path

from src.algoritmos.busqueda import busqueda_binaria, busqueda_lineal
from src.algoritmos.ordenamiento import ordenar_insercion, ordenar_seleccion
from src.config import TEMA
from src.dominio.biblioteca import BibliotecaMusical
from src.dominio.cancion import Cancion
from src.excepciones import ArchivoInvalidoError, ColaVaciaError, PilaVaciaError
from src.persistencia.binario import (
    actualizar_registro,
    alta_binario,
    baja_binario,
    cargar_binario,
    guardar_binario,
)
from src.persistencia.texto import DATA, cargar_csv, guardar_csv
from src.tads.cola import Cola
from src.tads.lista_enlazada import ListaEnlazada
from src.tads.pila import Pila

TEMAS = {
    "pokedex": "Pokédex",
    "recetario": "Recetario",
    "musica": "Biblioteca musical",
}

coleccion_principal = ListaEnlazada()
historial = Pila()
cola_reproduccion = Cola()

RUTA_TXT = DATA / "canciones.csv"
RUTA_BIN = DATA / "canciones.bin"
ENCABEZADOS = ["id", "titulo", "artista", "album", "genero", "anio", "duracion_seg"]

def armar_catalogo_desde_txt(ruta: Path = RUTA_TXT) -> list[Cancion]:
    """Lee canciones.csv con cargar_texto y devuelve una lista de objetos Cancion."""
    filas = cargar_csv(ruta)
    return [Cancion.from_dict(fila) for fila in filas]

def ver_detalle(catalogo) -> None:
    """Muestra todos los campos de una canción por su ID (Opción 2 - P02)."""
    entrada = input("Ingresá el ID de la canción para ver su detalle: ").strip()
    try:
        id_buscado = int(entrada)
    except ValueError:
        print("Error: el ID debe ser un número entero.")
        return
    for item in catalogo:
        item_id = int(item["id"]) if isinstance(item, dict) else item.id
        if item_id == id_buscado:
            print("\n--- Detalle de la canción ---")
            if isinstance(item, dict):
                print(f"  ID:       {item['id']}")
                print(f"  Título:   {item['titulo']}")
                print(f"  Artista:  {item['artista']}")
                print(f"  Álbum:    {item['album']}")
                print(f"  Género:   {item['genero']}")
                print(f"  Año:      {item['anio']}")
                print(f"  Duración: {item['duracion_seg']} segundos")
            else:
                print(f"  ID:       {item.id}")
                print(f"  Título:   {item.titulo}")
                print(f"  Artista:  {item.artista}")
                print(f"  Álbum:    {item.album}")
                print(f"  Género:   {item.genero}")
                print(f"  Año:      {item.anio}")
                print(f"  Duración: {item.duracion_seg} segundos")
            return
    print(f"No existe una canción con ID {id_buscado}.")

def filas_del_catalogo(catalogo) -> list[dict]:
    """Convierte los objetos Cancion del catálogo en dicts para guardar_texto."""
    filas = []
    for c in catalogo:
        filas.append(c.to_dict() if hasattr(c, "to_dict") else dict(c))
    return filas

def guardar_todo(catalogo) -> None:
    """Sincroniza el catálogo en memoria con canciones.csv y canciones.bin."""
    guardar_csv(RUTA_TXT, filas_del_catalogo(catalogo), ENCABEZADOS)
    guardar_binario(RUTA_BIN, catalogo)

def posicion_del_id(catalogo, id_buscado: int) -> int:
    """Devuelve la posición 0-based de la canción con ese id, o -1 si no está."""
    for pos, cancion in enumerate(catalogo):
        if cancion.id == id_buscado:
            return pos
    return -1

def cargar_dataset(nombre_archivo: str = "canciones.csv") -> list[Cancion]:
    """Carga inicial del catálogo usando la capa de persistencia de E5."""
    ruta_archivo = DATA / nombre_archivo
    try:
        return armar_catalogo_desde_txt(ruta_archivo)
    except ArchivoInvalidoError as exc:
        print(f"Error al cargar dataset: {exc}")
        return []

def listar_catalogo(catalogo) -> None:
    """Muestra los elementos cargados en memoria."""
    if not catalogo:
        print("El catálogo está vacío o no se pudo cargar.")
        return

    print(f"\n--- Catálogo cargado ({len(catalogo)} canciones) ---")
    for cancion in catalogo:
        print(f"  {cancion} - {cancion.genero} ({cancion.duracion_seg}s)")

def pendiente():
    print("Todavía no está implementado. Completar en la entrega que corresponde.")

def manejar_coleccion_principal(catalogo: list[Cancion]):
    while True:
        print("\nColección principal y ABM persistente")
        print("1. Agregar elemento a mi colección (ListaEnlazada)")
        print("2. Ver mi colección (ListaEnlazada)")
        print("3. Alta de canción en catálogo (persistente)")
        print("4. Modificar canción por ID (acceso directo en .bin)")
        print("5. Baja de canción por ID (persistente)")
        print("0. Volver")
        opcion = input("> ").strip()

        if opcion == "0":
            return
        elif opcion == "1":
            valor = input("Ingresá un elemento: ").strip()
            if not valor:
                print("El valor no puede estar vacío.")
                continue
            coleccion_principal.insertar_al_final(valor)
            print(f"Agregado: {valor}")
        elif opcion == "2":
            if coleccion_principal.esta_vacia():
                print("La colección principal está vacía.")
            else:
                print("Elementos:")
                for elemento in coleccion_principal:
                    print(f"- {elemento}")
        elif opcion == "3":
            try:
                nuevo_id = int(input("ID numérico: ").strip())
                if posicion_del_id(catalogo, nuevo_id) != -1:
                    print("Ya existe una canción con ese ID.")
                    continue
                titulo = input("Título: ").strip()
                artista = input("Artista: ").strip()
                album = input("Álbum: ").strip()
                genero = input("Género: ").strip()
                anio = int(input("Año: ").strip())
                duracion = int(input("Duración (segundos): ").strip())
                if not titulo or not artista:
                    print("Título y artista son obligatorios.")
                    continue
                nueva = Cancion(nuevo_id, titulo, artista, album, genero, anio, duracion)
                catalogo.append(nueva)
                if not RUTA_BIN.exists():
                    guardar_binario(RUTA_BIN, catalogo)
                else:
                    alta_binario(RUTA_BIN, nueva)
                guardar_texto(RUTA_TXT, filas_del_catalogo(catalogo), ENCABEZADOS)
                print(f"Canción agregada y persistida: {nueva}")
            except ValueError:
                print("Error: ID, año y duración deben ser números enteros.")
            except ArchivoInvalidoError as exc:
                print(f"Error de archivo: {exc}")
        elif opcion == "4":
            try:
                id_mod = int(input("ID de la canción a modificar: ").strip())
                pos = posicion_del_id(catalogo, id_mod)
                if pos == -1:
                    print("No se encontró una canción con ese ID.")
                    continue
                actual = catalogo[pos]
                print(f"Actual: {actual} - {actual.genero} ({actual.duracion_seg}s)")
                nuevo_titulo = input(f"Nuevo título [{actual.titulo}]: ").strip() or actual.titulo
                nuevo_artista = input(f"Nuevo artista [{actual.artista}]: ").strip() or actual.artista
                nuevo_album = input(f"Nuevo álbum [{actual.album}]: ").strip() or actual.album
                nuevo_genero = input(f"Nuevo género [{actual.genero}]: ").strip() or actual.genero
                anio_str = input(f"Nuevo año [{actual.anio}]: ").strip()
                dur_str = input(f"Nueva duración seg [{actual.duracion_seg}]: ").strip()
                nuevo_anio = int(anio_str) if anio_str else actual.anio
                nueva_dur = int(dur_str) if dur_str else actual.duracion_seg

                modificada = Cancion(
                    actual.id, nuevo_titulo, nuevo_artista, nuevo_album,
                    nuevo_genero, nuevo_anio, nueva_dur
                )
                catalogo[pos] = modificada
                if not RUTA_BIN.exists():
                    guardar_binario(RUTA_BIN, catalogo)
                else:
                    actualizar_registro(RUTA_BIN, pos, modificada)
                guardar_texto(RUTA_TXT, filas_del_catalogo(catalogo), ENCABEZADOS)
                print("Canción modificada por posición en .bin (seek) y actualizada en .csv.")
            except ValueError:
                print("Error: ingresá valores numéricos válidos.")
            except ArchivoInvalidoError as exc:
                print(f"Error de archivo: {exc}")
        elif opcion == "5":
            try:
                id_baja = int(input("ID de la canción a dar de baja: ").strip())
                pos = posicion_del_id(catalogo, id_baja)
                if pos == -1:
                    print("No se encontró una canción con ese ID.")
                    continue
                eliminada = catalogo.pop(pos)
                if RUTA_BIN.exists():
                    baja_binario(RUTA_BIN, pos)
                guardar_texto(RUTA_TXT, filas_del_catalogo(catalogo), ENCABEZADOS)
                print(f"Canción eliminada del catálogo y de los archivos: {eliminada}")
            except ValueError:
                print("Error: el ID debe ser un número entero.")
            except ArchivoInvalidoError as exc:
                print(f"Error de archivo: {exc}")
        else:
            print("Opción inválida.")

def manejar_historial():
    while True:
        print("\nHistorial (pila)")
        print("1. Apilar")
        print("2. Ver tope")
        print("3. Desapilar")
        print("0. Volver")
        opcion = input("> ").strip()

        if opcion == "0":
            return
        if opcion == "1":
            valor = input("Ingresá una acción: ").strip()
            if not valor:
                print("La acción no puede estar vacía.")
                continue
            historial.apilar(valor)
            print(f"Acción agregada al historial: {valor}")
        elif opcion == "2":
            try:
                print(f"Tope: {historial.ver_tope()}")
            except PilaVaciaError as exc:
                print(exc)
        elif opcion == "3":
            try:
                print(f"Se desapiló: {historial.desapilar()}")
            except PilaVaciaError as exc:
                print(exc)
        else:
            print("Opción inválida.")

def manejar_cola():
    while True:
        print("\nCola de reproducción")
        print("1. Encolar")
        print("2. Ver frente")
        print("3. Desencolar")
        print("0. Volver")
        opcion = input("> ").strip()

        if opcion == "0":
            return
        if opcion == "1":
            valor = input("Ingresá una canción: ").strip()
            if not valor:
                print("La canción no puede estar vacía.")
                continue
            cola_reproduccion.encolar(valor)
            print(f"Se encoló: {valor}")
        elif opcion == "2":
            try:
                print(f"Frente: {cola_reproduccion.ver_frente()}")
            except ColaVaciaError as exc:
                print(exc)
        elif opcion == "3":
            try:
                print(f"Se desencoló: {cola_reproduccion.desencolar()}")
            except ColaVaciaError as exc:
                print(exc)
        else:
            print("Opción inválida.")

def manejar_busqueda(catalogo, catalogo_ordenado):
    print("\nBuscar por título usando: 1) Lineal  2) Binaria")
    tipo = input("> ").strip()
    
    if tipo == "2" and not catalogo_ordenado:
        print("Error: El catálogo debe estar ordenado por título antes de usar búsqueda binaria.")
        return

    clave = input("Ingresá el título exacto: ")
    
    if tipo == "1":
        resultado = busqueda_lineal(catalogo, clave, lambda c: c.titulo)
    elif tipo == "2":
        resultado = busqueda_binaria(catalogo, clave, lambda c: c.titulo)
    else:
        print("Opción inválida.")
        return

    if resultado:
        print(f"Encontrado: {resultado.titulo}")
    else:
        print("No encontrado.")

def manejar_ordenamiento(catalogo):
    print("\nOrdenar por: 1) Título  2) Duración / ID")
    criterio = input("> ").strip()
    print("Algoritmo: 1) Selección (no estable)  2) Inserción (estable)")
    algo = input("> ").strip()

    if criterio == "1":
        obtener_clave = lambda c: c.titulo
    elif criterio == "2":
        obtener_clave = lambda c: c.duracion 
    else:
        print("Opción inválida.")
        return False

    if algo == "1":
        ordenar_seleccion(catalogo, obtener_clave)
        print("Catálogo ordenado por selección.")
    elif algo == "2":
        ordenar_insercion(catalogo, obtener_clave)
        print("Catálogo ordenado por inserción.")
    else:
        print("Opción inválida.")
        return False

    if criterio == "1":
        return True
    else:
        return False

def manejar_archivos(catalogo: list[Cancion]) -> list[Cancion]:
    print("\nGuardar / cargar archivos")
    print("  a) Cargar catálogo desde texto (.csv/.txt)")
    print("  b) Guardar catálogo en texto (.csv/.txt)")
    print("  c) Guardar catálogo en binario (.bin)")
    print("  d) Cargar catálogo desde binario (.bin)")
    print("  e) Probar carga de archivo inválido (o ingresar ruta manual)")
    sub = input("Subopción > ").strip().lower()

    try:
        if sub == "a":
            catalogo = armar_catalogo_desde_txt(RUTA_TXT)
            print(f"Catálogo cargado desde texto: {len(catalogo)} canciones.")
        elif sub == "b":
            guardar_csv(RUTA_TXT, filas_del_catalogo(catalogo), ENCABEZADOS)
            print("Catálogo guardado en texto.")
        elif sub == "c":
            guardar_binario(RUTA_BIN, catalogo)
            print("Catálogo guardado en binario (.bin).")
        elif sub == "d":
            lista_enlazada = cargar_binario(RUTA_BIN)
            catalogo = list(lista_enlazada)
            print(f"Catálogo cargado desde binario: {len(catalogo)} canciones.")
        elif sub == "e":
            ruta_manual = input("Ingresá la ruta del archivo a probar (ej: data/basura.bin): ").strip()
            if ruta_manual.endswith(".bin"):
                lista_enlazada = cargar_binario(Path(ruta_manual))
                catalogo = list(lista_enlazada)
            else:
                catalogo = armar_catalogo_desde_txt(Path(ruta_manual))
            print(f"Archivo cargado correctamente ({len(catalogo)} canciones).")
        else:
            print("Subopción inválida.")
    except ArchivoInvalidoError as error:
        print(f"Archivo inválido: {error}")

    return catalogo

def manejar_recursion() -> None:
    """Ejecuta la operación recursiva buscando las versiones derivadas de una canción."""
    entrada = input("Ingresá el ID de la canción base: ").strip()
    try:
        cancion_id = int(entrada)
    except ValueError:
        print("Error: el ID debe ser un número entero.")
        return

    try:
        biblioteca = BibliotecaMusical()
        biblioteca.mostrar_derivadas(cancion_id)
    except Exception as exc:
        print(f"Error al consultar versiones: {exc}")

def mostrar_menu():
    nombre = TEMAS.get(TEMA, TEMA or "(sin tema)")
    print()
    print(f"=== {nombre} — AyED C2 2026 ===")
    print("1. Listar catálogo")
    print("2. Ver detalle")
    print("3. Buscar")
    print("4. Ordenar")
    print("5. Operación recursiva")
    print("6. Colección principal")
    print("7. Historial (pila)")
    print("8. Cola")
    print("9. Guardar / cargar archivos")
    print("0. Salir")

def main():
    if TEMA not in TEMAS:
        print("Seteá TEMA en src/config.py: 'pokedex', 'recetario' o 'musica'.")
        return

    catalogo = cargar_dataset()
    catalogo_ordenado = False
    opcion = None

    while opcion != "0":
        mostrar_menu()
        opcion = input("> ").strip()

        if opcion == "0":
            print("Chau.")
        elif opcion == "1":
            listar_catalogo(catalogo)
        elif opcion == "2":
            ver_detalle(catalogo)
        elif opcion == "3":
            manejar_busqueda(catalogo, catalogo_ordenado)
        elif opcion == "4":
            catalogo_ordenado = manejar_ordenamiento(catalogo)
        elif opcion == "5":
            manejar_recursion()
        elif opcion == "6":
            manejar_coleccion_principal(catalogo)
        elif opcion == "7":
            manejar_historial()
        elif opcion == "8":
            manejar_cola()
        elif opcion == "9":
            catalogo = manejar_archivos(catalogo)
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()
