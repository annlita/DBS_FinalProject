-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: NetGuardDB
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `equipment`
--

DROP TABLE IF EXISTS `equipment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `equipment` (
  `EID` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `type` varchar(100) NOT NULL,
  `location` varchar(255) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `VID` int DEFAULT NULL,
  `purchase_date` date DEFAULT NULL,
  `warranty_end_date` date DEFAULT NULL,
  PRIMARY KEY (`EID`),
  KEY `VID` (`VID`),
  CONSTRAINT `equipment_ibfk_1` FOREIGN KEY (`VID`) REFERENCES `vendor` (`VID`) ON DELETE SET NULL,
  CONSTRAINT `equipment_chk_1` CHECK ((`status` in (_cp850'Active',_cp850'Inactive',_cp850'Maintenance')))
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `equipment`
--

LOCK TABLES `equipment` WRITE;
/*!40000 ALTER TABLE `equipment` DISABLE KEYS */;
INSERT INTO `equipment` VALUES (1,'Juniper Firewall','Firewall','Data Center A','Active',1,'2022-04-01','2027-04-01'),(2,'Cisco Switch','Switch','Server Room B','Maintenance',2,'2023-01-10','2028-01-10'),(3,'HP Blade Server','Server','Main Rack','Active',3,'2023-06-15','2026-06-15'),(4,'Aruba Wireless AP','Access Point','Floor 3','Inactive',4,'2022-07-20','2025-07-20'),(5,'Palo Alto IDS','Intrusion Detection','Security Room','Active',5,'2024-02-05','2029-02-05'),(6,'Dell NAS Storage','Storage','Backup Room','Active',6,'2023-05-22','2027-05-22'),(7,'IBM Router','Router','Data Center B','Inactive',7,'2021-12-30','2026-12-30'),(8,'Check Point VPN','VPN Gateway','Office 1','Active',8,'2023-09-01','2028-09-01'),(9,'Netgear Firewall','Firewall','Security Room','Active',9,'2022-03-18','2027-03-18'),(10,'F5 Load Balancer','Load Balancer','Server Room C','Active',10,'2023-11-11','2028-11-11');
/*!40000 ALTER TABLE `equipment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `maintenancecontract`
--

DROP TABLE IF EXISTS `maintenancecontract`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `maintenancecontract` (
  `CID` int NOT NULL AUTO_INCREMENT,
  `EID` int DEFAULT NULL,
  `VID` int DEFAULT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `service_level` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`CID`),
  KEY `EID` (`EID`),
  KEY `VID` (`VID`),
  CONSTRAINT `maintenancecontract_ibfk_1` FOREIGN KEY (`EID`) REFERENCES `equipment` (`EID`) ON DELETE CASCADE,
  CONSTRAINT `maintenancecontract_ibfk_2` FOREIGN KEY (`VID`) REFERENCES `vendor` (`VID`) ON DELETE CASCADE,
  CONSTRAINT `maintenancecontract_chk_1` CHECK ((`service_level` in (_cp850'Basic',_cp850'Standard',_cp850'Premium')))
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `maintenancecontract`
--

