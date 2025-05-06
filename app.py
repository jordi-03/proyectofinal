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
    categorias = Categoria.query.all()
    return render_template('index.html', categorias=categorias)

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        email = request.form['email']
        contrasena = request.form['contrasena']
        hash_contrasena = generate_password_hash(contrasena)
        nuevo_usuario = Usuario(email=email, contrasena=hash_contrasena)
        db.session.add(nuevo_usuario)
        db.session.commit()
        flash('¡Registro exitoso, ahora inicia sesión!')
        return redirect(url_for('login'))
    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        contrasena = request.form['contrasena']
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and check_password_hash(usuario.contrasena, contrasena):
            session['usuario_id'] = usuario.id
            flash('Has iniciado sesión!')
            return redirect(url_for('index'))
        flash('Credenciales inválidas.')
    return render_template('login.html')






if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)