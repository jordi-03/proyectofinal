Tienda Trenor en Línea con Flask

Este proyecto es una aplicación web desarrollada con **Flask**, que simula una tienda en línea. Permite a los usuarios registrarse, iniciar sesión, ver productos organizados por categorías, y administrar productos y categorías.

---

##Estructura del Proyecto
/proyectofinal/
│
├── app.py # Archivo principal de la aplicación Flask
├── instance/
│ └── trenor.db # Base de datos SQLite
├── static/
│ ├── imgs/ # Imágenes de productos
│ └── style.css # Estilos CSS
├── templates/ #Plantillas
│ ├── agregar_categoria.html
│ ├── agregar_producto.html
│ ├── index.html
│ ├── layout.html
│ ├── login.html
│ ├── registro.html
│ └── ver_categoria.html
└── README.md # Este archivo

#Para crear un entorno virtual
python -m venv venv
source venv/bin/activate    # En Linux/macOS
venv\Scripts\activate       # En Windows

#Instalar las dependencias
pip install -r requirements.txt

#Ejecutar la app
Por defecto, la aplicación se ejecutará en http://localhost:5000


