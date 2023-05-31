import datetime

#hora_actual = datetime.datetime.now()

#print(hora_actual)

fecha_actual = datetime.datetime.now()

fecha = datetime.datetime.strftime(fecha_actual, '%Y-%m-%d')
hora = datetime.datetime.strftime(fecha_actual, '%H: %M: %S')

print(fecha)
print(hora)