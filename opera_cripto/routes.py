from opera_cripto import app
from opera_cripto.models import *
from flask import Flask, render_template, request, url_for, redirect
import sqlite3
from datetime import date, datetime
import time
from flask_wtf import FlaskForm
import requests 
import json
from opera_cripto import ORIGIN_DATA
from config import APIKEY
from opera_cripto.conexion import Conexion


#APIKEY =  app.config['APIKEY']
#ORIGIN_DATA = app.config['ORIGIN_DATA']

@app.route('/')
def listaMovimientos(): # mostrar tabla SQL
    query = "SELECT Fecha, Hora, Moneda_from, Cantidad_from, Moneda_to, Cantidad_to, Cantidad_from/Cantidad_to as precio_unitario_to FROM Movimientos;"
    mensaje = ""
    try:
        compras = consulta(query)
    except Exception as e:
        print("**ERROR**: Acceso base de datos - {}".format(type(e).__name__))
        mensaje = "Error en acceso a la base de datos."
        return render_template("index.html", error=mensaje)
    
    monedero_actual = calc_monedero()
    return render_template("index.html", datos=compras, monedero=monedero_actual, error=mensaje, title="Inicio")

@app.route('/purchase', methods=['GET', 'POST'])
def purchase():
    # 1) Formulario vacío:
    if request.method == 'GET':
        form_vacio = MovementForm()
        try:
            monedero = calc_monedero()
        except Exception as e:
            print("**ERROR**: Acceso base de datos - {}".format(type(e).__name__))
            mensaje = "Error en acceso a la base de datos."
            return render_template("index.html", error=mensaje, title="Purchase")
        
        lista_from = ['EUR'] 
        
        try:
            for moneda, q in monedero.items():
                if q>0:
                    lista_from.append(moneda)
            form_vacio.Moneda_from.choices = lista_from 
        except:
            monedero = 'vacio'
            form_vacio.Moneda_from.choices = lista_from
        
        return render_template("purchase.html", form=form_vacio, vacio='yes', monedero=monedero, title="Purchase")
    
    else: #2) request.method == 'POST': Grabar o Calcular
        form = MovementForm()
        form.Moneda_from.choices = [request.form.get('Moneda_from')] 
        form.Moneda_to.choices = [request.form.get('Moneda_to')] 
        monedero = calc_monedero()
        
        if  request.form.get('submit') == 'Grabar' and form.validate():
            try: 
                query = "INSERT INTO Movimientos (Fecha, Hora, Moneda_from, Cantidad_from, Moneda_to, Cantidad_to) VALUES (?,?,?,?,?,?);"
                consulta(query, (request.form.get("Fecha"), request.form.get("Hora"), request.form.get("Moneda_from"),
                                request.form.get("Cantidad_from"), request.form.get("Moneda_to"), request.form.get("Cantidad_to")))
                
                return redirect(url_for('listaMovimientos'))
            except:
                error = "Error: Debe efectuar el cálculo (botón calculadora) antes de validar la compra."
                return render_template("purchase.html", form=form, vacio='yes', error=error, monedero=monedero, title="Purchase")
        else:
            amount = request.form.get('Cantidad_from') 
            crypto = request.form.get('Moneda_from') 
            convert = request.form.get('Moneda_to')
            
            #3) Errores en la conversión de monedas:
            error = validarConversion(amount, crypto, convert)
            if error != None:
                return render_template("purchase.html", form=form, vacio='yes', error=error, monedero=monedero, title="Purchase")
            
            # 4) Finalmente: consulta a la API ¿?
            try:
                
                fecha_compra = time.strftime("%d/%m/%Y")
                hora_compra = time.strftime("%H: %M: %S")
                url = 'https://rest.coinapi.io/v1/exchangerate/{}/{}?apikey={}'.format(crypto, convert, APIKEY)                
                dicc = peticionAPI(url)
                precioUnitario = float(amount)/float(dicc["rate"])                
                return render_template("purchase.html", vacio='no', form=form, q_to=dicc["rate"], precioUnitario=precioUnitario, hora_compra=hora_compra, fecha_compra=fecha_compra, monedero=monedero, amount=amount)
            except Exception as error:
                print("**ERROR**: Conexion url en PURCHASE - {}".format(type(error).__name__), error) 
                error = "Problema de conexión. Contacte con el administrador."
                return render_template("purchase.html", vacio='yes', form=form, error=error, monedero=monedero, title="Purchase")

