package com.push.strategy;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.push.dto.PushResult;
import com.push.entity.GroupMember;
import org.springframework.stereotype.Component;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

/**
 * WeLink应用号推送策略实现（模拟）
 *
 * 接口文档：http://kweuat.huawei.com/feedmsg/publicservices/template/sendTemplateMessage
 */
@Component
public class WeLinkAppPushStrategy implements PushPlatformStrategy {

    private final ObjectMapper objectMapper = new ObjectMapper();

    @Override
    public Map<String, Object> buildPushRequest(Map<String, Object> config,
                                                 Map<String, Object> dynamicParams,
                                                 List<GroupMember> groupMembers) {
        Map<String, Object> request = new HashMap<>();

        // ========== 静态参数（从 config 获取） ==========
        request.put("app_id", config.get("app_id"));
        request.put("theme_id", config.get("theme_id"));
        request.put("templateNo", config.get("templateNo"));
        request.put("from_user_account", config.get("from_user_account"));
        request.put("type", config.getOrDefault("type", "1"));  // 默认为通知类
        request.put("displayType", config.get("displayType"));
        request.put("noticeType", config.get("noticeType"));

        // ========== 动态参数（从 dynamicParams 获取） ==========
        // 模板标题参数（需要转成 JSON 字符串）
        Map<String, Object> titleParams = new HashMap<>();
        if (dynamicParams.containsKey("titleName")) {
            titleParams.put("tName", dynamicParams.get("titleName"));
        }
        if (dynamicParams.containsKey("title")) {
            titleParams.put("tName", dynamicParams.get("title"));
        }
        request.put("templateTitleParams", toJsonString(titleParams));

        // 模板内容参数（需要转成 JSON 字符串）
        Map<String, Object> contentParams = new HashMap<>();
        if (dynamicParams.containsKey("contentName")) {
            contentParams.put("cName", dynamicParams.get("contentName"));
        }
        if (dynamicParams.containsKey("content")) {
            contentParams.put("cName", dynamicParams.get("content"));
        }
        if (dynamicParams.containsKey("action")) {
            contentParams.put("doName", dynamicParams.get("action"));
        }
        request.put("templateContentParams", toJsonString(contentParams));

        // 跳转链接
        request.put("jump_url", dynamicParams.getOrDefault("jumpUrl", ""));

        // ========== 接收人（从 groupMembers 获取） ==========
        // to_user_account 格式：z00512371,dwx477491（用逗号分隔）
        String toUserAccount = groupMembers.stream()
                .map(GroupMember::getEmployeeNo)
                .collect(Collectors.joining(","));
        request.put("to_user_account", toUserAccount);

        return request;
    }

    @Override
    public PushResult execute(Map<String, Object> request) {
        // 模拟推送成功（实际项目中调用真实API）
        System.out.println("=== WeLink应用号推送（模拟） ====");
        System.out.println("接口路径: http://kweuat.huawei.com/feedmsg/publicservices/template/sendTemplateMessage");
        System.out.println("请求参数: " + request);
        try {
            // 模拟网络延迟
            Thread.sleep(200);

            // 实际项目中应该使用 Feign 调用真实 API
            // weLinkAppFeignClient.sendTemplateMessage(request);

            return PushResult.success("WeLink应用号推送成功");
        } catch (Exception e) {
            return PushResult.failure("WeLink应用号推送失败: " + e.getMessage());
        }
    }

    @Override
    public String getPlatformCode() {
        return "WELINK_APP";
    }

    /**
     * 将 Map 转换为 JSON 字符串
     */
    private String toJsonString(Map<String, Object> map) {
        try {
            return objectMapper.writeValueAsString(map);
        } catch (Exception e) {
            return "{}";
        }
    }
}
