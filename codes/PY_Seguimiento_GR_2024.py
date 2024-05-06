
""" 22 MINUTOS
PROCESAMIENTO DE LAS BASES DE SEGUIMIENTO DIARIO, SIAF-SEACE, METAS, SALDOS, ESTRUCTURA2?

"""

#importar módulos
import openpyxl as openpyxl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import re
import os
from datetime import datetime, timedelta #, date
from os import path

#Ocultando las advertencias
import warnings
import math
warnings.filterwarnings('ignore')

now = datetime.now()
print(now)
print(now.strftime("%d"))
ayer = datetime.now() - timedelta(days=1)
anteayer = datetime.now() - timedelta(days=2)
m1 = datetime.now() - timedelta(30)
m2 = datetime.now() - timedelta(60)
m3 = datetime.now() - timedelta(90)
s1 = datetime.now() - timedelta(7)

path_output = r'C:/Users/externomef/Documents/JANNELY/BASES/ProyectosAnalytica/SeguimientoMens/Outputs'
# CAMBIAR FECHAS: <<<<<<<<<<<<<<< REALIZAR CAMBIOS 
fecha_corte = now.strftime("%d") + now.strftime("%m") + now.strftime("%Y") # es la fecha actual en formato dd/mm/yyyy
fecha_corte_ayer = ayer.strftime("%d") + ayer.strftime("%m") + ayer.strftime("%Y") # fecha de corte de ayer
fecha_corte_3m =  '16' + m3.strftime("%m") + m3.strftime("%Y")  # fecha de corte de hace tres meses (15 na)
fecha_corte_2m =  '16' + m2.strftime("%m") + m2.strftime("%Y") # fecha de corte de hace 2 meses (15 na)
fecha_corte_1m =  m1.strftime("%d") + m1.strftime("%m") + m1.strftime("%Y") # fecha de corte de hace 1 mes (15 na)
fecha_corte_1s =  s1.strftime("%d") + s1.strftime("%m") + s1.strftime("%Y") # fecha de corte de hace una semana

#%% Unidades de análisis
# 1. NIVGOB, SECTOR, PLIEGO, EJECUTORA, SEC_EJEC, PRODUCTO_PROYECTO(CUI), FUENTE, GENERICA, SUBGENERICA
#       VARIABLES_FIRST: DEPARTAMENTO, PROVINCIA, DISTRITO
#       VARIABLES_SUM: PIA, PIM, CERTIFICADO, COMPROMISO_ANUAL, DEVENGADOS

# 2. NIVGOB, SECTOR, PLIEGO, PRODUCTO_PROYECTO(CUI), FUENTE, 
#       VARIABLES_FIRST: DEPARTAMENTO, PROVINCIA, DISTRITO, EJECUTORA(PRINCIPAL/UNICA)
#       VARIABLES_SUM: PIA, PIM, CERTIFICADO, COMPROMISO_ANUAL, DEVENGADOS

# 3. NIVGOB, SECTOR, PLIEGO, PRODUCTO_PROYECTO(CUI) 
#       VARIABLES_FIRST: DEPARTAMENTO, PROVINCIA, DISTRITO, EJECUTORA(PRINCIPAL/UNICA)
#       VARIABLES_SUM: PIA, PIM, CERTIFICADO, COMPROMISO_ANUAL, DEVENGADOS

#%% CARGA DE BASES (aproximadamente 23 minutos en cargar)
print(datetime.now())
# seguimiento de gasto actual y anterior


#++++++ BASES OBTENIDAS DE LOS COMPARTIDOS DE DPSP-ECI:
bd_seg22 = pd.read_excel(os.path.join(r'C:/Users/externomef/Documents/data_J', '2.PIAPIMDevGirxMetaEsp_2023_GR_' + fecha_corte +".xlsx"), sheet_name='GR') # Hasta que salga la versión final
bd_seg23 = pd.read_excel(os.path.join(r'C:/Users/externomef/Documents/data_J', '2.PIAPIMDevGirxMetaEsp_2024_GR_'+ fecha_corte +".xlsx"), sheet_name='GR') 

# los siguientes casos van según el avance del año, así que se necesita un verificador de que el archivo exista:
if os.path.isfile(os.path.join(r'C:\Users\externomef\Documents\data_J', '2.PIAPIMDevGirxMetaEsp_2024_GR_'+ fecha_corte_1s +".xlsx")) is True:
    bd_seg23_1sem = pd.read_excel(os.path.join(r'C:\Users\externomef\Documents\data_J', '2.PIAPIMDevGirxMetaEsp_2024_GR_'+ fecha_corte_1s +".xlsx"), sheet_name='GR')

if os.path.isfile(os.path.join(r'C:\Users\externomef\Documents\data_J', '2.PIAPIMDevGirxMetaEsp_2024_GR_'+ fecha_corte_1m +".xlsx")) is True:
    bd_seg23_1mes = pd.read_excel(os.path.join(r'C:\Users\externomef\Documents\data_J', '2.PIAPIMDevGirxMetaEsp_2024_GR_'+ fecha_corte_1m +".xlsx"), sheet_name='GR') ##

if os.path.isfile(os.path.join(r'C:\Users\externomef\Documents\data_J', '2.PIAPIMDevGirxMetaEsp_2024_GR_'+ fecha_corte_2m +".xlsx")) is True:
    bd_seg23_2mes = pd.read_excel(os.path.join(r'C:\Users\externomef\Documents\data_J', '2.PIAPIMDevGirxMetaEsp_2024_GR_'+ fecha_corte_2m +".xlsx"), sheet_name='GR')

if os.path.isfile(os.path.join(r'C:\Users\externomef\Documents\data_J', '2.PIAPIMDevGirxMetaEsp_2024_GR_'+ fecha_corte_3m +".xlsx")) is True:
    bd_seg23_3mes = pd.read_excel(os.path.join(r'C:\Users\externomef\Documents\data_J', '2.PIAPIMDevGirxMetaEsp_2024_GR_'+ fecha_corte_3m +".xlsx"), sheet_name='GR')

# datos del proyecto / estructura
bd_estr = pd.read_excel(os.path.join(r'C:\Users\externomef\Documents\data_J', 'Estructura2_GNGRGLMN_Proy2024_'+ fecha_corte + ".xlsx"), sheet_name='Estructura 2', usecols='B, C, D, E, G, H, I, O, P, U, V, AB, AC, AE, AF, AG, AH, AI, BT, BU') # fecha_corte_ayer

# seguimiento de dispositivos
if os.path.isfile(os.path.join(r'C:\Users\externomef\Documents\data_J', 'Dispositivos_Legales_2024_' + fecha_corte +".xlsx")) is True:
    bd_transfds = pd.read_excel(os.path.join(r'C:\Users\externomef\Documents\data_J', 'Dispositivos_Legales_2024_' + fecha_corte +".xlsx"), sheet_name='DL', usecols='C, D, F, G, H, I, J, K, M, N, O, U, Y, Z') # para identificar dispositivos legales que hayan transferido 

if os.path.isfile(os.path.join(r'C:\Users\externomef\Documents\data_J', 'FONDES_DET_2024_' + fecha_corte +".xlsx")) is True:
    bd_fondes = pd.read_excel(os.path.join(r'C:\Users\externomef\Documents\data_J', 'FONDES_DET_2024_' + fecha_corte +".xlsx")) # para identificar proyectos FONDES

#++++++ BASES OBTENIDAS DEL FORMATO 19, LUEGO DE SER CONSOLIDADA POR EL EQUIPO DE INVERSIONES:
# metas presupuestarias
path_metas = r'C:/Users/externomef/Documents/ProyectosAnalytica/z_GenBDS/zz_Formato19'
bd_metas = pd.read_csv(os.path.join(path_metas, 'formato19_2024_union'+".csv"))

#++++++ BASES OBTENIDAS POR FUENTES EXTERNAS:
#++++++ 1- CORREO DE LA DGPMI
# base de obras paralizadas
bd_contraloria = pd.read_excel(os.path.join(r'C:\Users\externomef\Documents\DATA_BASES\bd_ObrasParalDGPMI', 'REP_OBRAS_PARALIZADAS (20240107)' +".xlsx"), sheet_name='INVERSIONES', skiprows=1, usecols='E, AZ')

#++++++ BASES COMPLEMENTARIAS PARA CADENAS INSTITUCINALES:
bd_secejec = pd.read_excel(os.path.join(r'C:\Users\externomef\Documents\DATA_BASES\bd_sec_ejecs', 'Ejecutoras_15122023' +".xlsx"))

print(datetime.now())

#%% FUNCIONES 
def crear_id(df, NIVEL_GOB, SECTOR, PLIEGO, EJECUTORA):
    df = df.assign(COD_ID = np.where(df[NIVEL_GOB].str.startswith('2'), (df[PLIEGO].str.split('. ', n=1).str[0] +"-" + df[EJECUTORA].str.split('. ', n=1).str[0]),
                                     (df[SECTOR].str.split('. ', n=1).str[0] +"-" + df[PLIEGO].str.split('. ', n=1).str[0] +"-"+ df[EJECUTORA].str.split('. ', n=1).str[0])))
    return df
   
def crear_idpliegog(df, NIVEL_GOB, SECTOR, PLIEGO):
    df = df.assign(COD_PLIEGO = df[NIVEL_GOB].str.split('. ',n=1).str[0] + '-' + df[SECTOR].str.split('. ', n=1).str[0] + '-' + df[PLIEGO].str.split('. ', n=1).str[0])
    return df

