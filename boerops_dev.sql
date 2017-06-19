-- --------------------------------------------------------
-- 主机:                           127.0.0.1
-- 服务器版本:                        5.7.17 - MySQL Community Server (GPL)
-- 服务器操作系统:                      Linux
-- HeidiSQL 版本:                  9.4.0.5174
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- 导出 boerops_dev 的数据库结构
CREATE DATABASE IF NOT EXISTS `boerops_dev` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin */;
USE `boerops_dev`;

-- 导出  表 boerops_dev.hosts 结构
CREATE TABLE IF NOT EXISTS `hosts` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `hostname` varchar(32) COLLATE utf8mb4_bin NOT NULL,
  `ip_address` varchar(32) COLLATE utf8mb4_bin NOT NULL,
  `ssh_port` int(8) unsigned NOT NULL DEFAULT '22',
  `username` varchar(32) COLLATE utf8mb4_bin NOT NULL,
  `password` varchar(64) COLLATE utf8mb4_bin DEFAULT NULL,
  `ssh_method` tinyint(1) DEFAULT '0' COMMENT '0-password;1-public key',
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ip_address` (`ip_address`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='主机资产表';

-- 数据导出被取消选择。
-- 导出  表 boerops_dev.projects 结构
CREATE TABLE IF NOT EXISTS `projects` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(64) COLLATE utf8mb4_bin NOT NULL,
  `repo_url` varchar(128) COLLATE utf8mb4_bin NOT NULL COMMENT 'git repo url',
  `checkout_dir` varchar(128) COLLATE utf8mb4_bin NOT NULL COMMENT '检出目录',
  `compile_dir` varchar(128) COLLATE utf8mb4_bin NOT NULL COMMENT '编译/打包/发布目录',
  `compile_cmd` text COLLATE utf8mb4_bin COMMENT '编译命令',
  `playbook_path` varchar(128) COLLATE utf8mb4_bin NOT NULL COMMENT 'ansible playbook yaml文件',
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='项目信息表';

-- 数据导出被取消选择。
-- 导出  表 boerops_dev.rel_host_project 结构
CREATE TABLE IF NOT EXISTS `rel_host_project` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned NOT NULL,
  `project_id` int(10) unsigned NOT NULL,
  `created_at` datetime NOT NULL COMMENT 'create time',
  `updated_at` datetime NOT NULL COMMENT 'update time',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='主机、项目关联';

-- 数据导出被取消选择。
-- 导出  表 boerops_dev.roles 结构
CREATE TABLE IF NOT EXISTS `roles` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(32) COLLATE utf8mb4_bin NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='用户角色';

-- 数据导出被取消选择。
-- 导出  表 boerops_dev.users 结构
CREATE TABLE IF NOT EXISTS `users` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(64) COLLATE utf8mb4_bin NOT NULL,
  `password_hash` varchar(128) COLLATE utf8mb4_bin NOT NULL,
  `name` varchar(64) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '姓名',
  `job` varchar(64) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '职位',
  `email` varchar(64) COLLATE utf8mb4_bin DEFAULT NULL,
  `phone` varchar(16) COLLATE utf8mb4_bin DEFAULT NULL,
  `apikey` varchar(64) COLLATE utf8mb4_bin DEFAULT NULL,
  `created_at` datetime NOT NULL COMMENT 'create time',
  `updated_at` datetime NOT NULL COMMENT 'update time',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='用户信息';

-- 数据导出被取消选择。
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
