import numpy as np
import pandas as pd

df1 = pd.read_csv('oop/Lu-177_2023_11/results.csv', header=[0, 1])
df2 = pd.read_excel('ref_case/results_file.xlsx', usecols='A,B,C,D,E,F,G,H,J,K,L,M,N', skiprows=2)

# Assert equal number of rows
df2 = df2[30:690]
df2 = df2.reset_index(drop=True)
assert len(df1) == len(df2)

# Columns to compare
columns_df2 = ['CPM', 'ENDTIME', 'CPM.1', 'ENDTIME.1', 'T MUESTRA (s)', 'DTIME MUESTRA', 'ct muestra',
               'CPM NETAS', 'ct muestra netas', 'uct']
columns_df1 = [('Background', 'Count rate (cpm)'), ('Background', 'End time'), ('Sample', 'Count rate (cpm)'),
               ('Sample', 'End time'), ('Sample', 'Real time (s)'), ('Sample', 'Dead time (s)'), ('Sample', 'Counts'),
               ('Net', 'Count rate (cpm)'), ('Net', 'Counts'), ('Net', 'Counts uncertainty')]
# Assert equal number of columns to compare
assert len(columns_df1) == len(columns_df2)

# Filter columns to compare in dataframes
df1_filtered = df1[columns_df1]
df2_filtered = df2[columns_df2]

df1[('Background', 'End time')] = pd.to_datetime(df1[('Background', 'End time')], format='%Y-%m-%d %H:%M:%S')
df1[('Sample', 'End time')] = pd.to_datetime(df1[('Sample', 'End time')], format='%Y-%m-%d %H:%M:%S')

# Assert equal number of columns
assert len(df1_filtered) == len(df2_filtered)

# Compare the DataFrames
for col1, col2 in zip(columns_df1, columns_df2):
    if pd.api.types.is_datetime64_any_dtype(df1[col1]):
        if not df1[col1].equals(df2[col2]):
            print(f"Values in columns '{col1}' and '{col2}' are NOT the same.")
    else:
        if not np.allclose(df1[col1], df2[col2]):
            print(f"Values in columns '{col1}' and '{col2}' are NOT the same.")

# for i in range(660):
#     if not df2['ENDTIME.1'][i] == df1[('Sample', 'End time')][i]:
#         print(i, df1[('Sample', 'End time')][i], df2['ENDTIME.1'][i], df2['ENDTIME.1'][i]==df1[('Sample', 'End time')][i])
# Hay una discrepancia sistematica en el end time del fondo, en todos los ciclos, toma el mismo valor para las repeticiones 29 y 30.
# Hay una discrepancia sistematica en el end time de la muestra, en todos los ciclos, en las repeticiones 15 y 18.

diff = (df1[('Net', 'Counts uncertainty')] - df2['uct']) / df2['uct'] * 100
print(diff.min(), diff.max(), diff.mean(), diff.std())
# Diferencias con el excel probando distintas formas de cálculo de la incertidumbre en el código
# 0.014997304198455323 0.4044726165342672 0.09222668520691783 0.06465814225011496
# 0.014997304198455323 0.4044726165342672 0.09222668520691821 0.06465814225011474
# 0.014997304198455323 0.4044726165342672 0.09222668520691821 0.06465814225011474
# La diferencia es siempre la misma. No parece provenir de un error en el código.
diff = (df1[('Background', 'Count rate (cpm)')] - df2['CPM']) / df2['CPM'] * 100
print(diff.min(), diff.max(), diff.mean(), diff.std())
# 0.0 0.0 0.0 0.0
diff = (df1[('Sample', 'Count rate (cpm)')] - df2['CPM.1']) / df2['CPM.1'] * 100  # 0.0 0.0 0.0 0.0
print(diff.min(), diff.max(), diff.mean(), diff.std())
# 0.0 0.0 0.0 0.0
diff = (df1[('Sample', 'Real time (s)')] - df2['T MUESTRA (s)']) / df2['T MUESTRA (s)'] * 100
print(diff.min(), diff.max(), diff.mean(), diff.std())
# 0.0 0.0 0.0 0.0
diff = (df1[('Sample', 'Counts')] - df2['ct muestra']) / df2['ct muestra'] * 100  # 0.0 0.0 0.0 0.0
print(diff.min(), diff.max(), diff.mean(), diff.std())
# -1.7255951604750615e-14 1.5739020345225235e-14 -7.054068310746494e-16 5.934076294611973e-15
# No hay diferencias en las variables de origen. Las diferencias tan pequeñas en la incertidumbre deben de ser a causa del redondeo.
