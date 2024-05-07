import pandas as pd
import tkinter as tk
from datetime import datetime, timedelta
from tkinter import filedialog
from tkinter.filedialog import asksaveasfilename


def ejecutar_conversor():   
    # Crea una ventana de Tkinter y ocúltala
    root = tk.Tk()
    root.withdraw()

    # Abre el cuadro de diálogo para seleccionar el archivo y guarda la ruta del archivo seleccionado
    file_path = filedialog.askopenfilename()

    # Lee el archivo excel
    df = pd.read_excel(file_path)


    # Función para convertir HH:MM:SS:SSS a tiempo decimal
    def convertir_a_decimal(tiempo):
        h, m, s, ms = map(int, tiempo.split(':'))
        tiempo_decimal = h + m/60 + s/3600 + ms/3600000
        return tiempo_decimal

    # Función para convertir tiempo decimal a HH:MM:SS:SSS
    def convertir_tiempo(tiempo_decimal):
        horas = int(tiempo_decimal)
        minutos = (tiempo_decimal*60) % 60
        segundos = (tiempo_decimal*3600) % 60
        milisegundos = (tiempo_decimal*3600000) % 1000
        return "%02d:%02d:%02d:%03d" % (horas, minutos, segundos, milisegundos)

    # Aplicar la función de conversión a la columna de tiempo
    df['Timer [hh decimal]'] = df['Timer [hh:mm:ss]'].apply(convertir_a_decimal)

    # Aplicar la función de conversión a la columna de tiempo
    df['tiempo'] = df['Timer [hh decimal]'].apply(convertir_tiempo)

    # Abre el cuadro de diálogo para guardar el archivo y guarda la ruta del archivo seleccionado
    save_path = asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])

    # Guarda el DataFrame modificado en la ruta seleccionada
    if save_path:
        df.to_excel(save_path, index=False)