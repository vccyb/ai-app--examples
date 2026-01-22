-- ============================================
-- 推送配置更新 SQL
-- 根据外部推送平台接口文档优化配置参数
-- ============================================

-- 注意：执行前请备份数据库
-- mysqldump -u root -p push_system > backup.sql

-- ============================================
-- 方案一：删除旧配置，插入新配置（推荐）
-- ============================================

-- 1. 删除旧的推送配置
DELETE FROM push_config WHERE platform_code IN ('W3_TODO', 'WELINK_APP');

-- 2. 插入新的推送配置（根据外部接口文档）

-- W3 待办配置 - QA_REPORT
INSERT INTO push_config (business_type_id, platform_code, enabled, config_json) VALUES
(1, 'W3_TODO', 1, '{
  "appName": "QA报告系统",
  "appURL": "http://w3-beta.huawei.com",
  "type": "J2EE",
  "reserve1": "",
  "reserve2": "qa_report",
  "reserve10": "0"
}');

-- W3 待办配置 - TEST_REPORT
INSERT INTO push_config (business_type_id, platform_code, enabled, config_json) VALUES
(2, 'W3_TODO', 1, '{
  "appName": "测试报告系统",
  "appURL": "http://w3-beta.huawei.com",
  "type": "J2EE",
  "reserve1": "",
  "reserve2": "test_report",
  "reserve10": "0"
}');

-- WeLink 应用号配置 - TEST_REPORT
INSERT INTO push_config (business_type_id, platform_code, enabled, config_json) VALUES
(2, 'WELINK_APP', 1, '{
  "app_id": "com.huawei.feed",
  "theme_id": "d99b0ccaad7a4395b5f2aa558218dc9c",
  "templateNo": "20251223000522",
  "from_user_account": "z00512371",
  "type": "1",
  "displayType": "text",
  "noticeType": 1
}');


{
  "appName": "测试报告系统",
  "appURL": "http://w3-beta.huawei.com",
  "type": "J2EE",
  "reserve1": "",
  "reserve2": "test_report",
  "reserve10": "0"
}

{
  "appName": "测试报告系统",
  "appURL": "http://w3-beta.huawei.com",
  "type": "J2EE",
  "reserve1": "",
  "reserve2": "test_report",
  "reserve10": "0"
}

-- ============================================
-- 方案二：使用 UPDATE 语句更新现有配置（可选）
-- ============================================

-- 如果不想删除重建，可以使用 UPDATE 语句更新现有配置

-- 更新 W3_TODO 配置 - QA_REPORT
-- UPDATE push_config
-- SET config_json = '{
--   "appName": "QA报告系统",
--   "appURL": "http://w3-beta.huawei.com",
--   "type": "J2EE",
--   "reserve1": "",
--   "reserve2": "qa_report",
--   "reserve10": "0"
-- }'
-- WHERE business_type_id = 1 AND platform_code = 'W3_TODO';

-- 更新 W3_TODO 配置 - TEST_REPORT
-- UPDATE push_config
-- SET config_json = '{
--   "appName": "测试报告系统",
--   "appURL": "http://w3-beta.huawei.com",
--   "type": "J2EE",
--   "reserve1": "",
--   "reserve2": "test_report",
--   "reserve10": "0"
-- }'
-- WHERE business_type_id = 2 AND platform_code = 'W3_TODO';

-- 更新 WELINK_APP 配置 - TEST_REPORT
-- UPDATE push_config
-- SET config_json = '{
--   "app_id": "com.huawei.feed",
--   "theme_id": "d99b0ccaad7a4395b5f2aa558218dc9c",
--   "templateNo": "20251223000522",
--   "from_user_account": "z00512371",
--   "type": "1",
--   "displayType": "text",
--   "noticeType": 1
-- }'
-- WHERE business_type_id = 2 AND platform_code = 'WELINK_APP';


-- ============================================
-- 验证更新结果
-- ============================================

-- 查看更新后的配置
SELECT
    bt.business_code,
    bt.business_name,
    pc.platform_code,
    pp.platform_name,
    pc.enabled,
    pc.config_json
FROM push_config pc
JOIN business_type bt ON pc.business_type_id = bt.id
JOIN push_platform pp ON pc.platform_code = pp.platform_code
ORDER BY bt.business_code, pc.platform_code;
