import tkinter as tk
import numpy as np
from tkinter import filedialog, messagebox, Tk, PhotoImage, Label, ttk
from pandastable import Table
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from PIL import Image, ImageTk

def generate_ypf_format(df, progress_bar, progress_status, root, graph_button):
    print("Generando formato YPF")
    global df_ypf
    #Crear las columnas del excel
    df['idCaracteristica'] = df["Number"]
    df = df.assign(idEvento="")
    df['Soldadura'] = df["JointNumber"]
    df["LongTubo [m]"] = df["LJoint"]
    df["SubTipo"] = df["FeatureType"]
    df["FeatureType"] = df["FeatureType"]
    df['FeatureIdentification'] = df['FeatureIdentification']
    df['AnomalyClass'] = df['AnomalyClass']
    df['DistanciaRef [m]'] = df["Distance"]
    df['DSAAr [m]'] = df['UpWeld']
    df['DSAAb [m]'] = df['DownWeld']
    df['DMAAr [m]'] = df['UpMarker']
    df['DMAAb [m]'] = df['DownMarker']
    df['PosSolLong'] = "" 
    df['EspPared [mm]'] = df['WallThickness']
    df['Prof [%]'] = df['Depth']
    df['LongFalla [mm]'] = df['Length']
    df['AnchoFalla [mm]'] = df['Width']
    df['CapaFalla'] = df['SurfaceLocation']
    df['PosicionRelativa'] = df['LocationClass']
    df['PosFalla'] = df['Orientation']
    df['Comentario'] = df['Description']
    df = df.assign(Latitud="")
    df = df.assign(Longitud="")
    df = df.assign(Altura="")
    df['Latitud [°]'] = df['Latitud']
    df['Longitud [°]'] = df['Longitud']
    df['Altura [m]'] = df['Altura']
    df['ProfEfectiva [%]'] = df['EffectiveDepth']
    df['LongEfectiva [mm]'] = df['EffectiveLength']
    df['ERF AE'] = df['ERFRStreng']
    df['PF B31G [MPa]'] = df["PBurstB31G"]
    df['PF 0.85 [MPa]'] = df['PBurstB31GModif']
    df['PF AE [MPa]'] = df['PBurstRStreng']
    df['FS B31G'] = df["FSB31G"]
    df['FS 0.85'] = df['FSB31GModif']
    df['FS AE'] = df['FSRStreng']
    df['MAPO [MPa]'] = df["MAOP"]
    df["Cluster"] = df["Cluster"]

    # Actualiza la barra de progreso
    progress_bar['value'] = 10
    progress_status['text'] = "Progreso: {}%".format(progress_bar['value'])
    root.update_idletasks()  

        #Elimina los datos nulos
    df['AnomalyClass'] = df['AnomalyClass'].replace('Unknown', '')
    df['AnomalyClass'] = df['AnomalyClass'].replace('Pitting', 'PITT')
    df['AnomalyClass'] = df['AnomalyClass'].replace('General', 'GENE')
    df['AnomalyClass'] = df['AnomalyClass'].replace('Pinhole', 'PINH')
    df['AnomalyClass'] = df['AnomalyClass'].replace('AxialGrooving', 'AXGR')
    df['AnomalyClass'] = df['AnomalyClass'].replace('AxialSlotting', 'AXSL')
    df['AnomalyClass'] = df['AnomalyClass'].replace('CircumferentialGrooving', 'CIGR')
    df['AnomalyClass'] = df['AnomalyClass'].replace('CircumferentialSlotting', 'CISL')
    df['Cluster'] = df['Cluster'].replace(0, "")
    df['EspPared [mm]'] = df['EspPared [mm]'].replace('0,00', '')
    df['Prof [%]'] = df['Prof [%]'].replace('0,00', '')
    df['LongEfectiva [mm]'] = df['LongEfectiva [mm]'].replace(0, '')
    df["ProfEfectiva [%]"] = df["ProfEfectiva [%]"].replace('0,00', '')
    df["ERF AE"] = df["ERF AE"].replace('0,00', '')
    df["PF B31G [MPa]"] = df["PF B31G [MPa]"].replace('0,00', '')
    df["PF 0.85 [MPa]"] = df["PF 0.85 [MPa]"].replace('0,00', '')
    df["PF AE [MPa]"] = df["PF AE [MPa]"].replace('0,00', '')
    df["FS B31G"] = df["FS B31G"].replace('0,00', '')
    df["FS 0.85"] = df["FS 0.85"].replace('0,00', '')
    df["FS AE"] = df["FS AE"].replace('0,00', '')
    df["MAPO [MPa]"] = df["MAPO [MPa]"].replace('0,00', '')

    def reemplazar_valor_largo(row):
        if row['LongFalla [mm]'] == 5 and row['AnchoFalla [mm]'] == 5:
            return ''
        else:
            return row['LongFalla [mm]']
        
    def reemplazar_valor_ancho(row):
        if row['LongFalla [mm]'] == 5 and row['AnchoFalla [mm]'] == 5:
            return ''
        else:
            return row['AnchoFalla [mm]']
    
        # Actualiza la barra de progreso
    progress_bar['value'] = 20
    progress_status['text'] = "Progreso: {}%".format(progress_bar['value'])
    root.update_idletasks()  


