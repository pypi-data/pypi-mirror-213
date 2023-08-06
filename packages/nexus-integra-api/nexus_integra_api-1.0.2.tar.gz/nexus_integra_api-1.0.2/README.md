# nexus_integra_api
Este repositorio tiene como propósito reunir en una única libería todas las funciones necesarias para trabajar con la API de Nexus en Python.
En lugar de importar los archivos a la carpeta del proyecto cada vez que se usan puede instalarse la librería en la PATH de Python 

## Table of Contents

* [Instalación](#instalacion)
* [Uso](#uso)
* [Ejemplos](#ejemplos)
  * [Lectura de datos](#lectura)
  * [Subida de datos](#subida)
  * [Alarmas](#alarmas)
  * [Email Alerts](#email)
* [Contribuir](#contribuir)
* [Change Log](#changelog)
* [Contacto](#contacto)

## Instalación <a class="anchor" id="instalacion"></a>

Usa el package manager pip para instalar la librería. Puede instalarse de forma local o desde el repositorio de PyPi

```
pip install nexus_integra_api
```

## Uso <a class="anchor" id="uso"></a>
Para importar todo el contenido de la librería, una vez instalada hay que realizar el siguiente import:

    import nexus_api
Si únicamente se desea la clase en la que residen las funciones que trabajan con la API:

    from nexus_api import APINexus
Lo que otorga acceso a la clase APINexus en la que residen todas las funciones necesarias.

## Ejemplo de uso <a class="anchor" id="ejemplos"></a>

En primer lugar se especifican los parámetros de conexión y se crea el objeto Nexus, además de los imports necesarios
```
from nexus_api import APINexus
import pandas as pd
import datetime

API_Host = 'nexus-cdi-demo.globalomnium.com'  
API_Port = 56000 
NexusToken = 'xxxxxxxxxxxxxxxxx' 
version = 'v1'
logger = [objeto logger - puede ser None]
NX = APINexus.APINexus(API_Host, API_Port, NexusToken, version, logger)
```

### Lectura de datos <a class="anchor" id="lectura"></a>

### filter_installation


la funcion recibe como parametros la fecha ini, fecha fin, un df con los uid y
los nombres de las variables de la instalación y el filtro de texto aplicar (pueden ser varios)

Args:

- Datefrom (datetime)
- Dateto (datetime)
- columnas (dataframe): df con los metadatos de los tags de Nexus 
- uids: (optional) (list): lista de los uids de las variables deseadas. No puede usarse con filter_txt
- filter_txt (optional: list or str): lista de nombres de las variables deseadas. Si se deja en blanco o no se encuentran variables se devuelve toda la instalación. No puede usarse con uids
- resolucion (int): de 0 a 10 [ RES_30_SEC, RES_1_MIN, RES_15_MIN, RES_1_HOUR, RES_1_DAY, RES_1_MONTH, RES_1_YEAR, RES_5_MIN, RES_200_MIL, RES_500_MIL, RES_1_SEC ]
- fuente (int): [0 -->RAW, 1 -->STATS_PER_HOUR, 2 -->STATS_PER_DAY, 3 -->STATS_PER_MONTH, 4 -->TRANSIENT]

Returns:
- filtered_hist (dataframe). Dataframe con los campos [index, timeStamp, name, value, uid]

Ejemplo:

```
# Lectura de loe metadatos de todos los tags contenidos en la API (necesario)
datos = self.NX.callGetTags()
columnas = json_normalize(datos)

# Profundidad del análisis en fechas desde hoy
delta_days = 3
date_to = datetime.datetime.now()
date_from = date_to - datetime.timedelta(days=delta_days)

filtered_hist = NX.filter_installation(date_from, date_to, columnas, resolucion=4)
```
Si quisiéramos filtrar las variables por texto o uids:
```
# Por uids:
uids = ['abc1', 'abc2', ...]
filtered_hist = NX.filter_installation(date_from, date_to, columnas, uids=uids, resolucion=4)
# Por texto:
filtros = ['var1', 'var2', ...]
filtered_hist = NX.filter_installation(date_from, date_to, columnas, filter_txt=filtros, resolucion=4)
```

### filter_tagview

La funcion recibe como parametros la fecha ini, fecha fin, un df con los uid y
los nombres de las variables de la instalación y el filtro de texto aplicar (pueden ser varios)

Args:
- Datefrom (datetime)
- Dateto (datetime)
- columnas (dataframe)
- filter_txt (optional: list or str)
- resolucion (int): de 0 a 10 [ RES_30_SEC, RES_1_MIN, RES_15_MIN, RES_1_HOUR, RES_1_DAY, RES_1_MONTH, RES_1_YEAR, RES_5_MIN, RES_200_MIL, RES_500_MIL, RES_1_SEC ]
- fuente (int): [0 -->RAW, 1 -->STATS_PER_HOUR, 2 -->STATS_PER_DAY, 3 -->STATS_PER_MONTH, 4 -->TRANSIENT]

Returns:
- filtered_hist (dataframe). Dataframe con los campos [index, timeStamp, name, value, uid]

Exactamente igual que la anterior pero aplicable a vistas de variables (recomendado)

Primero hay que especificar el uid de la vista de variables deseada. Puede obtenerse desde Nexus o obtenerse a través de métodos de la API
```
# Leer vistas de variables asociadas al token  
tagviews = NX.callGetDocuments()  
tagviews = json_normalize(tagviews)  
# Busqueda del uid de la vista
uid_tagview = tagviews.uid[0]
```
Se especifica la ventana temporal deseada:
```
# Profundidad del análisis en fechas desde hoy  
delta_days = xxx  
date_format = '%m/%d/%Y %H:%M:%S %Z'  
date_to = datetime.datetime.now()  
date_from = date_to - datetime.timedelta(days=delta_days)
```
Hay que especificar las variables deseadas de la vista de variables elegida. Con este código se obtienen todos los uids de las variables de la vista.
```
# Variables en la vista de variables  
vbles = NX.callGetTagViews(uid_tagview)  
df = pd.DataFrame(vbles)  
columnas = df['columns']  
columnas = json_normalize(columnas)  
```
Finalmente se obtiene el histórico llamando a la función:
```
filtered_hist = NX.filter_tagview(date_from, date_to, columnas, uid_tagview)
```
También puede filtrarse por texto o uid dentro de la vista
```
# Por uids:
uids = ['abc1', 'abc2', ...]
filtered_hist = NX.filter_tagview(date_from, date_to, columnas, uid_vista, uids=uids, resolucion=4)
# Por texto:
filtros = ['var1', 'var2', ...]
filtered_hist = NX.filter_tagview(date_from, date_to, columnas, uid_vista, filter_txt=filtros, resolucion=4)
```


### Subida de datos <a class="anchor" id="subida"></a>

Los datos que se suban a través de la API se encontrarán en la instalación habilitada para el token.

En primer lugar hay que asegurarse de crear las variables necesarias. Este paso puede omitirse si ya han sido creadas:

### callPostTagInsert
Consulta de tags con permisos de escritura. Si la variable no existe se crea

Args:
- variable_name(str): nombre de la variable a consultar o crear

### callPostValueHist

Función de escritura de variables en histórico.

Args:
- df_value_timestamp: dataframe con las variables y sus valores y timestamp

Ejemplo:

Una vez creadas las variables, pueden insertarse datos tanto en histórico como en tiempo real.
**Importante**: para subir los datos se requiere un dataframe con la siguiente estructura:

| timeStamp      	| name      	| value          	|
|----------------	|-----------	|----------------	|
| epoch time (s) 	| variable1 	| valor numérico 	|
| epoch time (s) 	| variable2 	| valor numérico 	|

```
test_df = pd.DataFrame({'timeStamp': [time.time()], 'name': ['api_test'], 'value': [1]})
NX.callPostValueHist(test_df)
```

El método acepta datetime64[ns] pero se recomienda pasar primero a epoch time. Para pasar de fecha en datetime a epoch se puede usar:
```
df['timeStamp'] = df['timeStamp'].apply(lambda x: x.timestamp())
```

### callPostValueRTmult
Escritura de variable en tiempo real.

Args:
- df_variable_name_value: dataframe con las variables y valores a escribir

Ejemplo:
```
test_df = pd.DataFrame({'timeStamp': [time.time()], 'name': ['api_test'], 'value': [1]})
NX.callPostValueRTmult(test_df)
```
Realmente la columna timeStamp no es necesaria en este caso, pero se recomienda mantener la estructura común al resto de métodos

### callPostValue_operate(self, variable_uid, variable_value)
Escritura de variable sobre PLC

Args:
- variable_uid: nombre de la variable a escribir en el PLC
- variable_value: valor de la variable a escribir

### Uso de alarmas <a class="anchor" id="alarmas"></a>
Desde la versión **0.4** del encapsulado pueden modificarse alarmas en la API. Para ello se debe obtener el uid de la alarma a modificar y luego llamar a la función:
#### Obtener uids de alarmas del token
```
alarmas = NX.callGetAlarms()
```

#### Obtener información de alarma por uid
```
alarma = NX.callGetAlarmByuid(uid)
```

#### Obtener uids de alarmas por nombres. Puede usarse una lista de nombres o un string con un nombre
```
uids_alarmas = NX.get_alarms_uids_by_names([names])
```
#### Obtener uids de alarmas por grupos de alarmas. Puede usarse una lista de grupos o un string con un grupo
```
uids_grupo = NX.get_alarms_uids_by_groups([groups])
```

#### Cambiar el estado de la alarma. Debe especificarse el uid de la alarma y el estado a cambiar ('ARE' o 'EXR')
```
NX.callPostAckAlarm(uid, estado)
```

#### Cambiar el mensaje de estado de la alarma
```
NX.callPostAlarmEvent(uid, msg)
```

### Email Alerts <a class="anchor" id="email"></a>
Desde la versión **0.5** se añade soporte para generar alarmas de correo eléctronico.

Para usar la función debe crearse un objeto de tipo EmailAlerts. Deben proporcionarse los parámetros de conexión.
```
class EmailAlerts:
    """
    Email management
    Attributes:
        attachments: list of files to add to message. See add_attachment for individual files
        environment: name of the environment (used to identify application)
        message: email's body
        subject: email's subject
        smtp_address: configuration parameter
        email_password: password
        email_port: port of server
        email_sender: snder address
        email_receiver: receiver address
        cooldown (optional): time in hours to wait between two emails
    """
```
Se recomienda usar variables de entorno para proteger las credenciales. En caso de no estar definidas se deben especificar (reemplazar las líneas de os.getenv()):

```
import os

smtp_address = 'outlook.office365.com'
smtp_port = 587
# Tiempo en horas entre envíos sucesivos
cooldown = 1

# datos de la cuenta de envio
sender_email_address = os.getenv("SENDER_EMAIL_ADDRESS")
email_password = os.getenv("EMAIL_PASSWORD")
receiver_email_address = os.getenv("RECEIVER_EMAIL_ADDRESS")

email_alerts = EmailAlerts(smtp_address, smtp_port, sender_email_address, email_password, receiver_email_address, cooldown=cooldown)
```

Una vez creado el objeto email_alerts puede usarse con libertad, bien con los parámetros predeterminados o moficiando los componentes del mensaje

El asunto y el cuerpo del mensaje tienen valores predeterminados en función del nombre del archivo, pero environment es una variable requerida con la que identificar el entorno de producción.
```
enviroment = 'NEXUS_PROD'
subject = 'ALARMA'
body = 'Alarma de ' + environment

email_alerts.set_email_alert_info(subject, body, environment)
```


Se puede usar la alerta de correo en cualquier función, sea de la API o no. Si la ejecución falla, 
se captura la excepción y se envía un correo con el error (mensaje predeterminado).

Si se quiere incorporar a un script entero, debe usarse la función main()

```
# Uso del decorador para generar el correo

@email_alerts.email_alert_decorator
def main():
    # Aquí va todo el código del programa...
    raise Exception('Error en la función')
    
if __name__ == '__main__':
    main() # Si aparece un error, se envía un correo con el error
```

## Contribuir <a class="anchor" id="contribuir"></a>

Cualquier función o sugerencia añadida es bien recibida.

Sugerencias:

- Traducir documentación

## Change log <a class="anchor" id="changelog"></a>

###v0.9.0 - 15/02/2023
**Added**
- Operate method to write directly into PLC variables
- NexusAPI custom exception
- logging options

###v0.8.0 - 04/11/2022
**Added**
- Support for cooldown options in email_alerts: pass time in hours as cooldown parameter in EmailAlerts
class to avoid sending more than 1 email in a given time

###v0.7.0 - 20/09/2022
**Important**
This update changes data structure of filter_tagview and filter_installation response. Please check your code before updating


**Added**
  - filter_tagview and filter_installation search by uid support
  - filter_tagview and filter_installation match structure (index, uid, name, value, timeStamp (datetime))

**Fix**
  - Now filter_installation and filter_tagview will raise an error if API response is not valid

**Updated**
  - Better docs

###v0.6.2 - 09/09/2022
**Updated**
- Better docs

**Fix**
- Now filter_installation/tagview raises an exception if dataframe structure is not correct

###v0.6.0 - 10/05/2022
**Added**
- Email attachments

###v0.5.0 - 12/04/2022

**Added**

 - Email alerts functions

**Changed**

 - Documentation

###v0.4.0 - 30/03/2022

**Added**
  
- API V2 alarm functions
  * callPostAckAlarm(uid, status)
  * callPostAlarmEvent(uid, msg)
  * callGetAlarms()
  * callGetAlarmByuid(uid)
  * get_alarms_uids_by_names([names])
  * get_alarms_uids_by_groups([groups])
- Unit tests
- .env file in order protect credentials
- Bypassed 50k row limit in POST methods
- Added support to datetime objects in callPostValueHist
  
**Modified**
  
- Unified callPostValueHist and callPostValueHistmult (deprecated)
  
###v0.3.2 - 11/03/2022
**Added**
- Add filter_installation and filter_tagview as replacement for GetFiltered
- Add README.md

## Contacto <a class="anchor" id="chapter6"></a>
[**Pau Juan**](mailto:pau.juan@nexusintegra.io)
*Operaciones*


[**Laura Moreno**](mailto:laura.moreno@nexusintegra.io)
*Operaciones*


[**Ricardo Gómez**](mailto:ricardo.gomez.aldaravi@nexusintegra.io)
*Operaciones*

[Nexus Integra](https://nexusintegra.io/)
