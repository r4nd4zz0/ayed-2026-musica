import csv
from collections import defaultdict
from pathlib import Path
from src.dominio.cancion import Cancion
from src.dominio.version import VersionCancion
from src.tads.lista_enlazada import ListaEnlazada
from src.excepciones import ColeccionLlenaError
class BibliotecaMusical:
    def __init__(self, carpeta_datos: str | Path | None = None):
        if carpeta_datos is None:
            carpeta_datos = Path(__file__).resolve().parents[2] / "data"
        self.carpeta_datos = Path(carpeta_datos)
        self.canciones: dict[int, Cancion] = {}
        self.versiones_por_base: dict[int, list[VersionCancion]] = defaultdict(list)
        self.cargar_datos()
    def cargar_datos(self) -> None:
        ruta_canciones = self.carpeta_datos / "canciones.csv"
        ruta_versiones = self.carpeta_datos / "versiones.csv"
        if not ruta_canciones.exists() or not ruta_versiones.exists():
            raise FileNotFoundError("No se encontraron los archivos CSV del tema música.")
        with open(ruta_canciones, encoding="utf-8", newline="") as archivo:
            for fila in csv.DictReader(archivo):
                cancion = Cancion.from_dict(fila)
                self.canciones[cancion.id] = cancion
        with open(ruta_versiones, encoding="utf-8", newline="") as archivo:
            for fila in csv.DictReader(archivo):
                version = VersionCancion.from_dict(fila)
                self.versiones_por_base[version.version_de_id].append(version)
    def obtener_cancion(self, cancion_id: int) -> Cancion:
        if cancion_id not in self.canciones:
            raise KeyError(f"No existe la canción con id {cancion_id}.")
        return self.canciones[cancion_id]
    def listar_catalogo(self) -> list[Cancion]:
        return list(self.canciones.values())
    def buscar_por_titulo(self, texto: str) -> list[Cancion]:
        texto = texto.lower().strip()
        if not texto:
            return []
        return [
            cancion
            for cancion in self.canciones.values()
            if texto in cancion.titulo.lower()
        ]
    def derivadas_de(self, cancion_id: int, visitadas: set[int] | None = None) -> list[VersionCancion]:
        if visitadas is None:
            visitadas = set()
        if cancion_id in visitadas:
            return []
        visitadas.add(cancion_id)
        resultado: list[VersionCancion] = []
        for version in self.versiones_por_base.get(cancion_id, []):
            resultado.append(version)
            resultado.extend(self.derivadas_de(version.cancion_id, visitadas))
        return resultado
    def mostrar_derivadas(self, cancion_id: int) -> None:
        try:
            cancion = self.obtener_cancion(cancion_id)
        except KeyError:
            print(f"No existe la canción con id {cancion_id}.")
            return
        derivadas = self.derivadas_de(cancion_id)
        print(f"\nVersiones derivadas de: {cancion.titulo} [{cancion.id}]")
        if not derivadas:
            print("No tiene versiones derivadas.")
            return
        def imprimir_hijos(base_id: int, nivel: int = 0) -> None:
            for version in self.versiones_por_base.get(base_id, []):
                actual = self.obtener_cancion(version.cancion_id)
                print(f"{'  ' * nivel}- {actual.titulo} ({version.tipo})")
                imprimir_hijos(version.cancion_id, nivel + 1)
        imprimir_hijos(cancion_id)
class Playlist:
    def __init__(self, tope=10):
        self._canciones = ListaEnlazada()
        self._tope = tope
    def agregar(self, cancion):
        if self._canciones.tamanio() >= self._tope:
            raise ColeccionLlenaError(f"La playlist está llena (máximo {self._tope}).")
        self._canciones.insertar_al_final(cancion)
    def listar(self):
        for cancion in self._canciones:
            print(f" - {cancion.titulo}")