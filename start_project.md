# Instrucciones para crear un proyecto

Estas son los pasos que seguí para empezar el proyecto. Seguí los pasos de [este tutorial](https://tutorial.djangogirls.org/es/django_installation/).

## Inicilización del proyecto

- Crear un venv:

```
python -m venv venv
```

- Activar el venv en Windows:

```
venv\Scripts\activate
```

- actualizar pip:

```
python -m pip install --upgrade pip
```

- Instalar requirements (esto incluye django):

```
pip install -r requirements.txt
```

En los requirements dejé la misma versión de django que se usa en el aux, no la última.

- Empezar un proyecto con:

```
django-admin startproject urappi 2025-1-CC4401-grupo-14
```

Con esto se crea un proyecto de la forma:

```
2025-1-CC4401-grupo-14
├───venv
├───manage.py
├───urappi
│        settings.py
│        urls.py
│        wsgi.py
│        __init__.py
└───requirements.txt
```

## Configuraciones iniciales

Primero es necesario crear una base de datos, para ello se ejecuta:

```
python manage.py migrate
```

## Correr el servidor

- Para correr el servidor:

```
python manage.py runserver
```

## Crear una aplicación

En general los proyectos se trabajan modularmente, por ello se crea una aplicación donde se trabajará la página web.

- Crear una nueva aplicación:

```
python manage.py startapp urappiapp
```

Con esto se creó un nuevo directorio urappiapp.

Luego se debe modificar el archivo `settings.py` para agregar esta nueva app:

- Incluir `import urappiapp`.
- Incluir `urappiapp` dentro de la variable `INSTALLED_APPS`.
