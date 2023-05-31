from opera_cripto.conexion import Conexion
from flask import Flask, render_template, request, url_for, redirect
import datetime
from flask_wtf import FlaskForm
from wtforms import IntegerField, DateField, StringField, FloatField, SubmitField, SelectField, ValidationError, TimeField, validators
from wtforms.validators import DataRequired, Length, NumberRange, InputRequired
import time
import requests 
import sqlite3
from opera_cripto import ORIGIN_DATA


class MovementForm(FlaskForm):
    lista_monedas = ['EUR','BTC','ETH','USDT','BNB','XRP','ADA','SOL','DOT','MATIC']
    Moneda_from = SelectField('From', choices=[], validators=[DataRequired()])
    Cantidad_from = FloatField('Q', validators=[InputRequired()], render_kw={'readonly': False})
    Moneda_to =  SelectField('To', choices=lista_monedas, validators=[DataRequired()])
    Cantidad_to = FloatField('Q', render_kw={'readonly': True}) 
    precio_unitario_to = FloatField('P.U.', render_kw={'readonly': True})
    Fecha = StringField('Fecha', render_kw={'readonly': True}) 
    Hora = StringField('Hora', render_kw={'readonly': True}) 
    
    submit = SubmitField('boton')


def consulta(query, params=()):
    ## función 1: establecer conexión con sqlite3
    conn = sqlite3.connect(ORIGIN_DATA)
    c = conn.cursor()
    c.execute(query, params)
    conn.commit()
    filas = c.fetchall()
    conn.close
       
    ## función 2: dar formato a la consulta como lista de diccionarios
    if len(filas) == 0:
        return filas

    columnNames = []
    for columnName in c.description:
        columnNames.append(columnName[0]) 

    listaDeDiccionarios = []

    for fila in filas:
        d = {}
        for ix, columnName in enumerate(columnNames): 
            d[columnName] = fila[ix] 
        listaDeDiccionarios.append(d)

    return listaDeDiccionarios 

#  ?¿
def peticionAPI(specific_url):
    response = requests.get(specific_url)
    if response.status_code == 200:
        api = response.json()
        return api
    else: 
        raise Exception("Problema de consulta tipo {}".format(response.status_code)) 
    
    '''
    url = 'https://rest.coinapi.io/v1/exchangerate/{crypto}/{convert}?apikey={APIKEY}'.format(crypto, convert, APIKEY)
    data = requests.get(url)
        if data.status_code == 200:
            data = data.json()
            for e in data['data']:
                print(e['rate'])
    '''    

def calc_monedero():
    lista_monedas = ['BTC','ETH','USDT','BNB','XRP','ADA','SOL','DOT','MATIC']
    monedero = {} 
    for moneda in lista_monedas:
        query = "SELECT sum(case when Moneda_to = ? then Cantidad_to else 0 end) - sum(case when  Moneda_from = ? then Cantidad_from else 0 end) as saldo_moneda FROM Movimientos;"
        tmp = consulta(query, (moneda, moneda))
        saldo = tmp[0]['saldo_moneda']
        monedero[moneda] = saldo
    return monedero

def validarConversion(amount, crypto, convert):
    monedero = calc_monedero()
    error = None
    try:
        if float(amount) <= 0:
            error = 'Cifra no válida. La cantidad debe ser superior a 0.'
            return error
    except:
        error = 'Cifra no válida. Use el punto para separar decimales.'
        return error
    
    if crypto != 'EUR' and monedero[crypto] < float(amount):
        error = 'Sólo dispone de {:.4f} {} para gastar. Consulte el monedero para ver la cantidad real.'.format(monedero[crypto], crypto)
        return error
    
    if crypto == convert:
        error = 'Las monedas From y To deben ser diferentes.'
        return error  
   
    if crypto != 'BTC' and convert == 'EUR':
        error = 'Sólo puede comprar EUR con BTC.'
        return error





''' 
   if crypto == 'EUR' and convert != 'BTC':
        error = 'Con EUR sólo puedes comprar BTC.'
        return error
           
fecha_actual = datetime.datetime.now() 

fecha = datetime.datetime.strftime(fecha_actual, '%Y-%m-%d')
hora = datetime.datetime.strftime(fecha_actual, '%H: %M: %S')
    

def select_all():
    conectar = Conexion("SELECT * FROM Movimientos")


    filas = conectar.res.fetchall()
    columnas = conectar.res.description

    lista_diccionario=[]
    
    for f in filas:
        diccionario ={}
        posicion=0
        for c in columnas:
            diccionario[c[0]] = f[posicion]
            posicion +=1
        lista_diccionario.append(diccionario)

    conectar.con.close()

    return lista_diccionario

def insert(registroForm, Fecha=fecha, Hora=hora):
    conectarInsert = Conexion("insert into movimientos(Moneda_from, Cantidad_from, Moneda_to) values (?,?,?)", registroForm)

    conectarInsert.con.commit()

    conectarInsert.con.close()

'''