# Aplica la función a cada fila y guarda el resultado en las columnas 'A' y 'B'
    df['LongFalla [mm]'] = df.apply(reemplazar_valor_largo, axis=1)
    df['AnchoFalla [mm]'] = df.apply(reemplazar_valor_ancho, axis=1)
    
    # Actualiza la barra de progreso
    progress_bar['value'] = 30
    progress_status['text'] = "Progreso: {}%".format(progress_bar['value'])
    root.update_idletasks() 

    #Pasar Cluster con definicion metalloss/millfault
    def completar_SubTipo(row):
        if row['FeatureType'] == 'Cluster' and row['FeatureIdentification'] == 'Metalloss':
            return 'ClusterMetalloss'
        elif row['FeatureType'] == 'Cluster' and row['FeatureIdentification'] == 'MillFault':
            return 'ClusterMillFault'
        else:
            return row['SubTipo']
    
    # Aplica la función a cada fila y guarda el resultado en la columna 'sSubTipo'
    df['SubTipo'] = df.apply(completar_SubTipo, axis=1)


    # Crea un diccionario con las palabras y sus traducciones
    traducciones = {
            'Weld': 'SOLDADURA',
            'Metalloss': 'PERDIDA DE METAL',
            'MillFault': 'ANOMALIA DE MANUFACTURA',
            'Tee': 'DERIVACION',
            'Tap': 'TOMA',
            'OffTake': 'TOMA FORJADA',
            'BendRight': 'CURVA',
            'ClusterMetalloss': 'PERDIDA DE METAL-CLUSTER',
            'ClusterMillFault': 'ANOMALIA DE MANUFACTURA-CLUSTER',
            'Flange': 'BRIDA',
            'Dent': 'ABOLLADURA',
            'Support': 'SOPORTE',
            'SupportFullCircular': 'SOPORTE CIRCUNFERENCIAL',
            'SupportGroundAnchor': 'SOPORTE SEMI-CIRCUNFERENCIAL',
            'Valve': 'VALVULA',
            'UnknownFeature': 'OBJETO DESCONOCIDO',
            'MetalObject': 'OBJETO METALICO',
            'RepairPatch': 'REPARACION PARCHE',
            'RepairPatchBegin': 'REPARACION MEDIA CAÑA-INICIO',
            'RepairPatchEnd': 'REPARACION MEDIA CAÑA-FIN',
            'BendLeft': 'CURVA',
            'BendDown': 'CURVA',
            'BendUp': 'CURVA',
            "CasingBegin" : "CAÑO CAMISA-INICIO" ,
            "CasingEnd" : "CAÑO CAMISA-FIN"
        }
    
    df['SubTipo'] = df['SubTipo'].replace(traducciones)

           # Actualiza la barra de progreso
    progress_bar['value'] = 40
    progress_status['text'] = "Progreso: {}%".format(progress_bar['value'])
    root.update_idletasks()  

    # Completa las celdas vacias (COMPLETAR CON LOS VALORES PARA ORDENAR EL EXCEL CON LOS DATOS REQUERIDOS)
    df.loc[df['SubTipo'] == 'SOLDADURA', 'FeatureType'] = 'WELD'
    df.loc[df['SubTipo'] == 'SOLDADURA', 'FeatureIdentification'] = 'ERW Pipe'
    df.loc[df['SubTipo'] == 'SOLDADURA', 'idEvento'] = '401'
    df.loc[df['SubTipo'] == 'SOLDADURA', "LongFalla [mm]"] = ''
    df.loc[df['SubTipo'] == 'SOLDADURA', "AnchoFalla [mm]"] = ''
    df.loc[df['SubTipo'] == 'PERDIDA DE METAL', 'FeatureType'] = 'ANOM'
    df.loc[df['SubTipo'] == 'PERDIDA DE METAL', 'FeatureIdentification'] = 'CORR'
    df.loc[df['SubTipo'] == 'PERDIDA DE METAL', 'idEvento'] = '102'
    df.loc[df['SubTipo'] == 'ANOMALIA DE MANUFACTURA', 'FeatureType'] = 'ANOM'
    df.loc[df['SubTipo'] == 'ANOMALIA DE MANUFACTURA', 'FeatureIdentification'] = 'MIAN'
    df.loc[df['SubTipo'] == 'ANOMALIA DE MANUFACTURA', 'idEvento'] = '101'
    df.loc[df['SubTipo'] == 'PERDIDA DE METAL-CLUSTER', 'FeatureType'] = 'ANOM'
    df.loc[df['SubTipo'] == 'PERDIDA DE METAL-CLUSTER', 'FeatureIdentification'] = 'COCL'
    df.loc[df['SubTipo'] == 'PERDIDA DE METAL-CLUSTER', 'idEvento'] = '102'
    df.loc[df['SubTipo'] == 'ANOMALIA DE MANUFACTURA-CLUSTER', 'FeatureType'] = 'ANOM'
    df.loc[df['SubTipo'] == 'ANOMALIA DE MANUFACTURA-CLUSTER', 'FeatureIdentification'] = 'MACL'
    df.loc[df['SubTipo'] == 'ANOMALIA DE MANUFACTURA-CLUSTER', 'idEvento'] = '101'
    df.loc[df['SubTipo'] == 'ABOLLADURA', 'FeatureType'] = 'ANOM'
    df.loc[df['SubTipo'] == 'ABOLLADURA', 'FeatureIdentification'] = 'DENP'
    df.loc[df['SubTipo'] == 'ABOLLADURA', 'idEvento'] = '103'
    df.loc[df['SubTipo'] == 'ABOLLADURA', 'AnomalyClass'] = ''
    df.loc[df['SubTipo'] == 'VALVULA', 'FeatureType'] = 'COMP'
    df.loc[df['SubTipo'] == 'VALVULA', 'FeatureIdentification'] = 'VALV'
    df.loc[df['SubTipo'] == 'VALVULA', 'idEvento'] = '302'
    df.loc[df['SubTipo'] == 'VALVULA', "LongFalla [mm]"] = ''
    df.loc[df['SubTipo'] == 'VALVULA', "AnchoFalla [mm]"] = ''
    df.loc[df['SubTipo'] == 'DERIVACION', 'FeatureType'] = 'COMP'
    df.loc[df['SubTipo'] == 'DERIVACION', 'FeatureIdentification'] = 'TEE'
    df.loc[df['SubTipo'] == 'DERIVACION', 'idEvento'] = '301'
    df.loc[df['SubTipo'] == 'DERIVACION', "LongFalla [mm]"] = ''
    df.loc[df['SubTipo'] == 'DERIVACION', "AnchoFalla [mm]"] = ''
    df.loc[df['SubTipo'] == 'TOMA', 'FeatureType'] = 'COMP'
    df.loc[df['SubTipo'] == 'TOMA', 'FeatureIdentification'] = 'OFFT'
    df.loc[df['SubTipo'] == 'TOMA', 'idEvento'] = '301'
    df.loc[df['SubTipo'] == 'TOMA', "LongFalla [mm]"] = ''
    df.loc[df['SubTipo'] == 'TOMA', "AnchoFalla [mm]"] = ''
    df.loc[df['SubTipo'] == 'TOMA FORJADA', 'FeatureType'] = 'COMP'
    df.loc[df['SubTipo'] == 'TOMA FORJADA', 'FeatureIdentification'] = 'HTAP'
    df.loc[df['SubTipo'] == 'TOMA FORJADA', 'idEvento'] = '304'
    df.loc[df['SubTipo'] == 'TOMA FORJADA', "LongFalla [mm]"] = ''
    df.loc[df['SubTipo'] == 'TOMA FORJADA', "AnchoFalla [mm]"] = ''
    df.loc[df['SubTipo'] == 'BRIDA', 'FeatureType'] = 'COMP'
    df.loc[df['SubTipo'] == 'BRIDA', 'FeatureIdentification'] = 'FLG'
    df.loc[df['SubTipo'] == 'BRIDA', 'idEvento'] = '301'
    df.loc[df['SubTipo'] == 'BRIDA', "LongFalla [mm]"] = ''
    df.loc[df['SubTipo'] == 'BRIDA', "AnchoFalla [mm]"] = ''
    df.loc[df['SubTipo'] == 'AGM', 'FeatureType'] = 'MARK'
    df.loc[df['SubTipo'] == 'AGM', 'FeatureIdentification'] = "AGM"
    df.loc[df['SubTipo'] == 'AGM', 'idEvento'] = '502'
    df.loc[df['SubTipo'] == 'AGM', "LongFalla [mm]"] = ''
    df.loc[df['SubTipo'] == 'AGM', "AnchoFalla [mm]"] = ''
    df.loc[df['SubTipo'] == 'REPARACION MEDIA CAÑA-INICIO', 'FeatureType'] = 'REPA'
    df.loc[df['SubTipo'] == 'REPARACION MEDIA CAÑA-INICIO', 'FeatureIdentification'] = 'WSLB'
    df.loc[df['SubTipo'] == 'REPARACION MEDIA CAÑA-INICIO', 'idEvento'] = '201'
    df.loc[df['SubTipo'] == 'REPARACION MEDIA CAÑA-INICIO', "LongFalla [mm]"] = ''
    df.loc[df['SubTipo'] == 'REPARACION MEDIA CAÑA-INICIO', "AnchoFalla [mm]"] = ''
    df.loc[df['SubTipo'] == 'REPARACION MEDIA CAÑA-FIN', 'FeatureType'] = 'REPA'
    df.loc[df['SubTipo'] == 'REPARACION MEDIA CAÑA-FIN', 'FeatureIdentification'] = 'WSLE'
    df.loc[df['SubTipo'] == 'REPARACION MEDIA CAÑA-FIN', 'idEvento'] = '201'
    df.loc[df['SubTipo'] == 'REPARACION MEDIA CAÑA-FIN', "LongFalla [mm]"] = ''
    df.loc[df['SubTipo'] == 'REPARACION MEDIA CAÑA-FIN', "AnchoFalla [mm]"] = ''
    df.loc[df['SubTipo'] == 'REPARACION PARCHE', 'FeatureType'] = 'REPA'
    df.loc[df['SubTipo'] == 'REPARACION PARCHE', 'FeatureIdentification'] = 'PATC'
    df.loc[df['SubTipo'] == 'REPARACION PARCHE', 'idEvento'] = '303'
    df.loc[df['SubTipo'] == 'REPARACION PARCHE', "LongFalla [mm]"] = ''
    df.loc[df['SubTipo'] == 'REPARACION PARCHE', "AnchoFalla [mm]"] = ''
    df.loc[df['SubTipo'] == 'CURVA', 'FeatureType'] = 'OTHE'
    df.loc[df['SubTipo'] == 'CURVA', 'FeatureIdentification'] = 'BEND'
    df.loc[df['SubTipo'] == 'CURVA', 'idEvento'] = '601'
    df.loc[df['SubTipo'] == 'CURVA', "LongFalla [mm]"] = ''
    df.loc[df['SubTipo'] == 'CURVA', "AnchoFalla [mm]"] = ''
    df.loc[df['SubTipo'] == 'OBJETO METALICO', 'FeatureType'] = 'ADME'
    df.loc[df['SubTipo'] == 'OBJETO METALICO', 'FeatureIdentification'] = 'CLMO'
    df.loc[df['SubTipo'] == 'OBJETO METALICO', 'idEvento'] = '105'
    df.loc[df['SubTipo'] == 'OBJETO DESCONOCIDO', 'FeatureType'] = 'OTHE'
    df.loc[df['SubTipo'] == 'OBJETO DESCONOCIDO', 'FeatureIdentification'] = 'OTHE'
    df.loc[df['SubTipo'] == 'OBJETO DESCONOCIDO', 'idEvento'] = '305'
    df.loc[df['SubTipo'] == 'OBJETO DESCONOCIDO', "LongFalla [mm]"] = ''
    df.loc[df['SubTipo'] == 'OBJETO DESCONOCIDO', "AnchoFalla [mm]"] = ''
    df.loc[df['SubTipo'] == 'SOPORTE', 'FeatureType'] = 'COMP'
    df.loc[df['SubTipo'] == 'SOPORTE', 'FeatureIdentification'] = 'ESUP'
    df.loc[df['SubTipo'] == 'SOPORTE', 'idEvento'] = '301'
    df.loc[df['SubTipo'] == 'SOPORTE', "LongFalla [mm]"] = ''
    df.loc[df['SubTipo'] == 'SOPORTE', "AnchoFalla [mm]"] = ''
    df.loc[df['SubTipo'] == 'SOPORTE SEMI-CIRCUNFERENCIAL', 'FeatureType'] = 'COMP'
    df.loc[df['SubTipo'] == 'SOPORTE SEMI-CIRCUNFERENCIAL', 'FeatureIdentification'] = 'ANCH'
    df.loc[df['SubTipo'] == 'SOPORTE SEMI-CIRCUNFERENCIAL', 'idEvento'] = '301'
    df.loc[df['SubTipo'] == 'SOPORTE SEMI-CIRCUNFERENCIAL', "LongFalla [mm]"] = ''
    df.loc[df['SubTipo'] == 'SOPORTE SEMI-CIRCUNFERENCIAL', "AnchoFalla [mm]"] = ''
    df.loc[df['SubTipo'] == 'SOPORTE CIRCUNFERENCIAL', 'FeatureType'] = 'COMP'
    df.loc[df['SubTipo'] == 'SOPORTE CIRCUNFERENCIAL', 'FeatureIdentification'] = 'ESUP'
    df.loc[df['SubTipo'] == 'SOPORTE CIRCUNFERENCIAL', 'idEvento'] = '301'
    df.loc[df['SubTipo'] == 'SOPORTE CIRCUNFERENCIAL', "LongFalla [mm]"] = ''
    df.loc[df['SubTipo'] == 'SOPORTE CIRCUNFERENCIAL', "AnchoFalla [mm]"] = ''
    df.loc[df['SubTipo'] == 'CAÑO CAMISA-INICIO', 'FeatureType'] = 'COMP'
    df.loc[df['SubTipo'] == 'CAÑO CAMISA-INICIO', 'FeatureIdentification'] = 'CASB'
    df.loc[df['SubTipo'] == 'CAÑO CAMISA-INICIO', 'idEvento'] = '305'
    df.loc[df['SubTipo'] == 'CAÑO CAMISA-INICIO', "LongFalla [mm]"] = ''
    df.loc[df['SubTipo'] == 'CAÑO CAMISA-INICIO', "AnchoFalla [mm]"] = ''
    df.loc[df['SubTipo'] == 'CAÑO CAMISA-FIN', 'FeatureType'] = 'COMP'
    df.loc[df['SubTipo'] == 'CAÑO CAMISA-FIN', 'FeatureIdentification'] = 'CASE'
    df.loc[df['SubTipo'] == 'CAÑO CAMISA-FIN', 'idEvento'] = '305'
    df.loc[df['SubTipo'] == 'CAÑO CAMISA-FIN', "LongFalla [mm]"] = ''
    df.loc[df['SubTipo'] == 'CAÑO CAMISA-FIN', "AnchoFalla [mm]"] = ''

    columnas = ["ProfEfectiva [%]", "LongEfectiva [mm]","ERF AE", "PF B31G [MPa]", "PF 0.85 [MPa]", "PF AE [MPa]", "FS B31G", "FS 0.85", "FS AE", "MAPO [MPa]"]
    df.loc[df['SubTipo'] == 'ABOLLADURA', columnas] = ""

    # Actualiza la barra de progreso
    progress_bar['value'] = 70
    progress_status['text'] = "Progreso: {}%".format(progress_bar['value'])
    root.update_idletasks()  

    #Traer la orientacion de la soldadura
    df.loc[df['SubTipo'] == 'SOLDADURA', 'PosSolLong'] = df['PosFalla']
    df.loc[df['SubTipo'] == 'SOLDADURA', 'PosFalla'] = ''

