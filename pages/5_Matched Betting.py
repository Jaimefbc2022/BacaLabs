import streamlit as st
import sqlite3
import pandas as pd
from datetime import date

# Configurar la base de datos
def init_db():
    conn = sqlite3.connect("bets.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_type TEXT NOT NULL,
            subtype TEXT,
            bookmaker TEXT,
            market TEXT,
            stake REAL,
            odds REAL,
            result TEXT,
            profit REAL
        )
    """)
    conn.commit()
    conn.close()

# Función para agregar una transacción
def add_transaction(transaction_type, subtype, bookmaker, market, stake, odds):
    conn = sqlite3.connect("bets.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO transactions (transaction_type, subtype, bookmaker, market, stake, odds, result, profit) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                   (transaction_type, subtype, bookmaker, market, stake, odds, None, None))
    conn.commit()
    conn.close()

# Función para actualizar una transacción
def update_transaction(transaction_id, result, profit):
    conn = sqlite3.connect("bets.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE transactions SET result = ?, profit = ? WHERE id = ?", (result, profit, transaction_id))
    conn.commit()
    conn.close()

# Función para eliminar una transacción
def delete_transaction(transaction_id):
    conn = sqlite3.connect("bets.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
    conn.commit()
    conn.close()

# Función para obtener las transacciones
def get_transactions():
    conn = sqlite3.connect("bets.db")
    df = pd.read_sql_query("SELECT * FROM transactions", conn)
    conn.close()
    return df

# Inicializar la base de datos
init_db()

# Configuración de la página
st.set_page_config(page_title="Matched Betting Tracker", page_icon="💰")

st.title("💰 Matched Betting Tracker")
st.write("Registra y gestiona todas tus transacciones de matched betting de manera sencilla.")

# Formulario para agregar una nueva transacción
st.sidebar.header("Agregar una nueva transacción")
with st.sidebar.form("add_transaction_form"):
    transaction_type = st.selectbox("Tipo de Transacción", ["Depósito", "Retiro", "Bet", "Otros"])
    subtype = None
    if transaction_type == "Bet":
        subtype = st.selectbox("Subtipo", ["Back Bet", "Lay Bet"])
    bet_type = None
    if subtype in ["Back Bet", "Lay Bet"]:
        bet_type = st.selectbox("Tipo de Apuesta", ["Free Bet", "Qualifying Bet"])
    bookmaker = st.text_input("Bookmaker")
    market = st.text_input("Mercado")
    stake = st.number_input("Stake", min_value=0.01, step=0.01)
    odds = st.number_input("Cuotas", min_value=1.01, step=0.01)
    submitted = st.form_submit_button("Agregar Transacción")
    if submitted and bookmaker and market and stake > 0 and odds > 1:
        add_transaction(transaction_type, bet_type, bookmaker, market, stake, odds)
        st.success("Transacción agregada correctamente.")

# Mostrar y gestionar transacciones
st.header("📋 Transacciones Registradas")
transactions_df = get_transactions()
if not transactions_df.empty:
    transaction_id = st.selectbox("Selecciona una transacción para actualizar o eliminar", transactions_df["id"].astype(str) + " - " + transactions_df["market"])
    transaction_id = int(transaction_id.split(" - ")[0])
    
    col1, col2 = st.columns(2)
    with col1:
        result = st.selectbox("Resultado", ["Ganada", "Perdida", "Pendiente"])
        profit = st.number_input("Ganancia/Pérdida", step=0.01)
        if st.button("Actualizar Transacción"):
            update_transaction(transaction_id, result, profit)
            st.success("Transacción actualizada correctamente.")
    
    with col2:
        if st.button("Eliminar Transacción", key="delete"):
            delete_transaction(transaction_id)
            st.warning("Transacción eliminada.")
    
    st.dataframe(transactions_df)
else:
    st.info("No hay transacciones registradas aún.")
