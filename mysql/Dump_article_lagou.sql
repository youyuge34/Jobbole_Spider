-- MySQL dump 10.13  Distrib 5.7.9, for osx10.9 (x86_64)
--
-- Host: localhost    Database: test
-- ------------------------------------------------------
-- Server version	5.7.9

/*!40101 SET @OLD_CHARACTER_SET_CLIENT = @@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS = @@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION = @@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE = @@TIME_ZONE */;
/*!40103 SET TIME_ZONE = '+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS = @@UNIQUE_CHECKS, UNIQUE_CHECKS = 0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS = @@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS = 0 */;
/*!40101 SET @OLD_SQL_MODE = @@SQL_MODE, SQL_MODE = 'NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES = @@SQL_NOTES, SQL_NOTES = 0 */;

--
-- Table structure for table `article_lagou`
--

DROP TABLE IF EXISTS `article_lagou`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `article_lagou` (
  `url`               VARCHAR(300) NOT NULL,
  `url_object_id`     VARCHAR(50)  NOT NULL,
  `title`             VARCHAR(100) NOT NULL,
  `salary`            VARCHAR(20)   DEFAULT NULL,
  `job_city`          VARCHAR(10)   DEFAULT NULL,
  `work_years`        VARCHAR(100)  DEFAULT NULL,
  `degree_need`       VARCHAR(30)   DEFAULT NULL,
  `job_type`          VARCHAR(20)   DEFAULT NULL,
  `publish_time`      VARCHAR(20)  NOT NULL,
  `tags`              VARCHAR(100)  DEFAULT NULL,
  `job_advantage`     VARCHAR(1000) DEFAULT NULL,
  `job_desc`          LONGTEXT     NOT NULL,
  `job_addr`          VARCHAR(50)   DEFAULT NULL,
  `company_url`       VARCHAR(300)  DEFAULT NULL,
  `company_name`      VARCHAR(100)  DEFAULT NULL,
  `crawl_time`        DATETIME     NOT NULL,
  `crawl_update_time` DATETIME      DEFAULT NULL,
  PRIMARY KEY (`url_object_id`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE = @OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE = @OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS = @OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS = @OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT = @OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS = @OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION = @OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES = @OLD_SQL_NOTES */;

-- Dump completed on 2017-09-26 12:34:27
