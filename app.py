from flask import Flask, render_template, flash, request, redirect, url_for
from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField, DateTimeLocalField, validators
from wtforms.validators import DataRequired, InputRequired
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy_report import Reporter
from wtforms_sqlalchemy.fields import QuerySelectField
from sqlalchemy import create_engine, MetaData, Table
from datetime import datetime

app=Flask(__name__)

# Aff database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:alonzo123X@database-1.crx15og5b3ep.us-east-1.rds.amazonaws.com/proyecto'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/proyecto'

engine = create_engine('mysql+pymysql://admin:alonzo123X@database-1.crx15og5b3ep.us-east-1.rds.amazonaws.com/proyecto')
metadata = MetaData(bind=engine)

# Secret key
app.config['SECRET_KEY'] = 'My super secret that no one is supposed to know'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Initializa the DataBase
db=SQLAlchemy(app)

#Create Model
class User(db.Model):
    __tablename__ = 'user'
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(50), nullable=False)
    password=db.Column(db.String(250), nullable=False)
    fullname=db.Column(db.String(250), nullable=False)
    #Create a String
    def __init__(self, username, password, fullname):
        self.username=username
        self.password=password
        self.fullname=fullname
        
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
    def __init__(self, DNI, nombre, apellido, especialidad):
        self.DNI=DNI
        self.nombre=nombre
        self.apellido=apellido
        self.especialidad=especialidad

def choice_query_doctor():
    return Doctor.query

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
    def __init__(self, DNI, nombre, apellido, nro_seguro):
        self.DNI=DNI
        self.nombre=nombre
        self.apellido=apellido
        self.nro_seguro=nro_seguro

def choice_query_paciente():
    return Paciente.query

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
    reserva_fecha_consulta=db.Column(db.DateTime, nullable=False)
    
    # Aqui pasamos el nombre de las clases y no el nombre de la tabla
    doctor = db.relationship('Doctor')
    paciente = db.relationship('Paciente')

    #Create a String
    def __init__(self,descripcion_consulta, id_doctor, id_paciente, reserva_fecha_consulta):
        self.descripcion_consulta=descripcion_consulta
        self.id_doctor=id_doctor
        self.id_paciente=id_paciente
        self.reserva_fecha_consulta=reserva_fecha_consulta

def choice_query_consulta():
    return Consulta.query

# Create form class
class ConsultaForm(FlaskForm):
    descripcion_consulta=StringField("Descripcion de la Consulta: ", validators=[InputRequired()])
    # id_doctor=StringField("Doctor: ", validators=[InputRequired()])
    # id_paciente=StringField("Paciente: ", validators=[InputRequired()])
    id_doctor = QuerySelectField("Nombre del Doctor: ", query_factory=choice_query_doctor, allow_blank=True, get_label='nombre', validators=[InputRequired()])
    id_paciente = QuerySelectField("Nombre del Paciente: ", query_factory=choice_query_paciente, allow_blank=True,get_label='nombre', validators=[InputRequired()])
    reserva_fecha_consulta=DateTimeLocalField('Fecha de Reserva: ', format='%Y-%m-%dT%H:%M', validators=[InputRequired()])
    submit=SubmitField('Submit')

#Create Model Registro
class Registro(db.Model):
    __tablename__ = 'registro'
    id_registro=db.Column(db.Integer, primary_key=True)
    descripcion_consulta=db.Column(db.String(120), nullable=False)
    name_doctor=db.Column(db.String(50), nullable=False)
    name_paciente=db.Column(db.String(50), nullable=False)
    reserva_fecha=db.Column(db.DateTime, nullable=False)

    #Create a String
    def __init__(self, descripcion_consulta, name_doctor, name_paciente, reserva_fecha):
        self.descripcion_consulta=descripcion_consulta
        self.name_doctor=name_doctor
        self.name_paciente=name_paciente
        self.reserva_fecha=reserva_fecha

def choice_query_registro():
    return Registro.query

# Create form class
class RegistroForm(FlaskForm):
    descripcion_consulta=StringField("Descripcion de la Consulta: ")
    name_doctor =StringField("Nombre del Doctor: ")
    name_paciente = StringField("Nombre del Paciente: ")
    reserva_fecha=DateTimeLocalField('Fecha de Reserva: ', format='%Y-%m-%dT%H:%M')
    submit=SubmitField('Submit')
    

