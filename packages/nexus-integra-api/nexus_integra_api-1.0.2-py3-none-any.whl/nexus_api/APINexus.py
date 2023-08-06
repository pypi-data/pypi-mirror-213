"""
APINexus
Class definition
"""
from __future__ import annotations

import datetime
import json

import pandas
import pandas as pd
import requests
import urllib3
from pandas import json_normalize
from nexus_api.NexusRequest import NexusRequest
from nexus_api.NexusValue import NexusValue
from nexus_api.exceptions import VoidDataframeException, CorruptDataframeException, NexusAPIException
import warnings


def WarningsAndJson(func):
    """Decorator including InsecureRequestWarning and then JSON() format"""

    def f(*args, **kwargs):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        rv = func(*args, **kwargs)
        if rv.status_code == 200:
            return rv.json()
        else:
            raise NexusAPIException(rv)

    return f


def no_row_limit_decorator(fnc):
    """Decorator to remove row limit in post methods"""

    def wrapper(*args, **kwargs):
        NX = args[0]
        df_nexus = args[1]
        n = len(df_nexus)
        if n > 49999:
            iter = round(n / 49999)
            for j in range(iter):
                ini = j * 49999
                fin = (j + 1) * 49999
                if fin < n:
                    df_nexus_write = df_nexus[ini:fin]
                else:
                    df_nexus_write = df_nexus[ini:n]
                response = fnc(NX, df_nexus_write)
        else:
            response = fnc(NX, df_nexus)
        return response

    return wrapper


