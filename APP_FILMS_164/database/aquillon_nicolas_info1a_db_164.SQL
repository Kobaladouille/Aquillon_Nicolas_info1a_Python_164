-- OM 2021.02.17
-- FICHIER MYSQL POUR FAIRE FONCTIONNER LES EXEMPLES
-- DE REQUETES MYSQL
-- Database: MACCAUD_OLIVIER_INFO1X_FILMS_164_2023

-- Destruction de la BD si elle existe.
-- Pour être certain d'avoir la dernière version des données

DROP DATABASE IF EXISTS aquillon_nicolas_info1a_db_164;

-- Création d'un nouvelle base de donnée

CREATE DATABASE IF NOT EXISTS aquillon_nicolas_info1a_db_164;

-- Utilisation de cette base de donnée

USE aquillon_nicolas_info1a_db_164;
-- --------------------------------------------------------
-- Hôte:                         127.0.0.1
-- Version du serveur:           8.0.30 - MySQL Community Server - GPL
-- SE du serveur:                Win64
-- HeidiSQL Version:             12.1.0.6537
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 oui */;


-- Listage de la structure de la base pour aquillon_nicolas_info1a_db_164
CREATE DATABASE IF NOT EXISTS `aquillon_nicolas_info1a_db_164` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `aquillon_nicolas_info1a_db_164`;

-- Listage de la structure de table aquillon_nicolas_info1a_db_164. t_entretien
CREATE TABLE IF NOT EXISTS `t_entretien` (
  `id_entretien` int NOT NULL AUTO_INCREMENT,
  `description_entretien` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_entretien`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table aquillon_nicolas_info1a_db_164.t_entretien : ~0 rows (environ)

-- Listage de la structure de table aquillon_nicolas_info1a_db_164. t_voiture
CREATE TABLE IF NOT EXISTS `t_voiture` (
  `id_voiture` int NOT NULL AUTO_INCREMENT,
  `marque` varchar(50) DEFAULT NULL,
  `modele` varchar(50) DEFAULT NULL,
  `chevaux` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_voiture`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table aquillon_nicolas_info1a_db_164.t_voiture : ~0 rows (environ)

-- Listage de la structure de table aquillon_nicolas_info1a_db_164. t_voiture_avoir_entretien
CREATE TABLE IF NOT EXISTS `t_voiture_avoir_entretien` (
  `id_voiture_entretien` int NOT NULL AUTO_INCREMENT,
  `fk_voiture` int DEFAULT NULL,
  `fk_entretien` int DEFAULT NULL,
  PRIMARY KEY (`id_voiture_entretien`),
  KEY `fk_voiture` (`fk_voiture`),
  KEY `fk_entretien` (`fk_entretien`),
  CONSTRAINT `FK_t_voiture_avoir_entretien_t_entretien` FOREIGN KEY (`fk_entretien`) REFERENCES `t_entretien` (`id_entretien`),
  CONSTRAINT `FK_t_voiture_avoir_entretien_t_voiture` FOREIGN KEY (`fk_voiture`) REFERENCES `t_voiture` (`id_voiture`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table aquillon_nicolas_info1a_db_164.t_voiture_avoir_entretien : ~0 rows (environ)

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
