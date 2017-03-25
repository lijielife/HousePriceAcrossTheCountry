DROP DATABASE IF EXISTS LianJia;

/* create database for LianJia */
CREATE DATABASE LianJia CHARACTER SET 'utf8' COLLATE 'utf8_general_ci';
USE LianJia;

/* create table for LianJia new house data */
CREATE TABLE LianJia_New_House(
   id INT NOT NULL AUTO_INCREMENT,
   loupan_name VARCHAR(200) NOT NULL,
   loupan_name_detail VARCHAR(500) NOT NULL,
   address VARCHAR(200) NOT NULL,
   price VARCHAR(200) NOT NULL,
   PRIMARY KEY (id)
);

/* create table for LianJia second house data */
CREATE TABLE LianJia_Second_House(
   id INT NOT NULL AUTO_INCREMENT,
   loupan_name VARCHAR(200) NOT NULL,
   loupan_name_detail VARCHAR(500) NOT NULL,
   area VARCHAR(200) NOT NULL,
   allocation VARCHAR(200) NOT NULL,
   address VARCHAR(200) NOT NULL,
   per_price VARCHAR(200) NOT NULL,
   price VARCHAR(200) NOT NULL,
   PRIMARY KEY (id)
);

/* create table for LianJia renting house data */
CREATE TABLE LianJia_Renting_House(
   id INT NOT NULL AUTO_INCREMENT,
   loupan_name VARCHAR(200) NOT NULL,
   loupan_name_detail VARCHAR(500) NOT NULL,
   allocation VARCHAR(200) NOT NULL,
   renting_type VARCHAR(200) NOT NULL,
   floor VARCHAR(200) NOT NULL,
   address VARCHAR(200) NOT NULL,
   price VARCHAR(200) NOT NULL,
   PRIMARY KEY (id)
);
