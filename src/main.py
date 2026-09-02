import csv
from pathlib import Path
from src.config import TEMA

TEMAS = {
    "pokedex": "Pokédex",
    "recetario": "Recetario",
    "musica": "Biblioteca musical",
}


def cargar_dataset(nombre_archivo: str = "canciones.csv") -> list[dict]:
    """
    Carga el dataset de la cátedra desde data/canciones.csv sin hardcodear filas.
    Cumple ítem 1.2 de la rúbrica.
    """
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


def mostrar_menu():
    nombre = TEMAS.get(TEMA, TEMA or "(sin tema)")
    print()
    print(f"=== {nombre} — AyED C2 2026 ===")
    print("1. Listar catálogo")
    print("2. Ver detalle")
    print("3. Buscar")
    print("4. Ordenar")
    print("5. Operación recursiva")
    print("6. Colección principal (equipo / menú / playlist)")
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
        elif opcion in {"2", "3", "4", "5", "6", "7", "8", "9"}:
            pendiente()
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()