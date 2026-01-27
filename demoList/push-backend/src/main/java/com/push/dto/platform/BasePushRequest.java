package com.push.dto.platform;

import java.util.Map;

/**
 * 推送请求基础接口
 * 所有平台特定的推送请求DTO都应该实现此接口
 *
 * 设计思路：
 * - 每个平台有自己特定的请求DTO（如W3TodoPushRequest、WeLinkAppPushRequest）
 * - 这些DTO直接实现BasePushRequest接口
 * - toMap()方法用于预览展示、历史记录存储等场景
 * - 实际调用第三方API时，直接使用强类型DTO对象
 */
public interface BasePushRequest {
    /**
     * 转换为Map格式（用于预览展示、历史记录存储等场景）
     * @return Map格式的请求参数
     */
    Map<String, Object> toMap();
}
