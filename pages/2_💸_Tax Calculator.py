import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from function_CalculateTaxes import calculate_Taxes
from function_FormatNumber import format_number, format_number_and_currency
from function_currencyExchange import get_exchange_rate

st.set_page_config(page_title="Tax Calculator", page_icon="💸")

st.title(":blue[Tax Calculator]: Crunch Your Numbers ")
#st.markdown("# Tax Calculator")
#st.sidebar.header("Tax Calculator")

st.write(
    """
    This app provides an intuitive and interactive way to calculate taxes
    and net salary for individuals in the UK and Spain. Simply input your
    gross income, select your country, and let the app handle the calculations,
    presenting you with clear visualizations and detailed breakdowns. 
    Explore how taxes impact your earnings effortlessly!
    """
)






st.write("### Input Data")
col1, col2 = st.columns(2)


country_value = col1.selectbox(
    "Country",
    options=["UK", "Spain"],  # Opciones más claras
    index=0  # Por defecto selecciona la primera opción
)
GAI_value = col2.number_input("Gross Annual Income", min_value = 0, value= 39000 )


total_taxes = calculate_Taxes(GAI_value, country_value)[0]
total_taxes_percentage = total_taxes / GAI_value

total_Income_taxes = calculate_Taxes(GAI_value, country_value)[1]
total_Income_taxes_percentage = total_Income_taxes / GAI_value

total_NI_taxes = calculate_Taxes(GAI_value, country_value)[2]
total_NI_taxes_percentage = total_NI_taxes / GAI_value

net_Annual_Salary = GAI_value - total_taxes
net_Monthly_Salary = net_Annual_Salary/12

st.divider()

st.write("### Ouput Data")




col1,col2 = st.columns(2)
col1.metric(label="Gross Annual Income", value=f"{format_number_and_currency(GAI_value,country_value)}")
col2.metric(label="Total Income Tax", value=f"{format_number_and_currency(total_taxes,country_value)}")
col1.metric(label="Net Annual Salary", value=f"{format_number_and_currency(net_Annual_Salary,country_value)}")
col2.metric(label="Net Monthly Salary", value=f"{format_number_and_currency(net_Monthly_Salary,country_value)}")

st.divider()

st.write("### Take-home money breakdown - Spain vs the UK")
# Create Chart Dataframe


data = [
    ["Spain", "Net Salary",GAI_value - calculate_Taxes(GAI_value, "Spain")[0]],
    ["Spain", "Income Tax", calculate_Taxes(GAI_value, "Spain")[1]],
    ["Spain", "National Insurance", calculate_Taxes(GAI_value, "Spain")[2]],
    
    ["UK", "Net Salary",GAI_value - calculate_Taxes(GAI_value, "UK")[0]],
    ["UK", "Income Tax", calculate_Taxes(GAI_value, "UK")[1]],
    ["UK", "National Insurance", calculate_Taxes(GAI_value, "UK")[2]]
]

# Crear el DataFrame
df = pd.DataFrame(data, columns=["Country", "Type", "Value"])

# Definir colores personalizados para cada tipo
color_map = {
    "Net Salary": "green",  # Color para "Net Salary"
    "Income Tax": "red",  # Color para "Income Tax"
    "National Insurance": "lightcoral"  # Color para "National Insurance"
}

# Crear un gráfico de barras apiladas con Plotly
fig = px.bar(df, 
             x="Country", 
             y="Value",
             text_auto='.2s',
             color="Type",  # El color de las barras será por el tipo (columna)
             #title="Take-home money breakdown - Spain vs the UK", 
             labels={"Value": "Values"},  # Etiqueta para los valores del eje Y
             barmode="stack",
             color_discrete_map=color_map)  # Asignar colores personalizados

fig.update_traces(
    textfont_size=12, 
    textangle=0, 
    textposition="auto", 
    cliponaxis=False,
    marker=dict(cornerradius=10), # Aplicar el redondeo de las barras
)

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig)



st.divider()

mode = st.radio(
        "Set currency exchange 👇",
        ["No Conversion", "Convert to EUR", "Convert to GBP"],
        key="visibility",
        horizontal=True,
    )


if mode == "No Conversion":
    
    exchange = 0
    
    gross_salary_SP = format_number_and_currency(GAI_value, "Spain")
    income_tax_SP = format_number_and_currency(calculate_Taxes(GAI_value, "Spain")[1], "Spain")
    NI_tax_SP = format_number_and_currency(calculate_Taxes(GAI_value, "Spain")[2], "Spain")
    total_tax_SP = format_number_and_currency(calculate_Taxes(GAI_value, "Spain")[0], "Spain")
    net_salary_SP = format_number_and_currency(GAI_value - calculate_Taxes(GAI_value, "Spain")[0], "Spain")
    
    gross_salary_UK = format_number_and_currency(GAI_value, "UK")
    income_tax_UK = format_number_and_currency(calculate_Taxes(GAI_value, "UK")[1], "UK")
    NI_tax_UK = format_number_and_currency(calculate_Taxes(GAI_value, "UK")[2], "UK")
    total_tax_UK = format_number_and_currency(calculate_Taxes(GAI_value, "UK")[0], "UK")
    net_salary_UK = format_number_and_currency(GAI_value - calculate_Taxes(GAI_value, "UK")[0], "UK")
    
    message = ""
    #f"The amount of :blue-background[_{gross_salary_SP}_] is equivalent to :orange-background[_{gross_salary_UK}_] based on the current exchange rate (:violet-background[{exchange} GBP/EUR]). The total taxes amount to :red-background[{total_tax_UK}]."

