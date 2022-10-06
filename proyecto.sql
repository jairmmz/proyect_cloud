create database proyecto;
use proyecto;

create table user(
	id int not null primary key auto_increment,
    username varchar(50),
    password varchar(250),
    fullname varchar(250)
);

insert into user values (1,'leytercpp','123456','Leyter Admin CPP');
select * from user;

create table doctor
(
id_doctor int primary key auto_increment,
DNI char(8),
nombre varchar(50),
apellido varchar(120),
especialidad varchar(120)
);

select * from doctor;

create table paciente
(
id_paciente int primary key auto_increment,
DNI char(8),
nombre varchar(50),
apellido varchar(120),
nro_seguro varchar(50)
);

select * from paciente;

create table consulta
(
id_consulta int primary key auto_increment,
descripcion_consulta varchar(120),
id_doctor int,
id_paciente int,
foreign key (id_doctor) references doctor (id_doctor),
foreign key (id_paciente) references paciente (id_paciente) 
);

select * from consulta;

use api_flask;
select * from tcurso;
select * from doctor;

select id_consulta,descripcion_consulta,doctor.nombre,paciente.nombre, reserva_fecha_consulta
from doctor inner join consulta
on doctor.id_doctor=consulta.id_doctor inner join paciente
on paciente.id_paciente=consulta.id_paciente;