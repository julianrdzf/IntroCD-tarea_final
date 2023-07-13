# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 17:26:45 2023

@author: Agustín Porley & Julián Rodríguez
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


file_name = 'winemag-data_first150k'
path = f'data/{file_name}.csv'
df_table = pd.read_csv(path, index_col=[0])

total_datos = df_table.shape[0]

vacios=np.zeros(len(df_table.columns))

for idx, column_name in enumerate(df_table.columns):      
    vacios[idx] = df_table[column_name].isna().sum()

#Vacios
vacios = np.expand_dims(vacios, axis=1).T
df_vacios = pd.DataFrame(vacios, columns=df_table.columns)

#Grafico vacios

plt.figure()
plt.barh(range(len(df_vacios.columns)), (np.ones(len(df_vacios.columns))-np.array(df_vacios.iloc[0])/total_datos)*100, color = '#35A29F')
plt.barh(range(len(df_vacios.columns)), np.array(df_vacios.iloc[0])/total_datos*100, left=(np.ones(len(df_vacios.columns))-np.array(df_vacios.iloc[0])/total_datos)*100, color = '#EF6262')
plt.yticks(range(len(df_vacios.columns)), np.array(df_vacios.columns), rotation = 0)
plt.gca().invert_yaxis()
plt.xlabel("Porcentaje de datos disponibles (%)")
plt.savefig('disponibilidad_datos.pdf',bbox_inches="tight")
plt.show()
 

#Duplicados
duplicados = df_table.duplicated()
duplicados_true = pd.DataFrame(df_table.duplicated(keep=False))
cantidad_duplicados = duplicados.sum()

#Duplicados sin tener en cuenta columnas

columnas = pd.DataFrame(df_table.columns)

columnas_dup = columnas.drop([1])

duplicados_sin_desc=df_table.duplicated(subset=np.array(columnas_dup[0]))
duplicados_sin_desc_true = pd.DataFrame(df_table.duplicated(subset=np.array(columnas_dup[0]),keep=False))
cant_duplicados_sin_desc = duplicados_sin_desc.sum()


##Combino tables
df_table_dup = pd.merge(df_table, duplicados_true, left_index=True, right_index=True)
df_table_dup.rename(columns = {0:'duplicated'}, inplace = True)

df_table_dup = pd.merge(df_table_dup, duplicados_sin_desc_true, left_index=True, right_index=True)
df_table_dup.rename(columns = {0:'duplicated_wo_desc'}, inplace = True)

verificar_dup_sin_desc = df_table_dup[df_table_dup['duplicated_wo_desc'] ==True]
verificar_dup_sin_desc = verificar_dup_sin_desc[verificar_dup_sin_desc['duplicated']==False]

###Lista de paises
paises = df_table.groupby("country")["country"].count().sort_values(ascending=False)

###Lista de tipos de vinos
tipos_vino = df_table.groupby("variety")["variety"].count().sort_values(ascending=False)


#Lista de localidades de Uruguay
localidades_uy = df_table[df_table["country"]=='Uruguay'].groupby("province")["province"].count().sort_values(ascending=False)

#Datos con igual country que province
igual_country_province = df_table.query('country == province')