elif mode == "Convert to EUR":
    
    exchange = float(get_exchange_rate("GBP","EUR"))
    
    gross_salary_SP = format_number_and_currency(GAI_value, "Spain")
    income_tax_SP = format_number_and_currency(calculate_Taxes(GAI_value, "Spain")[1], "Spain")
    NI_tax_SP = format_number_and_currency(calculate_Taxes(GAI_value, "Spain")[2], "Spain")
    total_tax_SP = format_number_and_currency(calculate_Taxes(GAI_value, "Spain")[0], "Spain")
    net_salary_SP = format_number_and_currency(GAI_value - calculate_Taxes(GAI_value, "Spain")[0], "Spain")
    
    gross_salary_UK = format_number_and_currency(GAI_value * exchange , "UK")
    income_tax_UK = format_number_and_currency(calculate_Taxes(GAI_value, "UK")[1]* exchange, "Spain")
    NI_tax_UK = format_number_and_currency(calculate_Taxes(GAI_value, "UK")[2]* exchange, "Spain")
    total_tax_UK = format_number_and_currency(calculate_Taxes(GAI_value, "UK")[0]* exchange, "Spain")
    net_salary_UK = format_number_and_currency(GAI_value* exchange - calculate_Taxes(GAI_value, "UK")[0]* exchange, "Spain")

    message = f"The amount of :blue-background[_{gross_salary_SP}_] is equivalent to :orange-background[_{gross_salary_UK}_] based on the current exchange rate (:violet-background[{exchange} GBP/EUR]). The total taxes amount to :red-background[{total_tax_UK}]."

else:
    
    exchange = get_exchange_rate("EUR","GBP")
    
    gross_salary_SP = format_number_and_currency(GAI_value*exchange, "Spain")
    income_tax_SP = format_number_and_currency(calculate_Taxes(GAI_value*exchange, "Spain")[1], "Spain")
    NI_tax_SP = format_number_and_currency(calculate_Taxes(GAI_value*exchange, "Spain")[2], "Spain")
    total_tax_SP = format_number_and_currency(calculate_Taxes(GAI_value*exchange, "Spain")[0], "Spain")
    net_salary_SP = format_number_and_currency(GAI_value*exchange - calculate_Taxes(GAI_value, "Spain")[0]*exchange, "Spain")
    
    gross_salary_UK = GAI_value 
    income_tax_UK = calculate_Taxes(GAI_value, "UK")[1] 
    NI_tax_UK = calculate_Taxes(GAI_value, "UK")[2] 
    total_tax_UK = calculate_Taxes(GAI_value, "UK")[0] 
    net_salary_UK = (gross_salary_UK - total_tax_UK) 
    
    message = f"The amount of :blue-background[_{gross_salary_UK}_] is equivalent to :orange-background[_{gross_salary_SP}_] based on the current exchange rate (:violet-background[{exchange} GBP/EUR]). The total taxes amount to :red-background[{total_tax_SP}]."

    

    
    
data = {
        "Concept": ["Gross Salary", "- Income Tax", "- National Insurance","Total Deductions", "Net Salary"],
         "Spain": [
             gross_salary_SP,
             income_tax_SP,
             NI_tax_SP,
             total_tax_SP,
             net_salary_SP
             
             
             ],
         "UK": [
             gross_salary_UK,
             income_tax_UK,
             NI_tax_UK,
             total_tax_UK,
             net_salary_UK
             ]
     }
    

    # data = {
    #     "Concept": ["Gross Salary", "- Income Tax", "- National Insurance","Total Deductions", "Net Salary"],
    #     "Spain": [format_number_and_currency(GAI_value,"Spain"), format_number_and_currency(calculate_Taxes(GAI_value, "Spain")[1],"Spain"), 
    #             format_number_and_currency(calculate_Taxes(GAI_value, "Spain")[2],"Spain"),
    #             format_number_and_currency(calculate_Taxes(GAI_value, "Spain")[0],"Spain"), 
    #             format_number_and_currency(GAI_value-calculate_Taxes(GAI_value, "Spain")[0],"Spain")],
    #     "UK": [format_number_and_currency(GAI_value,"UK"), format_number_and_currency(calculate_Taxes(GAI_value, "UK")[1],"UK"), 
    #             format_number_and_currency(calculate_Taxes(GAI_value, "UK")[2],"UK"),
    #             format_number_and_currency(calculate_Taxes(GAI_value, "UK")[0],"UK"), 
    #             format_number_and_currency(GAI_value-calculate_Taxes(GAI_value, "UK")[0],"UK")],
    # }
    
    
# Crear el DataFrame
df = pd.DataFrame(data)


# Función para resaltar una fila
def highlight_row(row):
    if row["Concept"] == "Total Deductions":  # Resalta la fila con el concepto "Gross Salary"
        return ['background-color: grey'] * len(row)  # Resalta la fila con color amarillo
    elif row["Concept"] == "Gross Salary":  # Resalta la fila con el concepto "Gross Salary"
        return ['background-color: #D3D3D3; color: black'] * len(row)  # Fondo gris claro con texto negro
    
    elif row["Concept"] == "Net Salary":  # Resalta la fila con el concepto "Gross Salary"
        return ['background-color: green; color: black'] * len(row)  # Fondo gris claro con texto negro
    
    return [''] * len(row)  # Sin resaltar otras filas

# Aplicar el estilo
styled_df = df.style.apply(highlight_row, axis=1)


# Mostrar la tabla como dataframe interactivo sin el índice
st.dataframe(styled_df, hide_index = True, use_container_width=True)




st.write(message)


