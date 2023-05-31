# Aplicación Web dirigida a la Inversión y Tradeo de Criptomonedas

Programa hecho en python utilizando el framework flask.
Desarrollado por Pedro Liébana Castellano para el Bootcamp, "Aprende a programar desde 0"

# PRIMEROS PASOS

Al descargar el archivo .zip desde github y abierto con Visual Studio Code, nos dirigimos hacia la pestaña "Terminal" para seleccionar "Nuevo terminal". Una vez abierto un nuevo terminal procederemos siguiendo estos pasos:

# Instalación

- Crear un entorno en python 
```
py -m venv venv
```

- Posteriormente procedemos a activar nuestro entorno
```
.\venv\Scripts\activate
```

- Por último, ejecutar el comando
```
pip install -r requirements.txt
```
La libreria utilizada en flask https://flask.palletsprojects.com/en/2.2.x/

# Ejecucion del programa

- Inicializar el servidor de flask
- En mac: 
```
export FLASK_APP=main.py
```
- En windows: 
```
set FLASK_APP=main.py
```

# Otra opción de ejecucion
- Instalar
```
pip install python-dotenv
```
- Crear un archivo .env y dentro agregar lo siguiente:
``` 
FLASK_APP=main.py
```
```
 FLASK_DEBUG=True
  ```
- Para lanzar en la terminal utilizamos el comando:
``` 
flask run 
```

# Comando para ejecutar el servidor:
```
flask --app main run
```
# Comando para ejecutar el servidor en otro puerto diferente por default es el 5000
```
flask --app main run -p 5002
```
# Comando para ejecutar el servidor en modo debug, para realizar cambios en tiempo real
```
flask --app main --debug run
```