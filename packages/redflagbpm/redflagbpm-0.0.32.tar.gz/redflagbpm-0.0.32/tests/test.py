

def mi_funcion(arg1, arg2, arg3):
    """
    Documentación
    :param arg1: es esto
    :param arg2: es aquello
    :param arg3: es esto otro
    """
    # mi código

    # controlo errores
    if arg1 is None:
        # si debo causar un error
        raise Exception("Mi error")

    mi_calculo = None

    # si debo retorar algo
    return mi_calculo



























import sys
sys.path.append("../src")
import redflagbpm

bpm=redflagbpm.BPMService()

# Leo los parámetros de configuración del mail en la BPM
env=bpm.service.env()

# Ejemplos de service

# Ejemplo: Notifico a un usuario
bpm.service.notifyUser("redflag","Hola","Estoy en pyhton3 remoto Liorén!")

#Ejemplo: me traigo código de la BPM
json_especies=bpm.service.code("GARCPD/ESPECIES_MAV")
print(json_especies)

#Ejemplo: me traigo parámetros
token=bpm.service.text("TOKEN_WS")
print(token)

#Ejemplo: ejecuto un VTL
vtl=bpm.service.execute("GARCPD/TEMPLATE",{})
print(vtl)

import venv

# Ejemplos de context
# bpm.context.nombre="Liorén"
# bpm.context['nombre']="Liorén"

print(bpm.context.nombre)
print(bpm.context['nombre'])

variables = {'persona.tipoId': 'CUIT',
             'persona.id': '30-51841045-4',
             'persona.perfilInversor': 'INDEF/VENCIDO',
             'max_riesgo': 1000.0,
             'perfil_inv_actualizado': 'Agresivo',
             'modificar_perfil': True}

bpm.call_timeout=2

bpm.reply("Hola Liorén")
