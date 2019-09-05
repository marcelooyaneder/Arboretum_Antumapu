#package imports
import pandas as pd
import os
import errno
import pyqrcode
from pathlib import Path
from pyshorteners import Shortener
import filecmp
import shutil

#http://arboretum.oost-vlaanderen.be/index.cfm?nummer=00006251 IDEA TIPO
#EL PASO SIGUIENTE ES CREAR UNA CARPETA EN QUE VAYAN LOS ARCHIVOS TXT, COMPARAR SI ES QUE EXISTEN EN ESTA, 
# Y SI ES QUE EXISTEN REVISAR POSIBLES CAMBIOS, AGREGAR LOS QUE NO EXISTEN   

#creation of classes and functions
#comparar archivos, crear una carpeta que contenga el output, verificar si los archivos de la carpeta original son iguales
#si estos son iguales borrar el archivo de la carpeta de comparación si es que no moverlo a la carpeta de info
#si el archivo no existe pasarlo a la otra carpeta.
def comparefiles(ID,info):
    filename1 = "temp/"+ID+'.txt'
    filename2= "files/"+ID+'.txt'
    os.makedirs(os.path.dirname(filename1), exist_ok=True)
    with open(filename1,'w') as fil:
        fil.write(str(info))
    if os.path.isfile(filename2)==True:
        if filecmp.cmp(filename1,filename2)==False:
            print('ive found some changes since the last time, on file...', ID,'.txt')
            print('changes has been saved')
            shutil.move(filename1,filename2)
        else:
            pass
    else:
        print('a new entry has been found, file...',ID,'.txt has been created.')
        os.makedirs(os.path.dirname(filename2), exist_ok=True)
        with open(filename2,'w') as fil:
            fil.write(str(info))
    shutil.rmtree('temp/', ignore_errors=False, onerror=None)
    return 

def infowriting(ID,info):
    filename = "files/"+ID+'.txt'
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename,'w') as fil:
        fil.write(str(info))
    return 

def qrcreation(ID,url):
    long_url=url+ID+'.txt'
    filename = "qrs/"+ID+'.png'
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    quick_response_code= pyqrcode.create(long_url)
    quick_response_code.png(filename, scale=8)
    quick_response_code.eps(filename, scale=2)

#Process
#read excel
data=pd.read_excel('Inventario_2019_Arboretum_Antumapu_Dwc.xlsx',sheet_name='Hoja1',header=0)
#rearrange dataframe
data=data.set_index("catalogNumber", drop = False)
#obtaining ID data
IDs=data['catalogNumber'].tolist()

#verificar si los archivos existen, si es que existen comparar estos, si no crearlos.
#get info a txt document ESTA FUNCIONANDO NO EJECUTAR YA QUE CREA DEMASIADOS ARCHIVOS

if os.path.isdir('/files')==True:
    for id in IDs:
        comparefiles(id.data.loc[id])
else:
    for id in IDs:
        infowriting(id,data.loc[id])

#for id in IDs:
#    infowriting(id,data.loc[id])
#    qrcreation(id,'https://github.com/marcelooyaneder/Arboretum_Antumapu/blob/master/files/')




#print ("File      Path:", Path(__file__).absolute()) ESTE ES EL PATH DE LA CARPETA
