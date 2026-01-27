package com.push.strategy;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.push.dto.PlatformPushResult;
import com.push.dto.platform.BasePushRequest;
import com.push.dto.platform.welink.WeLinkAppPushRequest;
import com.push.entity.GroupMember;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.stream.Collectors;

/**
 * WeLink应用号推送策略实现（模拟）
 *
 * 接口文档：http://kweuat.huawei.com/feedmsg/publicservices/template/sendTemplateMessage
 */
@Component
public class WeLinkAppPushStrategy implements PushPlatformStrategy {

    private static final Logger log = LoggerFactory.getLogger(WeLinkAppPushStrategy.class);
    private static final ObjectMapper objectMapper = new ObjectMapper();

    @Override
    public BasePushRequest buildPushRequest(Map<String, Object> config,
                                              Map<String, Object> dynamicParams,
                                              List<GroupMember> groupMembers) {
        WeLinkAppPushRequest request = new WeLinkAppPushRequest();

        // ========== 静态参数（从 config 获取） ==========
        request.setAppId((String) config.get("app_id"));
        request.setThemeId((String) config.get("theme_id"));
        request.setTemplateNo((String) config.get("templateNo"));
        request.setFromUserAccount((String) config.get("from_user_account"));
        request.setType((String) config.getOrDefault("type", "1"));
        request.setDisplayType((String) config.get("displayType"));
        request.setNoticeType((String) config.get("noticeType"));

        // ========== 动态参数（从 dynamicParams 获取） ==========

        // 模板标题参数
        request.setTitleName((String) dynamicParams.get("titleName"));
        request.setTitle((String) dynamicParams.get("title"));

        // 模板内容参数
        request.setContentName((String) dynamicParams.get("contentName"));
        request.setContent((String) dynamicParams.get("content"));
        request.setAction((String) dynamicParams.get("action"));

        // 跳转链接
        request.setJumpUrl((String) dynamicParams.getOrDefault("jumpUrl", ""));

        // 接收人（to_user_account 格式：z00512371,dwx477491）
        String toUserAccount = groupMembers.stream()
                .map(GroupMember::getEmployeeNo)
                .collect(Collectors.joining(","));
        request.setToUserAccount(toUserAccount);

        return request;
    }

    @Override
    public PlatformPushResult execute(Map<String, Object> request) {
        // 模拟推送成功（实际项目中调用真实API）
        log.info("=== WeLink应用号推送（模拟） ====");
        log.info("接口路径: http://kweuat.huawei.com/feedmsg/publicservices/template/sendTemplateMessage");
        log.info("请求参数: {}", request);

        try {
            // 模拟网络延迟
            Thread.sleep(200);

            // 实际项目中应该使用 Feign 调用真实 API
            // ResponseEntity<WeLinkResponse> response = weLinkAppFeignClient.sendTemplateMessage(request);

            // ========== 模拟WeLink API响应 ==========
            String mockMsgId = "WE_LINK_MSG_" + UUID.randomUUID().toString().substring(0, 8);
            String mockResponseBody = String.format(
                    "{\"code\":\"0\",\"message\":\"success\",\"data\":{\"msgId\":\"%s\",\"status\":\"sent\"}}",
                    mockMsgId);

            log.info("WeLink API响应: {}", mockResponseBody);

            // 构建详细的推送结果
            PlatformPushResult result = PlatformPushResult.success(
                    "WeLink应用号推送成功",
                    mockMsgId,  // WeLink返回的msgId作为traceId
                    mockResponseBody
            );
            result.setHttpStatusCode(200);
            result.setBusinessCode("0");
            result.setBusinessMessage("success");

            return result;

        } catch (Exception e) {
            log.error("WeLink应用号推送失败", e);

            // 构建失败结果
            PlatformPushResult result = PlatformPushResult.failure(
                    "WeLink应用号推送失败: " + e.getMessage(),
                    null,
                    getStackTrace(e)
            );
            result.setHttpStatusCode(500);
            result.setExceptionStack(getStackTrace(e));

            return result;
        }
    }

    /**
     * 获取异常堆栈信息
     */
    private String getStackTrace(Exception e) {
        if (e == null) {
            return null;
        }
        java.io.StringWriter sw = new java.io.StringWriter();
        java.io.PrintWriter pw = new java.io.PrintWriter(sw);
        e.printStackTrace(pw);
        return sw.toString();
    }

    @Override
    public String getPlatformCode() {
        return "WELINK_APP";
    }
}
