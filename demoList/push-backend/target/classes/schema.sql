-- ============================================
-- 推送系统数据库表结构
-- ============================================

-- 1. 推送平台表
CREATE TABLE IF NOT EXISTS push_platform (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
    platform_code VARCHAR(50) NOT NULL UNIQUE COMMENT '平台编码：W3_TODO, WELINK_APP',
    platform_name VARCHAR(100) NOT NULL COMMENT '平台名称',
    api_endpoint VARCHAR(255) COMMENT 'API地址（可选，配置中覆盖）',
    enabled TINYINT DEFAULT 1 COMMENT '是否启用 0-禁用 1-启用',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='推送平台表';

-- 2. 业务类型表
CREATE TABLE IF NOT EXISTS business_type (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
    business_code VARCHAR(50) NOT NULL UNIQUE COMMENT '业务编码：QA_REPORT, TEST_REPORT',
    business_name VARCHAR(100) NOT NULL COMMENT '业务名称',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='业务类型表';

-- 3. 推送配置表
CREATE TABLE IF NOT EXISTS push_config (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
    business_type_id BIGINT NOT NULL COMMENT '业务类型ID',
    platform_code VARCHAR(50) NOT NULL COMMENT '平台编码',
    enabled TINYINT DEFAULT 1 COMMENT '是否启用',
    config_json TEXT COMMENT '推送配置JSON（静态参数）',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    UNIQUE KEY uk_business_platform (business_type_id, platform_code),
    FOREIGN KEY (business_type_id) REFERENCES business_type(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='推送配置表';

-- 4. 推送历史表
CREATE TABLE IF NOT EXISTS push_history (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
    business_type_id BIGINT NOT NULL COMMENT '业务类型ID',
    platform_code VARCHAR(50) NOT NULL COMMENT '平台编码',
    group_id BIGINT COMMENT '使用的群组ID',
    business_key VARCHAR(100) COMMENT '业务主键（如报告ID）',
    request_json TEXT NOT NULL COMMENT '完整请求参数',
    response_json TEXT COMMENT '响应结果',
    status TINYINT DEFAULT 0 COMMENT '状态 0-失败 1-成功',
    error_message TEXT COMMENT '错误信息',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_business_type (business_type_id),
    INDEX idx_platform (platform_code),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='推送历史表';

-- 5. 推送群组表
CREATE TABLE IF NOT EXISTS push_group (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
    group_name VARCHAR(100) NOT NULL COMMENT '群组名称',
    description VARCHAR(255) COMMENT '群组描述',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='推送群组表';

-- 6. 群组成员表
CREATE TABLE IF NOT EXISTS group_member (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
    group_id BIGINT NOT NULL COMMENT '群组ID',
    employee_no VARCHAR(50) NOT NULL COMMENT '工号',
    employee_name VARCHAR(100) COMMENT '姓名',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    UNIQUE KEY uk_group_employee (group_id, employee_no),
    FOREIGN KEY (group_id) REFERENCES push_group(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='群组成员表';

-- ============================================
-- 初始化数据
-- ============================================

-- 初始化推送平台
INSERT INTO push_platform (platform_code, platform_name) VALUES
('W3_TODO', 'W3代办'),
('WELINK_APP', 'WeLink应用号');

-- 初始化业务类型
INSERT INTO business_type (business_code, business_name) VALUES
('QA_REPORT', 'QA报告'),
('TEST_REPORT', '测试报告');

-- 初始化推送配置示例（完整模板格式）
INSERT INTO push_config (business_type_id, platform_code, enabled, config_json) VALUES
(1, 'W3_TODO', 1, '{"type": "QA", "source": "QA系统", "title": "QA报告通知", "content": "您有新的QA报告待处理", "jumpUrl": "", "extras": {}}'),
(2, 'W3_TODO', 1, '{"type": "Test", "source": "测试系统", "title": "测试报告通知", "content": "测试报告已生成", "jumpUrl": "", "extras": {}}'),
(2, 'WELINK_APP', 1, '{"category": "test_report", "title": "测试报告", "content": "测试完成", "url": "", "userIdList": []}');

-- 初始化测试群组
INSERT INTO push_group (group_name, description) VALUES
('QA审核组', 'QA报告审核人员'),
('测试组', '测试相关人员');

-- 初始化群组成员
INSERT INTO group_member (group_id, employee_no, employee_name) VALUES
(1, 'c00807372', '张三'),
(1, 'c00807373', '李四'),
(2, 'c00807374', '王五'),
(2, 'c00807375', '赵六');
