CREATE DATABASE AnJuKe CHARACTER SET 'utf8' COLLATE 'utf8_general_ci';
USE AnJuKe;
CREATE TABLE AnJuKe_New_House(
   id INT NOT NULL AUTO_INCREMENT,
   loupan_name VARCHAR(200) NOT NULL,
   loupan_name_detail VARCHAR(500) NOT NULL,
   address VARCHAR(200) NOT NULL,
   price VARCHAR(200) NOT NULL,
   PRIMARY KEY (id)
);
CREATE TABLE AnJuKe_Second_House(
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
CREATE TABLE AnJuKe_Renting_House(
   id INT NOT NULL AUTO_INCREMENT,
   loupan_name VARCHAR(200) NOT NULL,
   loupan_name_detail VARCHAR(500) NOT NULL,
   allocation VARCHAR(200) NOT NULL,
   renting_type VARCHAR(200) NOT NULL,
   finish_type VARCHAR(200) NOT NULL,
   floor VARCHAR(200) NOT NULL,
   address VARCHAR(200) NOT NULL,
   price VARCHAR(200) NOT NULL,
   PRIMARY KEY (id)
);

CREATE DATABASE SouFangWang CHARACTER SET 'utf8' COLLATE 'utf8_general_ci';
USE SouFangWang;
CREATE TABLE SouFangWang_New_House(
   id INT NOT NULL AUTO_INCREMENT,
   loupan_name VARCHAR(200) NOT NULL,
   loupan_name_detail VARCHAR(500) NOT NULL,
   address VARCHAR(200) NOT NULL,
   price VARCHAR(200) NOT NULL,
   PRIMARY KEY (id)
);
CREATE TABLE SouFangWang_Second_House(
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
CREATE TABLE SouFangWang_Renting_House(
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
