# Segundo Parcial  
**Nombre:** Yesid Leonardo López  
**Código:** A00056408  
**Correo:** yesid.lopez@correo.icesi.edu.co  
**URL repositorio:** https://github.com/leonleo997/so-exam3.git  

## Desarrollo Parcial  

Antes de iniciar el desarrollo del parcial, crearemos un proyecto con la siguiente estructura:
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

Primero, en el archivo llamado [`stats.py`](https://github.com/leonleo997/so-exam3/blob/yesidlopez/exam3/op_stats/stats.py) que tendrá la implementación de los servicios:  
```console
#Stats.py  
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
Ahora, en el archivo app.py crearemos el API que se encargará de exponer los servicios de la anterior implementación
