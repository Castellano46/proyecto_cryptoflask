from opera_cripto import app
from opera_cripto.models import *
from flask import render_template, request, url_for, redirect
import time
from config import APIKEY

@app.route('/')
def listaMovimientos():
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
    
    else: 
        
        form = MovementForm()
        form.Moneda_from.choices = [request.form.get('Moneda_from')] 
        form.Moneda_to.choices = [request.form.get('Moneda_to')] 
        monedero = calc_monedero()
        
        if  request.form.get('submit') == 'Grabar':  #and form.validate():
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
            
            error = validarConversion(amount, crypto, convert)
            if error != None:
                return render_template("purchase.html", form=form, vacio='yes', error=error, monedero=monedero, title="Purchase")
            
            try:
                
                fecha_compra = time.strftime("%d/%m/%Y")
                hora_compra = time.strftime("%H:%M:%S")
                url = 'https://rest.coinapi.io/v1/exchangerate/{}/{}?apikey={}'.format(crypto, convert, APIKEY)                
                dicc = peticionAPI(url)
                amount = float(request.form.get('Cantidad_from')) 
                precioUnitario = float(amount)/float(amount*dicc["rate"])                
                return render_template("purchase.html", vacio='no', form=form, q_to=amount*dicc["rate"], precioUnitario=precioUnitario, 
                                       hora_compra=hora_compra, fecha_compra=fecha_compra, monedero=monedero, amount=amount)
            except Exception as error:
                print("**ERROR**: Conexion url en PURCHASE - {}".format(type(error).__name__), error) 
                error = "Problema de conexión. Contacte con el administrador."
                return render_template("purchase.html", vacio='yes', form=form, error=error, monedero=monedero, title="Purchase")

@app.route('/status')
def status():
    invertido = invert()
    recuperado = euros_recuperados()
    recuperado = round(recuperado, 2)
    valor_compra = invertido - recuperado
    resultado_c = ""
    if valor_compra == 0  or valor_compra == invertido:
        resultado_c= "nada"
    elif valor_compra > 0:
        resultado_c = "beneficio"
    else:
        resultado_c = "perdida"

    valor_compra = round(valor_compra, 2)
    valor_act = valor_actual()
    if valor_act == 0:
        resultado_a = "nada"
    elif valor_act >= valor_compra:
        resultado_a = "beneficio"
    else:
        resultado_a = "perdida"
    
    margen = valor_act - valor_compra
    if margen == 0:
        total = "nada"
    elif margen >= 0:
        total = "beneficio"
    else:
        total = "perdida"

    return render_template("status.html", title = "Status", invertido = invertido, recuperado = recuperado, valor_compra = valor_compra, 
                           resultado_c = resultado_c, valor_act = valor_act, resultado_a = resultado_a, total = total, margen = margen)
    