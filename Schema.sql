-- MySQL dump 10.13  Distrib 8.0.23, for Win64 (x86_64)
--
-- Host: 192.168.40.47    Database: Dashboard_DB
-- ------------------------------------------------------
-- Server version	8.0.25

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `pfsense_act`
--

DROP TABLE IF EXISTS `pfsense_act`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pfsense_act` (
  `id` int NOT NULL AUTO_INCREMENT,
  `act` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pfsense_direction`
--

DROP TABLE IF EXISTS `pfsense_direction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pfsense_direction` (
  `id` int NOT NULL AUTO_INCREMENT,
  `direction` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pfsense_ecn_header`
--

DROP TABLE IF EXISTS `pfsense_ecn_header`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pfsense_ecn_header` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ecn_header` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=399 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pfsense_firewall_rules`
--

DROP TABLE IF EXISTS `pfsense_firewall_rules`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pfsense_firewall_rules` (
  `id` int NOT NULL AUTO_INCREMENT,
  `pfsense_instance` int NOT NULL,
  `record_time` timestamp NOT NULL,
  `rule_number` int NOT NULL,
  `rule_description` text,
  PRIMARY KEY (`id`),
  KEY `pfsense_instance` (`pfsense_instance`),
  CONSTRAINT `pfsense_firewall_rules_ibfk_1` FOREIGN KEY (`pfsense_instance`) REFERENCES `pfsense_instances` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16711 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pfsense_flags`
--

DROP TABLE IF EXISTS `pfsense_flags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pfsense_flags` (
  `id` int NOT NULL AUTO_INCREMENT,
  `flags` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=82 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pfsense_instances`
--

DROP TABLE IF EXISTS `pfsense_instances`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pfsense_instances` (
  `id` int NOT NULL AUTO_INCREMENT,
  `pfsense_name` varchar(255) DEFAULT NULL,
  `hostname` varchar(255) DEFAULT NULL,
  `reachable_ip` varchar(255) DEFAULT NULL,
  `instance_user` varchar(255) DEFAULT NULL,
  `instance_password` varchar(255) DEFAULT NULL,
  `ssh_port` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `pfsense_name` (`pfsense_name`),
  UNIQUE KEY `hostname` (`hostname`)
) ENGINE=InnoDB AUTO_INCREMENT=1067 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pfsense_ip`
--

DROP TABLE IF EXISTS `pfsense_ip`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pfsense_ip` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ip` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=292 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pfsense_log_bucket`
--

DROP TABLE IF EXISTS `pfsense_log_bucket`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pfsense_log_bucket` (
  `id` int NOT NULL AUTO_INCREMENT,
  `log` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=559715 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pfsense_log_type`
--

DROP TABLE IF EXISTS `pfsense_log_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pfsense_log_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `log_type` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6411 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pfsense_logs`
--

DROP TABLE IF EXISTS `pfsense_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pfsense_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `type_code` int DEFAULT NULL,
  `record_time` timestamp NULL DEFAULT NULL,
  `pfsense_instance` int NOT NULL,
  `log_type` int DEFAULT NULL,
  `rule_number` int DEFAULT NULL,
  `sub_rule_number` int DEFAULT NULL,
  `anchor` int DEFAULT NULL,
  `tracker` int DEFAULT NULL,
  `real_interface` int DEFAULT NULL,
  `reason` int DEFAULT NULL,
  `act` int DEFAULT NULL,
  `direction` int DEFAULT NULL,
  `ip_version` int DEFAULT NULL,
  `tos_header` int DEFAULT NULL,
  `ecn_header` int DEFAULT NULL,
  `ttl` int DEFAULT NULL,
  `packet_id` int DEFAULT NULL,
  `packet_offset` int DEFAULT NULL,
  `flags` int DEFAULT NULL,
  `protocol_id` int DEFAULT NULL,
  `protocol` int DEFAULT NULL,
  `packet_length` int DEFAULT NULL,
  `source_ip` int DEFAULT NULL,
  `destination_ip` int DEFAULT NULL,
  `source_port` int DEFAULT NULL,
  `destination_port` int DEFAULT NULL,
  `data_length` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `pfsense_instance` (`pfsense_instance`),
  KEY `log_type` (`log_type`),
  KEY `real_interface` (`real_interface`),
  KEY `reason` (`reason`),
  KEY `act` (`act`),
  KEY `direction` (`direction`),
  KEY `tos_header` (`tos_header`),
  KEY `ecn_header` (`ecn_header`),
  KEY `flags` (`flags`),
  KEY `protocol` (`protocol`),
  KEY `source_ip` (`source_ip`),
  KEY `destination_ip` (`destination_ip`),
  CONSTRAINT `pfsense_logs_ibfk_1` FOREIGN KEY (`pfsense_instance`) REFERENCES `pfsense_instances` (`id`),
  CONSTRAINT `pfsense_logs_ibfk_10` FOREIGN KEY (`protocol`) REFERENCES `pfsense_protocol` (`id`),
  CONSTRAINT `pfsense_logs_ibfk_11` FOREIGN KEY (`source_ip`) REFERENCES `pfsense_ip` (`id`),
  CONSTRAINT `pfsense_logs_ibfk_12` FOREIGN KEY (`destination_ip`) REFERENCES `pfsense_ip` (`id`),
  CONSTRAINT `pfsense_logs_ibfk_2` FOREIGN KEY (`log_type`) REFERENCES `pfsense_log_type` (`id`),
  CONSTRAINT `pfsense_logs_ibfk_3` FOREIGN KEY (`real_interface`) REFERENCES `pfsense_real_interface` (`id`),
  CONSTRAINT `pfsense_logs_ibfk_4` FOREIGN KEY (`reason`) REFERENCES `pfsense_reason` (`id`),
  CONSTRAINT `pfsense_logs_ibfk_5` FOREIGN KEY (`act`) REFERENCES `pfsense_act` (`id`),
  CONSTRAINT `pfsense_logs_ibfk_6` FOREIGN KEY (`direction`) REFERENCES `pfsense_direction` (`id`),
  CONSTRAINT `pfsense_logs_ibfk_7` FOREIGN KEY (`tos_header`) REFERENCES `pfsense_tos_header` (`id`),
  CONSTRAINT `pfsense_logs_ibfk_8` FOREIGN KEY (`ecn_header`) REFERENCES `pfsense_ecn_header` (`id`),
  CONSTRAINT `pfsense_logs_ibfk_9` FOREIGN KEY (`flags`) REFERENCES `pfsense_flags` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=807 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pfsense_protocol`
--

DROP TABLE IF EXISTS `pfsense_protocol`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pfsense_protocol` (
  `id` int NOT NULL AUTO_INCREMENT,
  `protocol` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pfsense_real_interface`
--

DROP TABLE IF EXISTS `pfsense_real_interface`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pfsense_real_interface` (
  `id` int NOT NULL AUTO_INCREMENT,
  `interface` varchar(50) NOT NULL,
  `pfsense_instance` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `pfsense_real_interface_ibfk_1` (`pfsense_instance`),
  CONSTRAINT `pfsense_real_interface_ibfk_1` FOREIGN KEY (`pfsense_instance`) REFERENCES `pfsense_instances` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pfsense_reason`
--

DROP TABLE IF EXISTS `pfsense_reason`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pfsense_reason` (
  `id` int NOT NULL AUTO_INCREMENT,
  `reason` varchar(250) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pfsense_tos_header`
--

DROP TABLE IF EXISTS `pfsense_tos_header`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pfsense_tos_header` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tos_header` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping events for database 'Dashboard_DB'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-06-21 18:44:42
