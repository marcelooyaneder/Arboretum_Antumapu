
#INTRODUCCIÓN
Este software, desarrollado completamente en python, tiene la funcionalidad de leer una base de datos basada en Darwin Core y poder realizar un análisis de esta, a continuación se da una lista de las funciones implementadas que se tiene. 

 - Leer bases de datos basadas en DwC en formato .xlsx o .csv.
 - Eliminar columnas vacias que poseas en tu base de datos.
 - Identificar columnas que no pertenezcan a DwC.
 - Obtener códigos Qr que dirigan a un link con la información de tu base de datos. 
 - Poder filtrar tus datos para poder realizar cambios u obtener solo una lista de estos.

#EJECUCIÓN DEL PROGRAMA
##Instalación de paquetes
Dentro del repositorio se encuentra un archivo de texto, llamado "requeriments.txt" el cual contiene todos los paquetes para la correcta ejecución de este programa, antes de esto se recomienda tener lo siguiente instalado.

 - python >= 3.6
 - package manager pip

También es posible instalar conda, pero no se han realizado pruebas con este.
La primera acción si deseas ejecutar esto, directamente en tu pc, debes escribir lo siguiente en la terminal abierta en donde has descargado el repositorio y ejecutar lo siguiente. 

    pip install -U -r requirements.txt

Tambien se ha desarrollado la posibilidad de ejecutar esto en "Jupyter Notebook". Si es primera vez que instalas python y no tienes conda debes ejecutar lo siguiente

    pip install jupyter

Luego 

    Jupyter Notebook

Y tendrás una ventana en tu navegador como la siguiente.
![jupyter notebook init](https://lh3.googleusercontent.com/HLbKzsT1i5E8H33-IZ3EwOt1dtB55Jl6-nLQ03JcY80AsMlrUOJRLSsZz9CJNVPIYZuhNLpgSHvu "jupyter screenshot")ahí debes abrir el archivo "Main.ipynb" y ejecutar este, este archivo esta preconfigurado, por lo que solo debes ejecutarlo y se instalarán todas las dependencias faltantes automáticamente, y el programa se ejecutará. 

