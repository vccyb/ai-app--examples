package com.push.dto.platform.welink;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.push.dto.platform.BasePushRequest;
import lombok.Data;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * WeLink应用号推送请求DTO
 *
 * 接口文档：http://kweuat.huawei.com/feedmsg/publicservices/template/sendTemplateMessage
 */
@Data
public class WeLinkAppPushRequest implements BasePushRequest {

    private static final ObjectMapper objectMapper = new ObjectMapper();

    // ========== 静态参数（从配置获取） ==========

    /**
     * 应用ID
     */
    private String appId;

    /**
     * 主题ID
     */
    private String themeId;

    /**
     * 模板编号
     */
    private String templateNo;

    /**
     * 发送人工号
     */
    private String fromUserAccount;

    /**
     * 类型（1-通知类，2-待办类）
     */
    private String type;

    /**
     * 展示类型
     */
    private String displayType;

    /**
     * 通知类型
     */
    private String noticeType;

    // ========== 动态参数（从前端传入） ==========

    /**
     * 模板标题参数（JSON字符串）
     * 格式：{"tName": "标题值"}
     */
    private String templateTitleParams;

    /**
     * 模板内容参数（JSON字符串）
     * 格式：{"cName": "内容值", "doName": "操作值"}
     */
    private String templateContentParams;

    /**
     * 跳转链接
     */
    private String jumpUrl;

    /**
     * 接收人工号列表（逗号分隔）
     * 格式：z00512371,dwx477491
     */
    private String toUserAccount;

    /**
     * 标题名称（可选，用于构建模板参数）
     */
    private String titleName;

    /**
     * 标题（备用）
     */
    private String title;

    /**
     * 内容名称（可选，用于构建模板参数）
     */
    private String contentName;

    /**
     * 内容（备用）
     */
    private String content;

    /**
     * 操作名称（可选，用于构建模板参数）
     */
    private String action;

    /**
     * 转换为Map格式（用于预览展示、历史记录存储）
     */
    @Override
    public Map<String, Object> toMap() {
        Map<String, Object> map = new HashMap<>();

        // 静态参数
        map.put("app_id", appId);
        map.put("theme_id", themeId);
        map.put("templateNo", templateNo);
        map.put("from_user_account", fromUserAccount);
        map.put("type", type);
        map.put("displayType", displayType);
        map.put("noticeType", noticeType);

        // 构建模板标题参数
        Map<String, Object> titleParams = new HashMap<>();
        if (titleName != null) {
            titleParams.put("tName", titleName);
        } else if (title != null) {
            titleParams.put("tName", title);
        }

        try {
            map.put("templateTitleParams", objectMapper.writeValueAsString(titleParams));
        } catch (Exception e) {
            map.put("templateTitleParams", "{}");
        }

        // 构建模板内容参数
        Map<String, Object> contentParams = new HashMap<>();
        if (contentName != null) {
            contentParams.put("cName", contentName);
        } else if (content != null) {
            contentParams.put("cName", content);
        }
        if (action != null) {
            contentParams.put("doName", action);
        }

        try {
            map.put("templateContentParams", objectMapper.writeValueAsString(contentParams));
        } catch (Exception e) {
            map.put("templateContentParams", "{}");
        }

        // 跳转链接
        map.put("jump_url", jumpUrl != null ? jumpUrl : "");

        // 接收人
        map.put("to_user_account", toUserAccount);

        return map;
    }
}
