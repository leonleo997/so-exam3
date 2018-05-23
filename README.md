# Segundo Parcial  
**Nombre:** Yesid Leonardo López  
**Código:** A00056408  
**Correo:** yesid.lopez@correo.icesi.edu.co  
**URL repositorio:** https://github.com/leonleo997/so-exam3.git  

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
