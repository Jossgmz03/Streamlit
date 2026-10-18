"""
Crea la base de datos guests y la tabla people (email, comment) en Aiven.
Se ejecuta una sola vez:  python crearTablaPeople.py
"""

import tomllib

import psycopg2

# Lee los datos de conexión desde .streamlit/secrets.toml
with open(".streamlit/secrets.toml", "rb") as archivo:
    cfg = tomllib.load(archivo)["connections"]["postgresql"]


def conectar(base_de_datos):
    return psycopg2.connect(
        host=cfg["host"],
        port=int(cfg["port"]),
        dbname=base_de_datos,
        user=cfg["username"],
        password=cfg["password"],
        sslmode="require",
    )


# 1) Crear la base de datos guests (Aiven trae por defecto la base defaultdb)
conn = conectar("defaultdb")
conn.autocommit = True
with conn.cursor() as cur:
    cur.execute("SELECT 1 FROM pg_database WHERE datname = 'guests';")
    if cur.fetchone():
        print("La base de datos 'guests' ya existía.")
    else:
        cur.execute("CREATE DATABASE guests;")
        print("Base de datos 'guests' creada.")
conn.close()

# 2) Crear la tabla people dentro de guests
conn = conectar("guests")
with conn:
    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS people(
               email   VARCHAR(100),
               comment VARCHAR(500)
            );
            """
        )
        cur.execute("SELECT * FROM people;")
        print("Tabla 'people' lista. Registros actuales:", cur.fetchall())
conn.close()