#Pega el valor de orientacion de las soldaduras en las anomalias
    ultimo_valor = ''
    for index, row in df.iterrows():
        if row['SubTipo'] == 'SOLDADURA':
            ultimo_valor = row['PosSolLong']
        elif row['SubTipo'] in ['PERDIDA DE METAL', 'PERDIDA DE METAL-CLUSTER', 'ANOMALIA DE MANUFACTURA', 'ANOMALIA DE MANUFACTURA-CLUSTER', 'OBJETO METALICO', 'OBJETO DESCONOCIDO', 'REPARACION PARCHE']:
            df.loc[index, 'PosSolLong'] = ultimo_valor

        #Seleccionar solo las columnas que quiero
    df_ypf = df[["idCaracteristica", "idEvento", "Soldadura", "LongTubo [m]", "SubTipo", "FeatureType",  "FeatureIdentification", "AnomalyClass", "DistanciaRef [m]" ,
                 "DSAAr [m]", "DSAAb [m]", "DMAAr [m]", "DMAAb [m]", "PosSolLong", "EspPared [mm]", "Prof [%]", "LongFalla [mm]", "AnchoFalla [mm]", 
                 "CapaFalla", "Cluster","PosicionRelativa", "PosFalla", "Comentario", "Latitud [°]", "Longitud [°]", "Altura [m]", "ProfEfectiva [%]", "LongEfectiva [mm]",
                   "ERF AE", "PF B31G [MPa]", "PF 0.85 [MPa]", "PF AE [MPa]", "FS B31G", "FS 0.85", "FS AE", "MAPO [MPa]"]]
    
        # Actualiza la barra de progreso
    progress_bar['value'] = 100
    progress_status['text'] = "Listo"
    root.update_idletasks()  

    graph_button.config(state='normal')

    return df_ypf

