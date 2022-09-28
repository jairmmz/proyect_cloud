from flask import Flask, render_template, flash, request, redirect, url_for
from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, InputRequired
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


#https://wtforms.readthedocs.io/en/3.0.c/forms/

app=Flask(__name__)

# Aff database
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root@localhost/proyecto'
#app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://admin:gafqbm1cipi!@database-1.c5gtowjq1igh.us-east-1.rds.amazonaws.com/Examen'
#Secret key
app.config['SECRET_KEY']='My super secret taht no one is supposed to know'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Initializa the DataBase
db=SQLAlchemy(app)
#SQLAlchemy(app)

#Create Model
class User(db.Model):
    __tablename__ = 'user'
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(50), nullable=False)
    password=db.Column(db.String(250), nullable=False)
    fullname=db.Column(db.String(250), nullable=False)
    #Create a String
    def __repr__(self):
        return '<Nombre %r>'% self.username
# Create form class
class UserForm(FlaskForm):
    username=StringField("Usuario: ", validators=[DataRequired()])
    password=StringField("Contraseña: ", validators=[DataRequired()])
    submit=SubmitField('Submit')
    
    
#Create Model
class Doctor(db.Model):
    __tablename__ = 'doctor'
    id_doctor=db.Column(db.Integer, primary_key=True)
    DNI=db.Column(db.Integer, nullable=False)
    nombre=db.Column(db.String(50), nullable=False)
    apellido=db.Column(db.String(250), nullable=False)
    especialidad=db.Column(db.String(250), nullable=False)
    date_added=db.Column(db.DateTime, default=datetime.utcnow)
    #Create a String
    def __repr__(self):
        return '<Nombre %r>'% self.nombre

# Create form class
class DoctorForm(FlaskForm):
    DNI=StringField("DNI: ", validators=[DataRequired()])
    nombre=StringField("Nombre: ", validators=[DataRequired()])
    apellido=StringField("Apellido: ", validators=[DataRequired()])
    especialidad=StringField("Especialidad: ", validators=[DataRequired()])
    submit=SubmitField('Submit')

#Create Model
class Paciente(db.Model):
    __tablename__ = 'paciente'
    id_paciente=db.Column(db.Integer, primary_key=True)
    DNI=db.Column(db.String(8), nullable=False)
    nombre=db.Column(db.String(50), nullable=False)
    apellido=db.Column(db.String(120), nullable=False)
    nro_seguro =db.Column(db.String(50), nullable=False)
    date_added=db.Column(db.DateTime, default=datetime.utcnow)
    #Create a String
    def __repr__(self):
        return '<Nombre %r>'% self.nombre

# Create form class
class PacienteForm(FlaskForm):
    DNI=StringField("DNI del Paciente:", validators=[DataRequired()])
    nombre=StringField("Nombre del Paciente:", validators=[DataRequired()])
    apellido=StringField("Apellido: ", validators=[DataRequired()])
    nro_seguro=StringField("Nro Seguro: ", validators=[DataRequired()])
    submit=SubmitField('Submit')

#Create Model
class Consulta(db.Model):
    __tablename__ = 'consulta'
    id_consulta=db.Column(db.Integer, primary_key=True)
    descripcion_consulta=db.Column(db.String(120), nullable=False)
    id_doctor=db.Column(db.Integer, db.ForeignKey('doctor.id_doctor'), nullable=False)
    id_paciente=db.Column(db.Integer, db.ForeignKey('paciente.id_paciente'), nullable=False)
    date_added=db.Column(db.DateTime, default=datetime.utcnow)
    
    #Create a String
    def __repr__(self):
        return '<id_estudiante %r>'% self.id_estudiante

# Create form class
class ConsultaForm(FlaskForm):
    descripcion_consulta=StringField("Descripcion de la Consulta: ", validators=[DataRequired()])
    id_doctor=StringField("Doctor: ", validators=[DataRequired()])
    id_paciente=StringField("Paciente: ", validators=[DataRequired()])
    submit=SubmitField('Submit')

#Create Model
class Registro_consulta(db.Model):
    __tablename__ = 'registro_consulta'
    id_registro=db.Column(db.Integer, primary_key=True)
    id_doctor=db.Column(db.Integer, db.ForeignKey('doctor.id_doctor'), nullable=False)
    id_paciente=db.Column(db.Integer, db.ForeignKey('paciente.id_paciente'), nullable=False)
    id_consulta=db.Column(db.Integer, db.ForeignKey('consulta.id_consulta'), nullable=False)
    date_added=db.Column(db.DateTime, default=datetime.utcnow)
    #Create a String
    def __repr__(self):
        return '<Nombre %r>'% self.nombre
    
# Create form class
class NamerForm(FlaskForm):
    id_doctor=StringField("Doctor: ", validators=[DataRequired()])
    apellidos=StringField("Apellidos: ", validators=[DataRequired()])
    id_paciente=StringField("Paciente: ", validators=[DataRequired()])
    id_consulta=StringField("Consulta: ", validators=[DataRequired()])
    submit=SubmitField('Submit')

# Create form class
class RegistroForm(FlaskForm):
    id_doctor=StringField("Doctor: ", validators=[DataRequired()])
    apellidos=StringField("Apellidos: ", validators=[DataRequired()])
    id_paciente=StringField("Paciente: ", validators=[DataRequired()])
    id_consulta=StringField("Consulta: ", validators=[DataRequired()])
    submit=SubmitField('Submit')

