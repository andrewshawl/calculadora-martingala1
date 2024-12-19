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
        "Cantidad acumulada (lotes)": cantidad_total / tamanio_lote,
        "Flotante": 0  # Inicialmente, el flotante es 0
    })

    for nivel in range(1, niveles + 1):
        precio_actual += espacios_precio[nivel - 1]
        cantidad_a_comprar = cantidad_actual / tamanio_lote * factor_martingala
        cantidad_actual = cantidad_a_comprar * tamanio_lote
        costo_total += cantidad_actual * precio_actual
        cantidad_total += cantidad_actual

        precio_promedio_ponderado = costo_total / cantidad_total
        flotante = (precio_actual - precio_promedio_ponderado) * (cantidad_total / tamanio_lote) * tamanio_lote

        transacciones.append({
            "Nivel": nivel,
            "Precio": precio_actual,
            "Cantidad a comprar (lotes)": cantidad_a_comprar,
            "Costo acumulado": costo_total,
            "Cantidad acumulada (lotes)": cantidad_total / tamanio_lote,
            "Flotante": flotante
        })

    break_even = costo_total / cantidad_total
    return break_even, transacciones

def calcular_precio_salida(break_even, porcentaje_ganancia):
    return break_even * (1 + porcentaje_ganancia / 100)  # Ganancia variable

# Interfaz de Streamlit
st.title("Calculadora de Martingala: Subida o Bajada")

# Entradas del usuario
cantidad_inicial = 0.13  # Default fijo
precio_inicial = st.number_input("Precio inicial del oro:", min_value=0.01, value=2000.0, step=0.01)
niveles = st.number_input("Número de niveles (máximo 4):", min_value=1, max_value=4, value=3, step=1)
tipo_martingala = st.selectbox("Tipo de martingala:", ["Subida", "Bajada"])
porcentaje_ganancia = st.number_input("Porcentaje de ganancia deseado (%):", min_value=0.1, value=1.5, step=0.1)

# Valores fijos
factor_martingala = 2.0
capital_total = 1_000_000  # Capital fijo

# Calcular y mostrar resultados
if st.button("Calcular Break Even y Punto de Salida"):
    break_even, transacciones = calcular_break_even(cantidad_inicial, precio_inicial, factor_martingala, niveles, tipo_martingala)
    precio_salida = calcular_precio_salida(break_even, porcentaje_ganancia)

    st.write(f"### El precio de break even es: {break_even:.2f}")
    st.write(f"### El precio de salida para un {porcentaje_ganancia:.1f}% de ganancia es: {precio_salida:.2f}")

    # Mostrar la tabla con los resultados
    df_transacciones = pd.DataFrame(transacciones)
    st.write("### Detalles de las transacciones:")
    st.dataframe(df_transacciones)

