# TP integrador — AyED C2 2026

Aplicación de consola desarrollada en Python para gestionar una biblioteca musical y practicar estructuras de datos, recursión, algoritmos, persistencia y análisis de complejidad.

### Integrantes

| Nombre | Mail | GitHub |
| :--- | :--- | :--- |
| Nicolás Randazzo | nicorandazzo03@hotmail.com | r4nd4zz0 |
| Mauricio Medina | mauriciomedinamt@gmail.com | mauricio0004 |

## Tema elegido

**Biblioteca musical.** El programa administra canciones con identificador, título, artista, álbum, género, año y duración. También representa relaciones entre una canción original y sus versiones derivadas, como covers, versiones en vivo y remixes.

Las operaciones disponibles desde el menú incluyen:

- listar y buscar canciones;
- ordenar el catálogo por título o duración;
- mostrar recursivamente las versiones derivadas de una canción;
- gestionar una lista enlazada, una pila de historial y una cola de reproducción;
- agregar, modificar y eliminar canciones;
- guardar y cargar datos en CSV y en archivos binarios con registro de longitud fija.

Los datos de origen se encuentran en `data/canciones.csv` y `data/versiones.csv`.

## Cómo ejecutar

Requisitos:

- Python 3.10 o superior;
- no se requieren paquetes externos;
- ejecutar desde la raíz del repositorio.

```bash
python -m src.main
```

En Windows, si `python` no está disponible:

```powershell
py -3 -m src.main
```

En Linux/macOS también puede estar disponible el comando `python3`:

```bash
python3 -m src.main
```

El programa utiliza archivos existentes dentro de `data/`. Las operaciones de ABM pueden crear o modificar `data/canciones.csv` y `data/canciones.bin`.

## Pruebas manuales

No existe una suite automatizada ni un framework de testing. Para comprobar el funcionamiento:

1. Ejecutar `python -m src.main`.
2. Seleccionar `1` para listar el catálogo.
3. Seleccionar `3` y probar las búsquedas lineal y binaria.
4. Antes de probar la búsqueda binaria, seleccionar `4` y ordenar el catálogo por título.
5. Seleccionar `5` e ingresar el ID `1` para comprobar las versiones derivadas.
6. Probar el alta, modificación y baja desde la opción `6`.
7. Verificar que las operaciones de guardar/cargar funcionan desde la opción `9`.

Los casos esperados y el protocolo de pruebas se documentan en [`docs/PROTOCOLO_PRUEBAS.md`](docs/PROTOCOLO_PRUEBAS.md).

## Limitaciones conocidas

- Es una aplicación de consola; no posee interfaz gráfica ni API web.
- No utiliza una base de datos externa ni una biblioteca de persistencia adicional.
- Las búsquedas son exactas por título en el caso binario. La búsqueda lineal implementada coincide el título completo recibido por la entrada.
- Para usar la búsqueda binaria, el catálogo debe haberse ordenado previamente por título desde el menú.
- El archivo binario utiliza campos de texto de ancho fijo. Los textos más largos que los anchos definidos se recortan al guardar.
- Los archivos CSV se procesan con el separador coma; los datos y encabezados deben respetar su formato.
- La colección principal, el historial y la cola son estructuras en memoria y no persisten al cerrar el programa, salvo el catálogo administrado en CSV y binario.
- El programa no reproduce audio ni se conecta a servicios musicales externos.
- Actualmente no cuenta con pruebas unitarias automatizadas ni CI.
- Al ser un TP académico, algunas operaciones aceptan datos simples sin validaciones tan completas como las de una aplicación de producción.

## Documentación

- [`docs/INFORME.md`](docs/INFORME.md): modelo, recursión, TADs, complejidad y persistencia.
- [`docs/PROTOCOLO_PRUEBAS.md`](docs/PROTOCOLO_PRUEBAS.md): protocolo de pruebas.
- [`docs/DECLARACION_IA.md`](docs/DECLARACION_IA.md): declaración de uso de herramientas de IA.
- [`GIT.md`](GIT.md): instrucciones mínimas de Git y etiquetado.

## Entregas

Cada vencimiento se marca con un tag. Ver `GIT.md`.

| Tag | Vence |
| --- | --- |
| `preentrega` (opcional, solo repo) | domingo 30-ago-2026 23:59 |
| `entrega-1` | domingo 06-sep-2026 23:59 |
| `entrega-2` | domingo 20-sep-2026 23:59 |
| `entrega-3` | domingo 04-oct-2026 23:59 |
| `entrega-4` | domingo 01-nov-2026 23:59 |
| `entrega-5` | domingo 15-nov-2026 23:59 |
| `entrega-6` | domingo 22-nov-2026 23:59 |

Defensa oral (reemplaza el 2do parcial): 25 y 27-nov-2026.

La cátedra corrige el **tag**, no el último commit suelto de `main`.

El grupo se avisa por mail a diego.ambrossio@unab.edu.ar **y** angel.bianco@unab.edu.ar. Ver `GIT.md`.
