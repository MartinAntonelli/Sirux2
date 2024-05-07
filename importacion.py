import pandas as pd
import tkinter as tk
from tkinter import filedialog
import re

def ejecutar_importacion():
    
    # Crea una ventana de Tkinter y ocúltala
    root = tk.Tk()
    root.withdraw()

    # Abre el cuadro de diálogo para seleccionar el archivo y guarda la ruta del archivo seleccionado
    file_path = filedialog.askopenfilename()

    # Lee el archivo CSV
    df = pd.read_csv(file_path, encoding="ISO-8859-1", sep=";")

    print(df.columns)

    #"Latitud [°]", "Longitud [°]", "Altura [m]" Columnas df Final
    df['Odometria'] = df['ï»¿hola'].str.replace(',', '.').astype(float)
    df['latitud'] = df['latitud'].str.replace(',', '.').astype(float)
    df['longitud'] = df['longitud'].str.replace(',', '.').astype(float)
    df['altura'] = df['altura'].str.replace(',', '.').astype(float)

    # Convertir las columnas seleccionadas a tipo float
    df_seleccionado = df[['Odometria', 'latitud', 'longitud', 'altura']].astype(float)

    # Realiza la interpolación para cada columna
    df_interpolado = df_seleccionado.interpolate(method='linear', limit_direction='both')

        # Agrega la columna "Comentario" al DataFrame interpolado
    df_interpolado = pd.concat([df_interpolado, df['Comentario']], axis=1)

    # Abre el cuadro de diálogo para seleccionar la ruta de guardado del archivo
    save_file_path = filedialog.asksaveasfilename(defaultextension=".xlsx")

    # Guarda el resultado en un archivo Excel
    df_interpolado.to_excel(save_file_path, index=False)

