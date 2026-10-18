# Netflix app — Dashboard de filmes

Dashboard interactivo en Streamlit conectado a Firestore (colección `movies`)
y a PostgreSQL en Aiven (base `guests`, tabla `people`).

## Funcionalidades
- Lectura de la colección `movies` en un DataFrame al arrancar.
- Checkbox para mostrar todos los filmes.
- Búsqueda por título (que contenga, sin distinguir mayúsculas/minúsculas).
- Filtro por director con total de filmes encontrados.
- Formulario para insertar filmes en Firestore.
- Libro de visitas: registrar y consultar comentarios en PostgreSQL.

## Archivos
| Archivo | Descripción |
|---|---|
| `netflix_app.py` | Aplicación principal |
| `requirements.txt` | Módulos de Python necesarios |
| `convertKeys.py` | Convierte `keys.json` a `.streamlit/secrets.toml` |
| `crearTablaPeople.py` | Crea la base `guests` y la tabla `people` |

## Ejecución local
```
python -m venv streamlit-env
source streamlit-env/Scripts/activate
pip install -r requirements.txt
streamlit run netflix_app.py
```
Las credenciales van en `.streamlit/secrets.toml` (no se subió al rep)