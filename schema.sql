-- MySQL dump 10.13  Distrib 5.5.57, for Linux (x86_64)
--
-- Host: 35.154.141.143    Database: gps_development
-- ------------------------------------------------------
-- Server version	5.5.57

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `SequelizeMeta`
--

DROP TABLE IF EXISTS `SequelizeMeta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `SequelizeMeta` (
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`name`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `SequelizeMeta_name_unique` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `alerts`
--

DROP TABLE IF EXISTS `alerts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alerts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `alert_type` varchar(255) DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  `vehicle_no` varchar(255) DEFAULT NULL,
  `truck_history_id` int(11) DEFAULT NULL,
  `createdAt` datetime NOT NULL,
  `updatedAt` datetime NOT NULL,
  `alert_msg` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `vehicle_no` (`vehicle_no`),
  KEY `truck_history_id` (`truck_history_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7784501 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `daily_histories`
--

DROP TABLE IF EXISTS `daily_histories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `daily_histories` (
  `date` datetime DEFAULT NULL,
  `vehicle_no` varchar(255) NOT NULL DEFAULT '',
  `running_time` int(11) DEFAULT NULL,
  `stop_time` int(11) DEFAULT NULL,
  `idle_time` int(11) DEFAULT NULL,
  `distance_travelled` decimal(10,2) DEFAULT NULL,
  `start_landmark` varchar(255) DEFAULT NULL,
  `end_landmark` varchar(255) DEFAULT NULL,
  `start_state` varchar(255) DEFAULT NULL,
  `end_state` varchar(255) DEFAULT NULL,
  `start_date` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `end_date` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `overspeed_instances` decimal(10,2) DEFAULT NULL,
  `max_speed` decimal(10,2) DEFAULT NULL,
  `odometer_km` decimal(10,2) DEFAULT NULL,
  `n_running` int(11) DEFAULT NULL,
  `n_stop_time` int(11) DEFAULT NULL,
  `n_idle_time` int(11) DEFAULT NULL,
  `n_distance_travelled` decimal(10,2) DEFAULT NULL,
  `n_odometer_km` decimal(10,2) DEFAULT NULL,
  `max_timestamp` decimal(10,2) DEFAULT NULL,
  `count` int(11) DEFAULT NULL,
  `createdAt` datetime NOT NULL,
  `updatedAt` datetime NOT NULL,
  PRIMARY KEY (`vehicle_no`,`start_date`,`end_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `daily_populator_logger`
--

DROP TABLE IF EXISTS `daily_populator_logger`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `daily_populator_logger` (
  `date` datetime DEFAULT NULL,
  `vehicle_no` varchar(255) NOT NULL DEFAULT '',
  `job` varchar(255) NOT NULL DEFAULT '',
  `start_date` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `end_date` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `count` int(11) DEFAULT NULL,
  `createdAt` datetime DEFAULT NULL,
  `updatedAt` datetime DEFAULT NULL,
  PRIMARY KEY (`vehicle_no`,`job`,`start_date`,`end_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `device_histories`
--

DROP TABLE IF EXISTS `device_histories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `device_histories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `IMEI` varchar(255) DEFAULT NULL,
  `vehicle_no` varchar(255) DEFAULT NULL,
  `phone_number` varchar(255) DEFAULT NULL,
  `createdAt` datetime NOT NULL,
  `updatedAt` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `IMEI` (`IMEI`),
  CONSTRAINT `device_histories_ibfk_1` FOREIGN KEY (`IMEI`) REFERENCES `devices` (`IMEI`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11299 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `devices`
--

DROP TABLE IF EXISTS `devices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `devices` (
  `IMEI` varchar(255) NOT NULL DEFAULT '',
  `GSM_phone_number` varchar(255) DEFAULT NULL,
  `createdAt` datetime NOT NULL,
  `updatedAt` datetime NOT NULL,
  `vehicle_no` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`IMEI`),
  UNIQUE KEY `uc_vehicle` (`vehicle_no`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `duration_based_histories`
--

DROP TABLE IF EXISTS `duration_based_histories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `duration_based_histories` (
  `vehicle_no` varchar(255) NOT NULL DEFAULT '',
  `distance_travelled` decimal(10,2) DEFAULT NULL,
  `avg_speed` decimal(10,2) DEFAULT NULL,
  `start_timestamp` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `end_timestamp` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `start_landmark` varchar(255) DEFAULT NULL,
  `end_landmark` varchar(255) DEFAULT NULL,
  `old_state` varchar(255) DEFAULT NULL,
  `new_state` varchar(255) DEFAULT NULL,
  `duration` int(11) DEFAULT NULL,
  `distance_km` decimal(10,2) DEFAULT NULL,
  `createdAt` datetime NOT NULL,
  `updatedAt` datetime NOT NULL,
  `end_lat` decimal(10,6) DEFAULT NULL,
  `end_long` decimal(10,6) DEFAULT NULL,
  `start_lat` decimal(10,6) DEFAULT NULL,
  `start_long` decimal(10,6) DEFAULT NULL,
  `old_distance_km` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`vehicle_no`,`start_timestamp`,`end_timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `look_up_histories`
--

DROP TABLE IF EXISTS `look_up_histories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `look_up_histories` (
  `latitude` decimal(10,6) NOT NULL DEFAULT '0.000000',
  `longitude` decimal(10,6) NOT NULL DEFAULT '0.000000',
  `landmark` varchar(255) DEFAULT NULL,
  `createdAt` datetime NOT NULL,
  `updatedAt` datetime NOT NULL,
  PRIMARY KEY (`latitude`,`longitude`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `look_up_histories2`
--

DROP TABLE IF EXISTS `look_up_histories2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `look_up_histories2` (
  `latitude` decimal(10,6) NOT NULL DEFAULT '0.000000',
  `longitude` decimal(10,6) NOT NULL DEFAULT '0.000000',
  `landmark` varchar(255) DEFAULT NULL,
  `createdAt` datetime NOT NULL,
  `updatedAt` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `new_poi_histories`
--

DROP TABLE IF EXISTS `new_poi_histories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `new_poi_histories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `vehicle_no` varchar(255) NOT NULL,
  `enter_time` datetime NOT NULL,
  `exit_time` datetime NOT NULL,
  `poi_id` int(11) NOT NULL,
  `trip_id` varchar(255) DEFAULT NULL,
  `createdAt` datetime NOT NULL,
  `updatedAt` datetime NOT NULL,
  `entry_lat` decimal(10,6) DEFAULT NULL,
  `entry_long` decimal(10,6) DEFAULT NULL,
  `exit_lat` decimal(10,6) DEFAULT NULL,
  `exit_long` decimal(10,6) DEFAULT NULL,
  `exit_inside_poi` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `poi_histories`
--

DROP TABLE IF EXISTS `poi_histories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `poi_histories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `vehicle_no` varchar(255) DEFAULT NULL,
  `enter_time` datetime DEFAULT NULL,
  `exit_time` datetime DEFAULT NULL,
  `createdAt` datetime NOT NULL,
  `updatedAt` datetime NOT NULL,
  `poi_id` int(11) DEFAULT NULL,
  `trip_id` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `poi_id` (`poi_id`),
  KEY `trip_id` (`trip_id`),
  CONSTRAINT `poi_histories_ibfk_2` FOREIGN KEY (`poi_id`) REFERENCES `pois` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `poi_histories_ibfk_3` FOREIGN KEY (`trip_id`) REFERENCES `trips` (`trip_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2975383 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pois`
--

DROP TABLE IF EXISTS `pois`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pois` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `latitude` decimal(10,6) DEFAULT NULL,
  `longitude` decimal(10,6) DEFAULT NULL,
  `radius` decimal(10,2) DEFAULT NULL,
  `poi_nick_name` varchar(255) DEFAULT NULL,
  `poi_act_name` varchar(255) DEFAULT NULL,
  `mrole_id` int(11) DEFAULT NULL,
  `mrole_type` varchar(255) DEFAULT NULL,
  `createdAt` datetime NOT NULL,
  `updatedAt` datetime NOT NULL,
  `poi_type` varchar(255) DEFAULT NULL,
  `poi_bounds` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7862 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `route_mapping`
--

DROP TABLE IF EXISTS `route_mapping`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `route_mapping` (
  `route` varchar(255) DEFAULT NULL,
  `type` varchar(255) DEFAULT NULL,
  `object` varchar(255) DEFAULT NULL,
  `instance` varchar(255) DEFAULT NULL,
  `case` varchar(255) DEFAULT NULL,
  `createdAt` datetime NOT NULL,
  `updatedAt` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `route_mappings`
--

DROP TABLE IF EXISTS `route_mappings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `route_mappings` (
  `route` varchar(255) DEFAULT NULL,
  `type` varchar(255) DEFAULT NULL,
  `object` varchar(255) DEFAULT NULL,
  `instance` varchar(255) DEFAULT NULL,
  `case` varchar(255) DEFAULT NULL,
  `createdAt` datetime NOT NULL,
  `updatedAt` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `schema_migrations`
--

DROP TABLE IF EXISTS `schema_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `schema_migrations` (
  `version` varchar(255) NOT NULL,
  UNIQUE KEY `unique_schema_migrations` (`version`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `trip_pois`
--

DROP TABLE IF EXISTS `trip_pois`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `trip_pois` (
  `createdAt` datetime NOT NULL,
  `updatedAt` datetime NOT NULL,
  `poi_id` int(11) NOT NULL DEFAULT '0',
  `trip_id` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`poi_id`,`trip_id`),
  KEY `trip_id` (`trip_id`),
  CONSTRAINT `trip_pois_ibfk_1` FOREIGN KEY (`poi_id`) REFERENCES `pois` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `trip_pois_ibfk_2` FOREIGN KEY (`trip_id`) REFERENCES `trips` (`trip_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `trip_trucks`
--

DROP TABLE IF EXISTS `trip_trucks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `trip_trucks` (
  `createdAt` datetime NOT NULL,
  `updatedAt` datetime NOT NULL,
  `trip_id` varchar(255) NOT NULL DEFAULT '',
  `vehicle_no` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`trip_id`,`vehicle_no`),
  KEY `vehicle_no` (`vehicle_no`),
  CONSTRAINT `trip_trucks_ibfk_1` FOREIGN KEY (`trip_id`) REFERENCES `trips` (`trip_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `trip_trucks_ibfk_2` FOREIGN KEY (`vehicle_no`) REFERENCES `trucks` (`vehicle_no`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `trips`
--

DROP TABLE IF EXISTS `trips`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `trips` (
  `trip_id` varchar(255) NOT NULL DEFAULT '',
  `start_date` datetime DEFAULT NULL,
  `end_date` datetime DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `createdAt` datetime NOT NULL,
  `updatedAt` datetime NOT NULL,
  PRIMARY KEY (`trip_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `truck_histories`
--

DROP TABLE IF EXISTS `truck_histories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `truck_histories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `latitude` float(15,9) DEFAULT NULL,
  `longitude` float(15,9) DEFAULT NULL,
  `speed` decimal(10,2) DEFAULT NULL,
  `landmark` varchar(255) DEFAULT NULL,
  `GPStimestamp` datetime DEFAULT NULL,
  `status_code` int(11) DEFAULT NULL,
  `ignition_state` tinyint(1) DEFAULT NULL,
  `raw_data` varchar(255) DEFAULT NULL,
  `odometer_km` decimal(10,2) DEFAULT NULL,
  `distance_km` decimal(10,2) DEFAULT NULL,
  `GSM_signal_strength` decimal(10,2) DEFAULT NULL,
  `battery_level` decimal(10,2) DEFAULT NULL,
  `power_status_high` tinyint(1) DEFAULT NULL,
  `alert_data` varchar(255) DEFAULT NULL,
  `signal_strength` int(11) DEFAULT NULL,
  `battery_voltage` decimal(10,2) DEFAULT NULL,
  `accelerometer_status_high` tinyint(1) DEFAULT NULL,
  `idle_time` bigint(20) DEFAULT NULL,
  `moving_time` bigint(20) DEFAULT NULL,
  `createdAt` datetime NOT NULL,
  `updatedAt` datetime NOT NULL,
  `vehicle_no` varchar(255) DEFAULT NULL,
  `gps_timestamp` datetime DEFAULT NULL,
  `state` varchar(255) DEFAULT NULL,
  `stop_time` bigint(20) DEFAULT NULL,
  `ist_timestamp` datetime DEFAULT NULL,
  `is_scraped` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `createdAt` (`createdAt`),
  KEY `ist_timestamp` (`ist_timestamp`),
  KEY `gps_timestamp` (`gps_timestamp`),
  KEY `lat_long_index` (`latitude`,`longitude`),
  KEY `GPStimestamp` (`GPStimestamp`),
  KEY `vehicle_ts` (`vehicle_no`,`ist_timestamp`),
  CONSTRAINT `truck_histories_ibfk_1` FOREIGN KEY (`vehicle_no`) REFERENCES `trucks` (`vehicle_no`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=136872304 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `trucks`
--

DROP TABLE IF EXISTS `trucks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `trucks` (
  `vehicle_no` varchar(255) NOT NULL DEFAULT '',
  `latitude` float(15,9) DEFAULT NULL,
  `longitude` float(15,9) DEFAULT NULL,
  `landmark` varchar(255) DEFAULT NULL,
  `speed` decimal(10,2) DEFAULT NULL,
  `odometer_km` decimal(10,2) DEFAULT NULL,
  `distance_km` decimal(10,2) DEFAULT NULL,
  `speed_limit` decimal(10,2) DEFAULT '60.00',
  `last_stop_time` int(11) DEFAULT NULL,
  `last_start_time` int(11) DEFAULT NULL,
  `last_ignition_on_hours` decimal(10,2) DEFAULT NULL,
  `last_ignition_off_hours` decimal(10,2) DEFAULT NULL,
  `last_ignition_on_time` varchar(255) DEFAULT NULL,
  `last_ignition_off_time` varchar(255) DEFAULT NULL,
  `battery_level` decimal(10,2) DEFAULT NULL,
  `power_status_high` tinyint(1) DEFAULT NULL,
  `alert_data` varchar(255) DEFAULT NULL,
  `signal_strength` int(11) DEFAULT NULL,
  `battery_voltage` decimal(10,2) DEFAULT NULL,
  `accelerometer_status_high` tinyint(1) DEFAULT NULL,
  `idle_time` bigint(20) DEFAULT NULL,
  `moving_time` bigint(20) DEFAULT NULL,
  `gps_timestamp` datetime DEFAULT NULL,
  `state` varchar(255) DEFAULT NULL,
  `createdAt` datetime NOT NULL,
  `updatedAt` datetime NOT NULL,
  `stop_time` bigint(20) DEFAULT NULL,
  `ist_timestamp` datetime DEFAULT NULL,
  `is_scraped` tinyint(1) DEFAULT NULL,
  `is_disconnected` tinyint(1) DEFAULT NULL,
  `IMEI` varchar(255) DEFAULT NULL,
  `is_sim` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`vehicle_no`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `vehicle_no` varchar(255) NOT NULL DEFAULT '',
  `user_id` int(11) NOT NULL,
  `createdAt` datetime NOT NULL,
  `updatedAt` datetime NOT NULL,
  PRIMARY KEY (`vehicle_no`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vehicle_pois`
--

DROP TABLE IF EXISTS `vehicle_pois`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vehicle_pois` (
  `createdAt` datetime NOT NULL,
  `updatedAt` datetime NOT NULL,
  `poi_id` int(11) NOT NULL DEFAULT '0',
  `vehicle_no` varchar(255) NOT NULL DEFAULT '',
  `is_active` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`poi_id`,`vehicle_no`),
  KEY `vehicle_no` (`vehicle_no`),
  CONSTRAINT `vehicle_pois_ibfk_1` FOREIGN KEY (`poi_id`) REFERENCES `pois` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `vehicle_pois_ibfk_2` FOREIGN KEY (`vehicle_no`) REFERENCES `trucks` (`vehicle_no`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-12-02 13:57:59
