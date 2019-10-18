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
        columns_dwc=pd.read_csv('dwc_terms\simple_dwc_horizontal.csv',header=0,sep=';').columns.tolist() #ver como variar de ; o , 
        columns_difference=list(set(columns_df)-set(columns_dwc))
        if not columns_difference:
            pass
        else:
            msg='select columns to delete from your analysis'
            title='select to delete'       
            choicebox=eg.multchoicebox(msg,title,columns_difference)
            try:
                for label in choicebox:
                    data.drop(label,axis=1,inplace=True)
            except:
                pass
        msg='select a column to be the index of the dataframe'
        title='select index'       
        indexo=eg.choicebox(msg,title,columns_df)
        data=data.set_index(indexo, drop = False)
        return data,indexo,columns_df
    
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

    def datafiltering_by_class(self,data):
        #print (data.query('specificEpithet=="americana"'))
        #https://cmdlinetips.com/2018/01/how-to-get-unique-values-from-a-column-in-pandas-data-frame/
        query=data["Class"].unique()
        print('The following Class values are in your data: ')
        for indexo, values in enumerate(query):
            print(indexo,values)
        indexo2=int(input('insert the number for query your data: '))
        var2=query[indexo2]
        query_df_by_class=data.query('Class==@var2')
        return query_df_by_class

    def datafiltering_by_order(self,data):
        query=data["order"].unique()
        print('The following order values are in your data: ')
        for indexo, values in enumerate(query):
            print(indexo,values)
        indexo2=int(input('insert the number for query your data: '))
        var2=query[indexo2]
        query_df_by_order=data.query('order==@var2')
        return query_df_by_order
    
    def datafiltering_by_family(self,data):
        query=data["family"].unique()
        print('The following family values are in your data: ')
        for indexo, values in enumerate(query):
            print(indexo,values)
        indexo2=int(input('insert the number for query your data: '))
        var2=query[indexo2]
        query_df_by_family=data.query('family==@var2')
        return query_df_by_family
    
    def datafiltering_by_genus(self,data):
        query=data["genus"].unique()
        print('The following genus values are in your data: ')
        for indexo, values in enumerate(query):
            print(indexo,values)
        indexo2=int(input('insert the number for query your data: '))
        var2=query[indexo2]
        query_df_by_genus=data.query('genus==@var2')
        return query_df_by_genus
    
    def datafiltering_by_specificEpithet(self,data):
        query=data["specificEpithet"].unique()
        print('The following specificEpithet values are in your data: ')
        for indexo, values in enumerate(query):
            print(indexo,values)
        indexo2=int(input('insert the number for query your data: '))
        var2=query[indexo2]
        query_df_by_specificEpithet=data.query('specificEpithet==@var2')
        return query_df_by_specificEpithet
    
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

def comparefiles(ID,info,option): #option 0 for showroom, 1 for normal use
    filename1 = "temp/"+ID+'.txt'
    if option==0:
        filename2= "showroom_files/"+ID+'.txt'
    else:
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

def infowriting(ID,info,option):
    try: 
        if option ==0:
            filename = "files/"+ID+'.txt' #no showroom option
        elif option==1:
            filename = "showroom_files/"+ID+'.txt' #showroom option
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
def qr_manager(ID,short_url,option):
    #option 1 for dwc file management
    #option 0 for dwc showroom file management
    try:
        if option ==1:
            filename = "qrs/"+ID+'.png'
        else:
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

dataframe=file_manager()
buttons1=eg.buttonbox(msg='select an option',title='select an option',choices=['Open a file','Create a custom dwc file'])
if buttons1=='Open a file':
    data,indexo,columns_df=dataframe.file_opener() #no considerar para file_creation
    IDs=data.index.tolist() #no considerar para file_creation 
    buttons2=eg.buttonbox(msg='do you wish to create files for a showroom',title='select a option',choices=['Yes','No'])
    if buttons2=='Yes':
        data_showroom=data.copy()
        msg='select the columns to keep on your showroom dataframe'
        title='select'
        choicebox=eg.multchoicebox(msg,title,columns_df)
        showroom_columns=list(set(columns_df)-set(choicebox)) #columnas que no estan presentes
        try:
            for label in showroom_columns:
                data_showroom.drop(label,axis=1,inplace=True)
        except:
            pass
    elif buttons2=='No':
        pass
