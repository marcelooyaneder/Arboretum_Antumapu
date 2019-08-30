#package imports
import pandas as pd

#creation of classes and functions

def infowriting(ID,info):
    with open(ID+'.txt','w') as fil:
        fil.write(str(info))
    pass
    return 


#Process
#read excel
data=pd.read_excel('Inventario_2019_Arboretum_Antumapu_Dwc.xlsx',sheet_name='Hoja1',header=0)
#rearrange dataframe
data=data.set_index("catalogNumber", drop = False)
#obtaining ID data
IDs=data['catalogNumber'].tolist()

#get info into a txt document ESTA FUNCIONANDO NO EJECUTAR YA QUE CREA DEMASIADOS ARCHIVOS
#for id in IDs:
#    infowriting(id,data.loc[id])