LOCK TABLES `maintenancecontract` WRITE;
/*!40000 ALTER TABLE `maintenancecontract` DISABLE KEYS */;
INSERT INTO `maintenancecontract` VALUES (1,1,1,'2022-05-01','2027-05-01','Premium'),(2,2,2,'2023-02-01','2028-02-01','Standard'),(3,3,3,'2023-07-01','2026-07-01','Basic'),(4,4,4,'2022-08-01','2025-08-01','Premium'),(5,5,5,'2024-03-01','2029-03-01','Standard'),(6,6,6,'2023-06-01','2027-06-01','Basic'),(7,7,7,'2022-01-01','2026-01-01','Premium'),(8,8,8,'2023-10-01','2028-10-01','Standard'),(9,9,9,'2022-04-01','2027-04-01','Basic'),(10,10,10,'2023-12-01','2028-12-01','Premium');
/*!40000 ALTER TABLE `maintenancecontract` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `securityincident`
--

DROP TABLE IF EXISTS `securityincident`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `securityincident` (
  `IID` int NOT NULL AUTO_INCREMENT,
  `EID` int DEFAULT NULL,
  `description` text NOT NULL,
  `severity` varchar(50) DEFAULT NULL,
  `reporter` int DEFAULT NULL,
  `report_date` date NOT NULL,
  `resolve_date` date DEFAULT NULL,
  PRIMARY KEY (`IID`),
  KEY `EID` (`EID`),
  KEY `reporter` (`reporter`),
  CONSTRAINT `securityincident_ibfk_1` FOREIGN KEY (`EID`) REFERENCES `equipment` (`EID`) ON DELETE CASCADE,
  CONSTRAINT `securityincident_ibfk_2` FOREIGN KEY (`reporter`) REFERENCES `user` (`UID`) ON DELETE SET NULL,
  CONSTRAINT `securityincident_chk_1` CHECK ((`severity` in (_cp850'Low',_cp850'Medium',_cp850'High',_cp850'Critical')))
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `securityincident`
--

LOCK TABLES `securityincident` WRITE;
/*!40000 ALTER TABLE `securityincident` DISABLE KEYS */;
INSERT INTO `securityincident` VALUES (1,1,'Firewall bypass detected.','High',2,'2024-02-20',NULL),(2,2,'Unauthorized switch access.','Medium',3,'2024-01-15','2024-01-18'),(3,3,'Server overheating issue.','Low',1,'2024-03-10',NULL),(4,4,'Access point signal interference.','Medium',4,'2024-02-28','2024-03-02'),(5,5,'IDS triggered multiple alerts.','Critical',5,'2024-03-05',NULL),(6,6,'Unauthorized storage access.','High',6,'2024-03-08','2024-03-12'),(7,7,'Router firmware outdated.','Medium',7,'2024-03-11',NULL),(8,8,'VPN connection failure.','High',8,'2024-03-14','2024-03-17'),(9,9,'Firewall misconfiguration detected.','Critical',9,'2024-03-18',NULL),(10,10,'Load balancer overload.','Medium',1,'2024-03-22','2024-03-25');
/*!40000 ALTER TABLE `securityincident` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `UID` int NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`UID`),
  UNIQUE KEY `email` (`email`),
  CONSTRAINT `user_chk_1` CHECK ((`role` in (_cp850'Admin',_cp850'IT Technician',_cp850'Security Officer')))
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'user1@network.com','password1','Admin'),(2,'user2@network.com','password2','IT Technician'),(3,'user3@network.com','password3','Security Officer'),(4,'user4@network.com','password4','IT Technician'),(5,'user5@network.com','password5','Admin'),(6,'user6@network.com','password6','Security Officer'),(7,'user7@network.com','password7','IT Technician'),(8,'user8@network.com','password8','Security Officer'),(9,'user9@network.com','password9','Admin'),(10,'user10@network.com','password10','IT Technician');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vendor`
--

DROP TABLE IF EXISTS `vendor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vendor` (
  `VID` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `contact_person` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `address` text,
  PRIMARY KEY (`VID`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendor`
--

LOCK TABLES `vendor` WRITE;
/*!40000 ALTER TABLE `vendor` DISABLE KEYS */;
INSERT INTO `vendor` VALUES (1,'Juniper Networks','Alice Johnson','alice@juniper.com','+111223344','789 Cloud St.'),(2,'Palo Alto Networks','Bob Williams','bob@paloalto.com','+222334455','456 Cyber Ave.'),(3,'Dell Technologies','Chris Evans','chris@dell.com','+333445566','321 Tech Hub.'),(4,'HP Enterprise','David Lee','david@hpe.com','+444556677','147 Server Lane.'),(5,'IBM','Emma Watson','emma@ibm.com','+555667788','369 AI Street.'),(6,'Aruba Networks','Frank Brown','frank@aruba.com','+666778899','258 Security Blvd.'),(7,'Check Point','Grace Kelly','grace@checkpoint.com','+777889900','147 Firewall St.'),(8,'Sophos','Henry Adams','henry@sophos.com','+888990011','357 Encryption Rd.'),(9,'F5 Networks','Ivy Scott','ivy@f5.com','+999001122','159 Load Balancer Ave.'),(10,'Netgear','Jack Daniels','jack@netgear.com','+000112233','852 Wireless┬áPkwy.');
/*!40000 ALTER TABLE `vendor` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-02  8:44:13