class APINexus:
    def __init__(self, IP_Maquina="localhost", Puerto=56000, token="", version="1.0", logger=None):
        """
        Metodo de inicialización de la clase. Aquí se define la IP y el puerto al que hemos de conectar así como el token

        Args:
            IP_Maquina (str): url de nexus
            Puerto (int): puerto de la API. 56000 de forma predeterminada
            token (str): token de la API
            version (str): 1.0, 2.0 or 3.0
        """
        self.IP_Maquina = IP_Maquina
        self.Puerto = str(Puerto)
        self.token = token
        self.version = version
        self._version_number = float(version)
        self.url_NX = "http://" + IP_Maquina + ":" + str(Puerto)
        self.header = {
            "nexustoken": self.token,
            "nexusapiversion": self.version,
            "Content-Type": "application/json",
        }
        self.logger = logger
        self.log_print("Creada nueva instancia de tipo NEXUS API")

    def log_print(self, message, severity='info'):
        if self.logger is not None:
            if severity == 'info':
                self.logger.info(message)
            elif severity == 'error':
                self.logger.error(message)
            elif severity == 'debug':
                self.logger.debug(message)
            else:
                raise ValueError('Severity not supported')
        else:
            print(message)

    def __json_normalize_check(self, response) -> pd.DataFrame:
        """
        Intenta convertir a DataFrame la respuesta en json de la API. Si no es posible, es que ha habido un fallo (la respuesta no sigue el formato establecido)
        Args:
            response: json con valor de la llamada a NexusAPI
        """
        try:
            return json_normalize(response)
        except Exception as e:
            self.log_print(f'Error de comunicación en NexusAPI. Motivo: {e}')
            raise NexusAPIException(response)

    def statusConnection(self, url_completa):
        """COD respuesta de la API"""
        resp = requests.get(url_completa, headers=self.header)
        return resp.status_code

    @WarningsAndJson
    def __getResponse(self, url):
        """GET method using Request"""
        return requests.get(url, verify=False, headers=self.header)

    @WarningsAndJson
    def __postResponse(self, url, body):
        """POST method using Request"""
        return requests.post(url, verify=False, headers=self.header, data=body)

    def callGetDocuments(self):
        """Lectura de vistas compartidas con el mismo token"""
        url_completa = self.url_NX + "/api/Documents"
        return self.__getResponse(url_completa)

    def callGetTagViews(self, uid: str):
        """Lectura de variables contenidas en una vista. Como parametros recibe unicamente el uid de la vista que queremos leer ya que el token , la IP y el puerto ya se han definido en la instanciacion de la clase"""
        url = self.url_NX + "/api/Documents/tagviews/" + uid
        return self.__getResponse(url)

    def callGetTagViewsRealTime(self, uid: str, uids_vbles: list):
        """Lectura de variables de una vista. Devuelve el valor en tiempo real de las variables establecidas en el array uids, contenidas en la vista uid """
        body = json.dumps(uids_vbles)
        url = self.url_NX + "/api/Documents/tagviews/" + uid + "/realtime"
        return self.__postResponse(url, body)

    def callGetDataviewHistory(self, uid: str, nexusRequest: NexusRequest):
        """Lectura de valores historicos de variables"""
        body = json.dumps(
            nexusRequest, default=lambda o: o.__dict__, sort_keys=True, indent=2
        )
        url = self.url_NX + "/api/Documents/tagviews/" + uid + "/historic"
        return self.__postResponse(url, body)

    def callGetDataview_History(self, uid, uids, StartTs, EndTs, dataSource, resolution):
        """Lectura de valores historicos de variables a partir de los parámetros pasados a la funcion
        StartTS como timestamp y EndTs como timestamp"""
        body = json.dumps(
            {"uids": uids, "startTs": StartTs, "endTs": EndTs, "dataSource": dataSource, "resolution": resolution})

        url = self.url_NX + "/api/Documents/tagviews/" + uid + "/historic"
        return self.__postResponse(url, body)

    def callGetTagsWritable(self):
        """Metodo de consultas de tags escribibles"""
        url = self.url_NX + "/api/Tags/writable"
        return self.__getResponse(url)

    def callGetTags(self):
        """Método de consulta de tags de la instalación"""
        url = self.url_NX + "/api/Tags"
        return self.__getResponse(url)

    def callGetTags_Attributes(self):
        """Método de consulta de los atributos de los tags de la instalación"""
        if self._version_number < 3:
            raise NotImplementedError('Nexus API version must be greater than 3.0')
        url = self.url_NX + "/api/Tags/Attributes"
        return self.__getResponse(url)

    def callGetTagswithAtt(self, bool_att=True):
        """Método de consulta de tags de la instalación
        Se incluye el parámetro bool_att que permite mostrar o no los
        attributos a partir de la versión V3.0
        """
        if self._version_number < 3:
            raise NotImplementedError('Nexus API version must be greater than 3.0')
        url = self.url_NX + "/api/Tags?IncludeAttributes=" + str(bool_att)

        return self.__getResponse(url)

    def callGetTagsRealTime(self, uids_vbles):
        """Devuelve valor RT de los tags de la instalacion definidos en un array UIDS_VBLES"""
        body = json.dumps(uids_vbles)
        url = self.url_NX + "/api/Tags/realtime"
        return self.__postResponse(url, body)

    def callGetTagsHistory(self, nexusRequest):
        """Deprecated. Devuelve valor historico de los tags especificados en la estructura NexusRequest"""
        body = json.dumps(nexusRequest, default=lambda o: o.__dict__, sort_keys=True, indent=2)
        url = self.url_NX + "/api/Tags/historic"
        return self.__postResponse(url, body)

    def callGetTags_History(self, uids, StartTs, EndTs, dataSource, resolution, aggOperation="LAST_VALUE"):
        """Devuelve valor historico de los tags especificados en los parametros, añade el parámetro aggOperation"""
        if self._version_number < 3:
            raise NotImplementedError('Nexus API version must be greater than 3.0')
        if len(uids) > 100:
            raise AttributeError('Too many tags. Please set the number of tags less or equal than 100')
        body = json.dumps(
            {"uids": uids, "startTs": StartTs, "endTs": EndTs, "dataSource": dataSource, "resolution": resolution,
             "aggOperation": aggOperation})
        url = self.url_NX + "/api/Tags/historic"
        return self.__postResponse(url, body)

    def callGetTags_rawHistory(self, uids, StartTs, EndTs):
        """Devuelve valor historico de los tags especificados en los parametros devolviendo solo los valores raw"""
        if self._version_number < 3:
            raise NotImplementedError('Nexus API version must be greater than 3.0')
        body = json.dumps({"uids": uids, "startTs": StartTs, "endTs": EndTs})
        url = self.url_NX + "/api/Tags/rawhistoric"

        return self.__postResponse(url, body)

    def callGetAPITags_Filtered(self, installations: list = None, drivers: list = None, tags: list = None,
                                attributes: list = None):
        """Busca tags disponibles en el token filtrando por distintos elementos
        Args:
            installations:
            drivers:
            tags:
            attributes (not implemented yet)
            """
        if self._version_number < 3:
            raise NotImplementedError('Nexus API version must be greater than 3.0')
        # TODO: El metodo original permitirá filtrar por atributos pero como se desconoce como hacerlo y estamos en depuración de momento dejo solo estas tres opciones
        args = locals()
        for _, arg in args.items():
            if arg is None:
                arg = []
        body = json.dumps(
            {"SearchByInstallationName": installations, "SearchByDriverName": drivers, "SeachByTagName": tags})
        url = self.url_NX + "/api/Tags/filtered"

        return self.__postResponse(url, body)

    def callPostTags_InsertorUpdate(self, NameofTag, nameofattribute1="", valueofattribute1="", nameofattribute2="",
                                    valueofattribute2="", nameofattribute3="", valueofattribute3=""):
        """Permite actualizar un tag o crearlo con atributos, se permiten 3 atributos en pack de nombre de atributo + valor de attributo
        """
        if self._version_number < 3:
            raise NotImplementedError('Nexus API version must be greater than 3.0')
        body = json.dumps([{"Name": NameofTag, "Attributes": [
            {"attributeName": nameofattribute1,
             "value": valueofattribute1
             },
            {"attributeName": nameofattribute2,
             "value": valueofattribute2
             },
            {"attributeName": nameofattribute3,
             "value": valueofattribute3
             }
        ]
                            }
                           ])

        url = self.url_NX + "/api/Tags/InsertOrUpdate"
        return self.__postResponse(url, body)

    # TODO: Eliminar el header personalizado de alarmas cuando la versión de la API sea acumulativa
    @WarningsAndJson
    def callGetAlarms(self):
        """Lectura de alarmas compartidas con el mismo token"""
        if self._version_number < 2:
            raise NotImplementedError('Version 1.0 does not support alarm methods')
        url_completa = self.url_NX + "/api/Alarms"
        return requests.get(url_completa, verify=False, headers=self.header)

    @WarningsAndJson
    def callGetAlarmByuid(self, uid):
        """Lectura de alarmas compartidas con el mismo token"""
        if self._version_number < 2:
            raise NotImplementedError('Version 1.0 does not support alarm methods')
        url_completa = self.url_NX + "/api/Alarms/alarm/" + uid
        return requests.get(url_completa, verify=False, headers=self.header)

    # @WarningsAndJson -- no se necesita ya que se requiere comparar el objeto response
    def callPostAckAlarm(self, uid, status: str):
        """Lectura de alarmas compartidas con el mismo token
        status: 'ARE' or 'EXR'
        """
        if self._version_number < 2:
            raise NotImplementedError('Version 1.0 does not support alarm methods')
        if status == 'ARE' or status == 'EXR':
            url_completa = self.url_NX + "/api/Alarms/alarm/" + uid + "/acknowledge"
            body = "\"" + status + "\""
            return requests.post(url_completa, verify=False, headers=self.header, data=body)
        else:
            raise ValueError("Status must be 'ARE' or 'EXR'")

    # @WarningsAndJson
    def callPostAlarmEvent(self, uid, msg: str):
        """
        Usado para insertar mensajes en el histórico de la alarma con uid específico
        args:
            uid: uid de la alarma
        """
        if self._version_number < 2:
            raise NotImplementedError('Version 1.0 does not support alarm methods')
        url_completa = self.url_NX + "/api/Alarms/alarm/" + uid + "/event"
        return requests.post(url_completa, verify=False, headers=self.header, json={'Message': msg})

    def get_writable_tags(self) -> pd.DataFrame:
        """
        Get all writable tags from token.
        Returns:
             data: dataframe with tag info. If version is v3, will also return attribute info
        """
        url_get = self.url_NX + "/api/Tags/writable"
        variables = self.__getResponse(url_get)
        data = self.__json_normalize_check(variables)
        return data

    def callPostTagInsert(self, variables: str | list[str]) -> pd.DataFrame | None:
        """
        Check if provided tag names exist, then create them if not
        Args:
            variables (str or list): variable name or names to be created
        Returns:
            response: Dataframe of Nexus info for tags created
            """
        # Crear variables que no existen:
        # 1. Si se ha proporcionado un str, pasar a lista
        if isinstance(variables, str):
            variables = [variables]
        body = json.dumps(variables)
        self.log_print(f'Tags to be created: {body}')
        url_post = self.url_NX + "/api/Tags/Insert"
        self.log_print(url_post)
        return self.__postResponse(url_post, body)

    def get_rt_data_tagview(self, uid_tagview: str = None, filters=None):
        """
        Gets the real time data from Nexus.
        Args:
            NX: Nexus object
            uid_tagview: uid of the tagview. If None, it will select the first one from the token
            filters: name of the variables to filter. If None, it will select all the variables
        Returns:
            df: dataframe with the data
        """
        if uid_tagview is None:
            tagviews = self.callGetDocuments()
            tagviews = self.__json_normalize_check(tagviews)
            uid_tagview = tagviews.uid[0]
        vbles = pd.DataFrame(self.callGetTagViews(uid_tagview))['columns']
        vbles = self.__json_normalize_check(vbles)
        if filters is None:
            uids = vbles['uid'].to_list()
        else:
            filters = [filters] if isinstance(filters, str) else filters
            uids = vbles[vbles.name.isin(filters)].uid.to_list()
        # Read RT values from tagview
        data = self.__json_normalize_check(self.callGetTagViewsRealTime(uid_tagview, uids))
        diccio = dict([(i, j) for i, j in zip(vbles.uid, vbles.name)])
        data['timeStamp'] = pd.to_datetime(data['timeStamp'], unit='s')
        data['name'] = data['uid'].map(diccio)
        return data

    def callPostValueRT(self, variable_name, variable_value):
        """Escritura de variable en tiempo real.
        args:
            variable_name: nombre de la variable a escribir
            variable_value: valor de la variable a escribir
        """
        # La función comprueba primero si existe la variable en la que se quiere escribir
        url = self.url_NX + "/api/Tags/writable"
        # self.log_print(url_completa)
        variables = self.__getResponse(url)
        variables_norm = self.__json_normalize_check(variables)
        variables_names = list(variables_norm.name)

        # La función escribe en la variable
        if variable_name in variables_names:
            variable_uid = list(
                variables_norm[variables_norm.name == variable_name].uid
            )[0]
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            url_completa = self.url_NX + "/api/Tags/realtime/insert"
            nexusvalue = NexusValue(variable_uid, variable_value)
            payload = (
                    "["
                    + json.dumps(
                nexusvalue, default=lambda o: o.__dict__, sort_keys=False, indent=2
            )
                    + "]"
            )
            # self.log_print(payload)
            # payload= "[{\"uid\": \"" + variable_uid + "\",\"value\": " + str(variable_value) + ",\"timeStamp\": " + str(timestamp) + "}]"

            headers = {
                "nexustoken": self.token,
                "nexusapiversion": self.version,
                "Content-Type": "application/json",
            }
            response = requests.request(
                "POST", url_completa, headers=headers, data=payload
            )

            if response.status_code == 200:
                dataReceived = "Escritura correcta"
            else:
                dataReceived = (
                        "Se ha intentado escribir en la variable "
                        + variable_name
                        + " con uid "
                        + variable_uid
                        + " pero la operación ha fallado"
                )
                self.log_print(response.text.encode("utf8"))
        # Si no existe, devuelve un mensaje para que el usuario cree la variable deseada (no lo hace automático para evitar creación de variables por errores tipográficos
        else:
            dataReceived = "La variable en la que se ha solicitado escribir no existe. Por favor creela mediante la función callPostTagInsert"

        return dataReceived

    def callPostValue_operate_mult(self, df: pd.DataFrame):
        """Escritura de variable en tiempo real en PLC.
        Args:
            df: dataframe con los campos ['uid', 'value'] de las variables a escribir
        """

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        url_completa = self.url_NX + "/api/Tags/operate"
        df = df[['uid', 'value']]
        payload = df.to_json(orient='records')

        headers = {
            "nexustoken": self.token,
            "nexusapiversion": self.version,
            "Content-Type": "application/json",
        }
        response = requests.request(
            "POST", url_completa, headers=headers, data=payload
        )

        if response.status_code == 200:
            dataReceived = "Escritura correcta"
        else:
            dataReceived = response.content
        self.log_print(response.text.encode("utf8"))
        return dataReceived

    def callPostValue_operate(self, variable_uid, variable_value):
        """Escritura de variable en tiempo real.
        args:
            variable_uid: nombre de la variable a escribir en el PLC
            variable_value: valor de la variable a escribir
        """

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        url_completa = self.url_NX + "/api/Tags/operate"
        nexusvalue = NexusValue(variable_uid, variable_value)
        payload = (
                "["
                + json.dumps(
            nexusvalue, default=lambda o: o.__dict__, sort_keys=False, indent=2
        )
                + "]"
        )

        headers = {
            "nexustoken": self.token,
            "nexusapiversion": self.version,
            "Content-Type": "application/json",
        }
        response = requests.request(
            "POST", url_completa, headers=headers, data=payload
        )

        if response.status_code == 200:
            dataReceived = "Escritura correcta"
        else:
            dataReceived = (
                    "Se ha intentado escribir en la variable "
                    + " con uid "
                    + variable_uid
                    + " pero la operación ha fallado"
            )
        self.log_print(response.text.encode("utf8"))
        # Si no existe, devuelve un mensaje para que el usuario cree la variable deseada (no lo hace automático para evitar creación de variables por errores tipográficos

        return dataReceived

    @no_row_limit_decorator
    def callPostValueHist(self, df_value_timestamp):
        """Función de escritura de variable para diferentes historicos.
        args:
            df_value_timestamp: dataframe con las variables y sus valores y timestamp
        """
        # la funcion mira cuantas variables diferentes contiene el dataframe y comprueba si todas ellas existen
        vbles = list(df_value_timestamp.name.unique())
        n = len(vbles)
        self.log_print('se intenta escribir en ' + str(n) + ' variables')
        # La función comprueba primero si existe la variable en la que se quiere escribir
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        url_completa = self.url_NX + "/api/Tags/writable"
        response = requests.get(url_completa, verify=False, headers=self.header)
        variables = response.json()
        variables_pd = pandas.DataFrame(variables)
        variables_norm = self.__json_normalize_check(variables)
        diccio = dict([(i, j) for i, j in zip(variables_pd.name, variables_pd.uid)])

        variables_names = list(variables_norm.name)
        NOK = 0
        for j in vbles:
            if j not in variables_names:
                NOK = 1
                self.log_print('la variable ' + str(j) + 'no esta creada ')

        if NOK == 0:
            df2 = df_value_timestamp.copy()
            df2['uid'] = df2['name'].map(diccio)

            df2.drop(columns=["name"], inplace=True)
            if df2['timeStamp'].dtype == 'datetime64[ns]':
                warnings.warn('timeStamp in datetime format: please check that it is in UTC')
                df2['timeStamp'] = df2['timeStamp'].astype('int64') / 1e9
            self.log_print(str(df2))
            payload = pandas.DataFrame.to_json(
                df2, date_format="epoch", orient="records"
            )
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            url_completa = self.url_NX + "/api/Tags/historic/insert"
            headers = {
                "nexustoken": self.token,
                "nexusapiversion": self.version,
                "Content-Type": "application/json",
            }
            response = requests.request(
                "POST", url_completa, headers=headers, data=payload
            )

            if response.status_code == 200:
                dataReceived = "Escritura correcta"
            else:
                dataReceived = (
                        "Se ha intentado escribir en la variable "
                        + " pero la operación ha fallado" + str(response.status_code)
                )
                self.log_print(response.text.encode("utf8"))
        # Si no existe, devuelve un mensaje para que el usuario cree la variable deseada (no lo hace automático para evitar creación de variables por errores tipográficos
        else:
            dataReceived = "La variable en la que se ha solicitado escribir no existe. Por favor creela mediante la función callPostTagInsert"
            payload = []

        return dataReceived, payload

    @no_row_limit_decorator
    def callPostValueHistmult(self, df_value_timestamp):
        """Deprecated. Use callPostValueHist instead.
        Función de escritura de variable para diferentes historicos.
        args:
            df_value_timestamp: dataframe con las variables y sus valores y timestamp
        """
        # la funcion mira cuantas variables diferentes contiene el dataframe y comprueba si todas ellas existen
        vbles = list(df_value_timestamp.name.unique())
        n = len(vbles)
        self.log_print('se intenta escribir en ' + str(n) + ' variables')
        # La función comprueba primero si existe la variable en la que se quiere escribir
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        url_completa = self.url_NX + "/api/Tags/writable"
        response = requests.get(url_completa, verify=False, headers=self.header)
        variables = response.json()
        variables_pd = pandas.DataFrame(variables)
        variables_norm = self.__json_normalize_check(variables)
        diccio = dict([(i, j) for i, j in zip(variables_pd.name, variables_pd.uid)])

        variables_names = list(variables_norm.name)
        NOK = 0
        for j in vbles:
            if j not in variables_names:
                NOK = 1
                self.log_print('la variable ' + str(j) + 'no esta creada ')

        if NOK == 0:
            df2 = df_value_timestamp.copy()
            df2['uid'] = df2['name'].map(diccio)

            df2.drop(columns=["name"], inplace=True)
            if df2['timeStamp'].dtype == 'datetime64[ns]':
                warnings.warn('timeStamp in datetime format: please check that it is in UTC')
                df2['timeStamp'] = df2['timeStamp'].astype('int64') / 1e9
            self.log_print(str(df2))
            payload = pandas.DataFrame.to_json(
                df2, date_format="epoch", orient="records"
            )
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            url_completa = self.url_NX + "/api/Tags/historic/insert"
            headers = {
                "nexustoken": self.token,
                "nexusapiversion": self.version,
                "Content-Type": "application/json",
            }
            response = requests.request(
                "POST", url_completa, headers=headers, data=payload
            )

            if response.status_code == 200:
                dataReceived = "Escritura correcta"
            else:
                dataReceived = (
                        "Se ha intentado escribir en la variable "
                        + " pero la operación ha fallado" + str(response.status_code)
                )
                self.log_print(response.text.encode("utf8"))
        # Si no existe, devuelve un mensaje para que el usuario cree la variable deseada (no lo hace automático para evitar creación de variables por errores tipográficos
        else:
            dataReceived = "La variable en la que se ha solicitado escribir no existe. Por favor creela mediante la función callPostTagInsert"
            payload = []

        return dataReceived, payload

    @no_row_limit_decorator
    def callPostValueRTmult(self, df_variable_name_value):
        """Escritura de variable en tiempo real.
        args:
            df_variable_name_value: dataframe con las variables y valores a escribir
        """
        vbles = list(df_variable_name_value.name.unique())
        n = len(vbles)
        # La función comprueba primero si existe la variable en la que se quiere escribir
        url = self.url_NX + "/api/Tags/writable"
        variables = self.__getResponse(url)
        variables_pd = pandas.DataFrame(variables)
        variables_norm = self.__json_normalize_check(variables)
        diccio = dict([(i, j) for i, j in zip(variables_pd.name, variables_pd.uid)])
        df2 = df_variable_name_value
        df2['uid'] = df2['name'].map(diccio)
        df2.drop(columns=["name"], inplace=True)
        payload = pandas.DataFrame.to_json(df2, date_format="epoch", orient="records")

        variables_names = list(variables_norm.name)
        NOK = 0
        for j in vbles:
            if j not in variables_names:
                NOK = 1
                self.log_print('la variable ' + str(j) + 'no esta creada')

        if NOK == 0:
            # La función escribe en la variable
            self.log_print('se actualiza el valor RT de ' + str(n) + ' vbles')
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            url_completa = self.url_NX + "/api/Tags/realtime/insert"
            headers = {
                "nexustoken": self.token,
                "nexusapiversion": self.version,
                "Content-Type": "application/json",
            }
            response = requests.request("POST", url_completa, headers=headers, data=payload)
            if response.status_code == 200:
                dataReceived = "Escritura correcta"
            else:
                dataReceived = (
                        "Se ha intentado escribir en la variable "
                        + " pero la operación ha fallado" + str(response.status_code)
                )
                self.log_print(response.text.encode("utf8"))

        return dataReceived

    def filter_installation(self, datefrom: datetime.datetime, dateto: datetime.datetime, columnas=None,
                            filter_txt=None, uids=None, resolucion=3,
                            fuente=0) -> pd.DataFrame:
        """
        la funcion recibe como parametros la fecha ini, fecha fin, un df con los uid y
        los nombres de las variables de la instalación y el filtro de texto aplicar
        Args:
            datefrom (datetime)
            dateto (datetime)
            columnas (dataframe): dataframe con la información de los tags a leer. Debe contener menos de 100 tags para versiones mayores a v3. Si no se proporciona, usa el de toda la instalacion
            uids: (optional) (list): lista de los uids de las variables deseadas. No puede usarse con filter_txt
            filter_txt (optional: list or str): lista de nombres de las variables deseadas. No puede usarse con uids
            resolucion (int): de 0 a 10 [ RES_30_SEC, RES_1_MIN, RES_15_MIN, RES_1_HOUR, RES_1_DAY, RES_1_MONTH, RES_1_YEAR, RES_5_MIN, RES_200_MIL, RES_500_MIL, RES_1_SEC ]
            fuente (int): [0 -->RAW, 1 -->STATS_PER_HOUR, 2 -->STATS_PER_DAY, 3 -->STATS_PER_MONTH, 4 -->TRANSIENT]
        Returns:
            filtered_hist (dataframe)
        """
        if uids is not None and filter_txt is not None:
            raise ValueError('Error en uids y filter_txt. No pueden usarse ambos parámetros de búsqueda')
        # Check parameters
        if columnas is None:
            datos = self.callGetTags()
            columnas = json_normalize(datos)
        if uids is None:
            uids = []
            if isinstance(filter_txt, list):
                for filter in filter_txt:
                    uids_loop = list(columnas[columnas['name'].str.contains(filter, case=False)].uid)
                    uids.extend(uids_loop)
            else:
                if filter_txt:
                    uids = list(columnas[columnas['name'].str.contains(filter_txt, case=False)].uid)
            if not uids:
                self.log_print(
                    'Los filtros proporcionados no encuentran ninguna variable. Se devolverá toda la instalación')
                uids = list(columnas.uid)
        # Remove duplicate UIDS
        uids = list(set(uids))
        fecha_ini = datefrom
        fecha_fin = dateto
        if self._version_number < 3:
            nexusRequest = NexusRequest(uids, fecha_ini, fecha_fin, fuente, resolucion)
            filtered_hist = self.callGetTagsHistory(nexusRequest)
        elif self._version_number >= 3:
            # Check that len is less than 100 tags
            n = len(uids)
            if n > 100:
                data = []
                iter = round(n / 100)
                for j in range(iter):
                    ini = j * 100
                    fin = (j + 1) * 100
                    if fin < n:
                        uids_cache = uids[ini:fin]
                    else:
                        uids_cache = uids[ini:]
                    cache = self.callGetTags_History(uids_cache, datefrom.timestamp(), dateto.timestamp(), fuente,
                                                     resolucion)
                    data.extend(cache)
                filtered_hist = data

            else:
                filtered_hist = self.callGetTags_History(uids, datefrom.timestamp(), dateto.timestamp(), fuente,
                                                         resolucion)
        else:
            raise AttributeError(f'Version provided not implemented {self.version}')
        filtered_hist = self.__json_normalize_check(filtered_hist)
        # Check that there is no error in the dataframe
        self.__check_response_error_df(filtered_hist)
        filtered_hist.timeStamp = pandas.to_datetime(filtered_hist.timeStamp, unit='s')
        diccio = dict([(i, j) for i, j in zip(columnas.uid, columnas.name)])
        filtered_hist['name'] = filtered_hist['uid'].map(diccio)
        return filtered_hist

    def filter_tagview(self, datefrom: datetime.datetime, dateto: datetime.datetime, columnas: pd.DataFrame,
                       uid_vista: str, filter_txt=None, uids=None, resolucion=3,
                       fuente=0) -> pd.DataFrame:
        """
        La funcion recibe como parametros la fecha ini, fecha fin, un df con los uid y
        los nombres de las variables de la instalación y el filtro de texto aplicar [pueden ser varios]
        Args:
            datefrom (datetime)
            dateto (datetime)
            columnas (dataframe): Dataframe con la informacion de las variables en la vista devuelto por callGetTagViews
            uid_vista: uid de la vista en la que se busca
            uids: (optional) (list): lista de los uids de las variables deseadas. No puede usarse con filter_txt
            filter_txt (optional: list or str): lista de nombres de las variables deseadas. No puede usarse con uids
            resolucion (int): de 0 a 10 [ RES_30_SEC, RES_1_MIN, RES_15_MIN, RES_1_HOUR, RES_1_DAY, RES_1_MONTH, RES_1_YEAR, RES_5_MIN, RES_200_MIL, RES_500_MIL, RES_1_SEC ]
            fuente (int): [0 -->RAW, 1 -->STATS_PER_HOUR, 2 -->STATS_PER_DAY, 3 -->STATS_PER_MONTH, 4 -->TRANSIENT]
        Returns:
            filtered_hist (dataframe)
        """
        # Check parameters
        if uids is not None and filter_txt is not None:
            raise ValueError('Error en uids y filter_txt. No pueden usarse ambos parámetros de búsqueda')
        if uids is None:
            uids = []
            if isinstance(filter_txt, list):
                for filter in filter_txt:
                    uids_loop = list(columnas[columnas['name'].str.contains(filter, case=False)].uid)
                    uids.extend(uids_loop)
            else:
                if filter_txt:
                    uids = list(columnas[columnas['name'].str.contains(filter_txt, case=False)].uid)
            if not uids:
                self.log_print(
                    'Los filtros proporcionados no encuentran ninguna variable. Se devolverá toda la instalación')
                uids = list(columnas.uid)
        # Remove duplicate UIDS
        uids = list(set(uids))
        fecha_ini = datefrom
        fecha_fin = dateto
        if self._version_number < 3:
            nexusRequest = NexusRequest(uids, fecha_ini, fecha_fin, fuente, resolucion)
            filtered_hist = self.callGetDataviewHistory(uid_vista, nexusRequest)
        elif self._version_number >= 3:
            filtered_hist = self.callGetDataview_History(uid_vista, uids, datefrom.timestamp(), dateto.timestamp(),
                                                         fuente, resolucion)
        else:
            raise AttributeError(f'Version provided not implemented {self.version}')
        filtered_hist = self.__json_normalize_check(filtered_hist)
        # Check dataframe for errors
        self.__check_response_error_df(filtered_hist)
        filtered_hist.timeStamp = pandas.to_datetime(filtered_hist.timeStamp, unit='s')
        diccio = dict([(i, j) for i, j in zip(columnas.uid, columnas.name)])
        filtered_hist['name'] = filtered_hist['uid'].map(diccio)
        return filtered_hist

    def get_alarms_uids_by_names(self, names):
        alarms = self.__json_normalize_check(self.callGetAlarms())
        names = [names] if isinstance(names, str) else names
        uids = alarms['uid'][alarms['name'].isin(names)]
        return uids

    def get_alarms_uids_by_groups(self, groups):
        alarms = self.__json_normalize_check(self.callGetAlarms())
        groups = [groups] if isinstance(groups, str) else groups
        uids = []
        for group in groups:
            uids.extend(alarms['uid'][alarms['groupName'].str.contains(group, case=False)].to_list())
        return uids

    @staticmethod
    def __check_response_error_df(filtered_hist: pd.DataFrame) -> None:
        """
        Checks the received dataframe from API request and raises an error if not valid
        """
        # Check that there is no error in the dataframe
        if 'StatusCode' in filtered_hist.keys():
            message = filtered_hist['Message']
            code = filtered_hist['StatusCode']
            ex_message = f'Status Code: {code}: {message}'
            raise ValueError(ex_message)
        # Check that dataframe is not empty
        elif filtered_hist.empty:
            raise VoidDataframeException
        # Check content
        elif not {'timeStamp', 'uid', 'value'}.issubset(filtered_hist.columns):
            raise CorruptDataframeException(filtered_hist)
        else:
            pass