def postmerge(df):
    replace_list = [i for i in df.columns if (i.endswith('_x'))]
    replace_list = [i[:-2] for i in replace_list]
    for i in replace_list:
        df[i] = df[i+'_x'].fillna(df[i+'_y'])
    df.drop([i for i in df.columns if (i.endswith('_x'))|(i.endswith('_y'))], inplace=True, axis=1)
    return df

def rangos_10(df, VARIABLE_10):
    df = df.assign(RANGO_VARIABLE_10 = np.where((df[VARIABLE_10]>0.9)&(df[VARIABLE_10]<=1), "(90-100%]", 
                                                np.where((df[VARIABLE_10]>0.8)&(df[VARIABLE_10]<=0.9), "(80-90%]",
                                                         np.where((df[VARIABLE_10]>0.7)&(df[VARIABLE_10]<=0.8), "(70-80%]",
                                                                  np.where((df[VARIABLE_10]>0.6)&(df[VARIABLE_10]<=0.7), "(60-70%]",
                                                                           np.where((df[VARIABLE_10]>0.5)&(df[VARIABLE_10]<=0.6), "(50-60%]",
                                                                                    np.where((df[VARIABLE_10]>0.4)&(df[VARIABLE_10]<=0.5), "(40-50%]",
                                                                                             np.where((df[VARIABLE_10]>0.3)&(df[VARIABLE_10]<=0.4), "(30-40%]",
                                                                                                      np.where((df[VARIABLE_10]>0.2)&(df[VARIABLE_10]<=0.3), "(20-30%]",
                                                                                                               np.where((df[VARIABLE_10]>0.1)&(df[VARIABLE_10]<=0.2), "(10-20%]",
                                                                                                                        np.where((df[VARIABLE_10]>0)&(df[VARIABLE_10]<=0.1), "(0%-10%]", 'Sin avance')))))))))))
    return df

#%% Identificador de Sec Ejec 
sec_ejec = bd_secejec.copy()

sec_ejec = crear_id(sec_ejec, 'NIVEL_GOB', 'SECTOR', 'PLIEGO', 'EJECUTORA')
sec_ejec = sec_ejec[['COD_ID', 'NIVEL_GOB', 'SECTOR', 'PLIEGO', 'EJECUTORA']]

#%% Para identificar luego los proyectos que han sido catalogados como paralizados por la contraloría
obras_paral = bd_contraloria.copy(deep=True)
obras_paral= obras_paral[['CODIGO UNICO', 'TIPO MOTIVO']]
obras_paral.rename(columns={'CODIGO UNICO':'CODIGO_UNICO', 'TIPO MOTIVO':'CAUSA_DE_PARALIZACION'}, inplace=True)
obras_paral['CODIGO_UNICO'] = obras_paral['CODIGO_UNICO'].astype(int).astype(str)
obras_paral = obras_paral.drop_duplicates(subset=['CODIGO_UNICO', 'CAUSA_DE_PARALIZACION'])
obras_paral = obras_paral.groupby(['CODIGO_UNICO']).agg({'CAUSA_DE_PARALIZACION':' - '.join}).reset_index()

#%% bases de seguimiento (toma aprox 30 segundos)
print(datetime.now())
colap_1 = ['COD_ID', 'CODIGO_UNICO', 'COD_FF', 'COD_GGSG']
colap_2 = ['COD_ID', 'CODIGO_UNICO', 'COD_FF']
colap_3 = ['COD_ID', 'CODIGO_UNICO']

seg_to_first_1 = ['NIVEL_GOB', 'SECTOR', 'PLIEGO', 'EJECUTORA', 'NOMBRE_PROYECTO', 'DEPARTAMENTO', 'PROVINCIA', 'DISTRITO', 'FUENTE', 'GENERICA', 'SUBGENERICA', 'SUBGENERICA_DET', 'ESPECIFICA', 'ESPECIFICA_DET']
seg_to_first_2 = ['NIVEL_GOB', 'SECTOR', 'PLIEGO', 'NOMBRE_PROYECTO', 'DEPARTAMENTO', 'PROVINCIA', 'DISTRITO' , 'FUENTE']
seg_to_first_3 = ['NIVEL_GOB', 'SECTOR', 'NOMBRE_PROYECTO', 'DEPARTAMENTO', 'PROVINCIA', 'DISTRITO']

seg_to_sum = ['PIA', 'PIM', 'CERTIFICADO', 'COMPROMISO_ANUAL', 'DEV01', 'DEV02', 'DEV03', 'DEV04', 'DEV05', 
              'DEV06', 'DEV07', 'DEV08', 'DEV09', 'DEV10', 'DEV11', 'DEV12', 'TOTAL_DEVENGADO']

# para evitar riesgos, hacemos la corrida x separado
############################################################################### AÑO = 2023
seg22 = bd_seg22.copy()

seg22['COD_FF'] = seg22['FUENTE'].str.split('. ',n=1).str[0]
seg22['COD_GG'] = seg22['GENERICA'].str.split('. ',n=1).str[0]
seg22['COD_SG'] = seg22['SUBGENERICA'].str.split('. ',n=1).str[0]
seg22['COD_SGD'] = seg22['SUBGENERICA_DET'].str.split('. ',n=1).str[0]
seg22['COD_ESP'] = seg22['ESPECIFICA'].str.split('. ',n=1).str[0]
seg22['COD_ESP_DET'] = seg22['ESPECIFICA_DET'].str.split('. ',n=1).str[0]
seg22['COD_GGSG'] = seg22['COD_GG'] + '.' + seg22['COD_SG'] + '.' + seg22['COD_SGD'] + '.' + seg22['COD_ESP'] + '.' + seg22['COD_ESP_DET']

seg22.rename(columns={'NIVEL_GOBIERNO':'NIVEL_GOB'}, inplace=True)
seg22 = crear_id(seg22, 'NIVEL_GOB', 'SECTOR', 'PLIEGO', 'EJECUTORA')
seg22 = crear_idpliegog(seg22, 'NIVEL_GOB', 'SECTOR', 'PLIEGO')
seg22['CODIGO_UNICO'] = seg22['PRODUCTO_PROYECTO'].str.split('. ',n=1).str[0]
seg22['NOMBRE_PROYECTO'] = seg22['PRODUCTO_PROYECTO'].str.split('. ',n=1).str[1]
seg22['TIPO_PROD_PROY'] = np.where(seg22['CODIGO_UNICO'].str.startswith('2'),'PROYECTOS','PRODUCTOS')
seg22 = seg22[(seg22['TIPO_PROD_PROY']=='PROYECTOS')]

dict_estb_1 = {}
for x in seg_to_first_1:
    dict_estb_1[x] = 'first'
for x in seg_to_sum:
    dict_estb_1[x] = 'sum'
    
dict_estb_2 = {}
for x in seg_to_first_2:
    dict_estb_2[x] = 'first'
for x in seg_to_sum:
    dict_estb_2[x] = 'sum'
    
dict_estb_3 = {}
for x in seg_to_first_3:
    dict_estb_3[x] = 'first'
for x in seg_to_sum:
    dict_estb_3[x] = 'sum'
    
seg22_2 = seg22.groupby(colap_2).agg(dict_estb_2).reset_index()

dict_rename = {}
for x in seg_to_sum:
    dict_rename[x] = x+'_2023'
seg22_2.rename(columns=dict_rename, inplace=True)

############################################################################### AÑO = 2024
seg23 = bd_seg23.copy()

seg23['COD_FF'] = seg23['FUENTE'].str.split('. ',n=1).str[0]
seg23['COD_GG'] = seg23['GENERICA'].str.split('. ',n=1).str[0]
seg23['COD_SG'] = seg23['SUBGENERICA'].str.split('. ',n=1).str[0]
seg23['COD_SGD'] = seg23['SUBGENERICA_DET'].str.split('. ',n=1).str[0]
seg23['COD_ESP'] = seg23['ESPECIFICA'].str.split('. ',n=1).str[0]
seg23['COD_ESP_DET'] = seg23['ESPECIFICA_DET'].str.split('. ',n=1).str[0]
seg23['COD_GGSG'] = seg23['COD_GG'] + '.' + seg23['COD_SG'] + '.' + seg23['COD_SGD'] + '.' + seg23['COD_ESP'] + '.' + seg23['COD_ESP_DET']

seg23.rename(columns={'NIVEL_GOBIERNO':'NIVEL_GOB'}, inplace=True)
seg23 = crear_id(seg23, 'NIVEL_GOB', 'SECTOR', 'PLIEGO', 'EJECUTORA')
seg23 = crear_idpliegog(seg23, 'NIVEL_GOB', 'SECTOR', 'PLIEGO')
seg23['CODIGO_UNICO'] = seg23['PRODUCTO_PROYECTO'].str.split('. ',n=1).str[0]
seg23['NOMBRE_PROYECTO'] = seg23['PRODUCTO_PROYECTO'].str.split('. ',n=1).str[1]
seg23['TIPO_PROD_PROY'] = np.where(seg23['CODIGO_UNICO'].str.startswith('2'),'PROYECTOS','PRODUCTOS')
seg23 = seg23[(seg23['TIPO_PROD_PROY']=='PROYECTOS')]

