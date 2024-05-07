import tkinter as tk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import filedialog, messagebox, Tk, PhotoImage, Label, ttk

def ejecutar_macheo():
    #Seleccionar tally GPower
    archivo = filedialog.askopenfilename(filetypes=[('Archivos de Excel', '*.xlsx')])

    # Lee el archivo excel
    df_GP = pd.read_excel(archivo)

    #Seleccionar tally Cliente
    archivo2 = filedialog.askopenfilename(filetypes=[('Archivos de Excel', '*.xlsx')])

    # Lee el archivo excel
    df_Cliente = pd.read_excel(archivo2)

    # Combina los dos DataFrames
    df3 = pd.merge(df_GP, df_Cliente, left_index=True, right_index=True)

    df3["LJoint"] = df3["LJoint"].str.replace(',', '.').astype(float)
    df3["LongTubo"] = df3["LongTubo"].astype(str).str.replace(',', '.').astype(float)

    df3["Diferencia"] = df3["LJoint"] - df3["LongTubo"]
    df3["Promedio"] = df3["Diferencia"] / df3["LongTubo"]

    df3_Final = df3[["JointNumber", "Distance", "LJoint", "FeatureType", "Soldadura", "Distancia", "LongTubo", "SubTipo", "Diferencia", "Promedio"]]

    # Buscar en la columna "Diferencia" y obtener los índices donde el valor es mayor a 0.7
    indices = df3_Final.index[(df3_Final['Diferencia'] > 0.3) | (df3_Final['Diferencia'] < -0.3)].tolist()

    # Para cada índice encontrado, insertar una fila vacía en las columnas
    for i in indices:
        if i > 0:
            new_row = pd.Series([''] * 4, index=df3_Final.columns[:4])
            df3_Final = pd.concat([df3_Final.loc[:i-1], new_row, df3_Final.loc[i:]], ignore_index=True)
        elif i < 0:
            new_row = pd.Series([''] * 4, index=df3_Final.columns[5:8])
            df3_Final = pd.concat([df3_Final.loc[:i-1], new_row, df3_Final.loc[i:]], ignore_index=True)


        # Abre el cuadro de diálogo para seleccionar la ruta de guardado del archivo
    save_file_path = filedialog.asksaveasfilename(defaultextension=".xlsx")

    # Guarda el resultado en un archivo Excel
    df3_Final.to_excel(save_file_path, index=False)
    
    return df_GP, df_Cliente, df3_Final

def colocar_atributos():

    #Copia los atributos (Espesor, Orientacion de SW, Comentarios, etc.) del tally cliente al tally GPower

    pass

