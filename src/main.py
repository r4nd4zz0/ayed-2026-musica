from pathlib import Path

from src.config import TEMA
from src.dominio.biblioteca import BibliotecaMusical

TEMAS = {
    "pokedex": "Pokédex",
    "recetario": "Recetario",
    "musica": "Biblioteca musical",
}

biblioteca = BibliotecaMusical(Path(__file__).resolve().parent.parent / "data")


def listar_catalogo() -> None:
    canciones = biblioteca.listar_catalogo()
    if not canciones:
        print("El catálogo está vacío o no se pudo cargar.")
        return

    print(f"\n--- Catálogo cargado ({len(canciones)} canciones) ---")
    for cancion in canciones:
        print(f"[{cancion.id}] {cancion.titulo} - {cancion.artista} ({cancion.album}, {cancion.anio})")


def ver_detalle() -> None:
    try:
        dato = int(input("Ingresá el id de la canción: ").strip())
    except ValueError:
        print("El id debe ser un número entero.")
        return

    try:
        cancion = biblioteca.obtener_cancion(dato)
    except KeyError:
        print(f"No existe la canción con id {dato}.")
        return

    print("\nDetalle de canción:")
    print(f"- id: {cancion.id}")
    print(f"- título: {cancion.titulo}")
    print(f"- artista: {cancion.artista}")
    print(f"- álbum: {cancion.album}")
    print(f"- género: {cancion.genero}")
    print(f"- año: {cancion.anio}")
    print(f"- duración: {cancion.duracion_seg} s")


def buscar_cancion() -> None:
    texto = input("Ingresá texto para buscar por título: ").strip()
    resultados = biblioteca.buscar_por_titulo(texto)
    if not resultados:
        print("No se encontraron canciones con ese texto.")
        return

    print(f"\nResultados ({len(resultados)}):")
    for cancion in resultados:
        print(f"[{cancion.id}] {cancion.titulo} - {cancion.artista}")


def operacion_recursiva() -> None:
    try:
        dato = int(input("Ingresá el id de la canción base: ").strip())
    except ValueError:
        print("El id debe ser un número entero.")
        return

    biblioteca.mostrar_derivadas(dato)


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

    opcion = None
    while opcion != "0":
        mostrar_menu()
        opcion = input("> ").strip()
        if opcion == "0":
            print("Chau.")
        elif opcion == "1":
            listar_catalogo()
        elif opcion == "2":
            ver_detalle()
        elif opcion == "3":
            buscar_cancion()
        elif opcion == "4":
            print("Todavía no está implementado. Completar en la entrega que corresponde.")
        elif opcion == "5":
            operacion_recursiva()
        elif opcion in {"6", "7", "8", "9"}:
            print("Todavía no está implementado. Completar en la entrega que corresponde.")
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()
