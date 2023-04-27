create database dbapi;
use dbapi;

create table usuarios (
    id integer not null auto_increment,
    nome varchar(50),
    login varchar(30),
    senha varchar(30)
    Primary key (id)
);

insert into usuarios(id,nome,login,senha) values(01, 'Sergio Juniors Garcez', 'sergingameplays', '1234');
insert into usuarios(id,nome,login,senha) values(02, 'Pelé', 'peleisalive', 'bra123');

