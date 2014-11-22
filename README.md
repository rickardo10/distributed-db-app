# Introducción

Este repositorio contiene una aplicación que facilita la organización en delegación de tareas. Se busca integrar esta aplicación con una base de datos distribuida, en específico, un cluster de MongoDB. La está construida en el **web framework** CherryPy.

# Conocimientos previos

## CherryPy

CherryPy le permite a los desarrolladores construir aplicaciones web que aprovechan al 100% la programación en Python. Los resultados son menos código en menos tiempo.

## Características

Las características por la cual CherryPy fue elegido son:

* Es confiable.
* Es fácil de correr múltiples HTTP servers.
* Es un sistema plugin flexible.
* Herramientas incluidas para caching, encoding, sessions, autorización, contenido estático, entre otras.
* Corre en Python 2.5+, 3.1+, PyPy, Jython y Android.

# Ejecucción del código

Para correr el presente código es necesario contar con python 3.1+ y las librerías de python CherryPy y pytz. Después de instalar python 3.1+ y las librerías correspondientes se debe clonar el repositorio e ingresar al folder.

```
git clone https://github.com/rickardo10/distributed-db-app.git
cd distributed-db-app
```

Correr la aplicación de python `app.py`

```
python app.py
```

# Conclusiones

Con esta aplicación es posible probar bases de datos relacionales y no relacionales. El uso de python simplifica el objetivo ya que contiene librerías especializadas que no limita el uso de cualquier base de datos.