# Create Add Tuition
@app.route('/doctor/add', methods=['GET','POST'])
def add_doctor():
    DNI = None
    form = DoctorForm()
    if form.validate_on_submit():
        doctors=Doctor(DNI=form.DNI.data, nombre=form.nombre.data, apellido=form.apellido.data,especialidad=form.especialidad.data)
        db.session.add(doctors)
        db.session.commit()
        DNI=form.DNI.data
        form.DNI.data=''
        form.nombre.data=''
        form.apellido.data=''
        form.especialidad.data=''
        flash("El registro se ha guardado correctamente!")
    our_doctors=Doctor.query.order_by(Doctor.date_added)
    return render_template('add_doctor.html', form=form, DNI=DNI, our_doctors=our_doctors)

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
        flash("Paciente agregado satisfactoriamente!")
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
    form_registro = RegistroForm()
    if form.validate_on_submit():
        
        my_descripcion_consulta = request.form.get('descripcion_consulta')
        my_idDoctor = request.form.get('id_doctor')
        my_idPaciente = request.form.get('id_paciente')
        my_fecha_reserva = request.form.get('reserva_fecha_consulta')
        
        # descripcion = request.form.get('descripcion_consulta')
        # nameDoctor = request.form.get('id_doctor')
        # namePaciente = request.form.get('id_paciente')
        # fecha_reserva = request.form.get('reserva_fecha_consulta')
        
        consulta = Consulta(my_descripcion_consulta, my_idDoctor, my_idPaciente, my_fecha_reserva)
        # registro = Registro(my_descripcion_consulta, my_idDoctor, my_idPaciente, my_fecha_reserva)
        
        # registro=Registro(descripcion=form.descripcion_consulta.data, nameDoctor=form.id_doctor.data, namePaciente=form.id_paciente.data, fecha_reserva=form.reserva_fecha_consulta.data)
        
        if my_idDoctor == "__None" or my_idPaciente == "__None":
            flash("Se requiere llenar los campos!")
        else:
            db.session.add(consulta)
            # db.session.add(registro)
            db.session.commit()

            descripcion_consulta=form.descripcion_consulta.data
            form.descripcion_consulta.data=''
            form.id_doctor.data=''
            form.id_paciente.data=''
            form.reserva_fecha_consulta.data=''
            flash("La consulta se ha realizado correctamente!")
    # our_consultas=Consulta.query.order_by(Consulta.id_consulta)
    # our_consultas=db.session.query(Consulta, Doctor, Paciente).join(Consulta.id_consulta,Consulta.doctor, Consulta.paciente).order_by(Consulta.id_consulta).all()
    our_consultas=engine.execute('select id_consulta,descripcion_consulta,doctor.nombre as nombre_doc,paciente.nombre as nombre, reserva_fecha_consulta from doctor inner join consulta  on doctor.id_doctor=consulta.id_doctor inner join paciente on paciente.id_paciente=consulta.id_paciente')
    return render_template('add_consulta.html',
    form=form, descripcion_consulta=descripcion_consulta, our_consultas=our_consultas)
    
 
# Update Doctor
@app.route('/doctor/update/<int:id_doctor>', methods=['GET', 'POST'])
def update_doctor(id_doctor):
    form = DoctorForm()
    name_update = Doctor.query.get_or_404(id_doctor)
    if request.method == "POST":   
        name_update.DNI = request.form['DNI']
        name_update.nombre = request.form['nombre']
        name_update.apellido = request.form['apellido']
        name_update.especialidad = request.form['especialidad']
        try:
            db.session.commit()
            flash("Se ha actualizado satisfactoriamente!")
            return redirect('/doctor/add')
        except:
            flash("Error! in update Doctor!")
            return render_template('update_doctor.html', form=form, name_update=name_update)
    else:
        return render_template('update_doctor.html', form=form, name_update=name_update)
    
#UPDATE CONSULTA
# Update Doctor
@app.route('/consulta/update/<int:id_consulta>', methods=['GET', 'POST'])
def update_consulta(id_consulta):
    form = ConsultaForm()
    name_update = Consulta.query.get_or_404(id_consulta)
    if request.method == "POST":   
        name_update.descripcion_consulta = request.form['descripcion_consulta']
        name_update.id_doctor = request.form['id_doctor']
        name_update.id_paciente = request.form['id_paciente']
        try:
            db.session.commit()
            flash("Se ha actualizado satisfactoriamente!")
            return redirect('/consulta/add')
        except:
            flash("Error! in update consulta!")
            return render_template('update_consulta.html', form=form, name_update=name_update)
    else:
        return render_template('update_consulta.html', form=form, name_update=name_update)

#Delete Matricula
@app.route('/deletedoctor/<id_doctor>')
def deletedoctor(id_doctor):
    doctors=Doctor.query.get(id_doctor)
    try:
        db.session.delete(doctors)
        db.session.commit()
        flash ("Doctor Delete Successfully!")
        return redirect('/doctor/add')
    except:
        flash ("Ops! There was a problem from deleted Doctor!")        
    return render_template('/doctor/add')


# DELETE PACIENTE
@app.route('/paciente/update/<int:id_paciente>', methods=['GET','POST'])
def update_paciente(id_paciente):
    name_update=Paciente.query.get_or_404(id_paciente)
    form = PacienteForm()
    if request.method == "POST":
        name_update=Paciente.query.get(id_paciente)
        name_update.DNI = request.form['DNI']
        name_update.nombre = request.form['nombre']
        name_update.apellido = request.form['apellido']
        name_update.nro_seguro = request.form['nro_seguro']
        try:
            db.session.commit()
            flash('Se ha registrado correctamente')
            return redirect("/paciente/add")
        except:
            flash('Error en la actualización!')
            return render_template("update_paciente", form=form, name_update=name_update)
    else:
        return render_template('update_paciente.html', form=form, name_update=name_update)

#Delete Escuelas
@app.route('/deletepaciente/<id_paciente>')
def deletepaciente(id_paciente):
    pacientes=Paciente.query.get(id_paciente)
    try:
        db.session.delete(pacientes)
        db.session.commit()
        flash ("Paciente Delete Successfully!")
        return redirect('/paciente/add')
    except:
        flash ("Ops! There was a problem from deleted Paciente!")  
    return render_template('/paciente/add')


#Delete Escuelas
@app.route('/deleteconsulta/<id_consulta>')
def deleteconsulta(id_consulta):
    consultas=Consulta.query.get(id_consulta)
    try:
        db.session.delete(consultas)
        db.session.commit()
        flash ("La consulta se ha eliminado satisfactoriamente!")
        return redirect('/consulta/add')
    except:
        flash ("Ops! There was a problem from deleted Consult!")  
    return render_template('/consulta/add')


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