def mostrar_grafico_ypf(df_ypf):
    print(df_ypf) 

    eg=df_ypf[["SubTipo", "DistanciaRef [m]", "FS AE", "EspPared [mm]", "Prof [%]"]]
    eg.loc[:, 'unos'] = 1
        # Crea una lista con los valores que deseas mantener
    valores = ["PERDIDA DE METAL", "ANOMALIA DE MANUFACTURA", "VALVULA", "AGM"]

        # Filtra el DataFrame para mantener solo las filas con los valores deseados en la columna 'sSubTipo'
    eg = eg[eg['SubTipo'].isin(valores)]
    eg["Prof [%]"] = eg["Prof [%]"].str.replace(',', '.')
    eg["Prof [%]"] = pd.to_numeric(eg["Prof [%]"], errors='coerce') / 100
    eg["DistanciaRef [m]"] = eg["DistanciaRef [m]"].str.replace(',', '.')
    eg["DistanciaRef [m]"] = pd.to_numeric(eg["DistanciaRef [m]"], errors='coerce')
    eg["FS AE"] = eg["FS AE"].str.replace(',', '.')
    eg["FS AE"] = pd.to_numeric(eg["FS AE"], errors='coerce')
    eg["EspPared [mm]"] = eg["EspPared [mm]"].str.replace(',', '.')
    eg["EspPared [mm]"] = pd.to_numeric(eg["EspPared [mm]"], errors='coerce')

    fig, (ax1, ax2,) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [2, 1]})

