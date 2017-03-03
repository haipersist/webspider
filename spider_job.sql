/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50711
Source Host           : localhost:3306
Source Database       : spider_job

Target Server Type    : MYSQL
Target Server Version : 50711
File Encoding         : 65001

Date: 2017-03-03 08:57:31
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for company
-- ----------------------------
DROP TABLE IF EXISTS `company`;
CREATE TABLE `company` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `address` varchar(255) DEFAULT NULL,
  `introduction` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `company` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of company
-- ----------------------------

-- ----------------------------
-- Table structure for jobs
-- ----------------------------
DROP TABLE IF EXISTS `jobs`;
CREATE TABLE `jobs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `welfare` varchar(255) DEFAULT '',
  `requirement` text NOT NULL,
  `link` varchar(255) NOT NULL COMMENT '\r\n\r\n\r\n\r\n\r\n\r\n',
  `company_id` int(11) DEFAULT NULL,
  `website_id` int(11) DEFAULT NULL,
  `pub_time` datetime NOT NULL,
  `load_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `salary` varchar(127) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `link` (`link`) USING BTREE,
  KEY `company_id` (`company_id`),
  KEY `website_id` (`website_id`),
  CONSTRAINT `jobs_ibfk_1` FOREIGN KEY (`company_id`) REFERENCES `company` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `jobs_ibfk_2` FOREIGN KEY (`website_id`) REFERENCES `website` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of jobs
-- ----------------------------

-- ----------------------------
-- Table structure for website
-- ----------------------------
DROP TABLE IF EXISTS `website`;
CREATE TABLE `website` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `website` varchar(255) NOT NULL,
  `homepage` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `website` (`website`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of website
-- ----------------------------
INSERT INTO `website` VALUES ('1', 'lagou', 'http://www.lagou.com');
INSERT INTO `website` VALUES ('2', 'dajie', 'http://www.dajie.com');
INSERT INTO `website` VALUES ('3', 'zhilian', 'http://www.zhaopin.com');
INSERT INTO `website` VALUES ('4', '51job', 'http://www.51job.com');
INSERT INTO `website` VALUES ('5', 'shuimu', 'http://www.newsmth.net/');
INSERT INTO `website` VALUES ('7', 'liepin', 'https://www.liepin.com');
