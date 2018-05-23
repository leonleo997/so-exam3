
# Segundo Parcial  
**Nombre:** Yesid Leonardo López  
**Código:** A00056408  
**Correo:** yesid.lopez@correo.icesi.edu.co  
**URL repositorio:** https://github.com/leonleo997/so-exam3.git  

**Tabla de contenido**  
- [A. Implementación de un servicio Flask](#a-implementaci%C3%B3n-de-un-servicio-flask)
- [B. Implementación de pruebas unitarias](#b-implementaci%C3%B3n-de-pruebas-unitarias)
- [C. Integración continua](#c-integraci%C3%B3n-continua)

## Desarrollo Parcial  

Antes de iniciar el desarrollo del parcial, vemos que el examen tiene la siguiente estructura:
.  
├── `op_stats`  
│   ├── `app.py`  
│   ├── `__init__.py`  
│   └── `stats.py`  
├── `requirements_dev.txt`  
├── `requirements.txt`  
├── `scripts`  
│   └── `deploy.sh`  
├── `setup.py`  
├── `tests`  
│   ├── `__init__.py`  
│   └── `test_stats.py`  
└── `tox.ini`  

# A. Implementación de un servicio Flask  

En esta sección crearemos servicios para: conocer el consumo de la CPU, memoria RAM disponible, espacio disponible en disco. Para probar el funcionamiento del API usaremos Postman.  

Primero, escribimos en el archivo llamado [`stats.py`](https://github.com/leonleo997/so-exam3/blob/yesidlopez/exam3/op_stats/stats.py) la implementación de los servicios:  
```console
#stats.py  
import psutil

class Stats():
  @classmethod
  def get_cpu_percent(cls):
    cpu_percent = psutil.cpu_percent()
    return cpu_percent

  @classmethod
  def get_ram(cls):
    ram_available = psutil.virtual_memory()[2]
    return ram_available

  @classmethod
  def get_disk(cls):
    disk_available = 100-psutil.disk_usage('/')[3]
    return disk_available

```  
Ahora, en el archivo [`app.py`](https://github.com/leonleo997/so-exam3/blob/yesidlopez/exam3/op_stats/app.py) crearemos el API que se encargará de exponer los servicios de la anterior implementación:  
```console
#app.py 
from flask import Flask
import json
import sys
sys.path.append('/home/operativos/so-exam3')
from op_stats.stats import Stats

app = Flask(__name__)

@app.route("/CPU")
def CPU():
    return json.dumps({'Consumo de CPU: ':Stats.get_cpu_percent()})

@app.route("/RAM")
def RAM():
    return json.dumps({'RAM disponible: ':Stats.get_ram()})

@app.route("/DISK")
def DISK():
    return json.dumps({'Disco disponible: ':Stats.get_disk()})


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8080)

```  
Una vez tenemos la implementación, y el api, usamos Postman para consumir los servicios que exponemos en `app.py`. Para esto, escribimos la ip (se puede ver usando `ip a`) junto con el puerto que se definió en el archivo y el nombre del servicio. Levantamos el servicio usando  
```console
operativos@Centos7:~/so-exam3$ python3 app.py 
```
A continuación, se muestran las capturas de la aplicación postman de cada servicio:  
Servicio CPU  
![alt text](https://github.com/leonleo997/so-exam3/blob/yesidlopez/exam3/Images/POSTMAN_CPU.PNG)  
Servicio RAM  
![alt text](https://github.com/leonleo997/so-exam3/blob/yesidlopez/exam3/Images/POSTMAN_RAM.PNG)  
Servicio disco
![alt text](https://github.com/leonleo997/so-exam3/blob/yesidlopez/exam3/Images/POSTMAN_DISK.PNG)  

Vemos que se realizaron las peticiones correctamente:   
![alt text](https://github.com/leonleo997/so-exam3/blob/yesidlopez/exam3/Images/pyton%20services.PNG)  


# B. Implementación de pruebas unitarias  

En esta sección haremos la implementación de pruebas unitarias. Para esto, escribimos en el archivo [`test_stats.py`](https://github.com/leonleo997/so-exam3/blob/yesidlopez/exam3/tests/test_stats.py) la implementación de las pruebas.  

```console
#test_stats.py
import pytest
from op_stats.app import app
from op_stats.stats import Stats

@pytest.fixture
def client():
  client = app.test_client()
  return client

def test_get_cpu_percent(mocker, client):
  mocker.patch.object(Stats, 'get_cpu_percent', return_value=100)
  response = client.get('/CPU')
  assert response.data.decode('utf-8') == '{"Consumo de CPU: ": 100}'
  assert response.status_code == 200

def test_get_ram(mocker, client):
  mocker.patch.object(Stats, 'get_ram', return_value=10)
  response = client.get('/RAM')
  assert response.data.decode('utf-8') == '{"RAM disponible: ": 10}'
  assert response.status_code == 200

def test_get_disk(mocker, client):
  mocker.patch.object(Stats, 'get_disk', return_value=40)
  response = client.get('/DISK')
  assert response.data.decode('utf-8') == '{"Disco disponible: ": 40}'
  assert response.status_code == 200
```  
Posteriormente, ejecutamos el comando ``pytest -v`` para correr las pruebas. Obtendremos el siguiente resultado:  
![alt text](https://github.com/leonleo997/so-exam3/blob/yesidlopez/exam3/Images/runing_test.PNG)  

# C. Integración continua  

En esta sección haremos la integración continua. Para esto, escribimos lo siguiente en el archivo `tox.ini`  

```console
[tox]
envlist = pytest 

[testenv]
basepython = python3

[testenv:pytest]
deps =
  -rrequirements_dev.txt
commands =
  pytest

```  
Este archivo contiene el archivo de los paquetes necesarios y los comandos a ejecutar. Para ejecutarlo, escribimos el siguientes comando ``tox -e pytest`` para ejecutar las pruebas.  
Vemos el resultado de la ejecución en la siguiente imagen  
![alt text](https://github.com/leonleo997/so-exam3/blob/yesidlopez/exam3/Images/tox%20-e.PNG)  

Pasamos a escribir en el archivo `.travis.yml` el archivo de configuración para Travis (herramienta de integración continua).  
```console
sudo: false
language: python
notifications:
  email: false
python:
- '3.4'
install: pip install tox-travis
script: tox -e pytest
```  
En este encontramos que el lenguaje con el que se ejecutará será python en su veersión 3.4. También, encontramos que se debe instalar tox-travis. Finalmente, sale el comando que debe ejecutar, en este caso: `tox -e pytest`.

Al realizar un pull request al repositorio [so-exam3](https://github.com/ICESI-Training/so-exam3) se ejecutarán automaticamente las pruebas definidas en la sección B. Obtenemos el siguiente resultado en travis:  
![](https://github.com/leonleo997/so-exam3/blob/yesidlopez/exam3/Images/travis.PNG)  
![](https://github.com/leonleo997/so-exam3/blob/yesidlopez/exam3/Images/travis2.PNG)  
![](https://github.com/leonleo997/so-exam3/blob/yesidlopez/exam3/Images/PullRequest.PNG)

Lo anterior, muestra que las pruebas fueron exitosas. 

