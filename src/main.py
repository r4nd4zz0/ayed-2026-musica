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

RUTA_TXT = DATA / "canciones.csv"
RUTA_BIN = DATA / "canciones.bin"
ENCABEZADOS = ["id", "titulo", "artista", "album", "genero", "anio", "duracion_seg"]

coleccion_principal = ListaEnlazada()
historial = Pila()
cola_reproduccion = Cola()


def armar_catalogo_desde_txt(ruta: Path = RUTA_TXT) -> list[Cancion]:
    """Carga el catálogo de canciones desde el archivo de texto/CSV."""
    return [Cancion.from_dict(fila) for fila in cargar_csv(ruta)]


def filas_del_catalogo(catalogo) -> list[dict]:
    """Convierte canciones del catálogo a filas para la persistencia de texto."""
    return [cancion.to_dict() for cancion in catalogo]


def persistir_texto(catalogo) -> None:
    guardar_csv(RUTA_TXT, filas_del_catalogo(catalogo), ENCABEZADOS)


def guardar_todo(catalogo) -> None:
    """Guarda una copia completa del catálogo en texto y en binario."""
    persistir_texto(catalogo)
    guardar_binario(RUTA_BIN, catalogo)


def posicion_del_id(catalogo, id_buscado: int) -> int:
    """Devuelve la posición 0-based del ID, o -1 cuando no existe."""
    for posicion, cancion in enumerate(catalogo):
        if cancion.id == id_buscado:
            return posicion
    return -1


def cargar_dataset(nombre_archivo: str = "canciones.csv") -> list[Cancion]:
    """Carga inicial del catálogo desde el dataset de texto de la cátedra."""
    try:
        return armar_catalogo_desde_txt(DATA / nombre_archivo)
    except (ArchivoInvalidoError, ValueError, KeyError) as error:
        print(f"Error al cargar dataset: {error}")
        return []


def listar_catalogo(catalogo) -> None:
    """Lista el catálogo recorriéndolo mediante su iterador."""
    if not catalogo:
        print("El catálogo está vacío o no se pudo cargar.")
        return
    print(f"\n--- Catálogo cargado ({len(catalogo)} canciones) ---")
    for cancion in catalogo:
        print(f"  {cancion} - {cancion.genero} ({cancion.duracion_seg}s)")


def ver_detalle(catalogo) -> None:
    entrada = input("Ingresá el ID de la canción para ver su detalle: ").strip()
    try:
        id_buscado = int(entrada)
    except ValueError:
        print("Error: el ID debe ser un número entero.")
        return
    for cancion in catalogo:
        if cancion.id == id_buscado:
            print("\n--- Detalle de la canción ---")
            print(f"  ID:       {cancion.id}")
            print(f"  Título:   {cancion.titulo}")
            print(f"  Artista:  {cancion.artista}")
            print(f"  Álbum:    {cancion.album}")
            print(f"  Género:   {cancion.genero}")
            print(f"  Año:      {cancion.anio}")
            print(f"  Duración: {cancion.duracion_seg} segundos")
            return
    print(f"No existe una canción con ID {id_buscado}.")


