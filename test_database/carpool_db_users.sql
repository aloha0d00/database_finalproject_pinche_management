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
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `student_id` varchar(20) DEFAULT NULL,
  `name` varchar(50) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  `avatar` varchar(255) DEFAULT NULL,
  `role` enum('student','driver','admin') NOT NULL DEFAULT 'student',
  `status` enum('active','inactive','banned') NOT NULL DEFAULT 'active',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `phone` (`phone`),
  UNIQUE KEY `student_id` (`student_id`),
  UNIQUE KEY `student_id_2` (`student_id`)
) ENGINE=InnoDB AUTO_INCREMENT=80 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'2021001','测试学生','13800138001',NULL,'$2b$12$r//XfFUxD/A6XX9dXIHnPepk/iGrr6mk7oINVozjKEqYDQbn6kWdm',NULL,'student','active','2025-12-19 14:44:04','2025-12-20 18:03:14'),(2,'2021002','李四','13800138002',NULL,'$2b$12$S5G3E5F7H9J1K3L5M7N9O',NULL,'student','active','2025-12-19 14:44:04','2025-12-19 14:44:04'),(4,'2021004','??','13800138004',NULL,'$2b$12$.86sUgR3g4U269XbBFkMKew8MOJyzy4BENFEJsEH1VL32DgvWg63K',NULL,'student','active','2025-12-19 14:53:00','2025-12-19 14:53:00'),(5,'202301','12','11111111111',NULL,'$2b$12$WUtnOK4QlVyNEFuGlBAhCO0ulIxT1ekMnCPeg.fNYnCfziGP23B1W',NULL,'student','active','2025-12-19 14:59:08','2025-12-19 14:59:08'),(14,'20210001','张三','13800138008',NULL,'$2b$12$VwIUZ/zFYUyem4Z2piJUkeqBhjbDHtkl2qNx6x31XX1cObQJO9k.6',NULL,'student','active','2025-12-19 17:49:02','2025-12-19 17:49:02'),(15,NULL,'耿昊','13354795027',NULL,'$2b$12$aAVpdMHZ4PHLUlv8bksycOu9V01t.bvrEzTiQE8P3ZVAlR0cHqwkO',NULL,'driver','active','2025-12-19 18:09:00','2025-12-19 18:09:00'),(20,NULL,'测试司机','13800000001',NULL,'$2b$12$zDR936/SvxJteCQvwqBL4eD48qeK3J6llmRNKKXsi6YYg/Jpz3C9q',NULL,'driver','active','2025-12-19 18:48:06','2025-12-19 18:48:06'),(21,'2024002','测试学生','13900000001',NULL,'$2b$12$q4h.s3uW8Us8vJpHFo6fo.7JZ4hIE1Osw8XrtptJBaaGBrNfyDC76',NULL,'student','active','2025-12-19 18:48:07','2025-12-19 18:48:07'),(65,'1','1','1',NULL,'$2b$12$uK42ui5M05mJEBR90D9UjuH.tJgo5MKEbf7ctqWljAm4KbRfBPNSS',NULL,'student','active','2025-12-20 16:33:18','2025-12-20 16:33:18'),(67,'11','1','11',NULL,'$2b$12$D5cuGWEwNGBrll4Y.RzY9OgTlDKTc5EMRweTi8cn1J.G1Qyi.x6dC',NULL,'student','active','2025-12-20 16:48:37','2025-12-20 16:48:37'),(69,NULL,'测试司机','13900139001',NULL,'$2b$12$4049CAZJlTA0AbAGwpFzVu8HG0CbSdzRmt9nB6hAqo8GIh1BjxEQ6',NULL,'driver','active','2025-12-20 18:03:14','2025-12-20 18:03:14'),(72,NULL,'111','111',NULL,'$2b$12$s7ZpDl92zJBqbsk2SjZwk.7NPY5MiTBfgJ90IaSiIUXkZ72TpSkKi',NULL,'driver','active','2025-12-20 19:20:58','2025-12-20 19:20:58');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
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
