# TP integrador — AyED C2 2026

Repositorio del grupo para el trabajo integrador de Algoritmos y Estructuras de Datos.

### Integrantes

| Nombre | Mail | GitHub |
| :--- | :--- | :--- |
| Nicolás Randazzo | nicorandazzo03@hotmail.com | r4nd4zz0 |
| Mauricio Medina | mauriciomedinamt@gmail.com | mauricio0004 |

**Tema elegido:** Biblioteca musical.

## Requisitos y ejecución

- Python 3.10 o superior.
- No requiere paquetes externos; utiliza la biblioteca estándar.
- Desde la raíz del repositorio:

```bash
python -m src.main
```

En Windows también se puede ejecutar con `py -3 -m src.main`.

El tema se configura en `src/config.py` (`TEMA = "musica"`). El catálogo inicial y las relaciones de versiones se leen de `data/canciones.csv` y `data/versiones.csv`. No es necesario instalar dependencias.

## Operaciones del menú

1. Listar el catálogo usando el iterador.
2. Ver el detalle de una canción por ID.
3. Buscar por título con búsqueda lineal; la binaria se habilita luego de ordenar por título.
4. Ordenar por título o por duración (desempate por ID), mediante selección o inserción.
5. Recorrer recursivamente las versiones derivadas.
6. Administrar la colección enlazada y realizar alta, modificación y baja persistentes de canciones.
7. Apilar, consultar el tope y desapilar acciones del historial.
8. Encolar, consultar el frente y desencolar canciones.
9. Cargar y guardar el catálogo en texto o en binario.
0. Salir.

Las altas, modificaciones y bajas del catálogo actualizan `data/canciones.csv`; también mantienen `data/canciones.bin` cuando se realizan por el submenú ABM. El archivo binario se genera al usar esa opción o la opción de guardar en binario. No se debe versionar el `.bin` generado.

## Limitaciones conocidas

- La búsqueda binaria es por título exacto y exige que el catálogo esté ordenado por título en la sesión actual.
- Pila, cola y colección auxiliar viven en memoria y se pierden al cerrar el programa; la persistencia requerida se aplica al catálogo.
- El formato binario tiene campos de texto de ancho fijo y puede recortar cadenas que excedan su capacidad; para texto con bytes UTF-8 multibyte, el recorte puede afectar el último carácter.
- El lector de texto implementado espera filas simples separadas por comas; no interpreta comas escapadas entre comillas.
- Los resultados de la regresión final deben corresponder a la ejecución del protocolo incluida en `docs/PROTOCOLO_PRUEBAS.md`.

## Documentación

- Informe del proyecto: [`docs/INFORME.md`](docs/INFORME.md).
- Protocolo de regresión: [`docs/PROTOCOLO_PRUEBAS.md`](docs/PROTOCOLO_PRUEBAS.md).
- Declaración de uso de IA: [`docs/DECLARACION_IA.md`](docs/DECLARACION_IA.md).
- Convenciones de Git y entregas: [`GIT.md`](GIT.md).