# Create Add Tuition
@app.route('/doctor/add', methods=['GET','POST'])
def add_doctor():
    DNI = None
    form = DoctorForm()
    if form.validate_on_submit():
        doctors=Doctor(DNI=form.DNI.data, nombre=form.nombre.data,
        apellido=form.apellido.data,especialidad=form.especialidad.data)
        db.session.add(doctors)
        db.session.commit()
    DNI=form.DNI.data
    form.DNI.data=''
    form.nombre.data=''
    form.apellido.data=''
    form.especialidad.data=''
    our_doctors=Doctor.query.order_by(Doctor.date_added)
    return render_template('add_doctor.html',
    form=form,
    DNI=DNI,
    our_doctors=our_doctors)

# Create Add Student
@app.route('/paciente/add', methods=['GET','POST'])
def add_paciente():
    DNI = None
    form = PacienteForm()
    if form.validate_on_submit():
        pacientes=Paciente.query.filter_by(DNI=form.DNI.data).first()
        if form.validate_on_submit():
            pacientes=Paciente(DNI =form.DNI.data, nombre=form.nombre.data, apellido =form.apellido.data,
            nro_seguro=form.nro_seguro.data)
            db.session.add(pacientes)
            db.session.commit()
        DNI=form.DNI.data
        form.DNI.data=''
        form.nombre.data=''
        form.apellido.data=''
        form.nro_seguro.data=''
    our_pacientes=Paciente.query.order_by(Paciente.date_added)
    return render_template('add_paciente.html',
    form=form,
    DNI=DNI,
    our_pacientes=our_pacientes)

# Create add Course
@app.route('/consulta/add', methods=['GET','POST'])
def add_consulta():
    descripcion_consulta = None
    form = ConsultaForm()
    if form.validate_on_submit():
        consultas=Consulta.query.filter_by(descripcion_consulta=form.descripcion_consulta.data).first()
        if form.validate_on_submit():
            consultas=Consulta(descripcion_consulta=form.descripcion_consulta.data, id_doctor=form.id_doctor.data, id_paciente =form.id_paciente.data)
            db.session.add(consultas)
            db.session.commit()
        descripcion_consulta=form.descripcion_consulta.data
        form.id_doctor.data=''
        form.id_paciente.data=''
    our_consultas=Consulta.query.order_by(Consulta.date_added)
    return render_template('add_consulta.html',
    form=form,
    descripcion_consulta=descripcion_consulta,
    our_consultas=our_consultas)

#Create add Schools
@app.route('/registro/add', methods=['GET','POST'])
def add_registro():
    id_doctor= None
    form = RegistroForm()
    if form.validate_on_submit():
        registros=Registro_consulta.query.filter_by(id_doctor=form.id_doctor.data).first()
        if form.validate_on_submit():
            registros=Registro_consulta(id_doctor=form.id_doctor.data, id_paciente=form.id_paciente.data, id_consulta=form.id_consulta.data)
            db.session.add(registros)
            db.session.commit()
        id_doctor=form.id_doctor.data
        form.id_doctor.data=''
        form.id_paciente.data=''
        form.id_consulta.data=''
        flash("User Add Successfully!")
    our_registros=Registro_consulta.query.order_by(Registro_consulta.date_added)
    return render_template('add_registro.html',
    form=form,
    id_doctor=id_doctor,
    our_registros=our_registros)

#Delete Matricula
@app.route('/deletedoctor/<id_doctor>')
def deletedoctor(id_doctor):
    doctors=Doctor.query.get(id_doctor)
    db.session.delete(doctors)
    db.session.commit()
    flash ("Matricula Delete Successfully!")
    return render_template("add_doctor.html")

#Delete Estuadiante
@app.route('/deleteregistro/<id_registro>')
def deletepacientex(id_registro):
    registros=Registro_consulta.query.get(id_registro)
    db.session.delete(registros)
    db.session.commit()
    flash ("Registro Delete Successfully!")
    return render_template("add_registro.html")

#Delete Escuelas
@app.route('/deletepaciente/<id_paciente>')
def deletepaciente(id_paciente):
    pacientes=Paciente.query.get(id_paciente)
    db.session.delete(pacientes)
    db.session.commit()
    flash ("Paciente Delete Successfully!")
    return render_template("add_paciente.html")

#Delete Escuelas
@app.route('/deleteconsulta/<id_consulta>')
def deletecurso(id_consulta):
    consultas=Consulta.query.get(id_consulta)
    db.session.delete(consultas)
    db.session.commit()
    flash ("Consulta Delete Successfully!")
    return render_template("add_consulta.html")


#RUTA RAIZ
@app.route('/')
def index():   
    return redirect(url_for ('login'))

#HOME
@app.route('/home')
def home():
    return render_template('home.html')

#LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    username=None
    password=None
    form=UserForm()
    # print(request.form['username'])
    # print(request.form['password'])
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data, password=form.password.data).first()
        if user is None:
            flash("Usuario o contraseña incorrecta.")
            form.username.data=''
            form.password.data=''
            return render_template("auth/login.html", form=form) 
        else:
            flash("Bienvenido Al Sitema.")
            return redirect("/home")      
    else:
        return render_template("auth/login.html", form=form) 






# Recargar automática para el server.
if __name__ == '__main__':
    app.run(debug=True)
