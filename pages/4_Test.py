import streamlit as st
import sqlite3
import pandas as pd
from datetime import date

# Configurar la base de datos
def init_db():
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reader TEXT NOT NULL,
            title TEXT NOT NULL,
            total_pages INTEGER NOT NULL,
            date TEXT,
            progress INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

# Función para agregar un libro
def add_book(title, reader, total_pages):
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, reader, total_pages, date, progress) VALUES (?, ?, ?, ?, ?)",
                   (title, reader, total_pages, None, 0))
    conn.commit()
    conn.close()

# Función para borrar un libro
def delete_book(book_id):
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()

# Función para registrar progreso
def add_progress(book_id, pages_read):
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE books
        SET progress = progress + ?,
            date = ?
        WHERE id = ?
    """, (pages_read, date.today().isoformat(), book_id))
    conn.commit()
    conn.close()

# Función para obtener los libros
def get_books():
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, reader, title, total_pages, progress FROM books")
    books = cursor.fetchall()
    conn.close()
    return books

# Función para obtener el progreso
def get_progress():
    conn = sqlite3.connect("books.db")
    query = """
        SELECT reader,date, title, total_pages, progress
        FROM books
        WHERE progress > 0
        AND date = (SELECT MAX(date) FROM books);

    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Inicializar la base de datos
init_db()

# Configuración de la página
st.set_page_config(page_title="Reading Tracker", page_icon="📚")

# Descripción de la app
st.title(":blue[Reading Tracker]: Track Your Reading Progress")
st.write(
    """
    This app helps you keep track of the books you're reading and your daily progress. 
    Add your books, log the pages you read each day, and analyze your reading trends 
    with interactive visualizations and summaries. Stay motivated and achieve your 
    reading goals effortlessly!
    """
)

# Interfaz de Streamlit
st.sidebar.header("Options")

# Agregar un nuevo libro
if st.sidebar.checkbox("Add a new book"):
    with st.form("add_book_form"):
        title = st.text_input("Book Title")
        reader = st.text_input("Reader")
        total_pages = st.number_input("Total Pages", min_value=1, step=1)
        submitted = st.form_submit_button("Add Book")

        if submitted:
            if title and reader and total_pages > 0:
                add_book(title, reader, total_pages)
                st.success(f"The book '{title}' was successfully added.")
            else:
                st.error("Please fill out all fields correctly.")

# Eliminar un libro
if st.sidebar.checkbox("Delete a book"):
    books = get_books()
    if books:
        book_titles = {book[2]: book[0] for book in books}  # Mapeo de título a ID
        selected_book = st.sidebar.selectbox("Select a book to delete", list(book_titles.keys()))
        if st.sidebar.button("Delete Book"):
            delete_book(book_titles[selected_book])
            st.success(f"The book '{selected_book}' was successfully deleted.")
    else:
        st.sidebar.warning("No books available to delete.")

# Registrar progreso diario
books = get_books()
if books:
    book_titles = {book[2]: book[0] for book in books}  # Mapeo de título a ID
    st.sidebar.subheader("Log Daily Progress")
    selected_book = st.sidebar.selectbox("Select a book", list(book_titles.keys()))
    pages_read = st.sidebar.number_input("Pages read today", min_value=1, step=1)
    if st.sidebar.button("Log Progress"):
        add_progress(book_titles[selected_book], pages_read)
        st.success(f"Progress logged for '{selected_book}'.")
else:
    st.sidebar.warning("No books registered. Add one first.")

# Mostrar análisis
st.header("📊 Reading Analysis")
progress_data = get_progress()
if not progress_data.empty:
    st.subheader("Progress Summary")
    
    progress_data['completed'] =  progress_data['progress'] /  progress_data['total_pages']
    progress_data['completed']  = progress_data['completed'] .apply(lambda x: f'{x:.2f}%')
    st.dataframe(progress_data)

    st.subheader("Pages Read Per Book")
    book_summary = progress_data.groupby("title")["progress"].sum().reset_index()
    book_summary = book_summary.rename(columns={"progress": "Total Read"})
    st.bar_chart(book_summary, x="title", y="Total Read")
    
    
    
    st.subheader("Pages Read Per Reader")
    book_summary = progress_data.groupby("reader")["progress"].sum().reset_index()
    book_summary = book_summary.rename(columns={"progress": "Total Read"})
    st.bar_chart(book_summary, x="reader", y="Total Read")
    
    
    # Llamar a la función para obtener los datos
    progress_data_2 = get_progress()
   

    # Asegurarse de que 'date' sea de tipo datetime
    progress_data_2['date'] = pd.to_datetime(progress_data_2['date'])

    # Pivotar el DataFrame para que cada título sea una columna
    pivot_data = progress_data_2.pivot(index='date', columns='title', values='progress')

    # Mostrar el gráfico de líneas en Streamlit
    st.line_chart(pivot_data)
else:
    st.info("No progress data yet. Start logging your daily reading.")