dict_estb_1 = {}
for x in seg_to_first_1:
    dict_estb_1[x] = 'first'
for x in seg_to_sum:
    dict_estb_1[x] = 'sum'
    
dict_estb_2 = {}
for x in seg_to_first_2:
    dict_estb_2[x] = 'first'
for x in seg_to_sum:
    dict_estb_2[x] = 'sum'
    
dict_estb_3 = {}
for x in seg_to_first_3:
    dict_estb_3[x] = 'first'
for x in seg_to_sum:
    dict_estb_3[x] = 'sum'
    
seg23_1 = seg23.groupby(colap_1).agg(dict_estb_1).reset_index()
seg23_2 = seg23.groupby(colap_2).agg(dict_estb_2).reset_index()
seg23_3 = seg23.groupby(colap_3).agg(dict_estb_3).reset_index()

dict_rename = {}
for x in seg_to_sum:
    dict_rename[x] = x+'_2024'
seg23_1.rename(columns=dict_rename, inplace=True)
seg23_2.rename(columns=dict_rename, inplace=True)
seg23_3.rename(columns=dict_rename, inplace=True)

print(datetime.now())

#%% Seguimiento del mes anterior y la semana anterior
try:
    seg23_1mes = bd_seg23_1mes.copy()
    seg23_1mes.rename(columns={'NIVEL_GOBIERNO':'NIVEL_GOB'}, inplace=True)
    seg23_1mes = crear_id(seg23_1mes, 'NIVEL_GOB', 'SECTOR', 'PLIEGO', 'EJECUTORA')
    seg23_1mes['COD_FF'] = seg23_1mes['FUENTE'].str.split('. ',n=1).str[0]
    seg23_1mes['CODIGO_UNICO'] = seg23_1mes['PRODUCTO_PROYECTO'].str.split('. ',n=1).str[0]

    seg23_1mes = seg23_1mes.groupby(['COD_ID', 'COD_FF', 'CODIGO_UNICO']).agg({'PIM':'sum', 'CERTIFICADO':'sum', 'COMPROMISO_ANUAL':'sum', 'TOTAL_DEVENGADO':'sum'}).reset_index()
    seg23_1mes.rename(columns={'PIM':'PIM_MESPREV', 'CERTIFICADO':'CERTIFICADO_MESPREV', 'COMPROMISO_ANUAL':'COMPROMISO_MESPREV', 'TOTAL_DEVENGADO':'DEVENGADO_MESPREV'}, inplace=True)
except:
    print('no se cargó o no existen los datos de hace 1 mes para este año')
    
try:
    seg23_2mes = bd_seg23_2mes.copy()
    seg23_2mes.rename(columns={'NIVEL_GOBIERNO':'NIVEL_GOB'}, inplace=True)
    seg23_2mes = crear_id(seg23_2mes, 'NIVEL_GOB', 'SECTOR', 'PLIEGO', 'EJECUTORA')
    seg23_2mes['COD_FF'] = seg23_2mes['FUENTE'].str.split('. ',n=1).str[0]
    seg23_2mes['CODIGO_UNICO'] = seg23_2mes['PRODUCTO_PROYECTO'].str.split('. ',n=1).str[0]

    seg23_2mes = seg23_2mes.groupby(['COD_ID', 'COD_FF', 'CODIGO_UNICO']).agg({'PIM':'sum', 'CERTIFICADO':'sum', 'COMPROMISO_ANUAL':'sum', 'TOTAL_DEVENGADO':'sum'}).reset_index()
    seg23_2mes.rename(columns={'PIM':'PIM_MES2PREV', 'CERTIFICADO':'CERTIFICADO_MES2PREV', 'COMPROMISO_ANUAL':'COMPROMISO_MES2PREV', 'TOTAL_DEVENGADO':'DEVENGADO_MES2PREV'}, inplace=True)
except:
    print('no se cargó o no existen los datos de hace 2 meses para este año')
    
try:
    seg23_3mes = bd_seg23_3mes.copy()
    seg23_3mes.rename(columns={'NIVEL_GOBIERNO':'NIVEL_GOB'}, inplace=True)
    seg23_3mes = crear_id(seg23_3mes, 'NIVEL_GOB', 'SECTOR', 'PLIEGO', 'EJECUTORA')
    seg23_3mes['COD_FF'] = seg23_3mes['FUENTE'].str.split('. ',n=1).str[0]
    seg23_3mes['CODIGO_UNICO'] = seg23_3mes['PRODUCTO_PROYECTO'].str.split('. ',n=1).str[0]

    seg23_3mes = seg23_3mes.groupby(['COD_ID', 'COD_FF', 'CODIGO_UNICO']).agg({'PIM':'sum', 'CERTIFICADO':'sum', 'COMPROMISO_ANUAL':'sum', 'TOTAL_DEVENGADO':'sum'}).reset_index()
    seg23_3mes.rename(columns={'PIM':'PIM_MES3PREV', 'CERTIFICADO':'CERTIFICADO_MES3PREV', 'COMPROMISO_ANUAL':'COMPROMISO_MES3PREV', 'TOTAL_DEVENGADO':'DEVENGADO_MES3PREV'}, inplace=True)
except:
    print('no se cargó o no existen los datos de hace 3 meses para este año')
    
try:
    seg23_1sem = bd_seg23_1sem.copy()
    seg23_1sem.rename(columns={'NIVEL_GOBIERNO':'NIVEL_GOB'}, inplace=True)
    seg23_1sem = crear_id(seg23_1sem, 'NIVEL_GOB', 'SECTOR', 'PLIEGO', 'EJECUTORA')
    seg23_1sem['COD_FF'] = seg23_1sem['FUENTE'].str.split('. ',n=1).str[0]
    seg23_1sem['CODIGO_UNICO'] = seg23_1sem['PRODUCTO_PROYECTO'].str.split('. ',n=1).str[0]

    seg23_1sem = seg23_1sem.groupby(['COD_ID', 'COD_FF', 'CODIGO_UNICO']).agg({'PIM':'sum', 'CERTIFICADO':'sum', 'COMPROMISO_ANUAL':'sum', 'TOTAL_DEVENGADO':'sum'}).reset_index()
    seg23_1sem.rename(columns={'PIM':'PIM_SEMPREV', 'CERTIFICADO':'CERTIFICADO_SEMPREV', 'COMPROMISO_ANUAL':'COMPROMISO_SEMPREV', 'TOTAL_DEVENGADO':'DEVENGADO_SEMPREV'}, inplace=True)
except:
    print('no se cargó o no existen los datos de hace 1 semana para este año')
    
#%%############################################################################## (2 segundos)
# CODIGOS DE UNIVERSIDADES PARA DISTINGUIRLAS DEL MINEDU

codigos_universidades = bd_seg23.copy(deep=True)
codigos_universidades = codigos_universidades[codigos_universidades['SECTOR']=='10. EDUCACION']
codigos_universidades = codigos_universidades[codigos_universidades['PLIEGO'].astype(str).str[0] == '5'] # Pliegos que inician con "5" son universidades
codigos_universidades = codigos_universidades.PLIEGO.str.split('.',n=1).str[0].unique()

#%% Estructuras con datos complementarios de los proyectos
estructuras = bd_estr.copy(deep=True)
estructuras = crear_id(estructuras, 'NIVEL_GOB', 'SECTOR', 'PLIEGO', 'EJECUTORA')
estructuras['CODIGO_UNICO'] = estructuras['CODIGO_UNICO'].astype(int).astype(str)
estructuras = estructuras.drop_duplicates(subset=['CODIGO_UNICO', 'COD_ID'])

#%% Metas de todos los trimestres

meses_dict = {'01':'ENERO', '02':'FEBRERO', '03':'MARZO', '04':'ABRIL', '05':'MAYO', '06':'JUNIO', '07':'JULIO', '08':'AGOSTO', 
              '09':'SETIEMBRE', '10':'OCTUBRE', '11':'NOVIEMBRE', '12':'DICIEMBRE'}

# Metas del 2024 - Trimestral
metas = bd_metas.copy()
metas = metas[metas['NIVEL_GOB']=='2. GOBIERNO REGIONAL']
metas.drop(columns=['NIVEL_GOB', 'COD_FTE'], inplace=True)
metas['CODIGO_UNICO'] = metas['CODIGO_UNICO'].astype(int).astype(str)

if datetime.now().month >= 1:
    for n in list(range(1,13)):
        metas.rename(columns={'META_'+ meses_dict[str(n).zfill(2)] +'_TRIM1': 'META_'+ str(n).zfill(2) +'_T1'}, inplace=True)
    metas_lista = [i for i in metas.columns.to_list() if ((i.startswith('META_'))&(i.endswith('T1')))]
    meta_trim1 = metas_lista.copy()
    metas['META_2024.VT1'] = metas[metas_lista].sum(axis=1, min_count=1)
        
if datetime.now().month >= 4:
    for n in list(range(4,13)):
        metas.rename(columns={'META_'+ meses_dict[str(n).zfill(2)] +'_TRIM2': 'META_'+ str(n).zfill(2) +'_T2'}, inplace=True)
    metas_lista = [i for i in metas.columns.to_list() if ((i.startswith('META_'))&(i.endswith('T2')))]
    meta_trim2 = metas_lista.copy()
    metas['META_2024.VT2'] = metas[metas_lista].sum(axis=1, min_count=1)
    
