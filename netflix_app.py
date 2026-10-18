import json

import pandas as pd
import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account
from sqlalchemy import text

st.set_page_config(page_title="Netflix app")

key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project=key_dict["project_id"])
dbMovies = db.collection("movies")

conn = st.connection("postgresql", type="sql")


@st.cache_data
def load_movies():
    movies_ref = list(dbMovies.stream())
    movies_dict = list(map(lambda x: x.to_dict(), movies_ref))
    return pd.DataFrame(movies_dict, columns=["name", "genre", "director", "company"])


def search_by_title(data, title):
    return data[data["name"].str.contains(title, case=False, na=False, regex=False)]


def filter_by_director(data, director):
    return data[data["director"] == director]


def insert_movie(name, genre, director, company):
    doc_ref = dbMovies.document(name)
    doc_ref.set({
        "name": name,
        "genre": genre,
        "director": director,
        "company": company,
    })


def insert_guest(email, comment):
    with conn.session as session:
        session.execute(
            text("INSERT INTO people (email, comment) VALUES (:email, :comment);"),
            {"email": email, "comment": comment},
        )
        session.commit()


def load_guests():
    with conn.session as session:
        result = session.execute(text("SELECT email, comment FROM people;"))
        return result.fetchall()


st.header("Netflix app")
data_load_state = st.text("Loading data...")
data = load_movies()
data_load_state.text("Done! (using st.cache_data)")

if "mensaje" in st.session_state:
    st.success(st.session_state.pop("mensaje"))

sidebar = st.sidebar

if sidebar.checkbox("Mostrar todos los filmes", value=True):
    st.subheader("Todos los filmes")
    st.dataframe(data)

titulo = sidebar.text_input("Título del filme :")
btnBuscar = sidebar.button("Buscar filmes")

if btnBuscar:
    filmes = search_by_title(data, titulo)
    st.write(f"Total filmes mostrados : {len(filmes)}")
    st.dataframe(filmes)

directores = sorted(data["director"].dropna().unique())
directorSel = sidebar.selectbox("Seleccionar Director", directores)
btnFiltrar = sidebar.button("Filtrar director")

if btnFiltrar:
    filmes = filter_by_director(data, directorSel)
    st.write(f"Total filmes : {len(filmes)}")
    st.dataframe(filmes)

sidebar.markdown("---")
sidebar.subheader("Nuevo filme")

with sidebar.form("nuevo_filme", clear_on_submit=True):
    name = st.text_input("Name")
    company = st.selectbox("Company", sorted(data["company"].dropna().unique()))
    director = st.selectbox("Director", directores)
    genre = st.selectbox("Genre", sorted(data["genre"].dropna().unique()))
    submit = st.form_submit_button("Crear nuevo filme")

if submit:
    if name:
        insert_movie(name, genre, director, company)
        load_movies.clear()
        st.session_state["mensaje"] = f"Filme '{name}' insertado correctamente"
        st.rerun()
    else:
        sidebar.error("Escribe el nombre del filme.")

sidebar.markdown("---")
sidebar.subheader("Libro de visitas")

with sidebar.form("libro_visitas", clear_on_submit=True):
    email = st.text_input("email :")
    comment = st.text_input("Comentario :")
    btnRegistrar = st.form_submit_button("Registrar Visita")

if btnRegistrar:
    if email and comment:
        insert_guest(email, comment)
        sidebar.success("Visita registrada, ¡gracias!")
    else:
        sidebar.error("Escribe tu email y un comentario.")

sidebar.markdown("---")
if sidebar.button("Ver visitas"):
    visitas = load_guests()
    if not visitas:
        sidebar.write("Aún no hay comentarios.")
    for i, (correo, comentario) in enumerate(visitas, start=1):
        sidebar.write(f"{i}.- {comentario} | {correo}")