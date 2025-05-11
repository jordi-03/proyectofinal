from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'jordi1234'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trenor.db'
db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    contrasena = db.Column(db.String(256), nullable=False)

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(300))
    precio = db.Column(db.Float, nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'))
    imagen = db.Column(db.String(300))


@app.route('/')
def index():
    if 'usuario_id' not in session:
        return render_template('index.html') 
    else:
        return render_template('index.html')  

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        email = request.form['email']
        contrasena = request.form['password']
        hash_contrasena = generate_password_hash(contrasena)
        nuevo_usuario = Usuario(email=email, contrasena=hash_contrasena)
        db.session.add(nuevo_usuario)
        db.session.commit()
        flash('¡Registro exitoso, ahora inicia sesión!', 'success')
        return redirect(url_for('login'))
    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        contrasena = request.form['password']
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and check_password_hash(usuario.contrasena, contrasena):
            session['usuario_id'] = usuario.id
            flash('Has iniciado sesión correctamente!', 'success')
            return redirect(url_for('index'))
        flash('Credenciales inválidas, intenta nuevamente.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('usuario_id', None)
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('index'))

@app.route('/agregar_categoria', methods=['GET', 'POST'])
def agregar_categoria():
    if 'usuario_id' not in session:
        flash('Debes iniciar sesión para agregar categorías.', 'warning')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        nueva_categoria = Categoria(nombre=nombre)
        db.session.add(nueva_categoria)
        db.session.commit()
        flash('Categoría añadida con éxito!', 'success')
        return redirect(url_for('index'))
    
    return render_template('agregar_categoria.html')

@app.route('/agregar_producto', methods=['GET', 'POST'])
def agregar_producto():
    if 'usuario_id' not in session:
        flash('Debes iniciar sesión para agregar productos.', 'warning')
        return redirect(url_for('login'))

    categorias = Categoria.query.all()
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = float(request.form['precio'])
        categoria_id = int(request.form['categoria_id'])
        imagen = request.form['imagen']
        nuevo_producto = Producto(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            categoria_id=categoria_id,
            imagen=imagen
        )
        db.session.add(nuevo_producto)
        db.session.commit()
        flash('Producto añadido con éxito!', 'success')
        return redirect(url_for('index'))
    
    return render_template('agregar_producto.html', categorias=categorias)

@app.route('/ver_categoria')
def ver_categoria():
    if 'usuario_id' not in session:
        flash('Debes iniciar sesión para ver los productos.', 'danger')
        return redirect(url_for('login'))
    
    productos = Producto.query.all()
    return render_template('ver_categoria.html', productos=productos)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True)
