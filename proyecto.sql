create database proyecto;
use proyecto;

create table doctor
(
id_doctor int primary key auto_increment,
DNI char(8),
nombre varchar(50),
apellido varchar(120),
especialidad varchar(120)
);

create table paciente
(
id_paciente int primary key auto_increment,
DNI char(8),
nombre varchar(50),
apellido varchar(120),
nro_seguro varchar(50)
);

create table consulta
(
id_consulta int primary key auto_increment,
descripcion_consulta varchar(120),
id_doctor int,
id_paciente int,
foreign key (id_doctor) references doctor (id_doctor),
foreign key (id_paciente) references paciente (id_paciente) 
);

create table registro_consulta
(
id_registro int primary key auto_increment,
id_doctor int,
id_paciente int,
id_consulta int,
foreign key (id_doctor) references doctor (id_doctor),
foreign key (id_paciente) references paciente (id_paciente),
foreign key (id_consulta)references consulta (id_consulta)
);