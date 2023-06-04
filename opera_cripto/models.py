from opera_cripto.conexion import Conexion
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, SelectField
from wtforms.validators import DataRequired, InputRequired
import requests 
import sqlite3
from opera_cripto import ORIGIN_DATA
from config import APIKEY

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
    conn = sqlite3.connect(ORIGIN_DATA)
    c = conn.cursor()
    c.execute(query, params)
    conn.commit()
    filas = c.fetchall()
    conn.close
       
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

def peticionAPI(specific_url):
    response = requests.get(specific_url)
    if response.status_code == 200:
        api = response.json()
        return api
    else: 
        raise Exception("Problema de consulta tipo {}".format(response.status_code)) 
    
def valorCrypto(crypto):
    url = f'https://rest.coinapi.io/v1/exchangerate/{crypto}/EUR'
    headers = {'X-CoinAPI-Key' : APIKEY}
    response = requests.get(url, headers=headers)
    r = response.json()
    rate = r["rate"]
    return rate
    
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
    
    '''
    if crypto == 'EUR' and convert != 'BTC':
        error = 'Con EUR sólo puedes comprar BTC.'
        return error
    '''
    try:
        if float(amount) <= 0:
            error = 'Cifra no válida. La cantidad debe ser superior a 0.'
            return error
    except:
        error = 'Cifra o caracter no válido. Use el punto para separar decimales.'
        return error
            
    if crypto != 'EUR' and monedero[crypto] < float(amount):
        error = 'Sólo dispone de {:.4f} {} para gastar. Consulte el monedero para ver la cantidad real.'.format(monedero[crypto], crypto)
        return error
        
    if crypto == convert:
        error = 'Las monedas From y To deben ser diferentes.'
        return error  

def invert():
    conectarInvertidos = Conexion("SELECT Moneda_from, Cantidad_from  from movimientos")
    filas = conectarInvertidos.res.fetchall()
    invertido = 0
    pun=0
    for i in filas:
        if filas[pun][0] == "EUR":
            invertido += filas[pun][1]
        pun += 1
    conectarInvertidos.conn.close()   
    return invertido

def euros_recuperados():
    conectarInvertidos = Conexion("SELECT Moneda_to, Cantidad_to  from movimientos")
    rec = conectarInvertidos.res.fetchall()
    recuperado = 0
    pun=0
    for i in rec:
        if rec[pun][0] == "EUR":
            recuperado += rec[pun][1]
        pun += 1
    conectarInvertidos.conn.close()   
    return recuperado

def valor_actual():
    conectarInvertidos = Conexion("SELECT Moneda_to, Cantidad_to  from movimientos")
    crypto_inver = conectarInvertidos.res.fetchall()
    invertido = 0
    pun=0
    for i in crypto_inver:
        if crypto_inver[pun][0] != "EUR":
            crypto = crypto_inver[pun][0]
            crypto_q = float(crypto_inver[pun][1])
            conver = valorCrypto(crypto)
            sum = conver * crypto_q
            invertido += sum
        else:
            crypto = crypto_inver[pun][0]
            crypto_q = float(crypto_inver[pun][1])
            conver = valorCrypto(crypto)
            sum = conver * crypto_q
            invertido -= sum
        pun += 1
    conectarInvertidos.conn.close()   
    return invertido
