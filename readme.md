# INTRODUCCIÓN
Este software, desarrollado completamente en python, tiene la funcionalidad de leer una base de datos basada en Darwin Core (DwC) y poder realizar un análisis de esta, a continuación se da una lista de las funciones implementadas que se tiene.  Por el momento para mostrar tus datos es necesario que tu proyecto este alojado en GitHub.

 - Leer bases de datos basadas en DwC en formato .xlsx o .csv.
 - Eliminar columnas vacias que poseas en tu base de datos.
 - Identificar columnas que no pertenezcan a DwC.
 - Obtener códigos Qr que dirigan a un link con la información de tu base de datos. 
 - Poder filtrar tus datos para poder realizar cambios u obtener solo una lista de estos.

> Recomendamos utilizar la versión de jupyter notebook, si es que no estas familiarizado con python.\
Tambien existe la versión pura del código en python, es exactamente igual a la de jupyter, salvo algunas excepciones para mejor visualización de los datos en jupyter.

# EJECUCIÓN DEL PROGRAMA

## Instalación de Software y paquetes
Para el correcto funcionamiento del software es necesario tener lo siguiente instalado en tu pc.

 - python 3.7, lo puedes descargar en el siguiente link https://www.python.org/downloads/release/python-370/
   - Al instalar python asegurate de tener marcada la casilla "Add python 3.7 to PATH" 
![](https://lh3.googleusercontent.com/nkCqWV88bAT5wzDic6_IQDG6S0fVMuJjTRo5Kqc8A914MsyOd0CRBHL871WsEeQ6hNl6oz5SPy5Q "python PATH")
 - package manager pip (incluido en la instalación previa).
 - GitHub Desktop.
 - Descargar este repositorio.

Luego de la instalación de lo anterior, la acción siguiente si deseas ejecutar el software es escribir lo siguiente en la terminal (cmd o powershell en windows). 

    pip3 install jupyter

**El resto de los paquetes se instalará automáticamente cuando ejecutes el software.**

## Primeros pasos
 - Primero que todo es necesario darle un formato específico a el archivo a leer por el software (de preferencia excel), y el formato consta de lo siguiente: 
   - En la primera fila debe ir el nombre de las columnas de DwC, no importa el orden de estas, y debajo de estas debe ir la información, a continuación se muestra una imagen a modo de ejemplo.
   - Importante decir que si existe el valor "class" en tu base de datos, este debe ser cambiado por el valor "Class".

![](https://lh3.googleusercontent.com/FgeRnw0GgiSvFHWSpznlj61G53NOGtgadUZqFHZ7v4jZIJ1PrTuoPArOH0eMhVpMMWPqh1wlhb0a "Format")

 - Lo siguiente es alojar todos los archivos que necesitas en tu repositorio GitHub, adjuntamos un video en caso de que no conozcas el proceso.
 
[![](http://img.youtube.com/vi/gjMEehpSTNk/0.jpg)](http://www.youtube.com/watch?v=gjMEehpSTNk "")

 - Abrir GitHub Desktop y sincronizar el nuevo repositorio creado a tu pc. (recomendamos ver el siguiente video...)

[![](http://img.youtube.com/vi/IW28zJc7BN0/0.jpg)](http://www.youtube.com/watch?v=IW28zJc7BN0 "")

 - Copiar los contenidos descargados de este repositorio a tu **nuevo repositorio**.
 - Luego dirigirse a la carpeta documents y abrir el archivo "dynamiclinks_user_info.csv" y llenar este con los datos requeridos, donde:
    - GitHub_username: corresponde al nombre de usuario de tu cuenta GitHub.
    - Repository_name: corresponde al nombre del repositorio que mantiene tu proyecto.
    - api_key y sub_domain: son extraídos de la web de google Firebase dinamic links, contactarse a mi correo para conseguir una o indicarte como (marcelo.oyaneder.l@gmail.com)

 - Dirigirte a la carpeta en que estén los archivos descargados del repositorio, abrir nuevamente una terminal (esta debe tener la dirección de esta carpeta) y ejecutar lo siguiente:

    jupyter notebook

   - Y tendrás una ventana en tu navegador de la siguiente forma, aqui debes abrir el archivo "main.ipynb".

![jupyter notebook init](https://lh3.googleusercontent.com/HLbKzsT1i5E8H33-IZ3EwOt1dtB55Jl6-nLQ03JcY80AsMlrUOJRLSsZz9CJNVPIYZuhNLpgSHvu "jupyter screenshot")
 
- Por último es ejecutar el código, para esto en la ventana de jupyter notebook ir a la pestaña.

    kernel > Restart & Run all

- Seguir las indicaciones del software.
- Abrir GitHub Desktop y actualizar tus datos.

# CRÉDITOS
Software desarrllado en el _laboratorio de biología de plantas_ ubicado en el campus Antumapu perteneciente a la Universidad de Chile.
 - Autores: 
   - Marcelo Oyaneder Labarca.
   - Paulette Naulin Gysling.  
 - Contacto:
   - marcelo.oyaneder.l@gmail.com
   - pnaulin@uchile.cl

![](https://lh3.googleusercontent.com/kwADztygurIvFqRkhgTwMKz5QakvqDIFK8NO_8f5Oxhik9G8hYz9xfO3mPbBhJUftU5oLu4NTIfl)


