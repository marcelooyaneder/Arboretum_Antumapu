#package imports
import pandas as pd
import os
import errno
import pyqrcode
from pathlib import Path
import filecmp
import shutil
from python_firebase_url_shortener.url_shortener import UrlShortener
import time
import sys

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
            print('ive found some changes since the last time, on file...'+ID+'.txt')
            print('changes has been saved')
            shutil.move(filename1,filename2)
        else:
            pass
    else:
        print('a new entry has been found, file...'+ID+'.txt has been created.')
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
    print('a new entry has been found, file...'+ID+'.txt has been created.')
    return 

#agregar try y except functions
def dynamiclinks(longurl):
    api_key='' #this need to be created on the firebase webpage
    sub_domain='arboretum' #this need to be created on firebase webpage
    url_shortener = UrlShortener(api_key,sub_domain)
    shorturl=url_shortener.get_short_link(longurl)
    time.sleep(0.26) #to not break the limits of firebase
    return shorturl


def qrcreation(ID,short_url):
    filename = "qrs/"+ID+'.png'
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    quick_response_code= pyqrcode.create(short_url)
    quick_response_code.png(filename, scale=8)
    quick_response_code.eps(filename, scale=2)

def datafiltering(data):
    #print (data.query('specificEpithet=="americana"'))
    #https://cmdlinetips.com/2018/01/how-to-get-unique-values-from-a-column-in-pandas-data-frame/
    columns=data.columns.tolist()[4:9]
    print('The following data is available for query: ')
    for index, values in enumerate(columns):
        print(index, values)
    j=input('insert the number for query your data: ')
    

#MAIN

#import data
#read excel
data=pd.read_excel('Inventario_2019_Arboretum_Antumapu_Dwc.xlsx',sheet_name='Hoja1',header=0)
#rearrange dataframe
data=data.set_index("catalogNumber", drop = False)
#obtaining ID data
IDs=data['catalogNumber'].tolist()

#datafiltering(data)

#compare files or create them
print('compare/create files...')
if os.path.isdir('files')==True:
    for id in IDs:
        comparefiles(id,data.loc[id])
else:
    for id in IDs:
        infowriting(id,data.loc[id])
print ('there is nothing more to do here...')

#compare qr files or create them
print('compare/create qr files...')
if os.path.isdir('qrs')==True:
    for id in IDs:
        print('file {0} of file {1}\r'.format(id,IDs[-1]),end='')
        path="qrs/"+id+'.png'
        if os.path.isfile(path)==False:
            longurl='https://github.com/marcelooyaneder/Arboretum_Antumapu/blob/master/files/'+id+'.txt'
            shorturl=dynamiclinks(longurl)
            qrcreation(id,shorturl)
        else:
            pass
else:
    for id in IDs:
        print('file {0} of file {1}\r'.format(id,IDs[-1]),end='')
        longurl='https://github.com/marcelooyaneder/Arboretum_Antumapu/blob/master/files/'+id+'.txt'
        shorturl=dynamiclinks(longurl)
        qrcreation(id,shorturl)
