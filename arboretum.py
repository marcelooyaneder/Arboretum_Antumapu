#package imports
import pandas as pd

#Process
data=pd.read_excel('Inventario_2019_Arboretum_Antumapu_Dwc.xlsx',sheet_name='Hoja1',header=0)
data=data.set_index("catalogNumebr", drop = True)

print data.loc['AA1714','order']