def manejar_coleccion_principal(catalogo) -> None:
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
        if opcion == "1":
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
                if RUTA_BIN.exists():
                    alta_binario(RUTA_BIN, nueva)
                else:
                    guardar_binario(RUTA_BIN, [*catalogo, nueva])
                catalogo.append(nueva)
                persistir_texto(catalogo)
                print(f"Canción agregada y persistida: {nueva}")
            except (ValueError, ArchivoInvalidoError) as error:
                print(f"No se pudo dar de alta la canción: {error}")
        elif opcion == "4":
            try:
                id_mod = int(input("ID de la canción a modificar: ").strip())
                posicion = posicion_del_id(catalogo, id_mod)
                if posicion == -1:
                    print("No se encontró una canción con ese ID.")
                    continue
                actual = catalogo[posicion]
                print(f"Actual: {actual} - {actual.genero} ({actual.duracion_seg}s)")
                titulo = input(f"Nuevo título [{actual.titulo}]: ").strip() or actual.titulo
                artista = input(f"Nuevo artista [{actual.artista}]: ").strip() or actual.artista
                album = input(f"Nuevo álbum [{actual.album}]: ").strip() or actual.album
                genero = input(f"Nuevo género [{actual.genero}]: ").strip() or actual.genero
                anio_txt = input(f"Nuevo año [{actual.anio}]: ").strip()
                duracion_txt = input(f"Nueva duración seg [{actual.duracion_seg}]: ").strip()
                modificada = Cancion(
                    actual.id,
                    titulo,
                    artista,
                    album,
                    genero,
                    int(anio_txt) if anio_txt else actual.anio,
                    int(duracion_txt) if duracion_txt else actual.duracion_seg,
                )
                if RUTA_BIN.exists():
                    actualizar_registro(RUTA_BIN, posicion, modificada)
                else:
                    copia = list(catalogo)
                    copia[posicion] = modificada
                    guardar_binario(RUTA_BIN, copia)
                catalogo[posicion] = modificada
                persistir_texto(catalogo)
                print("Canción modificada por posición en .bin y actualizada en .csv.")
            except (ValueError, ArchivoInvalidoError, IndexError) as error:
                print(f"No se pudo modificar la canción: {error}")
        elif opcion == "5":
            try:
                id_baja = int(input("ID de la canción a dar de baja: ").strip())
                posicion = posicion_del_id(catalogo, id_baja)
                if posicion == -1:
                    print("No se encontró una canción con ese ID.")
                    continue
                eliminada = catalogo[posicion]
                if RUTA_BIN.exists():
                    baja_binario(RUTA_BIN, posicion)
                else:
                    copia = list(catalogo)
                    del copia[posicion]
                    guardar_binario(RUTA_BIN, copia)
                del catalogo[posicion]
                persistir_texto(catalogo)
                print(f"Canción eliminada del catálogo y de los archivos: {eliminada}")
            except (ValueError, ArchivoInvalidoError, IndexError) as error:
                print(f"No se pudo dar de baja la canción: {error}")
        else:
            print("Opción inválida.")


def manejar_historial() -> None:
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
            if valor:
                historial.apilar(valor)
                print(f"Acción agregada al historial: {valor}")
            else:
                print("La acción no puede estar vacía.")
        elif opcion == "2":
            try:
                print(f"Tope: {historial.ver_tope()}")
            except PilaVaciaError as error:
                print(error)
        elif opcion == "3":
            try:
                print(f"Se desapiló: {historial.desapilar()}")
            except PilaVaciaError as error:
                print(error)
        else:
            print("Opción inválida.")


def manejar_cola() -> None:
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
            if valor:
                cola_reproduccion.encolar(valor)
                print(f"Se encoló: {valor}")
            else:
                print("La canción no puede estar vacía.")
        elif opcion == "2":
            try:
                print(f"Frente: {cola_reproduccion.ver_frente()}")
            except ColaVaciaError as error:
                print(error)
        elif opcion == "3":
            try:
                print(f"Se desencoló: {cola_reproduccion.desencolar()}")
            except ColaVaciaError as error:
                print(error)
        else:
            print("Opción inválida.")


def manejar_busqueda(catalogo, catalogo_ordenado: bool) -> None:
    print("\nBuscar título: 1) Lineal  2) Binaria")
    tipo = input("> ").strip()
    if tipo not in {"1", "2"}:
        print("Opción inválida.")
        return
    if tipo == "2" and not catalogo_ordenado:
        print("Error: ordená el catálogo por título antes de usar búsqueda binaria.")
        return
    clave = input("Ingresá el título exacto: ").strip()
    if tipo == "1":
        resultado = busqueda_lineal(catalogo, clave, lambda cancion: cancion.titulo)
    else:
        resultado = busqueda_binaria(catalogo, clave, lambda cancion: cancion.titulo)
    print(f"Encontrado: {resultado}" if resultado else "No encontrado.")


