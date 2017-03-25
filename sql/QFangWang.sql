DROP DATABASE IF EXISTS QFangWang;

/* create database for QFangWang */
CREATE DATABASE QFangWang CHARACTER SET 'utf8' COLLATE 'utf8_general_ci';
USE QFangWang;

/* create table for QFangWang new house data */
CREATE TABLE QFangWang_New_House(
   id INT NOT NULL AUTO_INCREMENT,
   loupan_name VARCHAR(200) NOT NULL,
   loupan_name_detail VARCHAR(500) NOT NULL,
   address VARCHAR(200) NOT NULL,
   price VARCHAR(200) NOT NULL,
   PRIMARY KEY (id)
);

/* create table for QFangWang second house data */
CREATE TABLE QFangWang_Second_House(
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

/* create table for QFangWang renting house data */
CREATE TABLE QFangWang_Renting_House(
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
