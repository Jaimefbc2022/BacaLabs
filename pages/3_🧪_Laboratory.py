import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def show_content(password):
    correct_password = "29018"
    return correct_password == password

# Configura los estados iniciales si no existen
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    # Mostrar el input de contraseña
    password = st.text_input("Enter a password", type="password")

    if show_content(password):
        st.session_state.authenticated = True
        st.rerun()
    else:
        if password:  # Evitar mostrar error al inicio
            st.error("Incorrect password. Please try again. Hint: ZIP")

if st.session_state.authenticated:
    # Este bloque se ejecuta después de que el usuario ingresa la contraseña correcta
    st.write("Password correct! Welcome to the application.")


    # Create a sidebar selection
    selection = st.sidebar.radio(
        "Test page hiding",
        ["Show all pages", "Hide pages 1 and 2", "Hide Other apps Section"],
    )

    # Define a list of pages
    pages = ["Example One", "Example Two", "Other apps"]

    # Define a function to hide selected pages
    def hide_pages(pages_to_hide):
        for page in pages_to_hide:
            st.sidebar.markdown(f"## {page}")
            st.sidebar.markdown("This page is hidden.")

    # Main app content
    if selection == "Show all pages":
        # Display all pages in the sidebar
        for page in pages:
            st.sidebar.markdown(f"## {page}")
            st.sidebar.markdown("This is a sample page.")
    elif selection == "Hide pages 1 and 2":
        # Hide pages 1 and 2
        pages_to_hide = ["Example One", "Example Two"]
        hide_pages(pages_to_hide)
    elif selection == "Hide Other apps Section":
        # Hide the "Other apps" section
        pages_to_hide = ["Other apps"]
        hide_pages(pages_to_hide)

    # Add some content to the main area of the app
    st.title("Main Content")
    st.selectbox("test_select", options=["1", "2", "3"])




    # Crear el DataFrame con los datos proporcionados
    data = [
        ["Spain", "Tax", 1, 1, 0, 5500, 0.00],
        ["Spain", "Tax", 1, 2, 5500, 12450, 0.19],
        ["Spain", "Tax", 1, 3, 12450, 20200, 0.24],
        ["Spain", "Tax", 1, 4, 20200, 35200, 0.30],
        ["Spain", "Tax", 1, 5, 35200, 60000, 0.37],
        ["Spain", "Tax", 1, 6, 60000, 300000, 0.45],
        ["Spain", "Tax", 1, 7, 300000, 1e+22, 0.47],
        ["UK", "Tax", 1, 1, 0, 12570, 0.00],
        ["UK", "Tax", 1, 2, 12570, 50270, 0.20],
        ["UK", "Tax", 1, 3, 50270, 125140, 0.40],
        ["UK", "Tax", 1, 4, 125140, 1e+22, 0.45],
        ["UK", "NI", 2, 1, 0, 12570, 0.00],
        ["UK", "NI", 2, 2, 12570, 50270, 0.08],
        ["UK", "NI", 2, 3, 50270, 1e+22, 0.02]
    ]

    # Crear el DataFrame
    df = pd.DataFrame(data, columns=["Country", "Type", "TypeCode", "Range", "From", "To", "Percentage"])

    # Filtrar solo los datos de impuestos (Tax)
    df_tax = df[df["Type"] == "Tax"]

    # Crear un DataFrame para los valores de impuestos de cada país
    df_pivot = df_tax.pivot_table(index="Range", columns="Country", values="Percentage", aggfunc="sum", fill_value=0)

    # Crear un gráfico de barras apiladas con Streamlit
    st.bar_chart(df_pivot)


    st.divider()


    # Crear el DataFrame con los datos proporcionados
    data = [
        ["Spain", "Net Salary", 10],
        ["Spain", "Income Tax", 5],
        ["Spain", "National Insurance", 3],
        
        ["UK", "Net Salary", 12],  
        ["UK", "Income Tax", 3],
        ["UK", "National Insurance", 3]
    ]

    # Crear el DataFrame
    df = pd.DataFrame(data, columns=["Country", "Type", "Range"])

    # Crear un gráfico de barras apiladas con Plotly
    fig = px.bar(df, 
                x="Country", 
                y="Range",
                text_auto='.2s',# Usamos el rango para los valores de las barras
                color="Type",  # El color de las barras será por el tipo (columna)
                title="Impuestos por Rango de Ingresos - España vs Reino Unido", 
                labels={"Range": "Values"},  # Etiqueta para los valores del eje Y
                barmode="stack")

    fig.update_traces(textfont_size=12, textangle=0, textposition="inside", cliponaxis=False)

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)






    st.divider()




    Country_chart = pd.DataFrame({
        "Country": ["Spain", "UK"],  # Países (eje x)
        "Value": [15, 20]           # Valores (eje y)
    })

    # Configurar el índice para que sea el eje x
    Country_chart = Country_chart.set_index("Country")


    st.bar_chart(Country_chart)

    st.code(
        ''' import streamlit as st

        def show_content(password):
            correct_password = ""
            return correct_password == password

        # Configura los estados iniciales si no existen
        if "authenticated" not in st.session_state:
            st.session_state.authenticated = False
            

        if not st.session_state.authenticated:
            # Mostrar el input de contraseña
            password = st.text_input("Enter a password", type="password")

            if show_content(password):
                st.session_state.authenticated = True
                st.rerun()
            else:
                if password:  # Evitar mostrar error al inicio
                    st.error("Incorrect password. Please try again.")

        if st.session_state.authenticated:
            # Este bloque se ejecuta después de que el usuario ingresa la contraseña correcta
            st.write("Password correct! Welcome to the application.")
        ''', 
    language = "python"
    )
