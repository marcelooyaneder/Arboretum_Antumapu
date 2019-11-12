# -*- coding: utf-8 -*-

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
import easygui as eg
import numpy 
from PIL import Image


#FORMA DE ELIMINAR COLUMNAS QUE NO ME SIRVAN GUI CON MULTIOPCIONES
#FORMA PARA GUARDAR QR CON HOJAS

#http://arboretum.oost-vlaanderen.be/indexo.cfm?nummer=00006251 IDEA TIPO
#EL PASO SIGUIENTE ES CREAR UNA CARPETA EN QUE VAYAN LOS ARCHIVOS TXT, COMPARAR SI ES QUE EXISTEN EN ESTA, 
# Y SI ES QUE EXISTEN REVISAR POSIBLES CAMBIOS, AGREGAR LOS QUE NO EXISTEN   

#creation of classes and functions
#comparar archivos, crear una carpeta que contenga el output, verificar si los archivos de la carpeta original son iguales
#si estos son iguales borrar el archivo de la carpeta de comparación si es que no moverlo a la carpeta de info
#si el archivo no existe pasarlo a la otra carpeta.

#autoidenficar el separator en csv ; o ,
class file_manager:
    def file_opener(self):
        #search if a csv file has been created previusly 
        try:
            data=pd.read_csv('dataframe.csv',header=0,sep=';') #ver como variar de ; o ,
        except:
            file_path=eg.fileopenbox(msg='pick the file wish contain your data',title='directory',default='*',filetypes=None,multiple=False)
            if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
                data=pd.read_excel(file_path,sheet_name='Hoja1',header=0)
            elif file_path.endswith('.csv'):
                data=pd.read_csv(file_path,header=0,sep=';') #ver como variar de ; o ,
        columns_df=data.columns.tolist()
        msg='select a column to be the index of the dataframe'
        title='select index'       
        indexo=eg.choicebox(msg,title,columns_df)
        data=data.set_index(indexo, drop = False)
        og_data=data.copy()
        og_columns_df=og_data.columns.tolist()
        columns_dwc=pd.read_csv('dwc_terms\simple_dwc_horizontal.csv',header=0,sep=';').columns.tolist() #ver como variar de ; o , 
        columns_difference=list(set(columns_df)-set(columns_dwc))
        if not columns_difference:
            pass
        else:
            msg='the followings columns do not belong to DwC, select the ones you wish to delete'
            title='select to delete'       
            choicebox=eg.multchoicebox(msg,title,columns_difference)
            try:
                for label in choicebox:
                    data.drop(label,axis=1,inplace=True)
            except:
                pass
        return og_data,data,indexo,og_columns_df
    
    def file_creation(self):
        Record_level=pd.read_csv('dwc_terms\Record_level.csv',header=0,sep=';').columns.tolist()
        Ocurrence=pd.read_csv('dwc_terms\Ocurrence.csv',header=0,sep=';').columns.tolist()
        Organism=pd.read_csv('dwc_terms\organism.csv',header=0,sep=';').columns.tolist()
        Material_sample=pd.read_csv('dwc_terms\MaterialSample.csv',header=0,sep=';').columns.tolist()
        Event=pd.read_csv('dwc_terms\event.csv',header=0,sep=';').columns.tolist()
        Location=pd.read_csv('dwc_terms\location.csv',header=0,sep=';').columns.tolist()
        Geological_Context=pd.read_csv('dwc_terms\GeologicalContext.csv',header=0,sep=';').columns.tolist()
        Identification=pd.read_csv('dwc_terms\identification.csv',header=0,sep=';').columns.tolist()
        Taxon=pd.read_csv('dwc_terms\Taxon.csv',header=0,sep=';').columns.tolist()
        columns_dwc=[Record_level,Ocurrence,Organism,Material_sample,Event,Location,Geological_Context,Identification,Taxon]
        dwc_columns=[]
        for labels in columns_dwc:
            msg='select the terms for your custom dwc dataframe'
            title='select terms'       
            choicebox=eg.multchoicebox(msg,title,labels)
            try:
                dwc_columns.extend(choicebox)
            except:
                dwc_columns
        dataframe=pd.DataFrame(columns=dwc_columns)
        return dataframe

