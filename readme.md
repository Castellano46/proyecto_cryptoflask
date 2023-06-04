# Aplicación Web dirigida a la Inversión y Tradeo de Criptomonedas

Programa hecho en python utilizando el framework flask.
Desarrollado por Pedro Liébana Castellano para el Bootcamp, "Aprende a programar desde 0".

Con este programa podremos simular inversiones con diversas criptomonedas y visualizar el grado de beneficio o pérdida obtenido.

# PRIMEROS PASOS

- Descargar el archivo .zip desde github.
- Abrir el archivo con Visual Studio Code. 
- Posteriormente accederemos a nuestro navegador web para ingresar la siguiente url: https://docs.coinapi.io/ y de esta manera, obtener una APIKEY que nos llegará a nuestro correo electrónico.
- La APIKEY obtenida la copiaremos y pegaremos dentro de las comillas ("") de APIKEY="", en la sección llamada config.py.
- Dentro de la carpeta /data de nuestro proyecto crearemos una base de datos en DB Browser con los datos mostrados en data/create_Movimientos.sql. Llamaremos a esta base de datos 
```
cripto.sqlite
```
Cuando hayamos completado estos pasos procederemos a abrir un nuevo terminal en la pestaña "Terminal" de Visual Studio Code, seleccionaremos "Nuevo Terminal" y continuamos con la instalación.

# Instalación

- Crear un entorno en python 
```
py -m venv venv
```

- Seguidamente activaremos nuestro entorno
```
.\venv\Scripts\activate
```

- Por último, ejecutar el comando
```
pip install -r requirements.txt
```
La libreria utilizada en flask https://flask.palletsprojects.com/en/2.2.x/

# Ejecución del programa

- Inicializar el servidor de flask
- En mac: 
```
export FLASK_APP=main.py
```
- En windows: 
```
set FLASK_APP=main.py
```

# Otra opción de ejecución
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