if datetime.now().month >= 7:
    for n in list(range(7,13)):
        metas.rename(columns={'META_'+ meses_dict[str(n).zfill(2)] +'_TRIM3': 'META_'+ str(n).zfill(2) +'_T3'}, inplace=True)
    metas_lista = [i for i in metas.columns.to_list() if ((i.startswith('META_'))&(i.endswith('T3')))]
    meta_trim3 = metas_lista.copy()
    metas['META_2024.VT3'] = metas[metas_lista].sum(axis=1, min_count=1)
    
if datetime.now().month >= 10:
    for n in list(range(10,13)):
        metas.rename(columns={'META_'+ meses_dict[str(n).zfill(2)] +'_TRIM4': 'META_'+ str(n).zfill(2) +'_T4'}, inplace=True)
    metas_lista = [i for i in metas.columns.to_list() if ((i.startswith('META_'))&(i.endswith('T4')))]
    meta_trim4 = metas_lista.copy()
    metas['META_2024.VT4'] = metas[metas_lista].sum(axis=1, min_count=1)

metas = metas.merge(sec_ejec[['COD_ID', 'NIVEL_GOB', 'SECTOR', 'PLIEGO', 'EJECUTORA']], on=['COD_ID'], how='left', validate='m:1')

# Completitud para el dashboard
if datetime.now().month < 4:
    for t in list(range(2,5)):
            metas['META_2024.VT'+str(t)] = np.nan
            metas['PIM_PROYECTADO_2024_T'+str(t)] = np.nan
if (datetime.now().month >= 4)&(datetime.now().month < 7):
    for t in list(range(3,5)):
            metas['PIM_PROYECTADO_2024_T'+str(t)] = np.nan
if (datetime.now().month >= 7)&(datetime.now().month < 10):
    for t in list(range(2,5)):
            metas['PIM_PROYECTADO_2024_T'+str(t)] = np.nan

metas_mod = metas[['CODIGO_UNICO', 'MODALIDAD_EJECUCION', 'ESTADO_SITUACIONAL_PROYECTO']]
metas_mod = metas_mod[metas_mod['MODALIDAD_EJECUCION'].notna()]
metas_mod = metas_mod.sort_values(by=['CODIGO_UNICO', 'MODALIDAD_EJECUCION', 'ESTADO_SITUACIONAL_PROYECTO'], ascending=[True, False, False]).reset_index()
metas_mod = metas_mod.groupby(['CODIGO_UNICO']).agg({'MODALIDAD_EJECUCION':'first', 'ESTADO_SITUACIONAL_PROYECTO':'first'}).reset_index()

#%% Transferencias para alertar de proyectos que en este año han recibido recursos adicionales, lo cual no sería coherente
try:
    dstransf = bd_transfds.copy()
    dstransf.rename(columns={'NIV_GOBIERNO':'NIVEL_GOB'}, inplace=True)
    dstransf = dstransf[(dstransf['MARCO_PPTAL']>0)&(dstransf['TIPO_PROD_PROY']=='2. PROYECTOS')] # no solo a los del GR
    dstransf['CODIGO_UNICO'] = dstransf['PRODUCTO'].str.split(". ",n=1).str[0]
    dstransf = crear_id(dstransf, 'NIVEL_GOB', 'SECTOR', 'PLIEGO', 'EJECUTORA')
    
    dstransf = dstransf.groupby(['CODIGO_UNICO', 'COD_ID', 'DISPOSITIVO']).agg({'MARCO_PPTAL':'sum'}).reset_index()
    dstransf_incorpora = dstransf.groupby(['CODIGO_UNICO', 'COD_ID']).agg({'MARCO_PPTAL':'sum'}).reset_index()
    dstransf_incorpora.rename(columns={'MARCO_PPTAL':'INCORPORACIONES.DS2024'}, inplace=True)
    
    #--------------------------------
    dstransf_reduccion = bd_transfds.copy()
    dstransf_reduccion.rename(columns={'NIV_GOBIERNO':'NIVEL_GOB'}, inplace=True)
    dstransf_reduccion = dstransf_reduccion[(dstransf_reduccion['MARCO_PPTAL']<0)&(dstransf_reduccion['TIPO_PROD_PROY']=='2. PROYECTOS')] # no solo a los del GR
    dstransf_reduccion['CODIGO_UNICO'] = dstransf_reduccion['PRODUCTO'].str.split(". ",n=1).str[0]
    dstransf_reduccion = crear_id(dstransf_reduccion, 'NIVEL_GOB', 'SECTOR', 'PLIEGO', 'EJECUTORA')
    
    dstransf_reduccion = dstransf_reduccion.groupby(['CODIGO_UNICO', 'COD_ID', 'DISPOSITIVO']).agg({'MARCO_PPTAL':'sum'}).reset_index()
    dstransf_reduccion = dstransf_reduccion.groupby(['CODIGO_UNICO', 'COD_ID']).agg({'MARCO_PPTAL':'sum'}).reset_index()
    dstransf_reduccion.rename(columns={'MARCO_PPTAL':'REDUCCIONES.DS2024'}, inplace=True)

except:
    print('No existe o no se cargó la base de dispositivos')

#%% NOS PERMITE IDENTIFICAR SI UN PROYECTO TUVO MARCO FONDES EN EL 2024 Y POR CUÁNTO, A LA FECHA. ESTÁ EN TRES NIVELES: FF, CODID, CUI; CODID, CUI; SECTOR,PLIEGO,CUI
try:
    fondes = bd_fondes.copy()
    fondes.rename(columns={'NIVEL_GOBIERNO':'NIVEL_GOB', 'ENTIDAD':'EJECUTORA'}, inplace=True)
    fondes = crear_id(fondes, 'NIVEL_GOB', 'SECTOR', 'PLIEGO', 'EJECUTORA')
    fondes['CODIGO_UNICO'] =fondes['PRODUCTO_PROYECTO'].str.split(". ",n=1).str[0]
    fondes = fondes[['COD_ID', 'CODIGO_UNICO']].drop_duplicates() # duplicados = 0

except:
    print('No existe o no se cargó la base de fondes')
    
#%% REPORTE 1. A NIVEL DE FUENTE Y CODIGO DE GENERICA, PARA IDENTIFICAR LA CALIDAD DEL GASTO QUE SE REALIZA. 

# EL UNIVERSO SE CONFORMA DEL SEGUIMIENTO 23

seg23_xsg = seg23_1.copy()
seg23_xsg['ETIQUETA_SUBG'] = ''

# Infraestructura
seg23_xsg['ETIQUETA_SUBG'] = np.where(seg23_xsg['SUBGENERICA'].isin({'1. ADQUISICION DE EDIFICIOS Y ESTRUCTURAS', 
                                                                     '2. CONSTRUCCION DE EDIFICIOS Y ESTRUCTURAS'}), 'INFRAESTRUCTURA', seg23_xsg['ETIQUETA_SUBG'])

# Adquisicion de activos
seg23_xsg['ETIQUETA_SUBG'] = np.where(seg23_xsg['SUBGENERICA'].isin({'3. ADQUISICION DE VEHICULOS, MAQUINARIAS Y OTROS', 
                                                                     '4. ADQUISICION DE OBJETOS DE VALOR', 
                                                                     '6. ADQUISICION DE OTROS ACTIVOS FIJOS',
                                                                     '7. INVERSIONES INTANGIBLES'}), 'ADQUISICIONES_ACTIVOS', seg23_xsg['ETIQUETA_SUBG'])
seg23_xsg['ETIQUETA_SUBG'] = np.where((seg23_xsg['SUBGENERICA'].isin({'8. OTROS GASTOS DE ACTIVOS NO FINANCIEROS'}))&
                                      (seg23_xsg['ESPECIFICA'].isin({'4. OTROS GASTOS DIVERSOS DE ACTIVOS NO FINANCIEROS'}))&
                                      (seg23_xsg['ESPECIFICA_DET'].str[0].isin({'2'})), 'ADQUISICIONES_ACTIVOS', seg23_xsg['ETIQUETA_SUBG'])

# Terrenos
seg23_xsg['ETIQUETA_SUBG'] = np.where(seg23_xsg['SUBGENERICA'].isin({'5. ADQUISICION DE ACTIVOS NO PRODUCIDOS'}), 'TERRENOS', seg23_xsg['ETIQUETA_SUBG'])

# Estudios
seg23_xsg['ETIQUETA_SUBG'] = np.where((seg23_xsg['SUBGENERICA'].isin({'8. OTROS GASTOS DE ACTIVOS NO FINANCIEROS'}))&
                                      (seg23_xsg['ESPECIFICA'].isin({'2. ESTUDIO DE PREINVERSION', 
                                                                     '3. ELABORACION DE EXPEDIENTES TECNICOS'})), 'ESTUDIOS', seg23_xsg['ETIQUETA_SUBG'])

# Gasto en laudos
seg23_xsg['ETIQUETA_SUBG'] = np.where((seg23_xsg['SUBGENERICA'].isin({'8. OTROS GASTOS DE ACTIVOS NO FINANCIEROS'}))&
                                      (seg23_xsg['ESPECIFICA'].isin({'4. OTROS GASTOS DIVERSOS DE ACTIVOS NO FINANCIEROS'}))&
                                      (seg23_xsg['ESPECIFICA_DET'].str[0].isin({'4'})), 'LAUDOS', seg23_xsg['ETIQUETA_SUBG'])