#autosugerir el nombre cientifico
class subject:
    def __init__(self,data):
        self.data=data

    def datafiltering(self,data):
        columns_df=data.columns.tolist()
        msg='select a value to query'
        title='select'
        choicebox=eg.choicebox(msg,title,columns_df)
        querys=data[choicebox].unique()
        query_choicebox=eg.choicebox(msg,title,querys)
        data.query(f"{choicebox}=='{query_choicebox}'",inplace=True) 
        return data
    
    def datafiltering_predef(self,data,column):
        msg='select a value to query'
        title='select'
        querys=data[column].unique()
        query_choicebox=eg.choicebox(msg,title,querys)
        data.query(f"{column}=='{query_choicebox}'",inplace=True) 
        return data

    def change_values(self,data,subjects): 
        print('These are the following IDs who meet your query')
        for indexo, values in enumerate(subjects):
            print(indexo,values)        
        print('The following values are available for change: ')
        columns=data.columns.tolist()[:]
        for indexo, values in enumerate(columns):
            print(indexo,values)
        indexo1=int(input('Insert the number of the value you wish to update: '))
        set_value=input('enter the new value: ')
        ans=input('Are you sure you want to change the value from {0} to {1}\nY/n ?'.format(data.at[subjects[0],columns[indexo1]],set_value))
        if ans=='Y' or ans=='y':    
            for values in subjects:
                data.at[values,columns[indexo1]]=set_value
                data.at[values,'acceptedNameUsage']= '{0} {1} {2}'.format(data.at[values,'genus'],data.at[values,'specificEpithet'],data.at[values,'nameAcordingTo'])
            return data 
        else:
            pass 
        
    def add_values(self,data):
        msg = "Enter information about the new subject"
        title = "New subject entry "
        last_indexo =data.index[-1]
        new = int(last_indexo, 36) + 1
        new_id=numpy.base_repr(new, 36)
        fieldNames = data.columns.tolist()[1:]
        fieldValues = []
        fieldValues = eg.multenterbox(msg,title, fieldNames)
        fieldValues.insert(0,new_id)
        data.loc[fieldValues[0]]=fieldValues
        return data

    def save_values(self,data): #programar para que tire a csv
        pass

def comparefiles(ID,info,option): #option 1 for showroom, 0 files 
    filename1 = "temp/"+ID+'.txt'
    if option==1:
        filename2= "showroom_files/"+ID+'.txt'
    elif option==0:
        filename2= "files/"+ID+'.txt'
    os.makedirs(os.path.dirname(filename1), exist_ok=True)
    with open(filename1,'w') as fil:
        fil.write(str(info))
    if os.path.isfile(filename2)==True:
        if filecmp.cmp(filename1,filename2)==False:
            print('ive found some changes since the last time, on file... {0}.txt'.format(ID))
            print('changes has been saved')
            shutil.move(filename1,filename2)
        else:
            pass
    else:
        print('a new entry has been found, file... {0}.txt has been created.'.format(ID))
        os.makedirs(os.path.dirname(filename2), exist_ok=True)
        with open(filename2,'w') as fil:
            fil.write(str(info))
    shutil.rmtree('temp/', ignore_errors=False, onerror=None)
    return 

def infowriting(ID,info,option):  #option 1 for showroom, 0 files
    try: 
        if option ==0:
            filename = "files/"+ID+'.txt' 
        elif option==1:
            filename = "showroom_files/"+ID+'.txt' 
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename,'w') as fil:
            fil.write(str(info))
        print('a new entry has been found, file...'+ID+'.txt has been created.')
    except:
        print('permission to write in {0} has been denied...').format(filename)
    return 

def dynamiclinks(longurl):
    api_key='AIzaSyCsBqEkRDVJ8ZNp1E8HcbWDe_JEHu9Frgw' #this need to be created on the firebase webpage
    sub_domain='arboretum' #this need to be created on firebase webpage
    try:
        url_shortener = UrlShortener(api_key,sub_domain)
        shorturl=url_shortener.get_short_link(longurl)
    except:
        print('Oops! you have reached the limit of urls')
    time.sleep(0.2) #to not break the limits of firebase
    return shorturl

