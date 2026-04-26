import pandas as pd
import scipy.stats
import streamlit as st
import time

# Configuración de la memoria de la app (Session State)
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0
if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['no', 'iteraciones', 'media'])

st.header('Lanzar una moneda')

# Crear un gráfico de línea inicial
chart = st.line_chart([0.5])

def toss_coin(n):
    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)
    mean = None
    outcome_no = 0
    outcome_1_count = 0

    for r in trial_outcomes:
        outcome_no += 1
        if r == 1:
            outcome_1_count += 1
        mean = outcome_1_count / outcome_no
        chart.add_rows([mean])
        time.sleep(0.05) # Esto hace que el gráfico se vea "animado"
    return mean

# Interfaz de usuario
number_of_trials = st.slider('¿Número de intentos?', 1, 1000, 10)
start_button = st.button('Ejecutar')

if start_button:
    st.write(f'Experimento con {number_of_trials} intentos en curso...')
    st.session_state['experiment_no'] += 1
    mean = toss_coin(number_of_trials)
    
    # Guardar resultados en la tabla
    new_row = pd.DataFrame(data=[[st.session_state['experiment_no'], number_of_trials, mean]],
                           columns=['no', 'iteraciones', 'media'])
    st.session_state['df_experiment_results'] = pd.concat([st.session_state['df_experiment_results'], new_row], axis=0)
    st.session_state['df_experiment_results'] = st.session_state['df_experiment_results'].reset_index(drop=True)

# Mostrar la tabla de resultados
st.write(st.session_state['df_experiment_results'])