-- MySQL dump 10.13  Distrib 5.7.18, for Linux (x86_64)
--
-- Host: localhost    Database: boerops_dev
-- ------------------------------------------------------
-- Server version	5.7.18-0ubuntu0.16.04.1

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
-- Table structure for table `deploys`
--

DROP TABLE IF EXISTS `deploys`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `deploys` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `project_id` int(10) unsigned NOT NULL,
  `user_id` int(10) unsigned NOT NULL,
  `version` varchar(64) COLLATE utf8mb4_bin NOT NULL COMMENT 'commit id',
  `mode` tinyint(1) unsigned DEFAULT '0' COMMENT '0-test30; 1-test31; 2-prod; 3-rollback',
  `status` tinyint(1) unsigned DEFAULT '0' COMMENT '0-input; 1-test; 2-test_result; 3-prod; 4-prod_result; 5release',
  `comment` text COLLATE utf8mb4_bin COMMENT 'release note',
  `result` tinyint(1) unsigned DEFAULT NULL COMMENT '0-success; 1-failed',
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='发布部署';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `hosts`
--

DROP TABLE IF EXISTS `hosts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `hosts` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `hostname` varchar(32) COLLATE utf8mb4_bin NOT NULL,
  `ip_address` varchar(32) COLLATE utf8mb4_bin NOT NULL,
  `ssh_port` int(8) unsigned NOT NULL DEFAULT '22',
  `username` varchar(32) COLLATE utf8mb4_bin NOT NULL,
  `password` varchar(64) COLLATE utf8mb4_bin DEFAULT NULL,
  `ssh_method` tinyint(1) DEFAULT '0' COMMENT '0-password;1-public key',
  `environ` tinyint(1) DEFAULT '0' COMMENT '0-30test;1-31test;2-prod',
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ip_address` (`ip_address`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='主机资产表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `projects`
--

DROP TABLE IF EXISTS `projects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `projects` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(64) COLLATE utf8mb4_bin NOT NULL,
  `repo_url` varchar(128) COLLATE utf8mb4_bin NOT NULL COMMENT 'git repo url',
  `checkout_dir` varchar(128) COLLATE utf8mb4_bin NOT NULL COMMENT '检出目录',
  `compile_dir` varchar(128) COLLATE utf8mb4_bin NOT NULL COMMENT '编译/打包/发布目录',
  `compile_cmd` text COLLATE utf8mb4_bin COMMENT '编译命令',
  `playbook_path` varchar(128) COLLATE utf8mb4_bin NOT NULL COMMENT 'ansible playbook yaml文件',
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='项目信息表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rel_host_project`
--

DROP TABLE IF EXISTS `rel_host_project`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rel_host_project` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned NOT NULL,
  `project_id` int(10) unsigned NOT NULL,
  `created_at` datetime NOT NULL COMMENT 'create time',
  `updated_at` datetime NOT NULL COMMENT 'update time',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='主机、项目关联';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `roles` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(32) COLLATE utf8mb4_bin NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='用户角色';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(64) COLLATE utf8mb4_bin NOT NULL,
  `password_hash` varchar(128) COLLATE utf8mb4_bin NOT NULL,
  `name` varchar(64) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '姓名',
  `role_id` int(10) unsigned NOT NULL,
  `email` varchar(64) COLLATE utf8mb4_bin DEFAULT NULL,
  `phone` varchar(16) COLLATE utf8mb4_bin DEFAULT NULL,
  `apikey` varchar(64) COLLATE utf8mb4_bin DEFAULT NULL,
  `created_at` datetime NOT NULL COMMENT 'create time',
  `updated_at` datetime NOT NULL COMMENT 'update time',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='用户信息';
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-06-28 18:27:38
