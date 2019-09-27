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
class subject:
    def __init__(self,data):
        self.data=data

    def datafiltering_by_class(self,data):
        #print (data.query('specificEpithet=="americana"'))
        #https://cmdlinetips.com/2018/01/how-to-get-unique-values-from-a-column-in-pandas-data-frame/
        query=data["Class"].unique()
        print('The following Class values are in your data: ')
        for index, values in enumerate(query):
            print(index,values)
        index2=int(input('insert the number for query your data: '))
        var2=query[index2]
        query_df_by_class=data.query('Class==@var2')
        return query_df_by_class

    def datafiltering_by_order(self,data):
        query=data["order"].unique()
        print('The following order values are in your data: ')
        for index, values in enumerate(query):
            print(index,values)
        index2=int(input('insert the number for query your data: '))
        var2=query[index2]
        query_df_by_order=data.query('order==@var2')
        return query_df_by_order
    
    def datafiltering_by_family(self,data):
        query=data["family"].unique()
        print('The following family values are in your data: ')
        for index, values in enumerate(query):
            print(index,values)
        index2=int(input('insert the number for query your data: '))
        var2=query[index2]
        query_df_by_family=data.query('family==@var2')
        return query_df_by_family
    
    def datafiltering_by_genus(self,data):
        query=data["genus"].unique()
        print('The following genus values are in your data: ')
        for index, values in enumerate(query):
            print(index,values)
        index2=int(input('insert the number for query your data: '))
        var2=query[index2]
        query_df_by_genus=data.query('genus==@var2')
        return query_df_by_genus
    
    def datafiltering_by_specificEpithet(self,data):
        query=data["specificEpithet"].unique()
        print('The following specificEpithet values are in your data: ')
        for index, values in enumerate(query):
            print(index,values)
        index2=int(input('insert the number for query your data: '))
        var2=query[index2]
        query_df_by_specificEpithet=data.query('specificEpithet==@var2')
        return query_df_by_specificEpithet
    
    def change_values(self,data,subjects): 
        print('These are the following IDs who meet your query')
        for index, values in enumerate(subjects):
            print(index,values)        
        print('The following values are available for change: ')
        columns=data.columns.tolist()[:]
        for index, values in enumerate(columns):
            print(index,values)
        index1=int(input('Insert the number of the value you wish to update: '))
        set_value=input('enter the new value: ')
        ans=input('Are you sure you want to change the value from {0} to {1}\nY/n ?'.format(data.at[subjects[0],columns[index1]],set_value))
        if ans=='Y' or ans=='y':    
            for values in subjects:
                data.at[values,columns[index1]]=set_value
                data.at[values,'acceptedNameUsage']= '{0} {1} {2}'.format(data.at[values,'genus'],data.at[values,'specificEpithet'],data.at[values,'nameAcordingTo'])
            return data 
        else:
            pass 

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
    api_key='AIzaSyCsBqEkRDVJ8ZNp1E8HcbWDe_JEHu9Frgw' #this need to be created on the firebase webpage
    sub_domain='arboretum' #this need to be created on firebase webpage
    url_shortener = UrlShortener(api_key,sub_domain)
    shorturl=url_shortener.get_short_link(longurl)
    time.sleep(0.25) #to not break the limits of firebase
    return shorturl

def qrcreation(ID,short_url):
    filename = "qrs/"+ID+'.png'
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    quick_response_code= pyqrcode.create(short_url)
    quick_response_code.png(filename, scale=8,module_color=(0,102,0,255),background=(255, 255, 255, 255))

#MAIN

#import data
#read excel
data=pd.read_excel('Inventario_2019_Arboretum_Antumapu_Dwc.xlsx',sheet_name='Hoja1',header=0)
#rearrange dataframe
data=data.set_index("catalogNumber", drop = False)
#obtaining ID data
IDs=data['catalogNumber'].tolist()

#query data 

r1=subject(data)
ans1=str(input('The following query is by default: order-family-genus-specificEpithet, Do you want to accept it Y/n?,\nif you dont want to query write "pass": \n'))
if ans1 =='Y' or ans1 =='y' :
    order_filtering=r1.datafiltering_by_order(data)
    family_filtering=r1.datafiltering_by_family(order_filtering)
    genus_filtering=r1.datafiltering_by_genus(family_filtering)
    specificEpithet_filtering=r1.datafiltering_by_specificEpithet(genus_filtering)
    subjects=specificEpithet_filtering['catalogNumber'].tolist()
    print('The following subjects has been query', subjects)
elif ans1=='n' or ans1=='N':
    print('The following query will be done: Class-order-family-genus-specificEpithet')
    class_filtering=r1.datafiltering_by_class(data)
    order_filtering=r1.datafiltering_by_order(class_filtering)
    family_filtering=r1.datafiltering_by_family(order_filtering)
    genus_filtering=r1.datafiltering_by_genus(family_filtering)
    specificEpithet_filtering=r1.datafiltering_by_specificEpithet(genus_filtering)
    subjects=specificEpithet_filtering['catalogNumber'].tolist()
    print('The following subjects has been query', subjects)
else: 
    pass

if ans1 =='Y' or ans1 =='y' or ans1=='n' or ans1=='N':
    r1.change_values(data,subjects)
    data.to_excel('Inventario_2019_Arboretum_Antumapu_Dwc.xlsx','Hoja1')
else:
    pass

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
print('create non existing qr files...')
if os.path.isdir('qrs')==True:
    for id in IDs:
        print('file {0} of file {1}'.format(id,IDs[-1]),end='\r', flush=True)
        path="qrs/"+id+'.png'
        if os.path.isfile(path)==False:
            longurl='https://github.com/marcelooyaneder/Arboretum_Antumapu/blob/master/files/'+id+'.txt'
            shorturl=dynamiclinks(longurl)
            qrcreation(id,shorturl)
        else:
            pass
else:
    for id in IDs:
        print('file {0} of file {1}'.format(id,IDs[-1]),end='\r', flush=True)
        longurl='https://github.com/marcelooyaneder/Arboretum_Antumapu/blob/master/files/'+id+'.txt'
        shorturl=dynamiclinks(longurl)
        qrcreation(id,shorturl)