# Gasto en personal
seg23_xsg['ETIQUETA_SUBG'] = np.where((seg23_xsg['SUBGENERICA'].isin({'8. OTROS GASTOS DE ACTIVOS NO FINANCIEROS'}))&
                                      (seg23_xsg['ESPECIFICA'].isin({'4. OTROS GASTOS DIVERSOS DE ACTIVOS NO FINANCIEROS'}))&
                                      (seg23_xsg['ESPECIFICA_DET'].str[0].isin({'3', '1'})), 'PERSONAL', seg23_xsg['ETIQUETA_SUBG'])

# Gasto en personal
seg23_xsg['ETIQUETA_SUBG'] = np.where((seg23_xsg['SUBGENERICA'].isin({'8. OTROS GASTOS DE ACTIVOS NO FINANCIEROS'}))&
                                      (seg23_xsg['ESPECIFICA'].isin({'4. OTROS GASTOS DIVERSOS DE ACTIVOS NO FINANCIEROS'}))&
                                      (seg23_xsg['ESPECIFICA_DET'].str[0].isin({'9'})), 'OTROS', seg23_xsg['ETIQUETA_SUBG'])

# Gasto en transferenicas y subvenciones
seg23_xsg['ETIQUETA_SUBG'] = np.where((seg23_xsg['GENERICA'].str[0].isin({'4', '5'})), 'TRANSFERENCIAS', seg23_xsg['ETIQUETA_SUBG'])



seg23_xsg = seg23_xsg.groupby(['COD_ID', 'CODIGO_UNICO', 'COD_FF', 'ETIQUETA_SUBG']).agg({'TOTAL_DEVENGADO_2024':'sum'}).reset_index()
seg23_xsg['ETIQUETA_SUBG'] = seg23_xsg['ETIQUETA_SUBG'].replace({'ESTUDIOS':'_EST', 'PERSONAL':'_PERS', 'OTROS':'_OTRO', 'ADQUISICIONES_ACTIVOS':'_AAC', 'TRANSFERENCIAS':'_TRF', 'INFRAESTRUCTURA':'_INF', 'TERRENOS':'_TER', 'LAUDOS':'_LAU'})
seg23_xsg = seg23_xsg.pivot(index = ['COD_ID', 'CODIGO_UNICO', 'COD_FF'], columns='ETIQUETA_SUBG', values=['TOTAL_DEVENGADO_2024']).reset_index().rename_axis(None)
seg23_xsg.columns = [f'{i}{j}' for i, j in seg23_xsg.columns]

for n in ['TOTAL_DEVENGADO_2024_AAC', 'TOTAL_DEVENGADO_2024_EST', 'TOTAL_DEVENGADO_2024_INF', 'TOTAL_DEVENGADO_2024_OTRO', 'TOTAL_DEVENGADO_2024_PERS', 
          'TOTAL_DEVENGADO_2024_TER', 'TOTAL_DEVENGADO_2024_TRF', 'TOTAL_DEVENGADO_2024_LAU']:
    if n not in seg23_xsg.columns:
        seg23_xsg[n] = 0
    


#%% +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ REPORTE 2. TABLERO DE SEGUIMIENTO POR FF, CUI




# EL UNIVERSO SE CONFORMA DEL SEGUIMIENTO 23 + SEGUIMIENTO 22 + METAS

############################################################################### 1 Primero compilamos las bases de seguimiento.

# Insumo para el análisis por genéricas
bd_tablero2 = seg23_2.merge(seg23_xsg, on=['COD_ID', 'CODIGO_UNICO', 'COD_FF'], how='left', validate='1:1', indicator=False)
bd_tablero2.rename(columns={'TOTAL_DEVENGADO_2024_AAC':'TD2024_AAC', 'TOTAL_DEVENGADO_2024_CYO':'TD2024_CYO', 'TOTAL_DEVENGADO_2024_EST':'TD2024_EST',
                            'TOTAL_DEVENGADO_2024_INF':'TD2024_INF', 'TOTAL_DEVENGADO_2024_TER':'TD2024_TER', 'TOTAL_DEVENGADO_2024_PERS':'TD2024_PERS', 'TOTAL_DEVENGADO_2024_OTRO':'TD2024_OTRO',
                            'TOTAL_DEVENGADO_2024_TRF':'TD2024_TRF', 'TOTAL_DEVENGADO_2024_LAU':'TD2024_LAU'}, inplace=True)

# Insumo de las bases para variacion mensual y de la última semana
try:
    bd_tablero2 = bd_tablero2.merge(seg23_1mes, on=['COD_ID', 'CODIGO_UNICO', 'COD_FF'], how='left', validate='1:1', indicator=False)
except:
    print('sin información de hace 1 mes')
    
try:
    bd_tablero2 = bd_tablero2.merge(seg23_2mes, on=['COD_ID', 'CODIGO_UNICO', 'COD_FF'], how='left', validate='1:1', indicator=False)
except:
    print('sin información de hace 2 meses')
    
try:
    bd_tablero2 = bd_tablero2.merge(seg23_3mes, on=['COD_ID', 'CODIGO_UNICO', 'COD_FF'], how='left', validate='1:1', indicator=False)
except:
    print('sin informaci´n de hace 3 meses')
    
try:
    bd_tablero2 = bd_tablero2.merge(seg23_1sem, on=['COD_ID', 'CODIGO_UNICO', 'COD_FF'], how='left', validate='1:1', indicator=False)
except:
    print('sin información de hace 1 semana')

# Seguimiento del año anterior
bd_tablero2 = bd_tablero2.merge(seg22_2, on=['COD_ID', 'CODIGO_UNICO', 'COD_FF'], how='outer', validate='1:1', indicator=False)
bd_tablero2 = postmerge(bd_tablero2)
 
############################################################################### 2 Estructura 2 para información del proyecto

bd_tablero2 = bd_tablero2.merge(estructuras, on=['CODIGO_UNICO', 'COD_ID'], how='left', validate='m:1', indicator=False)
bd_tablero2 = postmerge(bd_tablero2)

bd_tablero2['EXP_TCO_ACTUAL'] = bd_tablero2['EXP_TCO_BCO'] # AJUSTANDO EL ET
bd_tablero2['EXP_TCO_ACTUAL'] = np.where(bd_tablero2['ET_VIGENTE']=='NO', 'NO', bd_tablero2['EXP_TCO_ACTUAL'])

bd_tablero2['TIPO_PROYECTO'] = bd_tablero2['TIPO_PROYECTO'].replace({'F. PROYECTOS CON FUR (IRI)':'IRI', '5. PROYECTOS DE INVERSION - INVIERTE':'PI',
                                                                   'N. PROYECTOS QUE NO SON PIPS (IOARR)':'IOARR', '4. PROYECTO GENERICO':'GENERICO',
                                                                   '1. PROYECTO CON PRE INVERSION SNIP':'PI-SNIP', 'G. PROYECTO DE GESTION Y OTROS':'GESTION', 
                                                                   '2. PROYECTO ANTERIOR AL SNIP':'PRE-SNIP', '3. PROYECTO EXONERADO POR DS':'EXONERADO', 
                                                                   'P. PROYECTOS DE PROCOMPITE':'PROCOMPITE', '6. PROYECTO DE EMERGENCIA':'EMERGENCIA'})

bd_tablero2['DEVENGADO_2024_CUI'] = bd_tablero2.groupby(['CODIGO_UNICO'])['TOTAL_DEVENGADO_2024'].transform('sum')
bd_tablero2['PIM_2024_CUI'] = bd_tablero2.groupby(['CODIGO_UNICO'])['PIM_2024'].transform('sum')

# AVANCE DE EJECUCIÓN AL 2023
bd_tablero2['PCT.AVANCE_AL2023'] = np.where((bd_tablero2['COSTO_ACTUAL_BCO'].fillna(0)<=0), np.nan, (bd_tablero2['ACM_DEV_AL2023']/bd_tablero2['COSTO_ACTUAL_BCO']))
bd_tablero2['PCT.AVANCE_AL2023'] = np.where(bd_tablero2['PCT.AVANCE_AL2023']>1, 1, bd_tablero2['PCT.AVANCE_AL2023'])

bd_tablero2['VARIABLE_10'] = bd_tablero2['PCT.AVANCE_AL2023'] # Para crear la variable de rango
bd_tablero2 = rangos_10(bd_tablero2, 'VARIABLE_10') # Variable de rango
bd_tablero2.rename(columns={'RANGO_VARIABLE_10':'RANGO.AVANCE_AL2023'}, inplace=True)
bd_tablero2['RANGO.AVANCE_AL2023'] = np.where((bd_tablero2['COSTO_ACTUAL_BCO'].fillna(0)==0), 'Sin costo', bd_tablero2['RANGO.AVANCE_AL2023'])

bd_tablero2.drop(columns=['VARIABLE_10', 'COD_FF'], inplace=True)

############################################################################### 3 Proyecciones de ejecucion o metas

bd_tablero2 = bd_tablero2.merge(metas, on=['CODIGO_UNICO', 'COD_ID', 'FUENTE'], how='outer', validate='1:1', indicator=False)
bd_tablero2 = postmerge(bd_tablero2)
bd_tablero2.drop(columns=['MODALIDAD_EJECUCION', 'ESTADO_SITUACIONAL_PROYECTO'], inplace=True)


