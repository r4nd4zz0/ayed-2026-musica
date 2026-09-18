from dataclasses import dataclass


@dataclass(frozen=True)
class VersionCancion:
    """Representa una versión derivada de una canción."""

    cancion_id: int
    version_de_id: int
    tipo: str

    @classmethod
    def from_dict(cls, fila: dict) -> "VersionCancion":
        return cls(
            cancion_id=int(fila["cancion_id"]),
            version_de_id=int(fila["version_de_id"]),
            tipo=fila["tipo"],
        )

    def __str__(self) -> str:
        return f"{self.cancion_id} -> {self.version_de_id} ({self.tipo})"
