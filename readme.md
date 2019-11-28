# INTRODUCCIÓN
Este software, desarrollado completamente en python, tiene la funcionalidad de leer una base de datos basada en Darwin Core y poder realizar un análisis de esta, a continuación se da una lista de las funciones implementadas que se tiene.  Por el momento para mostrar tus datos es necesario que tu proyecto este alojado en GitHub.

 - Leer bases de datos basadas en DwC en formato .xlsx o .csv.
 - Eliminar columnas vacias que poseas en tu base de datos.
 - Identificar columnas que no pertenezcan a DwC.
 - Obtener códigos Qr que dirigan a un link con la información de tu base de datos. 
 - Poder filtrar tus datos para poder realizar cambios u obtener solo una lista de estos.

> Recomendamos utilizar la versión de jupyter notebook, si es que no estas familiarizado con python, será mucho más facil. 
> Tambien existe la versión pura del código en python, es exactamente igual a la de jupyter, salvo excepciones para mejor visualización de los datos en jupyter.

# EJECUCIÓN DEL PROGRAMA
## Instalación de paquetes
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
![jupyter notebook init](https://lh3.googleusercontent.com/HLbKzsT1i5E8H33-IZ3EwOt1dtB55Jl6-nLQ03JcY80AsMlrUOJRLSsZz9CJNVPIYZuhNLpgSHvu "jupyter screenshot")
ahí debes abrir el archivo "main.ipynb" y ejecutar este, este archivo esta preconfigurado, por lo que solo debes ejecutarlo y se instalarán todas las dependencias faltantes automáticamente, y el programa se ejecutará. 

## Primeros pasos
 - Primero que todo es necesario darle un formato específico a el archivo a leer por el software, el formato consta de lo siguiente, en la primera fila debe ir el nombre de las columnas de DwC, no importa el orden de estas, y debajo de estas debe ir la información, a continuación se muestra una imagen de como debe ser. Importante decir que si existe el valor "class" en tu base de datos, este debe ser cambiado por el valor "Class".
 -  lo siguiente es abrir el archivo "main.ipynb", como se indico anteriormente

 - Luego debes modificar las lineas de código llamadas "longurl", de la siguiente forma, originalmente estás se encontrarán así.

       longurl=f'https://raw.githubusercontent.com/user_name/repo_name/master/files/{id}.txt'

- Donde :

  user_name: corresponde al nombre de usuario de tu cuenta GitHub.
  repo_name: corresponde al nombre del repositorio que mantiene tu proyecto.
 Por lo tanto al reemplazar quedaría de la siguiente forma.
 
		 longurl=f'https://raw.githubusercontent.com/marcelooyaneder/Arboretum_Antumapu/master/files/{id}.txt'

 - Paso siguiente es alojar todos los archivos que necesitas en tu repositorio GitHub, adjunto un video en caso de que no conozcas el proceso.
 
[![](http://img.youtube.com/vi/gjMEehpSTNk/0.jpg)](http://www.youtube.com/watch?v=gjMEehpSTNk "")
 
- Por último es ejecutar el código, para esto en la ventana de jupyter notebook ir a la pestaña

> kernel >
> Restart & Run all

- Seguir las indicaciones del software