elif buttons1=='Create a custom dwc file':
    data=dataframe.file_creation() #no considerar para file_opener
    data.to_csv('custom_dwc_frame.csv',sep=';', encoding='utf-8') #considerar para file opener
    print ('your file is ready....')

print(data)

#query data 
r1=subject(data)
ans1=str(input('The following query is by default: order-family-genus-specificEpithet, Do you want to accept it Y/n?,\nif you dont want to query write "pass": \n'))
if ans1 =='Y' or ans1 =='y' :
    order_filtering=r1.datafiltering_by_order(data)
    family_filtering=r1.datafiltering_by_family(order_filtering)
    genus_filtering=r1.datafiltering_by_genus(family_filtering)
    specificEpithet_filtering=r1.datafiltering_by_specificEpithet(genus_filtering)
    subjects=specificEpithet_filtering[indexo].tolist()
    print('The following subjects has been query', subjects)
elif ans1=='n' or ans1=='N':
    print('The following query will be done: Class-order-family-genus-specificEpithet')
    class_filtering=r1.datafiltering_by_class(data)
    order_filtering=r1.datafiltering_by_order(class_filtering)
    family_filtering=r1.datafiltering_by_family(order_filtering)
    genus_filtering=r1.datafiltering_by_genus(family_filtering)
    specificEpithet_filtering=r1.datafiltering_by_specificEpithet(genus_filtering)
    subjects=specificEpithet_filtering[indexo].tolist()
    print('The following subjects has been query', subjects)
else: 
    pass

#Change values
if ans1 =='Y' or ans1 =='y' or ans1=='n' or ans1=='N':
    r1.change_values(data,subjects)
else:
    pass

#Add values 
#r1.add_values(data)

#compare files or create them
print('compare/create files...')
if os.path.isdir('files')==True:
    for id in IDs:
        comparefiles(id,data.loc[id],1)
else:
    for id in IDs:
        infowriting(id,data.loc[id],0)

if buttons2=='Yes':
    if os.path.isdir('showroom_files')==True:
        for id in IDs:
            comparefiles(id,data_showroom.loc[id],0)
    else:
        for id in IDs:
            infowriting(id,data_showroom.loc[id],1)
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
            qr_manager(id,shorturl,1)
        else:
            pass
else:
    for id in IDs:
        print('file {0} of file {1}'.format(id,IDs[-1]),end='\r', flush=True)
        longurl='https://github.com/marcelooyaneder/Arboretum_Antumapu/blob/master/files/'+id+'.txt'
        shorturl=dynamiclinks(longurl)
        qr_manager(id,shorturl,1)

if buttons2=='Yes':
    if os.path.isdir('showroom_qrs')==True:
        for id in IDs:
            print('file {0} of file {1}'.format(id,IDs[-1]),end='\r', flush=True)
            path="showroom_qrs/"+id+'.png'
            if os.path.isfile(path)==False:
                longurl='https://github.com/marcelooyaneder/Arboretum_Antumapu/blob/master/showroom_files/'+id+'.txt'
                shorturl=dynamiclinks(longurl)
                qr_manager(id,shorturl,0)
            else:
                pass
    else:
        for id in IDs:
            print('file {0} of file {1}'.format(id,IDs[-1]),end='\r', flush=True)
            longurl='https://github.com/marcelooyaneder/Arboretum_Antumapu/blob/master/showroom_files/'+id+'.txt'
            shorturl=dynamiclinks(longurl)
            qr_manager(id,shorturl,0)
else:
    pass
print ('there is nothing more to do here...')