@app.route('/status')
def status():
    # 1)invertido
    query1 = 'SELECT SUM(Cantidad_from) as eur_from FROM Movimientos WHERE Moneda_from="EUR";'
    try:
        total_diccionario = consulta(query1)
    except Exception as e:
        print("**ERROR**: Acceso base de datos - {}".format(type(e).__name__))
        mensaje = "Error en acceso a la base de datos."
        return render_template("index.html", error=mensaje, title="Status")
    
    total_eur_invertido = total_diccionario[0]['eur_from'] 
    
    #2)valor de la compra
    query2 = 'SELECT sum(case when Moneda_to = "EUR" then Cantidad_to else 0 end) - sum(case when  Moneda_from = "EUR" then Cantidad_from else 0 end) as saldo_eur from Movimientos;'
    eur_diccionario = consulta(query2)
    saldo_euros_invertidos = eur_diccionario[0]['saldo_eur']
    
    #3) obtener precio unitario en EUR de todas las criptomonedas para obtener "recuperado": ¿?
    crypto =['BTC', 'ETH', 'USDT', 'BNB', 'XRP','ADA', 'SOL','DOT','MATIC'] 
    
    #"BTC,ETH,USDT,BNB,XRP,ADA,SOL,DOT,MATIC" 
        
    url = 'https://rest.coinapi.io/v1/exchangerate/{}/EUR?apikey={}'.format(crypto, APIKEY)
    try:
        dicc = peticionAPI(url)
    except Exception as error:
        #aqui marca el error (tipo 429 Too Many Requests el usuario ha enviado demasiadas peticiones en un tiempo determinado)
        print("**ERROR**: Conexion url en STATUS - {}".format(type(error).__name__), error)
        error = "Problemas de conexión. Contacte con el administrador."
        return render_template("status.html", invertido=0 , actual=0, error_conexion = error, title="Status")
    
    lista_monedas = ['BTC', 'ETH', 'USDT', 'BNB', 'XRP','ADA', 'SOL','DOT','MATIC']
    pu_crypto_eur = {}
    id_cryptos = {}
    for moneda in lista_monedas: 
        precio = dicc['data'][moneda]['quote']['EUR']['price']
        id_crypto = dicc['data'][moneda]['id']
        pu_crypto_eur[moneda] = precio
        id_cryptos[moneda] = id_crypto 
    
    #4)
    monedero = {} # cuantas monedas tengo de cada cripto
    monedero_eur = [] # valor en EUR de las monedas que tengo
    
    for moneda in lista_monedas:
        query3 = "SELECT sum(case when Moneda_to = ? then Cantidad_to else 0 end) - sum(case when  Moneda_from = ? then Cantidad_from else 0 end) as saldo_moneda FROM Movimientos;"
        tmp = consulta(query3, (moneda, moneda))
        saldo = tmp[0]['saldo_moneda']
        
        monedero[moneda] = saldo
        
        precio_unitario = float(pu_crypto_eur[moneda])
        try:
            monedero_eur.append(saldo * precio_unitario)
        except:
            return render_template("status.html", invertido=0 , actual=0, title="Status")
    
    valor_total_cryptos = 0
    for item in monedero_eur:
        valor_total_cryptos += item
    
    valor_actual = total_eur_invertido + saldo_euros_invertidos + valor_total_cryptos 
    
    return render_template("status.html", invertido=total_eur_invertido , actual=valor_actual, title="Status")