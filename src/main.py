import csv
from pathlib import Path

from src.config import TEMA
from src.excepciones import ColaVaciaError, PilaVaciaError
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


def cargar_dataset(nombre_archivo: str = "canciones.csv") -> list[dict]:
    """Carga el dataset de la cátedra desde data/canciones.csv sin hardcodear filas."""
    ruta_archivo = Path(__file__).resolve().parent.parent / "data" / nombre_archivo

    if not ruta_archivo.is_file():
        print(f"Error: no se encontró el archivo en {ruta_archivo}")
        return []

    catalogo = []
    with open(ruta_archivo, mode="r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            catalogo.append(fila)

    return catalogo


def listar_catalogo(catalogo: list[dict]) -> None:
    """Muestra los elementos cargados en memoria."""
    if not catalogo:
        print("El catálogo está vacío o no se pudo cargar.")
        return

    print(f"\n--- Catálogo cargado ({len(catalogo)} canciones) ---")
    for cancion in catalogo:
        print(f"[{cancion['id']}] {cancion['titulo']} - {cancion['artista']} ({cancion['album']}, {cancion['anio']})")


def pendiente():
    print("Todavía no está implementado. Completar en la entrega que corresponde.")


def manejar_coleccion_principal():
    while True:
        print("\nColección principal")
        print("1. Agregar elemento")
        print("2. Ver colección")
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
    opcion = None

    while opcion != "0":
        mostrar_menu()
        opcion = input("> ").strip()

        if opcion == "0":
            print("Chau.")
        elif opcion == "1":
            listar_catalogo(catalogo)
        elif opcion == "2":
            pendiente()
        elif opcion == "3":
            pendiente()
        elif opcion == "4":
            pendiente()
        elif opcion == "5":
            pendiente()
        elif opcion == "6":
            manejar_coleccion_principal()
        elif opcion == "7":
            manejar_historial()
        elif opcion == "8":
            manejar_cola()
        elif opcion == "9":
            pendiente()
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()