# Crea el primer gráfico utilizando el objeto 'ax1'
    ultimo_valor = eg["DistanciaRef [m]"].iloc[-1]
    ax1.grid(True, linestyle='--', color='lightgrey')
    ax1.plot([0, ultimo_valor], [1, 1], color='k', linestyle='-', label="Tuberia", linewidth=0.8)
    ax1.plot([0, 0], [0.95, 1.05], color='k')
    ax1.plot([ultimo_valor, ultimo_valor], [0.95, 1.05], color='k')
    ax1.scatter(eg["DistanciaRef [m]"], eg["Prof [%]"], color='#9F3C3C', label="Profundidad", marker="x")
    ax1.scatter(eg["DistanciaRef [m]"], eg["FS AE"], color='#7FC8EA', label="FS", marker="x")
    mask_valvula = eg["SubTipo"] == "VALVULA"
    ax1.scatter(eg.loc[mask_valvula, "DistanciaRef [m]"], eg.loc[mask_valvula, 'unos'], color='#2AD24B', label="Valvula", marker="^", s=100)
    mask_agm = eg["SubTipo"] == "AGM"
    ax1.scatter(eg.loc[mask_agm, "DistanciaRef [m]"], eg.loc[mask_agm, 'unos'], color='#C8C948', label="AGM", marker="p", s=70)
    max_val = eg["FS AE"].max()
    ax1.set_yticks(list(np.arange(0, 1 + 0.2, 0.2)) + list(np.arange(0, max_val + 0.2, 0.2)))
    ax1.set_yticklabels(['{:,.0%}'.format(tick) if tick < 1 else round(tick, 2) for tick in ax1.get_yticks()])
    ax1.set_title("Distribucion de Anomalias por Profundidad y  FS")

    # Agrega las etiquetas a los ejes x e y
    ax1.set_ylabel("Prof.[%]        <|>            Factor de Seguridad                     ")
    ax1.tick_params(axis='x', which='major', pad=20)


    # Crea el segundo gráfico utilizando el objeto 'ax2'
    ax2.plot(eg["DistanciaRef [m]"], eg["EspPared [mm]"], color= "#F1864C", label="Espesor")
    ax2.grid(True, linestyle='--', color='lightgrey')
    ax2.set_yticks([5.56, 6.35, 7.92, 9.52, 11.11, 12.70])
    ax2.xaxis.set_ticks_position('top')

    # Agrega las etiquetas a los ejes x e y
    ax2.set_xticklabels([])
    ax2.set_xlabel("Distancia [m]")
    ax2.set_ylabel("Espesor [mm]")

# Muestra la leyenda
    ax1.legend()
    ax2.legend()

    # Muestra la leyenda
    plt.legend()
    # Muestra el gráfico
    plt.show()
    print("Grafico YPF")