############################################################################### 3. VARIABLES COMPLEMENTARIAS (PARALIZADOS Y MODALIDAD)

# Obras paralizadas
bd_tablero2 = bd_tablero2.merge(obras_paral, on = ['CODIGO_UNICO'], how='left', validate='m:1', indicator=True)
bd_tablero2.rename(columns= {'_merge':'ID_ObraParal'}, inplace=True)
bd_tablero2['ID_ObraParal'] = bd_tablero2['ID_ObraParal'].astype(str).replace(['left_only','both','right_only'], ['No','Si','-'])

# FONDES
bd_tablero2 = bd_tablero2.merge(fondes, on=['COD_ID', 'CODIGO_UNICO'], how='left', validate='m:1', indicator=True) #----- FONDES
bd_tablero2.rename(columns= {'_merge':'ID_FONDES'}, inplace=True)
bd_tablero2['ID_FONDES'] = bd_tablero2['ID_FONDES'].astype(str).replace(['left_only','both','right_only'], ['No','Si','-'])

# Dispositivos legales (incorporaciones)
try:
    bd_tablero2 = bd_tablero2.merge(dstransf_incorpora, on=['COD_ID', 'CODIGO_UNICO'], how='left', validate='m:1', indicator=True) #------ Transferencias incorporadas
    bd_tablero2.rename(columns= {'_merge':'ID_INCORPORACIONES_DS'}, inplace=True)
    bd_tablero2['ID_INCORPORACIONES_DS'] = bd_tablero2['ID_INCORPORACIONES_DS'].astype(str).replace(['left_only','both','right_only'], ['No','Si','-'])
except:
    print('sin información de Incorporaciones x DS')
    bd_tablero2['INCORPORACIONES.DS2024'] = np.nan
    bd_tablero2['ID_INCORPORACIONES_DS'] = np.nan
    
# Dispositivos legales (reducciones)
try:
    bd_tablero2 = bd_tablero2.merge(dstransf_reduccion, on=['COD_ID', 'CODIGO_UNICO'], how='left', validate='m:1', indicator=True) #------ Transferencias reduccioni
    bd_tablero2.rename(columns= {'_merge':'ID_REDUCCIONES_DS'}, inplace=True)
    bd_tablero2['ID_REDUCCIONES_DS'] = bd_tablero2['ID_REDUCCIONES_DS'].astype(str).replace(['left_only','both','right_only'], ['No','Si','-'])
except:
    print('sin información de Reducciones x DS')
    bd_tablero2['REDUCCIONES.DS2024'] = np.nan
    bd_tablero2['ID_REDUCCIONES_DS'] = np.nan
    
# Universidades
bd_tablero2.loc[bd_tablero2['PLIEGO'].str.split('. ',n=1).str[0].isin(codigos_universidades), 'ID_UNIVERSIDADES'] = 'SI'
bd_tablero2['ID_UNIVERSIDADES'] = np.where(bd_tablero2['ID_UNIVERSIDADES'].isna(), 'NO', bd_tablero2['ID_UNIVERSIDADES'])
bd_tablero2['EDUCA_PLIEGO'] = np.where(bd_tablero2['SECTOR']=='10. EDUCACION', 'MINEDU.SUNEDU.IPD', 'NO SON EDUCACIÓN')
bd_tablero2['EDUCA_PLIEGO'] = np.where(bd_tablero2['PLIEGO'].str.split('. ',n=1).str[0].isin(codigos_universidades), 'UNIVERSIDADES', bd_tablero2['EDUCA_PLIEGO'])
        
# VARIABLE PARA DELIMITAR EL SECTOR DE ARCC Y UNIVERSIDADES
bd_tablero2['SECTOR_META']= bd_tablero2['SECTOR'] # DESAGRUPANDO PARA MINEDU - universidades y RCC
bd_tablero2['SECTOR_META'] = np.where(bd_tablero2['EDUCA_PLIEGO']=='UNIVERSIDADES', '10. EDUCACION - UNIVERSIDADES', 
                                         np.where(bd_tablero2['EDUCA_PLIEGO']=='MINEDU.SUNEDU.IPD', '10. EDUCACION - NO UNIVERSIDADES', bd_tablero2['SECTOR_META']))
bd_tablero2['SECTOR_META'] = np.where(bd_tablero2['EJECUTORA']=='017. AUTORIDAD PARA LA RECONSTRUCCIÓN CON CAMBIOS - RCC', 
                                     '017. AUTORIDAD PARA LA RECONSTRUCCIÓN CON CAMBIOS - RCC', bd_tablero2['SECTOR_META'])

# VARIABLES DE  MODALIDAD DE EJEC Y ESTADO
bd_tablero2 = bd_tablero2.merge(metas_mod, on=['CODIGO_UNICO'], how='left', validate='m:1', indicator=False)
bd_tablero2 = postmerge(bd_tablero2)
bd_tablero2['MODALIDAD_EJECUCION'] = bd_tablero2['MODALIDAD_EJECUCION'].replace({'Proyectos en Activos':'PA', 
                                                                                 'G2G':'G2G', 
                                                                                 np.nan:'OP', 
                                                                                 'Obra Pública':'OP',
                                                                                 'Falta Seleccionar...':'OP', 
                                                                                 'Obra Pública-PNIC-PNISC':'OP PNIC/PNISC', 
                                                                                 'OXI':'OXI', 
                                                                                 'PEIP':'PEIP',
                                                                                 'APP':'APP', 
                                                                                 'Núcleo Ejecutor':'N.Ejecutor'})
bd_tablero2.loc[bd_tablero2['COD_ID']=='10-010-125', 'MODALIDAD_EJECUCION'] = 'PEIP'
#bd_tablero2.loc[bd_tablero2['ID_OXI']=='OXI', 'MODALIDAD_EJECUCION'] = 'OXI'

bd_tablero2['ESTADO_SITUACIONAL_PROYECTO'] = bd_tablero2['ESTADO_SITUACIONAL_PROYECTO'].replace({'Viable o Aprobado':'Viable', 
                                                                                                 'En ejecución física':'Ejec. física', 
                                                                                                 'Con liquidación':'Liquidación',
                                                                                                 'ET/DE Aprobado':'ET/DE Aprob.', 
                                                                                                 'Culminado':'Culminado', 
                                                                                                 'Formulación y Evaluación':'Form. y eval.',
                                                                                                 'Pendiente de Liquidación':'Por liquidar', 
                                                                                                 'Proceso arbitral':'Proceso arb.',
                                                                                                 'Elaboración de ET/DE':'ET/DE en elab.', 
                                                                                                 'Paralizado':'Obra paral.', 
                                                                                                 'Falta Seleccionar...':'Sin información',
                                                                                                 np.nan:'Sin información'})

#%% VARIABLES ADICIONALES SOLO PARA FACILITAR LA REVISION DEL CUMPLIMIENTO

# Alerta sobre programación de gasto
dev_proyf = [] ## este serà 'DEV01', 'PROYECCION_01', 'DEV02', 'PROYECCION_02' ...
meta_cump_t1 = []
meta_cump_t2 = []
meta_cump_t3 = []
meta_cump_t4 = []

mesact = str(datetime.now().month).zfill(2)
trimvig = str(math.ceil((datetime.now().month)/3)- 1)  # ajustar cuando las metas del cuarto trim estén OK

k = 1
while k < 4:
    meta_cump_t1 = meta_cump_t1 + ['META_' + str(k).zfill(2) + '_T1'] # ------- PRIMER TRIMESTRE
    k = k + 1
k = 4
if datetime.now().month > 3:
    while k < datetime.now().month:
        meta_cump_t2 = meta_cump_t2 + ['META_' + str(k).zfill(2) + '_T2'] # ------- SEGUNDO TRIMESTRE
        k = k + 1
k = 7
if datetime.now().month > 6:
    while k < datetime.now().month:
        meta_cump_t3 = meta_cump_t3 + ['META_' + str(k).zfill(2) + '_T3'] # ------- TERCER TRIMESTRE
        k = k + 1
k = 10
if datetime.now().month > 9:
    while k < datetime.now().month:
        meta_cump_t4 = meta_cump_t4 + ['META_' + str(k).zfill(2) + '_T4'] # ------- CUARTO TRIMESTRE
        k = k + 1
    
k = 1 ## de enero hacia los meses posteriores
while k < (datetime.now().month): ## adicionar un "-1" si se quiere obtener del mes anterior
    dev_proyf = dev_proyf + ['DEV'+str(k).zfill(2) + '_2024']
    k = k + 1



############################################################################### Alerta sobre el cumplimiento agregado de las metas.
bd_tablero2['METAS_ANTERIORES'] = bd_tablero2[meta_cump_t1 + meta_cump_t2 + meta_cump_t3 + meta_cump_t4].sum(axis=1)
bd_tablero2['CUMPL.PROY_AGR'] = np.where(bd_tablero2['METAS_ANTERIORES']>0, bd_tablero2[dev_proyf].sum(axis=1) - bd_tablero2['METAS_ANTERIORES'], np.nan)
bd_tablero2['CERTIF_NODEV'] = np.where(bd_tablero2['PIM_2024']>0, bd_tablero2['CERTIFICADO_2024'] - bd_tablero2['TOTAL_DEVENGADO_2024'], np.nan)


