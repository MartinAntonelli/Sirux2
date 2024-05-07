import tkinter as tk
import numpy as np
from tkinter import filedialog, messagebox, Tk, PhotoImage, Label, ttk
from pandastable import Table
import pandas as pd
import matplotlib.pyplot as plt
import importacion
import Conversor
import macheo
import formato_oldelval, formato_otasa, formato_ypf
from matplotlib.ticker import FuncFormatter
from PIL import Image, ImageTk
from version import version

print("Version de la aplicacione: ", version)

seleccion = None

def seleccionar_archivo():
    global df
    # Abre una ventana para seleccionar el archivo de Excel
    archivo = filedialog.askopenfilename(filetypes=[('Archivos de Excel', '*.xlsx')])
    
    # Verifica que se haya seleccionado un archivo
    if archivo:
        # Carga el archivo de Excel en un DataFrame
        df = pd.read_excel(archivo)
        # Habilita el menú desplegable para seleccionar la opción de procesamiento
        option_menu.config(state='normal')

def on_option_select(seleccion):
    global df, seleccion_global
    print(f"Opción seleccionada: {seleccion}")
    if seleccion == 'OLDELVAL':
        df = formato_oldelval.generate_oldelval_format(df, progress_bar, progress_status, root, graph_button)
        seleccion_global = "OLDELVAL"
        
    elif seleccion == 'YPF':
        df = formato_ypf.generate_ypf_format(df, progress_bar, progress_status, root, graph_button)
        seleccion_global = "YPF"
        
    elif seleccion == 'OTASA':
        df = formato_otasa.generate_otasa_format(df, progress_bar, progress_status, root, graph_button)
        seleccion_global = "OTASA"
    # Muestra el DataFrame procesado en una tabla
    mostrar_dataframe(df)
    # Habilita el botón de exportación
    export_button.config(state='normal', command=lambda: exportar_archivo(df))
    print(seleccion_global)
    return seleccion_global

def mostrar_dataframe(df):
    # Crea un widget de tabla para mostrar el archivo traducido
    frame = tk.Frame(root)
    frame.grid(sticky='news') 
    
    # Agrega un botón para cerrar el DataFrame
    button = tk.Button(frame, text="Cerrar", command=frame.destroy)
    button.grid()  
    
    table = Table(frame)
    table.show()

    # Muestra el archivo traducido en el widget de tabla
    table.model.df = df
    table.redraw()

def exportar_archivo(df):
    # Abre una ventana de diálogo para guardar el archivo
    ruta = filedialog.asksaveasfilename(filetypes=[('Archivos de Excel', '*.xlsx')], defaultextension='.xlsx')
    # Verifica que se haya seleccionado una ruta
    if ruta:
        # Guarda el archivo en la ruta seleccionada
        df.to_excel(ruta, index=False)
        messagebox.showinfo('Exportación exitosa', 'Listo')

def mostrar_grafico():
    global seleccion_global
    print(seleccion)
    if seleccion_global == "OTASA":
        formato_otasa.mostrar_grafico_otasa(formato_otasa.df_otasa)

    elif seleccion_global == "OLDELVAL":
        formato_oldelval.mostrar_grafico_oldelval(formato_oldelval.df_oldelval)

    elif seleccion_global == "YPF":
        formato_ypf.mostrar_grafico_ypf(formato_ypf.df_ypf)

def on_enter(e):
    e.widget['background'] = 'white'  # Cambia el color de fondo a verde cuando el ratón entra
    e.widget['foreground'] = 'black'

def on_leave(e):
    e.widget['background'] = '#0E2F54'  # Cambia el color de fondo a su color original cuando el ratón sale
    e.widget['foreground'] = "white"
    
# Crea la ventana principal
root = tk.Tk()
root.title('Sirux')
root.iconbitmap('Miproyecto.ico')
root.geometry("1920x1080")
imagen = PhotoImage(file="Sirux.png")
background = Label(image=imagen)
background.place(x=0, y=0, relwidth=1, relheight=1)
background.config(bg="#0E2F54")
root.state('zoomed')

# Crea un marco para contener los botones
button_frame = tk.Frame(root)
button_frame.pack(side='top', fill='x', anchor='center') # Centra el marco en la parte superior de la ventana
button_frame.config(bg="#0E2F54")
inner_frame = tk.Frame(button_frame)
inner_frame.pack(side='top', anchor='center') # Centra el marco adicional en el marco button_frame

