/*
Navicat MySQL Data Transfer

Source Server         : 192.168.1.97
Source Server Version : 50544
Source Host           : 192.168.1.97:3306
Source Database       : ljcms

Target Server Type    : MYSQL
Target Server Version : 50544
File Encoding         : 65001

Date: 2015-12-01 16:43:28
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `tip`
-- ----------------------------
DROP TABLE IF EXISTS `tip`;
CREATE TABLE `tip` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `method` varchar(200) NOT NULL,
  `content` varchar(1000) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `method` (`method`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of tip
-- ----------------------------
INSERT INTO `tip` VALUES ('1', 'default', '无提示\r\n\r\n');
INSERT INTO `tip` VALUES ('2', 'server', '1.增加服务器：加入新的服务器;\r\n2.查看已添加的服务器信息：IP、\r\n名称、组、账号、密码、ssh端口、状态;\r\n3.更新：修改已添加的服务器信息;\r\n4.删除：删除指定服务器信息');
INSERT INTO `tip` VALUES ('3', 'server_add', '填写IP、名称，选择组;\r\n填写服务器账号、密码端口;\r\n选择是否开启监控（5分钟收集一次数据）');
INSERT INTO `tip` VALUES ('4', 'server_edit', '同新增服务器');
INSERT INTO `tip` VALUES ('5', 'group', '1.增加服务器组：增加新的服务器组;\r\n2.查看已添加的服务器组信息：名称、描述、成员;\r\n3.更新：修改已添加的服务器组信息;\r\n4.删除：删除指定的组');
INSERT INTO `tip` VALUES ('6', 'group_add', '1.填写组名称：;\r\n2.填写组描述：;\r\n3.选择组员');
INSERT INTO `tip` VALUES ('7', 'group_edit', '同新增组');
INSERT INTO `tip` VALUES ('8', 'hardware', '通过ansible获得的facts查看服务器的硬件信息');
INSERT INTO `tip` VALUES ('9', 'software', '通过ansible获得的facts查看服务器的软件信息');
INSERT INTO `tip` VALUES ('10', 'server_configure', '列出所有服务器配置数目；\r\n点击配置管理可查看服务器具体配置');
INSERT INTO `tip` VALUES ('11', 'server_configure_manage', '列出服务器的配置;\r\n新建配置，更新，删除;\r\n查看配置信息');
INSERT INTO `tip` VALUES ('12', 'server_configure_manage_new', '输入配置名称提交即生成一个配置文件');
INSERT INTO `tip` VALUES ('13', 'server_configure_edit', '对配置的内容进行修改，语法参考ansible-playbook');
INSERT INTO `tip` VALUES ('14', 'server_configure_action', '确认执行配置');
INSERT INTO `tip` VALUES ('15', 'server_configure_result', '配置执行结果');
INSERT INTO `tip` VALUES ('16', 'server_configure_time', '配置的定时设置，参考crontab');
INSERT INTO `tip` VALUES ('17', 'server_configure_time_log', '配置任务日志列表');
INSERT INTO `tip` VALUES ('18', 'server_configure_time_logresult', '配置任务日志记录');
INSERT INTO `tip` VALUES ('19', 'group_configure', '服务器组的配置');
INSERT INTO `tip` VALUES ('20', 'group_configure_manage', '组内配置管理');
INSERT INTO `tip` VALUES ('21', 'group_configure_new', '新增组配置');
INSERT INTO `tip` VALUES ('22', 'group_configure_edit', '组配置编辑');
INSERT INTO `tip` VALUES ('23', 'group_configure_action', '组配置执行结果');
INSERT INTO `tip` VALUES ('24', 'group_configure_time', '组配置的定时设置，参考crontab');
INSERT INTO `tip` VALUES ('25', 'group_configure_time_log', '组配置任务日志列表');
INSERT INTO `tip` VALUES ('26', 'group_configure_time_logresult', '组配置任务日志记录');
INSERT INTO `tip` VALUES ('27', 'filelist', '文件列表');
INSERT INTO `tip` VALUES ('28', 'file_upload', '文件上传');
INSERT INTO `tip` VALUES ('29', 'file_edit', '文件内容编辑');
INSERT INTO `tip` VALUES ('30', 'server_monitor', '服务器监控');
INSERT INTO `tip` VALUES ('31', 'server_monitor_view', '服务器详细页');
INSERT INTO `tip` VALUES ('32', 'group_monitor', '服务器组监控');
INSERT INTO `tip` VALUES ('33', 'group_monitor_view', '服务器组详细页');
