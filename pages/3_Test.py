import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px



from forex_python.converter import CurrencyRates

# Crear una instancia de CurrencyRates
cr = CurrencyRates()

st.write("hola")

# Obtener la tasa de cambio actual entre USD y EUR
exchange_rate = cr.get_rate("USD","EUR")



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


#if GAI_value > 0 and country_value != "" :
#    if country_value == "UK":
#        st.write(f"Your total taxes for a gross annual income of {pound_symbol}{format_number(GAI_value)} is: {pound_symbol}{format_number(taxes)}")
#    else:
#        st.write(f"Your total taxes for a gross annual income of {format_number(GAI_value)}{euro_symbol} is: {format_number(taxes)}{euro_symbol}")