# Crea un botón para seleccionar el archivo
boton = tk.Button(inner_frame, text='Seleccionar Archivo Excel', command=seleccionar_archivo, bg="#0E2F54", fg="White")
boton.pack(side='left', padx=10)
boton.bind("<Enter>", on_enter)
boton.bind("<Leave>", on_leave)

# Crea un menú desplegable para seleccionar la opción de procesamiento
options = ['OLDELVAL', 'YPF', 'OTASA']
option_var = tk.StringVar(root)
option_var.set(options[0])
option_menu = tk.OptionMenu(inner_frame, option_var, *options)
option_menu.config(bg="#0E2F54", fg="white")
option_menu.pack(side='left', padx=10)
option_var.trace('w', lambda *args: on_option_select(option_var.get()))

#Boton de Exportacion
export_button = tk.Button(inner_frame, text="Exportar", state='disabled', bg="#0E2F54", fg="white")
export_button.pack(side='left', padx=10)
export_button.bind("<Enter>", on_enter)
export_button.bind("<Leave>", on_leave)

# Crea un botón para mostrar el gráfico
graph_button = tk.Button(inner_frame, text='Grafico', command=lambda:mostrar_grafico(), state="disabled", bg="#0E2F54", fg="white")
graph_button.pack(side='left', padx=10)
graph_button.bind("<Enter>", on_enter)
graph_button.bind("<Leave>", on_leave)

# Botón de IMU interpolacion
import_button = tk.Button(inner_frame, text="IMU Interp", command=importacion.ejecutar_importacion, bg="#0E2F54", fg="white")
import_button.pack(side='left', padx=10)
import_button.bind("<Enter>", on_enter)
import_button.bind("<Leave>", on_leave)

# Botón de IMU conversor
import_button = tk.Button(inner_frame, text="IMU Conver", command=Conversor.ejecutar_conversor, bg="#0E2F54", fg="white")
import_button.pack(side='left', padx=10)
import_button.bind("<Enter>", on_enter)
import_button.bind("<Leave>", on_leave)

# Botón de Macheo
import_button = tk.Button(inner_frame, text="Macheo", command= macheo.ejecutar_macheo, bg="#0E2F54", fg="white")
import_button.pack(side='left', padx=10)
import_button.bind("<Enter>", on_enter)
import_button.bind("<Leave>", on_leave)

#Boton de salir
exit_button = tk.Button(inner_frame, text="Salir", command=root.quit, bg="#0E2F54", fg="white")
exit_button.pack(side='left', padx=10)
exit_button.bind("<Enter>", on_enter)
exit_button.bind("<Leave>", on_leave)


# Crea un marco para la versión en la parte inferior de la ventana
version_frame = tk.Frame(root, bg="#0E2F54")
version_frame.pack(side='bottom', fill='x')

# Crea la barra de progreso y la agrega al marco version_frame
progress_bar = ttk.Progressbar(version_frame, length=200)
progress_bar.pack(side='left')

# Crea una etiqueta para el estado de la barra de progreso y la coloca a la derecha de la barra de progreso
progress_status = tk.Label(version_frame, text="En espera...", bg="#0E2F54", fg="white")
progress_status.pack(side='left')

# Crea la etiqueta para el número de versión y la coloca en el lado derecho
version_label = tk.Label(version_frame, text='Versión: ' + version, bg="#0E2F54", fg="white")
version_label.pack(side='right')

# Abre la imagen original y la redimensiona
original_image = Image.open("logo.png")
resized_image = original_image.resize((100, 25), Image.LANCZOS)  # Cambia (100, 25) al tamaño que desees

# Convierte la imagen redimensionada a formato PhotoImage
logo_image = ImageTk.PhotoImage(resized_image)

# Crea una etiqueta para la imagen y la coloca en el centro del marco version_frame
logo_label = tk.Label(version_frame, image=logo_image, bg="#0E2F54")
logo_label.image = logo_image  # Mantén una referencia a la imagen
logo_label.pack(side="bottom", anchor = "center")

# Crea una etiqueta para el texto "Desing by" y la coloca en el centro del marco version_frame
text_label = tk.Label(version_frame, text="Creado por", bg="#0E2F54", fg="white")
text_label.pack(side='bottom', anchor='center')

# Inicia el bucle principal
root.mainloop()