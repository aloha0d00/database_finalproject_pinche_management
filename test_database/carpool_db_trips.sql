-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: carpool_db
-- ------------------------------------------------------
-- Server version	8.0.43

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
-- Table structure for table `trips`
--

DROP TABLE IF EXISTS `trips`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `trips` (
  `id` int NOT NULL AUTO_INCREMENT,
  `driver_id` int NOT NULL,
  `vehicle_id` int NOT NULL,
  `departure_location` varchar(255) NOT NULL,
  `arrival_location` varchar(255) NOT NULL,
  `departure_time` datetime NOT NULL,
  `available_seats` int NOT NULL,
  `price_per_seat` decimal(10,2) NOT NULL,
  `trip_status` enum('pending','ongoing','completed','cancelled') NOT NULL DEFAULT 'pending',
  `description` text,
  `departure_latitude` float DEFAULT NULL,
  `departure_longitude` float DEFAULT NULL,
  `arrival_latitude` float DEFAULT NULL,
  `arrival_longitude` float DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `driver_id` (`driver_id`),
  KEY `vehicle_id` (`vehicle_id`),
  CONSTRAINT `trips_ibfk_1` FOREIGN KEY (`driver_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `trips_ibfk_2` FOREIGN KEY (`vehicle_id`) REFERENCES `vehicles` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trips`
--

LOCK TABLES `trips` WRITE;
/*!40000 ALTER TABLE `trips` DISABLE KEYS */;
INSERT INTO `trips` VALUES (1,1,1,'学校南门','北京西站','2024-12-25 08:00:00',4,20.00,'pending',NULL,NULL,NULL,NULL,NULL,'2025-12-19 14:44:04','2025-12-19 14:44:04'),(2,1,1,'学校北门','北京站','2024-12-25 09:30:00',3,15.00,'pending',NULL,NULL,NULL,NULL,NULL,'2025-12-19 14:44:04','2025-12-19 14:44:04'),(3,1,1,'学校东门','首都机场','2024-12-26 10:00:00',2,40.00,'pending',NULL,NULL,NULL,NULL,NULL,'2025-12-19 14:44:04','2025-12-19 14:44:04'),(4,1,1,'学校东门','市中心','2025-12-20 14:30:00',3,25.00,'pending',NULL,NULL,NULL,NULL,NULL,'2025-12-19 15:36:52','2025-12-19 15:36:52'),(5,1,1,'学校东门','市中心','2025-12-20 14:30:00',3,25.00,'pending',NULL,NULL,NULL,NULL,NULL,'2025-12-19 17:31:50','2025-12-19 17:31:50'),(6,1,1,'北京科技大学','中关村','2025-12-22 14:30:00',3,20.00,'pending',NULL,NULL,NULL,NULL,NULL,'2025-12-19 17:34:59','2025-12-19 17:34:59'),(7,1,1,'北京科技大学','国贸','2025-12-23 15:30:00',2,30.00,'pending',NULL,NULL,NULL,NULL,NULL,'2025-12-19 17:45:22','2025-12-19 17:45:22'),(8,1,1,'北京科技大学','国贸','2025-12-23 15:30:00',2,30.00,'pending',NULL,NULL,NULL,NULL,NULL,'2025-12-19 17:45:56','2025-12-19 17:45:56'),(9,1,1,'北京科技大学','国贸','2025-12-23 15:30:00',2,30.00,'pending',NULL,NULL,NULL,NULL,NULL,'2025-12-19 17:49:29','2025-12-19 17:49:29'),(10,1,1,'北京科技大学','国贸','2025-12-23 15:30:00',2,30.00,'pending',NULL,NULL,NULL,NULL,NULL,'2025-12-19 18:05:43','2025-12-19 18:05:43'),(12,20,1,'测试起点','测试终点','2025-12-21 02:48:07',4,20.00,'pending',NULL,NULL,NULL,NULL,NULL,'2025-12-19 18:48:07','2025-12-19 18:48:07'),(15,72,3,'北京','上海','2025-12-27 03:25:00',6,12.00,'pending',NULL,NULL,NULL,NULL,NULL,'2025-12-20 19:25:10','2025-12-20 19:27:33');
/*!40000 ALTER TABLE `trips` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-21  6:31:10
