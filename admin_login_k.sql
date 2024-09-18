
/*
Navicat MySQL Data Transfer
Source Server         : mysql
Source Server Version : 50532
Source Host           : localhost:3306
Source Database       : elder_care
Target Server Type    : MYSQL
Target Server Version : 50532
File Encoding         : 65001
Date: 2019-11-28 15:09:36
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `admin_login_k`
-- ----------------------------
DROP TABLE IF EXISTS `admin_login_k`;
CREATE TABLE `admin_login_k` (
  `admin_id` char(20) NOT NULL,
  `admin_pass` char(20) DEFAULT NULL,
  PRIMARY KEY (`admin_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of admin_login_k
-- ----------------------------
INSERT INTO `admin_login_k` VALUES ('admin', 'admin');

-- ----------------------------
-- Table structure for `elder_k`
-- ----------------------------
CREATE TABLE elder_k (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    gender VARCHAR(10),
    age INT,
    health_status VARCHAR(255)
);

-- ----------------------------
-- Table structure for `service_records_k`
-- ----------------------------
DROP TABLE IF EXISTS `service_records_k`;

CREATE TABLE service_records_k (
  id INT AUTO_INCREMENT PRIMARY KEY,
  elder_id INT NOT NULL,
  service_id INT NOT NULL,
  service_date DATE DEFAULT NULL,
  staff_id INT NOT NULL,
  FOREIGN KEY (elder_id) REFERENCES elder_k(id),
  FOREIGN KEY (service_id) REFERENCES services_k(id),
  FOREIGN KEY (staff_id) REFERENCES staff_k(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- ----------------------------
-- Table structure for `staff_k`
-- ----------------------------
CREATE TABLE staff_k (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    position VARCHAR(50),
    contact VARCHAR(50),
    service_id INT,
    FOREIGN KEY (service_id) REFERENCES services_k(id)
);

-- ----------------------------
-- Table structure for `elder_login`
-- ----------------------------
CREATE TABLE elder_login (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) UNIQUE,
    password VARCHAR(50)
);

-- ----------------------------
-- Table structure for `services_k`
-- ----------------------------
CREATE TABLE services_k (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    is_public BOOLEAN NOT NULL DEFAULT 0
);

-- ----------------------------
-- Table structure for `bookings_k`
-- ----------------------------
CREATE TABLE bookings_k (
    id INT AUTO_INCREMENT PRIMARY KEY,
    elder_id INT,
    service_id INT,
    booking_date DATE,
    status VARCHAR(255) DEFAULT 'pending',
    staff_id INT,
    FOREIGN KEY (elder_id) REFERENCES elder_k(id),
    FOREIGN KEY (service_id) REFERENCES services_k(id),
    FOREIGN KEY (staff_id) REFERENCES staff_k(id)
);

-- 插入 services_k 表的数据（包含非公共服务）
INSERT INTO `services_k` (id, name, description, is_public) VALUES
(1, '定期身体检查', '健康检查服务', 0),
(2, '血压测量', '健康监测服务', 0),
(3, '健康咨询', '健康指导服务', 0),
(4, '医疗上门服务', '医疗护理服务', 0),
(5, '康复治疗', '康复服务', 0),
(6, '医生上门服务', '医疗服务', 0),
(7, '护理上门服务', '护理服务', 0),
(8, '个人卫生护理', '日常护理服务', 0),
(9, '物理治疗', '康复服务', 0),
(10, '康复治疗', '康复服务', 0),
(11, '语言治疗', '康复服务', 0),
(12, '心理辅导治疗', '心理辅导服务', 0),
(13, '术后康复治疗', '康复服务', 0),
(14, '营养配餐服务', '健康服务', 1),
(15, '助行器康复服务', '康复服务', 0),
(16, '家庭护理', '护理服务', 0),
(17, '药物管理', '健康服务', 0),
(18, '活动安排', '休闲娱乐服务', 1),
(19, '瑜伽', '休闲娱乐服务', 1),
(20, '太极', '休闲娱乐服务', 1),
(21, '社区聚会', '社交活动', 1),
(22, '老年大学', '社交活动', 1),
(23, '生日和节日庆祝活动', '社交活动', 1),
(24, '健身活动', '休闲娱乐服务', 1),
(25, '图书馆服务', '休闲娱乐服务', 1),
(26, '康乐活动服务', '休闲娱乐服务', 1),
(27, '家庭维修服务', '家政服务', 0);

-- 插入 staff_k 表的数据
INSERT INTO `staff_k` (id, name, position, contact, service_id) VALUES
(1, '张三', '护士', '1234567890', 2),
(2, '李四', '医生', '2345678901', 4),
(3, '王五', '理疗师', '3456789012', 5),
(4, '赵六', '护士', '4567890123', 7),
(5, '孙七', '理疗师', '5678901234', 9),
(6, '周八', '医生', '6789012345', 1),
(7, '吴九', '医生', '7890123456', 3),
(8, '郑十', '护士', '8901234567', 6),
(9, '冯十一', '医生', '9012345678', 8),
(10, '蒋十二', '心理辅导', '0123456789', 12);
(11, '李晨', '护士', '1111111111', 1),
(12, '张瑶', '医生', '2222222222', 1),
(13, '王磊', '健康咨询师', '3333333333', 2),
(14, '赵丽', '护士', '4444444444', 2),
(15, '钱峰', '健康咨询师', '5555555555', 3),
(16, '孙红', '医生', '6666666666', 3),
(17, '周杰', '医生', '7777777777', 4),
(18, '吴倩', '护士', '8888888888', 4),
(19, '郑翔', '理疗师', '9999999999', 5),
(20, '刘涛', '医生', '1010101010', 5),
(21, '金敏', '护士', '1110111011', 6),
(22, '黄强', '医生', '1212121212', 6),
(23, '吴静', '护士', '1313131313', 7),
(24, '杨伟', '医生', '1414141414', 7),
(25, '陈曦', '护理员', '1515151515', 8),
(26, '朱莹', '护理员', '1616161616', 8),
(27, '秦阳', '理疗师', '1717171717', 9),
(28, '何晴', '理疗师', '1818181818', 9),
(29, '高晨', '康复师', '1919191919', 10),
(30, '曹宁', '康复师', '2020202020', 10),
(31, '韩冰', '语言治疗师', '2121212121', 11),
(32, '邹悦', '语言治疗师', '2222222222', 11),
(33, '林峰', '心理治疗师', '2323232323', 12),
(34, '马丽', '心理治疗师', '2424242424', 12),
(35, '徐亮', '康复师', '2525252525', 13),
(36, '陶静', '康复师', '2626262626', 13),
(37, '田野', '护理员', '2727272727', 16),
(38, '段莹', '护理员', '2828282828', 16),
(39, '石杰', '药剂师', '2929292929', 17),
(40, '顾悦', '药剂师', '3030303030', 17),
(41, '孟超', '维修工', '3131313131', 27),
(42, '罗琳', '维修工', '3232323232', 27);

-- 插入更多老人的信息
INSERT INTO `elder_k` (name, gender, age, health_status) VALUES
('侯欣雨', '女', 72, '良好'),
('樊琪', '男', 75, '一般'),
('陈如意', '女', 68, '良好'),
('沈棋', '男', 80, '良好'),
('徐谢书', '女', 77, '一般'),
('薛鹏宇', '男', 74, '良好'),
('白云鹤', '女', 73, '差'),
('时继伟', '男', 79, '良好'),
('黄炀齐', '女', 71, '一般'),
('马新彬', '男', 76, '差'),
('徐瑞良', '女', 78, '良好'),
('王赛权', '男', 81, '一般'),
('周天', '女', 70, '良好'),
('段宇翔', '男', 82, '良好'),
('宋康齐', '女', 69, '良好'),
('李家豪', '男', 75, '一般');



ALTER TABLE service_records_k MODIFY staff_id INT NULL;
ALTER TABLE bookings_k MODIFY staff_id INT NULL;
