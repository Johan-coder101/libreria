import streamlit as st
import pandas as pd
import os
from PIL import Image

class Libro:
    def __init__(self, titulo, autor, anio, genero, isbn):
        self.titulo = titulo
        self.autor = autor
        self.anio = anio
        self.genero = genero
        self.isbn = isbn

    def __str__(self):
        return f"📚 {self.titulo}\n👤 {self.autor}\n📅 {self.anio}\n📘 {self.genero}\nISBN: {self.isbn}"

class Inventario:
    def __init__(self):
        self.libros = []

    def agregar_libro(self, libro):
        self.libros.append(libro)

    def eliminar_libro(self, isbn):
        self.libros = [libro for libro in self.libros if libro.isbn != isbn]

    def buscar_libro(self, titulo):
        for libro in self.libros:
            if libro.titulo.lower() == titulo.lower():
                return libro
        return None

    def listar_libros(self):
        if not self.libros:
            return "No hay libros en el inventario."
        else:
            lista = ""
            for i, libro in enumerate(self.libros, start=1):
                lista += f"Libro {i}:\n{str(libro)}\n\n"
            return lista

    def actualizar_libro(self, isbn, nuevo_titulo, nuevo_autor, nuevo_anio, nuevo_genero):
        for libro in self.libros:
            if libro.isbn == isbn:
                libro.titulo = nuevo_titulo
                libro.autor = nuevo_autor
                libro.anio = nuevo_anio
                libro.genero = nuevo_genero
                return True
        return False

    def generar_csv(self):
        data = {
            "Título": [libro.titulo for libro in self.libros],
            "Autor": [libro.autor for libro in self.libros],
            "Año": [libro.anio for libro in self.libros],
            "Género": [libro.genero for libro in self.libros],
            "ISBN": [libro.isbn for libro in self.libros],
        }
        df = pd.DataFrame(data)
        return df.to_csv(index=False)

# Inicializa el inventario si no está en la sesión
if "inventario" not in st.session_state:
    st.session_state.inventario = Inventario()

inventario = st.session_state.inventario

# Verifica si el archivo de imagen existe y es válido
image_path = "logolib.jpg"
try:
    if os.path.exists(image_path):
        img = Image.open(image_path)
        st.sidebar.image(img, width=150)
    else:
        st.warning(f"La imagen '{image_path}' no se encuentra en el directorio actual.")
except Exception as e:
    st.error(f"Error al cargar la imagen: {e}")

st.title("Gestión de Inventario de Librería")

menu = ["Agregar libro", "Actualizar libro", "Eliminar libro", "Buscar libro", "Listar libros", "Salir"]
choice = st.sidebar.selectbox("Menú", menu)

# Botón de descarga de CSV
csv = inventario.generar_csv()
st.sidebar.download_button(label="Descargar CSV", data=csv, file_name="inventario_libros.csv", mime="text/csv")

if choice == "Agregar libro":
    st.subheader("Agregar un nuevo libro")
    with st.form(key="agregar_libro_form"):
        titulo = st.text_input("Título")
        autor = st.text_input("Autor")
        anio = st.text_input("Año")
        genero = st.text_input("Género")
        isbn = st.text_input("ISBN")
        submit_button = st.form_submit_button(label="Agregar")

        if submit_button:
            if titulo and autor and anio and genero and isbn:
                try:
                    anio = int(anio)
                    libro = Libro(titulo, autor, anio, genero, isbn)
                    inventario.agregar_libro(libro)
                    st.success("Libro agregado correctamente.")
                except ValueError:
                    st.error("El año debe ser un número entero.")
            else:
                st.error("Por favor, complete todos los campos.")

elif choice == "Actualizar libro":
    st.subheader("Actualizar un libro existente")
    with st.form(key="actualizar_libro_form"):
        isbn = st.text_input("ISBN del libro a actualizar")
        nuevo_titulo = st.text_input("Nuevo título")
        nuevo_autor = st.text_input("Nuevo autor")
        nuevo_anio = st.text_input("Nuevo año")
        nuevo_genero = st.text_input("Nuevo género")
        submit_button = st.form_submit_button(label="Actualizar")

        if submit_button:
            if isbn and nuevo_titulo and nuevo_autor and nuevo_anio and nuevo_genero:
                try:
                    nuevo_anio = int(nuevo_anio)
                    if inventario.actualizar_libro(isbn, nuevo_titulo, nuevo_autor, nuevo_anio, nuevo_genero):
                        st.success("Libro actualizado correctamente.")
                    else:
                        st.error("ISBN no encontrado en el inventario.")
                except ValueError:
                    st.error("El año debe ser un número entero.")
            else:
                st.error("Por favor, complete todos los campos.")

elif choice == "Eliminar libro":
    st.subheader("Eliminar un libro")
    with st.form(key="eliminar_libro_form"):
        isbn = st.text_input("ISBN del libro a eliminar")
        submit_button = st.form_submit_button(label="Eliminar")

        if submit_button:
            if isbn:
                inventario.eliminar_libro(isbn)
                st.success("Libro eliminado correctamente.")
            else:
                st.error("Por favor, ingrese el ISBN del libro a eliminar.")

elif choice == "Buscar libro":
    st.subheader("Buscar un libro por título")
    with st.form(key="buscar_libro_form"):
        titulo = st.text_input("Título del libro a buscar")
        submit_button = st.form_submit_button(label="Buscar")

        if submit_button:
            if titulo:
                libro = inventario.buscar_libro(titulo)
                if libro:
                    st.text_area("Detalles del libro", str(libro), height=200)
                else:
                    st.error("Libro no encontrado.")
            else:
                st.error("Por favor, ingrese el título del libro a buscar.")

elif choice == "Listar libros":
    st.subheader("Listado de libros en el inventario")
    libros_list = inventario.listar_libros()
    st.text_area("Listado de libros", libros_list, height=300)

elif choice == "Salir":
    st.write('<script>window.close();</script>', unsafe_allow_html=True)
    st.stop()
