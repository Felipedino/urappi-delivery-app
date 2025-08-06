# 2025-1-CC4401-grupo-14

Proyecto del curso CC4401 - Universidad de Chile  
**Año:** 2025-1  
**Grupo:** 14

---

## Tabla de Contenidos

- [2025-1-CC4401-grupo-14](#2025-1-cc4401-grupo-14)
  - [Tabla de Contenidos](#tabla-de-contenidos)
  - [Descripción](#descripción)
  - [Instalación y Configuración](#instalación-y-configuración)
    - [1. Clonar el repositorio](#1-clonar-el-repositorio)
    - [2. Crear y activar entorno virtual](#2-crear-y-activar-entorno-virtual)
      - [En Windows:](#en-windows)
      - [En Linux/Max:](#en-linuxmax)
    - [3. Instalar dependencias](#3-instalar-dependencias)
    - [4. Instalar Tailwind CSS](#4-instalar-tailwind-css)
    - [5. Migrar la base de datos](#5-migrar-la-base-de-datos)
  - [Uso del Proyecto](#uso-del-proyecto)
    - [1. Compilar Tailwind CSS](#1-compilar-tailwind-css)
    - [2. Levantar el servidor de desarrollo](#2-levantar-el-servidor-de-desarrollo)
    - [3. Acceder a la aplicación](#3-acceder-a-la-aplicación)
  - [Tecnologías Utilizadas](#tecnologías-utilizadas)
  - [Notas sobre Tailwind CSS, daisyUI y de Estructura](#notas-sobre-tailwind-css-daisyui-y-de-estructura)
  - [Buenas Prácticas](#buenas-prácticas)

---


## Descripción

Este proyecto corresponde a una aplicación web desarrollada en Django, que utiliza Tailwind CSS 4 y daisyUI 5 para el diseño de la interfaz. El objetivo es servir como base para el desarrollo modular de aplicaciones web en el contexto del curso CC4401 Ingeniería de Software DCC-UChile. Incluye gestión de usuarios multi-rol, carrito multi-tienda, sistema de UPuntos (moneda virtual) y tracking de pedidos en tiempo real.


## Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/DCC-CC4401/2025-1-CC4401-grupo-14.git
cd 2025-1-CC4401-grupo-14
```

### 2. Crear y activar entorno virtual

`python -m venv venv`
#### En Windows:
`venv\Scripts\activate`
#### En Linux/Max:
`source venv/bin/activate`

### 3. Instalar dependencias
`python -m pip install --upgrade pip`

`pip install -r requirements.txt`

### 4. Instalar Tailwind CSS
Descarga el binario de Tailwind CSS ejecutando en PowerShell:

`Invoke-WebRequest -Uri "https://github.com/tailwindlabs/tailwindcss/releases/download/v4.1.4/tailwindcss-windows-x64.exe" -OutFile "urappi/static/urappi/tailwindcss.exe"`

### 5. Migrar la base de datos
`python manage.py migrate`

---

## Uso del Proyecto

### 1. Compilar Tailwind CSS

En una terminal, ejecuta:
`.\start-tailwind.bat`

O también sirve:
`cd urappi\static\urappi`

`.\tailwindcss.exe -i input.css -o output.css --watch`

Esto generará el CSS necesario a partir de los archivos fuente.

### 2. Levantar el servidor de desarrollo

En otra terminal, ejecuta:

`python manage.py runserver`


### 3. Acceder a la aplicación
Abre tu navegador y entra a http://localhost:8000

### 4. Ingresar como administrador (Opcional)
Ingresa a http://localhost:8000/admin y utiliza los credenciales admin:amongas123

---

## Tecnologías Utilizadas

- Python 3
- Django 5.2
- Tailwind CSS 4
- daisyUI 5
- HTML5 / CSS3
- VS Code (recomendado)

---

## Notas sobre Tailwind CSS, daisyUI y de Estructura

- El archivo `urappi/static/urappi/input.css` importa Tailwind y daisyUI.
- Los archivos estáticos y CSS personalizados están en `urappi/static/urappi/`.
- No subir archivo tailwindcss.exe, el tamaño excede el permitido en GitHub. (está en .gitignore)
- Para más información sobre daisyUI 5: daisyui.com
- Las carpetas `urappiapp/` y `home/` son aplicaciones Django.
- Los templates HTML están en las carpetas `templates/` de cada app.


---

## Buenas Prácticas

- Extiende siempre de base.html para mantener coherencia visual.
- Si agregas nuevas apps, recuerda incluirlas en `INSTALLED_APPS` en `settings.py`.
