-- creates clean database for weerstation
DROP USER IF EXISTS 'sensem'@'localhost';
DROP USER IF EXISTS 'senser'@'localhost';
DROP DATABASE IF EXISTS `weerstation`;
CREATE DATABASE `weerstation`;
USE `weerstation`;
CREATE TABLE `sensor` (
 `id` INT(11) NOT NULL AUTO_INCREMENT,
 `naam` VARCHAR(45),
 `eenheid` VARCHAR(45),
 PRIMARY KEY (`id`)
);
CREATE TABLE `meting` (
 `id` INT(11) NOT NULL AUTO_INCREMENT,
 `sensor_id` INT(11) NOT NULL,
 `tijd` TIMESTAMP,
 `waarde` FLOAT DEFAULT NULL,
 PRIMARY KEY (`id`),
 KEY `fk_meting_sensor` (`sensor_id`),
 CONSTRAINT `fk_meting_sensor` FOREIGN KEY (`sensor_id`) REFERENCES
`sensor` (`id`)
);
CREATE USER 'sensem'@'localhost' IDENTIFIED BY 'h@';
CREATE USER 'senser'@'localhost' IDENTIFIED BY 'h@';
GRANT INSERT ON weerstation.meting TO 'sensem'@'localhost';
GRANT SELECT ON weerstation.* TO 'senser'@'localhost';
