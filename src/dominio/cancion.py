from dataclasses import dataclass


@dataclass(frozen=True)
class Cancion:
    """Representa una canción del catálogo musical."""

    id: int
    titulo: str
    artista: str
    album: str
    genero: str
    anio: int
    duracion_seg: int

    @classmethod
    def from_dict(cls, fila: dict) -> "Cancion":
        return cls(
            id=int(fila["id"]),
            titulo=fila["titulo"],
            artista=fila["artista"],
            album=fila["album"],
            genero=fila["genero"],
            anio=int(fila["anio"]),
            duracion_seg=int(fila["duracion_seg"]),
        )

    def __str__(self) -> str:
        return f"[{self.id}] {self.titulo} - {self.artista} ({self.album}, {self.anio})"
