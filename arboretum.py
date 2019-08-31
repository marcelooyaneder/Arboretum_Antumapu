#package imports
import pandas as pd
import os
import errno
import pyqrcode

#http://arboretum.oost-vlaanderen.be/index.cfm?nummer=00006251 IDEA TIPO
#EL PASO SIGUIENTE ES CREAR UNA CARPETA EN QUE VAYAN LOS ARCHIVOS TXT, COMPARAR SI ES QUE EXISTEN EN ESTA, 
# Y SI ES QUE EXISTEN REVISAR POSIBLES CAMBIOS, AGREGAR LOS QUE NO EXISTEN   

#creation of classes and functions

def infowriting(ID,info):
    filename = "files/"+ID+'.txt'
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename,'w') as fil:
        fil.write(str(info))
    pass
    return 

def qrcreation(ID,url)
    filename = "qrs/"+ID+'.svg'
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    URL=
    url = pyqrcode.create('URL')
    url.svg(filename, scale=8)
    url.eps(filename, scale=2)

#Process
#read excel
data=pd.read_excel('Inventario_2019_Arboretum_Antumapu_Dwc.xlsx',sheet_name='Hoja1',header=0)
#rearrange dataframe
data=data.set_index("catalogNumber", drop = False)
#obtaining ID data
IDs=data['catalogNumber'].tolist()

#verificar si los archivos existen, si es que existen comparar estos, si no crearlos.
#get info into a txt document ESTA FUNCIONANDO NO EJECUTAR YA QUE CREA DEMASIADOS ARCHIVOS
for id in IDs:
    infowriting(id,data.loc[id])

#CREACION DE CODIGOS QR
#url = pyqrcode.create('URL')
#url.svg('uca-url.svg', scale=8)
#url.eps('uca-url.eps', scale=2)
#print(url.terminal(quiet_zone=1))
