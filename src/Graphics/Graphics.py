# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 09:05:41 2019

@author: Daniel Jimenez
"""

import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as dates
import numpy as np
from datetime import datetime
import os

main_path = os.path.abspath(__file__+"/../../..")+"/"

# Se carga el archivo.csv de la base de datos
file = main_path+'Data/'+ 'Ciclo_1.csv'

data = pd.read_csv(file)
N= len(data.created_at)
Time=[]

# Para cambiar formato de fecha de una lista
#for i in range(N):
#    Fecha= datetime.strptime(data2.Time[i],'%d/%m/%y %H:%M:%S')
#    Formato= datetime.strftime(Fecha,'%d-%b-%Y %H:%M:%S')
#    Time.append(Formato)    
#Time= pd.to_datetime(Time, format='%d-%b-%Y %H:%M:%S')
#   
# Borrar caracter UTC de lista fecha

for i in range(N):
    Fecha= data.created_at[i]
    Borrar = Fecha.strip(' UTC ')
    Time.append(Borrar)    
Time= pd.to_datetime(Time, format='%Y-%m-%d %H:%M:%S')

data.set_index(Time,inplace=True)



##
fig,axarr = plt.subplots(4,figsize=(15,7))
###
axarr[0].plot(data.index, data['field3'],'-')
axarr[0].set_ylabel('Humedad')
axarr[1].plot(data.index, data['field2'],'-',color='k')
axarr[1].set_ylabel('Temperatura.S')
axarr[2].plot(data.index, data['field1'],'-',color='g')
axarr[2].set_ylabel('Luz')
axarr[3].plot(data.index, data['field5'],'.',color='r')
axarr[3].set_ylabel('Motobomba')
fig.subplots_adjust(hspace=0.2)
plt.setp([a.get_xticklabels() for a in fig.axes[:-1]], visible=False)
