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
-- Table structure for table `participants`
--

DROP TABLE IF EXISTS `participants`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `participants` (
  `id` int NOT NULL AUTO_INCREMENT,
  `trip_id` int NOT NULL,
  `user_id` int NOT NULL,
  `seats_booked` int NOT NULL DEFAULT '1',
  `participant_status` enum('pending','accepted','rejected','completed','cancelled') NOT NULL DEFAULT 'pending',
  `payment_status` enum('unpaid','paid','refunded') NOT NULL DEFAULT 'unpaid',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_participant` (`trip_id`,`user_id`,`participant_status`),
  KEY `idx_trip_id` (`trip_id`),
  KEY `idx_user_id` (`user_id`),
  CONSTRAINT `participants_ibfk_1` FOREIGN KEY (`trip_id`) REFERENCES `trips` (`id`) ON DELETE CASCADE,
  CONSTRAINT `participants_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `participants`
--

LOCK TABLES `participants` WRITE;
/*!40000 ALTER TABLE `participants` DISABLE KEYS */;
INSERT INTO `participants` VALUES (1,1,4,1,'pending','unpaid','2025-12-19 14:55:53','2025-12-19 14:55:53'),(2,1,5,1,'pending','unpaid','2025-12-19 14:59:20','2025-12-19 14:59:20'),(3,2,5,1,'pending','unpaid','2025-12-19 15:00:08','2025-12-19 15:00:08'),(5,4,5,1,'pending','unpaid','2025-12-19 18:13:04','2025-12-19 18:13:04'),(6,7,15,1,'pending','unpaid','2025-12-19 18:18:02','2025-12-19 18:18:02'),(7,10,5,1,'pending','unpaid','2025-12-19 18:35:39','2025-12-19 18:35:39'),(8,8,5,1,'pending','unpaid','2025-12-19 18:35:42','2025-12-19 18:35:42'),(9,12,21,1,'pending','unpaid','2025-12-19 18:48:07','2025-12-19 18:48:07'),(10,12,5,1,'pending','unpaid','2025-12-19 18:59:20','2025-12-19 18:59:20'),(11,9,5,1,'pending','unpaid','2025-12-19 18:59:22','2025-12-19 18:59:22'),(13,7,65,1,'cancelled','unpaid','2025-12-20 16:33:23','2025-12-20 17:36:17'),(14,9,65,1,'cancelled','unpaid','2025-12-20 16:33:26','2025-12-20 17:36:15'),(15,10,65,1,'cancelled','unpaid','2025-12-20 16:33:27','2025-12-20 17:36:12'),(23,12,65,1,'cancelled','unpaid','2025-12-20 17:50:45','2025-12-20 17:50:50'),(33,15,65,1,'accepted','unpaid','2025-12-20 19:27:10','2025-12-20 19:27:33');
/*!40000 ALTER TABLE `participants` ENABLE KEYS */;
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