def manejar_ordenamiento(catalogo) -> bool:
    print("\nOrdenar por: 1) Título  2) Duración y, en empate, ID")
    criterio = input("> ").strip()
    print("Algoritmo: 1) Selección  2) Inserción")
    algoritmo = input("> ").strip()
    if criterio == "1":
        obtener_clave = lambda cancion: cancion.titulo
    elif criterio == "2":
        obtener_clave = lambda cancion: (cancion.duracion_seg, cancion.id)
    else:
        print("Opción inválida.")
        return False
    if algoritmo == "1":
        ordenar_seleccion(catalogo, obtener_clave)
    elif algoritmo == "2":
        ordenar_insercion(catalogo, obtener_clave)
    else:
        print("Opción inválida.")
        return False
    print("Catálogo ordenado.")
    return criterio == "1"


def manejar_archivos(catalogo) -> list[Cancion]:
    print("\nGuardar / cargar archivos")
    print("a) Cargar catálogo desde texto")
    print("b) Guardar catálogo en texto")
    print("c) Guardar catálogo en binario")
    print("d) Cargar catálogo desde binario")
    print("e) Probar archivo inválido o cargar una ruta manual")
    subopcion = input("Subopción > ").strip().lower()
    try:
        if subopcion == "a":
            catalogo = armar_catalogo_desde_txt(RUTA_TXT)
            print(f"Catálogo cargado desde texto: {len(catalogo)} canciones.")
        elif subopcion == "b":
            persistir_texto(catalogo)
            print("Catálogo guardado en texto.")
        elif subopcion == "c":
            guardar_binario(RUTA_BIN, catalogo)
            print("Catálogo guardado en binario (.bin).")
        elif subopcion == "d":
            catalogo = list(cargar_binario(RUTA_BIN))
            print(f"Catálogo cargado desde binario: {len(catalogo)} canciones.")
        elif subopcion == "e":
            ruta = Path(input("Ruta del archivo a probar: ").strip())
            catalogo = list(cargar_binario(ruta)) if ruta.suffix.lower() == ".bin" else armar_catalogo_desde_txt(ruta)
            print(f"Archivo cargado correctamente ({len(catalogo)} canciones).")
        else:
            print("Subopción inválida.")
    except (ArchivoInvalidoError, ValueError, KeyError) as error:
        print(f"Archivo inválido: {error}")
    return catalogo


def manejar_recursion() -> None:
    entrada = input("Ingresá el ID de la canción base: ").strip()
    try:
        cancion_id = int(entrada)
        BibliotecaMusical().mostrar_derivadas(cancion_id)
    except ValueError:
        print("Error: el ID debe ser un número entero.")
    except (FileNotFoundError, ArchivoInvalidoError) as error:
        print(f"Error al consultar versiones: {error}")


def mostrar_menu() -> None:
    nombre = TEMAS.get(TEMA, TEMA or "(sin tema)")
    print(f"\n=== {nombre} — AyED C2 2026 ===")
    print("1. Listar catálogo")
    print("2. Ver detalle")
    print("3. Buscar")
    print("4. Ordenar")
    print("5. Operación recursiva")
    print("6. Colección principal y ABM")
    print("7. Historial (pila)")
    print("8. Cola")
    print("9. Guardar / cargar archivos")
    print("0. Salir")


def main() -> None:
    if TEMA not in TEMAS:
        print("Seteá TEMA en src/config.py: 'pokedex', 'recetario' o 'musica'.")
        return
    catalogo = cargar_dataset()
    catalogo_ordenado = False
    while True:
        mostrar_menu()
        opcion = input("> ").strip()
        if opcion == "0":
            print("Chau.")
            return
        if opcion == "1":
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
            catalogo_ordenado = False
        elif opcion == "7":
            manejar_historial()
        elif opcion == "8":
            manejar_cola()
        elif opcion == "9":
            catalogo = manejar_archivos(catalogo)
            catalogo_ordenado = False
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()