#crear un Qr para showroom 
#Crear un Qr para manejo del lab
def qr_manager(ID,short_url,option): #option 1 for showroom, 0 files
    try:
        if option ==0:
            filename = "qrs/"+ID+'.png'
        elif option==1:
            filename = "qrs_showroom/"+ID+'.png'
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        quick_response_code= pyqrcode.create(short_url)
        with open(filename, 'wb') as f:
                quick_response_code.png(f, scale=8,module_color=(0,102,0,255),background=(255, 255, 255, 255))
        img = Image.open(filename)
        width, height = img.size
        logo_size =50
        logo = Image.open('118px-Leaf_icon_15.png')
        xmin = ymin = int((width / 2) - (logo_size / 2))
        xmax = ymax = int((width / 2) + (logo_size / 2))
        logo = logo.resize((xmax - xmin, ymax - ymin))
        img.paste(logo, (xmin, ymin, xmax, ymax))
        img.save(filename)
    except:
        print('permission to write in {0} has been denied...').format(filename)

####################################################################
##############################MAIN##################################
####################################################################

#######################################
########FILE MANAGEMENT SECTION########
#######################################

dataframe=file_manager()
file_mng_button=eg.buttonbox(msg='select an option',title='select an option',choices=['Open a file','Create a custom dwc file'])
if file_mng_button=='Open a file':
    og_data,data,indexo,og_columns_df=dataframe.file_opener() #no considerar para file_creation
    IDs=data.index.tolist() #no considerar para file_creation 
    showroom_option_button=eg.buttonbox(msg='do you wish to create files for a showroom',title='select a option',choices=['Yes','No'])
    if showroom_option_button=='Yes':
        data_showroom=og_data.copy()
        msg='select the columns to keep on your showroom dataframe'
        title='select'
        choicebox=eg.multchoicebox(msg,title,og_columns_df)
        showroom_columns=list(set(og_columns_df)-set(choicebox)) #columnas que no estan presentes
        try:
            for label in showroom_columns:
                data_showroom.drop(label,axis=1,inplace=True)
        except:
            pass
    elif showroom_option_button=='No':
        pass
elif file_mng_button=='Create a custom dwc file':
    data=dataframe.file_creation() #no considerar para file_opener
    data.to_csv('custom_dwc_frame.csv',sep=';', encoding='utf-8') #considerar para file opener
    print ('your file is ready....')

print(data)

##################################
########QUERY DATA SECTION########
##################################

query_choicebox_options=['Yes...Custom query','Query by: order-family-genus-specificEpithet','Query by: Class-order-family-genus-specificEpithet','No']
query_choicebox=eg.choicebox(msg='Do you wish to query your data...',title='Query options',choices=query_choicebox_options)
if query_choicebox==query_choicebox_options[0]:
    data_for_query=data.copy()
    r1=subject(data_for_query)
    answer_query_choicebox=True
    while answer_query_choicebox==True:
        r1.datafiltering(data_for_query)
        print(data_for_query)
        answer_query_choicebox=eg.ynbox(msg='Do you wish to make a new query?',title='Select an option')
    print('Your query has been finished....')
    print(data_for_query)
elif query_choicebox==query_choicebox_options[1]:
    data_for_query=data.copy()
    r1=subject(data_for_query)
    column_query_predef=['order','family','genus','specificEpithet']
    for columns_predef in column_query_predef:
        r1.datafiltering_predef(data_for_query,columns_predef)
    print('Your query has been finished....')
    print(data_for_query)
elif query_choicebox==query_choicebox_options[2]:
    data_for_query=data.copy()
    r1=subject(data_for_query)
    column_query_predef=['Class','order','family','genus','specificEpithet']
    for columns_predef in column_query_predef:
        r1.datafiltering_predef(data_for_query,columns_predef)
    print('Your query has been finished....')
    print(data_for_query)
else:
    pass