#- eliminar variables innecesarias para el tablero.
bd_tablero2.drop(columns=['SITUACION_BCO', 'MONTO_MODIF_EXP_TEC_BCO', 'MONTO_EXP_TEC_BCO', 'MONTO_CARTA_FIANZA', 'COSTO_ACTUALIZADO',
                          'EXP_TCO_BCO', 'ET_VIGENTE', 'MONTO_OBRA', 'DEVENGADO_2024_CUI', 'PIM_2024_CUI', 
                          ], inplace=True)

lista_columnas = bd_tablero2.columns.to_list()
lista_columnas = [e for e in lista_columnas if e not in ('EJECUTORA', 'NOMBRE_PROYECTO', 'SECTOR', 'PLIEGO', 'NIVEL_GOB', 'CODIGO_UNICO', 'COD_ID')]
bd_tablero2 = bd_tablero2[['NIVEL_GOB', 'SECTOR', 'PLIEGO', 'EJECUTORA', 'COD_ID', 'CODIGO_UNICO', 'NOMBRE_PROYECTO'] + lista_columnas]

bd_tablero2['ID_POWERBI'] =  bd_tablero2['COD_ID']  + '.' + bd_tablero2['FUENTE'].str.split('. ',n=1).str[0] + '.' + bd_tablero2['CODIGO_UNICO']
bd_tablero2['ID_POWERBI2'] =  bd_tablero2['COD_ID']  + '.' + bd_tablero2['CODIGO_UNICO']

#%% BASE 2: MODO PANEL PARA LOS MESES, Y DISTINGUIR ASI LAS METAS Y EJECUCION

meta_trim_var = meta_trim1.copy()
if datetime.now().month >= 4:
    meta_trim_var = meta_trim_var + meta_trim2
if datetime.now().month >= 7:
    meta_trim_var = meta_trim_var + meta_trim3
if datetime.now().month >= 10:
    meta_trim_var = meta_trim_var + meta_trim4
    
bd_tablero_mes = bd_tablero2[['COD_ID', 'CODIGO_UNICO', 'FUENTE',
                             'DEV01_2024', 'DEV02_2024', 'DEV03_2024', 'DEV04_2024', 'DEV05_2024', 'DEV06_2024', 'DEV07_2024', 'DEV08_2024', 'DEV09_2024',
                             'DEV10_2024', 'DEV11_2024', 'DEV12_2024',
                             'DEV01_2023', 'DEV02_2023', 'DEV03_2023', 'DEV04_2023', 'DEV05_2023', 'DEV06_2023', 'DEV07_2023', 'DEV08_2023', 'DEV09_2023',
                             'DEV10_2023', 'DEV11_2023', 'DEV12_2023'] + meta_trim_var 
                             ]

for x in list(range(1,13)):
    bd_tablero_mes.rename(columns={'DEV'+str(x).zfill(2)+'_2024':'DEV2024_'+str(x).zfill(2), 'DEV'+str(x).zfill(2)+'_2023':'DEV2023_'+str(x).zfill(2),
                                   'META_'+str(x).zfill(2)+'_T1':'METAT1_'+str(x).zfill(2), 
                                   'META_'+str(x).zfill(2)+'_T2':'METAT2_'+str(x).zfill(2),
                                   'META_'+str(x).zfill(2)+'_T3':'METAT3_'+str(x).zfill(2),
                                   'META_'+str(x).zfill(2)+'_T4':'METAT4_'+str(x).zfill(2)}, inplace=True)

bd_tablero_mes = pd.wide_to_long(bd_tablero_mes, stubnames=['DEV2024_', 'DEV2023_', 'METAT1_', 'METAT2_', 'METAT3_', 'METAT4_'], i=['COD_ID', 'CODIGO_UNICO', 'FUENTE'], j='MES').reset_index() # ,  sep='', suffix='\d+'

bd_tablero_mes['ID_POWERBI'] =  bd_tablero_mes['COD_ID']  + '.' + bd_tablero_mes['FUENTE'].str.split('. ',n=1).str[0] + '.' + bd_tablero_mes['CODIGO_UNICO']
bd_tablero_mes.rename(columns={'DEV2024_':'DEV2024', 'DEV2023_':'DEV2023', 'METAT1_':'META.T1', 'METAT2_':'META.T2', 'METAT3_':'META.T3', 'METAT4_':'META.T4'}, inplace=True)

## Etiquetado de meses
bd_tablero_mes['MES_EQ'] = bd_tablero_mes['MES'].astype(int).astype(str)
bd_tablero_mes['MES_EQ'] = bd_tablero_mes['MES_EQ'].str.zfill(2)
bd_tablero_mes['MES_EQ'] = bd_tablero_mes['MES_EQ'].replace({'01':'Ene', '02':'Feb', '03':'Mar', '04':'Abr', '05':'May', '06':'Jun', 
                                                             '07':'Jul', '08':'Ago', '09':'Sep', '10':'Oct', '11':'Nov', '12':'Dic'})

bd_tablero_mes['META_CONSOLIDADA'] = np.where(bd_tablero_mes['MES_EQ'].isin({'Ene', 'Feb', 'Mar'}), bd_tablero_mes['META.T1'],
                                              np.where(bd_tablero_mes['MES_EQ'].isin({'Abr', 'May', 'Jun'}), bd_tablero_mes['META.T2'],
                                                       np.where(bd_tablero_mes['MES_EQ'].isin({'Jul', 'Ago', 'Sep'}), bd_tablero_mes['META.T3'], bd_tablero_mes['META.T4']))) # completar luego

#%% BASE 3: SEGUIMIENTO MENSUALIZADO DEL PIM CERTIF COMP Y DEVEN

bd_tablero_seg = bd_tablero2.copy()
bd_tablero_seg = bd_tablero_seg[['COD_ID', 'FUENTE', 'CODIGO_UNICO'] + 
                                [i for i in bd_tablero2.columns if i.endswith('PREV')|i.endswith('2024')]]
bd_tablero_seg.drop(columns=[i for i in bd_tablero_seg.columns if (i[0:4] == 'DEV0')|(i[0:4] == 'DEV1')], inplace=True)

# El dato del PIA no se mueve
bd_tablero_seg['PIA_MES3PREV'] = bd_tablero_seg['PIA_2024']
bd_tablero_seg['PIA_MES2PREV'] = bd_tablero_seg['PIA_2024']
bd_tablero_seg['PIA_MESPREV'] = bd_tablero_seg['PIA_2024']
bd_tablero_seg['PIA_SEMPREV'] = bd_tablero_seg['PIA_2024']

bd_tablero_seg.rename(columns={'PIM_MES3PREV':'PIM_0', 'PIM_MES2PREV':'PIM_1', 'PIM_MESPREV':'PIM_2', 'PIM_SEMPREV': 'PIM_3', 'PIM_2024':'PIM_4', 
                              'CERTIFICADO_MES3PREV':'CERTIF_0', 'CERTIFICADO_MES2PREV':'CERTIF_1', 'CERTIFICADO_MESPREV':'CERTIF_2', 'CERTIFICADO_SEMPREV':'CERTIF_3', 'CERTIFICADO_2024':'CERTIF_4',
                              'COMPROMISO_MES3PREV':'COMPR_0', 'COMPROMISO_MES2PREV':'COMPR_1', 'COMPROMISO_MESPREV':'COMPR_2', 'COMPROMISO_SEMPREV':'COMPR_3', 'COMPROMISO_ANUAL_2024':'COMPR_4',
                              'DEVENGADO_MES3PREV':'DEVEN_0', 'DEVENGADO_MES2PREV':'DEVEN_1', 'DEVENGADO_MESPREV':'DEVEN_2', 'DEVENGADO_SEMPREV':'DEVEN_3', 'TOTAL_DEVENGADO_2024':'DEVEN_4',
                              'PIA_MES3PREV':'PIA_0', 'PIA_MES2PREV':'PIA_1', 'PIA_MESPREV':'PIA_2', 'PIA_SEMPREV':'PIA_3', 'PIA_2024':'PIA_4'}, inplace=True)

bd_tablero_seg = pd.wide_to_long(bd_tablero_seg, stubnames=['PIM_', 'CERTIF_', 'COMPR_', 'PIA_', 'DEVEN_'], i=['COD_ID', 'CODIGO_UNICO', 'FUENTE'], j='PEREVAL').reset_index() 
bd_tablero_seg.rename(columns={'PIM_':'PIM', 'CERTIF_':'CERTIF', 'COMPR_':'COMPR', 'PIA_':'PIA', 'DEVEN_':'DEVEN'}, inplace=True)

# Creamos la etiqueta para el periodo de evaluación
bd_tablero_seg['PER2'] = bd_tablero_seg['PEREVAL'].astype(str)
bd_tablero_seg['PER2'] = bd_tablero_seg['PER2'].replace({'0':'3 meses atrás', '1':'2 meses atrás', '2':'Mes anterior', '3':'Sem anterior', '4':'Actual'})

bd_tablero_seg['ID_POWERBI'] =  bd_tablero_seg['COD_ID']  + '.' + bd_tablero_seg['FUENTE'].str.split('. ',n=1).str[0] + '.' + bd_tablero_seg['CODIGO_UNICO']

#%% BASE 4: SEGUIMIENTO DEL MAPA DE DEVENGADO
bd_tab_map = bd_seg23.copy()

