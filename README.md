# Dulcer-aLilis_BSM_FRR_Backend

El proyecto consiste en el desarrollo de un sistema de gestión de datos para la Dulcería Lilis. Este sistema permitirá la manipulación completa de la información relativa a usuarios, productos y proveedores mediante operaciones CRUD (Crear, Leer, Actualizar y Eliminar).

# 🧁 Dulcería Lili's - Sistema de Gestión

Este proyecto es un sistema web desarrollado con **Django**, diseñado para gestionar usuarios, productos y pedidos de la Dulcería Lili's.  
Permite registrar, editar y eliminar datos de usuarios, además de administrar pedidos de forma sencilla y segura.

---

## 🚀 Requisitos previos

Asegúrate de tener instalados los siguientes componentes:

- Python 3.10 o superior  
- Django 5.1  
- MySQL o SQLite (según configuración)  
- pip (gestor de paquetes de Python)  
- Git  
- (Opcional para producción) Nginx + Gunicorn + AWS Ubuntu Server 22.04
- Base de Datos creada (Concuerde con el nombre de la base de datos en Settings.py)

---

## 🛠️ Instalación local

1. **Clonar el repositorio:**   
   https://github.com/Fabithelast25/DulceriaLilis_BSM_FRR_Backend.git
   cd DulceriaLilis_BSM_FRR_Backend
2. **Instalacion de requerimientos:**
   pip install -r requirements.txt
3. **Migracion de los modelos:**
   py manage.py makemigrations
   py manage.py migrate
4. **Iniciar Proyecto:**
   py manage.py runserver


## Credenciales (Funcionales en la instancia AWS)
user: benjitasilvamarquez2013@gmail.com
password: hola1234

***(Aun no se implementa un superusuario creado automaticamente al migrar el proyecto, para crear un usuario se tendra que quitar el login protegido del usuarioAdd y rolAdd)***
   
   