""" DEBO DECIDIR SI HARE LA FUNCION PARA OBTENER UN CSV O EXCEL 
ADEMAS DE REOBTENER EL VALOR SUBJECTS DE DATA_FOR_QUERY PARA CAMBIAR LOS VALORES SI ES QUE SE QUIERE 
DAR OPCION DE GUARDAR, CAMBIAR VALORES O MOSTRAR SUJETOS QUE CUMPLEN LOS REQUISITOS
SECCION EN DESARROLLO
"""
########################SECCION EN DESARROLLO##########################################
if not query_choicebox==query_choicebox_options[3] or query_choicebox==None:
    choicebox_for_after_query_options=['export your query to a xlsx file (readable for excel)','make changes on your query and export them to a xlsx file (this changes will be saved on your original file)','show the subjects wich match your query']
    choicebox_for_after_query=eg.choicebox(msg='Choose an option for your query...',title='Query options',choices=choicebox_for_after_query_options)
    if choicebox_for_after_query==choicebox_for_after_query_options[0]:
        #export your query to a xlsx file (readable for excel)
        pass
    elif choicebox_for_after_query==choicebox_for_after_query_options[1]:
        #make changes on your query and export them to a xlsx file (this changes will be saved on your original file)
        pass
    elif choicebox_for_after_query==choicebox_for_after_query_options[2]:
        #show the subjects wich match your query
        subjects=data_for_query[indexo].tolist()
        for values in subject:
            print(values)
    else:
        pass


#Change values
""" if ans1 =='Y' or ans1 =='y' or ans1=='n' or ans1=='N':
    r1.change_values(data,subjects)
else:
    pass
 """
#Add values 
#r1.add_values(data)

#compare files or create them
print('compare/create files...')
if os.path.isdir('files')==True:
    for id in IDs:
        comparefiles(id,data.loc[id],0)
else:
    for id in IDs:
        infowriting(id,data.loc[id],0)

if showroom_option_button=='Yes':
    if os.path.isdir('showroom_files')==True:
        for id in IDs:
            comparefiles(id,data_showroom.loc[id],1)
    else:
        for id in IDs:
            infowriting(id,data_showroom.loc[id],1)
print ('there is nothing more to do here...')

#compare qr files or create them
print('create non existing qrs files...')
if os.path.isdir('qrs')==True:
    for id in IDs:
        print('file {0} of file {1}'.format(id,IDs[-1]),end='\r', flush=True)
        path="qrs/"+id+'.png'
        if os.path.isfile(path)==False:
            longurl='https://github.com/marcelooyaneder/Arboretum_Antumapu/blob/master/files/'+id+'.txt'
            shorturl=dynamiclinks(longurl)
            qr_manager(id,shorturl,0)
        else:
            pass
else:
    for id in IDs:
        print('file {0} of file {1}'.format(id,IDs[-1]),end='\r', flush=True)
        longurl='https://github.com/marcelooyaneder/Arboretum_Antumapu/blob/master/files/'+id+'.txt'
        shorturl=dynamiclinks(longurl)
        qr_manager(id,shorturl,0)

if showroom_option_button=='Yes':
    print('create non existing qrs shorwoom files...')
    if os.path.isdir('showroom_qrs')==True:
        for id in IDs:
            print('file {0} of file {1}'.format(id,IDs[-1]),end='\r', flush=True)
            path="showroom_qrs/"+id+'.png'
            if os.path.isfile(path)==False:
                longurl='https://github.com/marcelooyaneder/Arboretum_Antumapu/blob/master/showroom_files/'+id+'.txt'
                shorturl=dynamiclinks(longurl)
                qr_manager(id,shorturl,1)
            else:
                pass
    else:
        for id in IDs:
            print('file {0} of file {1}'.format(id,IDs[-1]),end='\r', flush=True)
            longurl='https://github.com/marcelooyaneder/Arboretum_Antumapu/blob/master/showroom_files/'+id+'.txt'
            shorturl=dynamiclinks(longurl)
            qr_manager(id,shorturl,1)
else:
    pass
print ('there is nothing more to do here...')