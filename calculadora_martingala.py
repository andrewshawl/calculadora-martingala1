import streamlit as st
import pandas as pd

def calcular_break_even(cantidad_inicial, precio_inicial, factor_martingala, niveles, tipo_martingala):
    tamanio_lote = 100  # Tamaño fijo del lote
    cantidad_total = cantidad_inicial * tamanio_lote
    costo_total = cantidad_inicial * tamanio_lote * precio_inicial

    precio_actual = precio_inicial
    cantidad_actual = cantidad_inicial * tamanio_lote

    transacciones = []

    # Distancias entre niveles (3, 7, 15, 25 puntos)
    espacios_precio = [3, 7, 15, 25]
    if tipo_martingala == "Bajada":
        espacios_precio = [-x for x in espacios_precio]

    # Asegurarse de que haya suficientes niveles
    espacios_precio = espacios_precio[:niveles]

    # Agregar los datos iniciales (Nivel 0)
    transacciones.append({
        "Nivel": 0,
        "Precio": precio_actual,
        "Cantidad a comprar (lotes)": cantidad_inicial,
        "Costo acumulado": costo_total,
        "Cantidad acumulada (lotes)": cantidad_total / tamanio_lote
    })

    for nivel in range(1, niveles + 1):
        precio_actual += espacios_precio[nivel - 1]
        cantidad_a_comprar = cantidad_actual / tamanio_lote * factor_martingala
        cantidad_actual = cantidad_a_comprar * tamanio_lote
        costo_total += cantidad_actual * precio_actual
        cantidad_total += cantidad_actual

        transacciones.append({
            "Nivel": nivel,
            "Precio": precio_actual,
            "Cantidad a comprar (lotes)": cantidad_a_comprar,
            "Costo acumulado": costo_total,
            "Cantidad acumulada (lotes)": cantidad_total / tamanio_lote
        })

    break_even = costo_total / cantidad_total
    return break_even, transacciones

def calcular_precio_salida(break_even, capital_total):
    return break_even * (1 + 0.015)  # Ganancia del 1.5%

# Interfaz de Streamlit
st.title("Calculadora de Martingala: Subida o Bajada")

# Entradas del usuario
cantidad_inicial = st.number_input("Cantidad inicial de lotes comprados:", min_value=0.01, value=1.0, step=0.01)
precio_inicial = st.number_input("Precio inicial del oro:", min_value=0.01, value=2000.0, step=0.01)
factor_martingala = st.number_input("Factor de martingala:", min_value=1.0, value=2.0, step=0.1)
niveles = st.number_input("Número de niveles (máximo 4):", min_value=1, max_value=4, value=3, step=1)
capital_total = st.number_input("Capital total disponible:", min_value=1.0, value=10000.0, step=1.0)

# Selección del tipo de martingala
tipo_martingala = st.selectbox("Tipo de martingala:", ["Subida", "Bajada"])

# Calcular y mostrar resultados
if st.button("Calcular Break Even y Punto de Salida"):
    break_even, transacciones = calcular_break_even(cantidad_inicial, precio_inicial, factor_martingala, niveles, tipo_martingala)
    precio_salida = calcular_precio_salida(break_even, capital_total)

    st.write(f"### El precio de break even es: {break_even:.2f}")
    st.write(f"### El precio de salida para un 1.5% de ganancia sobre el capital total es: {precio_salida:.2f}")

    # Mostrar la tabla con los resultados
    df_transacciones = pd.DataFrame(transacciones)
    st.write("### Detalles de las transacciones:")
    st.dataframe(df_transacciones)