bd_tab_map.rename(columns={'NIVEL_GOBIERNO':'NIVEL_GOB'}, inplace=True)
bd_tab_map = crear_id(bd_tab_map, 'NIVEL_GOB', 'SECTOR', 'PLIEGO', 'EJECUTORA')
bd_tab_map = crear_idpliegog(bd_tab_map, 'NIVEL_GOB', 'SECTOR', 'PLIEGO')
bd_tab_map['CODIGO_UNICO'] = bd_tab_map['PRODUCTO_PROYECTO'].str.split('. ',n=1).str[0]
bd_tab_map['NOMBRE_PROYECTO'] = bd_tab_map['PRODUCTO_PROYECTO'].str.split('. ',n=1).str[1]
bd_tab_map['TIPO_PROD_PROY'] = np.where(bd_tab_map['CODIGO_UNICO'].str.startswith('2'),'PROYECTOS','PRODUCTOS')
bd_tab_map = bd_tab_map[(bd_tab_map['TIPO_PROD_PROY']=='PROYECTOS')]

bd_tab_map = bd_tab_map.groupby(['COD_ID', 'CODIGO_UNICO', 'DEPARTAMENTO', 'FUENTE']).agg({'PIM':'sum', 'TOTAL_DEVENGADO':'sum'}).reset_index()
bd_tab_map['IDDPTO'] = bd_tab_map['DEPARTAMENTO'].fillna('00').str[0:2]

bd_tab_map['ID_POWERBI'] =  bd_tab_map['COD_ID']  + '.' + bd_tab_map['FUENTE'].str.split('. ',n=1).str[0] + '.' + bd_tab_map['CODIGO_UNICO']

#%% BASE 5: PROYECTOS POR CARTERA
bd_estsit = bd_tablero2[['ID_POWERBI2', 'CODIGO_UNICO', 'COSTO_ACTUAL_BCO', 'MONTO_VIABILIDAD_BCO', 'ACM_DEV_AL2023', 'TOTAL_DEVENGADO_2024']].copy()
bd_estsit = bd_estsit.groupby(['CODIGO_UNICO']).agg({'COSTO_ACTUAL_BCO':'max', 'MONTO_VIABILIDAD_BCO':'max', 
                                                    'ACM_DEV_AL2023':'max', 'TOTAL_DEVENGADO_2024':'sum'}).reset_index()

bd_estsit['ACM_DEV_AL2023'] = np.where(bd_estsit['COSTO_ACTUAL_BCO'].fillna(0) == 0, 0, bd_estsit['ACM_DEV_AL2023'])
bd_estsit['TOTAL_DEVENGADO_2024'] = np.where(bd_estsit['COSTO_ACTUAL_BCO'].fillna(0) == 0, 0, bd_estsit['TOTAL_DEVENGADO_2024'])
bd_estsit['Avance_al2024_CUI'] = bd_estsit[['ACM_DEV_AL2023', 'TOTAL_DEVENGADO_2024']].sum(axis=1)

#%% ULTIMAS VARIABLES y LIMPIEZA PARA QUE LA BASE PESE MENOS
#- eliminar variables innecesarias para el tablero. ahora actualizado
bd_tablero2.drop(columns=['DEV01_2023', 'DEV02_2023', 'DEV03_2023', 'DEV04_2023', 'DEV05_2023', 'DEV06_2023', 'DEV07_2023', 'DEV08_2023', 'DEV09_2023', 'DEV10_2023', 'DEV11_2023', 'DEV12_2023'
                          ], inplace=True)

bd_tablero2['IDDPTO'] = bd_tablero2['DEPARTAMENTO'].fillna('00').str[0:2]
bd_tablero2['CODIGO_UNICO_PIA'] = np.where(bd_tablero2['PIA_2024'].fillna(0) > 0, bd_tablero2['CODIGO_UNICO'], np.nan)
bd_tablero2['CODIGO_UNICO_PIM'] = np.where(bd_tablero2['PIM_2024'].fillna(0) > 0, bd_tablero2['CODIGO_UNICO'], np.nan)
bd_tablero2['PROYECTO'] = bd_tablero2['CODIGO_UNICO'] + '. ' + bd_tablero2['NOMBRE_PROYECTO']

# Quitamos las mensualizadas hacia atrás
listdrop = [i for i in bd_tablero2.columns if i.endswith('MESPREV')|i.endswith('MES2PREV')|i.endswith('MES3PREV')|i.endswith('SEMPREV')]
bd_tablero2.drop(columns=listdrop, inplace=True)

# Quitamos las metas que no sirven paravalidacion
meta_trim_var = ['META_04_T1', 'META_05_T1', 'META_06_T1', 'META_07_T1', 'META_08_T1', 'META_09_T1', 'META_10_T1', 'META_11_T1', 'META_12_T1']
if datetime.now().month >= 4:
    meta_trim_var = meta_trim_var + ['META_07_T2', 'META_08_T2', 'META_09_T2', 'META_10_T2', 'META_11_T2', 'META_12_T2']
if datetime.now().month >= 7:
    meta_trim_var = meta_trim_var + ['META_10_T3', 'META_11_T3', 'META_12_T3']

#### Completitud para las metas para el PRIMER trimestre
if (datetime.now().month >= 1)&(datetime.now().month < 4):
    for t in list(range(4,13)):
        bd_tablero2['META_' + str(t).zfill(2) + '_T2'] = np.nan
    for t in list(range(7,13)):
        bd_tablero2['META_' + str(t).zfill(2) + '_T3'] = np.nan
    for t in list(range(10,13)):
        bd_tablero2['META_' + str(t).zfill(2) + '_T4'] = np.nan

#### Completitud para las metas para el SEGUNDO trimestre
if (datetime.now().month >= 1)&(datetime.now().month < 4):
    for t in list(range(7,13)):
        bd_tablero2['META_' + str(t).zfill(2) + '_T3'] = np.nan
    for t in list(range(10,13)):
        bd_tablero2['META_' + str(t).zfill(2) + '_T4'] = np.nan
    
#### Completitud para las metas para el TERCER trimestre
if (datetime.now().month >= 1)&(datetime.now().month < 4):
    for t in list(range(10,13)):
        bd_tablero2['META_' + str(t).zfill(2) + '_T4'] = np.nan

bd_tablero2.drop(columns=meta_trim_var, inplace=True)

bd_tablero2.rename(columns={'PIM_PROYECTADO_T1':'PIM_PROYECTADO_2024_T1',
                            'PIM_PROYECTADO_T2':'PIM_PROYECTADO_2024_T2',
                            'PIM_PROYECTADO_T3':'PIM_PROYECTADO_2024_T3',
                            'PIM_PROYECTADO_T4':'PIM_PROYECTADO_2024_T4'}, inplace=True)

# Homologacion de fuentes para que sean más simples
bd_tablero2['FUENTE'] = bd_tablero2['FUENTE'].replace({'1. RECURSOS ORDINARIOS':'RO', '2. RECURSOS DIRECTAMENTE RECAUDADOS':'RDR', '3. RECURSOS POR OPERACIONES OFICIALES DE CREDITO':'ROOC',
                                                       '4. DONACIONES Y TRANSFERENCIAS':'DYT', '5. RECURSOS DETERMINADOS':'RD'})
bd_tablero_mes['FUENTE'] = bd_tablero_mes['FUENTE'].replace({'1. RECURSOS ORDINARIOS':'RO', '2. RECURSOS DIRECTAMENTE RECAUDADOS':'RDR', '3. RECURSOS POR OPERACIONES OFICIALES DE CREDITO':'ROOC',
                                                       '4. DONACIONES Y TRANSFERENCIAS':'DYT', '5. RECURSOS DETERMINADOS':'RD'})
bd_tablero_seg['FUENTE'] = bd_tablero_seg['FUENTE'].replace({'1. RECURSOS ORDINARIOS':'RO', '2. RECURSOS DIRECTAMENTE RECAUDADOS':'RDR', '3. RECURSOS POR OPERACIONES OFICIALES DE CREDITO':'ROOC',
                                                       '4. DONACIONES Y TRANSFERENCIAS':'DYT', '5. RECURSOS DETERMINADOS':'RD'})
bd_tab_map['FUENTE'] = bd_tab_map['FUENTE'].replace({'1. RECURSOS ORDINARIOS':'RO', '2. RECURSOS DIRECTAMENTE RECAUDADOS':'RDR', '3. RECURSOS POR OPERACIONES OFICIALES DE CREDITO':'ROOC',
                                                       '4. DONACIONES Y TRANSFERENCIAS':'DYT', '5. RECURSOS DETERMINADOS':'RD'})

#%%
outputFile = os.path.join(path_output, 'ReporteGR_Seguimiento2024_'+fecha_corte+".xlsx")
with pd.ExcelWriter(outputFile) as ew:
        bd_tablero2.to_excel(ew, sheet_name='ID-CUI-FF', index = False)
        bd_tablero_mes.to_excel(ew, sheet_name='PROYECCIONES', index=False)
        bd_tablero_seg.to_excel(ew, sheet_name='SEGMENSUAL', index=False)
        bd_tab_map.to_excel(ew, sheet_name='MAPA', index=False)
        bd_estsit.to_excel(ew, sheet_name='ESTSIT', index=False)

#%%
now = datetime.now()
print(now)


