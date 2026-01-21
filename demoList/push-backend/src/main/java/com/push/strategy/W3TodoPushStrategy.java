package com.push.strategy;

import com.push.dto.PushResult;
import com.push.entity.GroupMember;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * W3代办推送策略实现（模拟）
 */
@Component
public class W3TodoPushStrategy implements PushPlatformStrategy {

    @Override
    public Map<String, Object> buildPushRequest(Map<String, Object> config,
                                                 Map<String, Object> dynamicParams,
                                                 List<GroupMember> groupMembers) {
        // 1. 基于配置模板构建，用前端参数覆盖
        Map<String, Object> request = TemplateUtils.buildFromTemplate(config, dynamicParams);

        // 2. 添加接收人
        List<String> receivers = TemplateUtils.extractEmployeeNos(groupMembers);
        request.put("receivers", receivers);

        return request;
    }

    @Override
    public PushResult execute(Map<String, Object> request) {
        // 模拟推送成功（实际项目中调用真实API）
        System.out.println("=== W3代办推送（模拟） ====");
        System.out.println("请求参数: " + request);
        try {
            // 模拟网络延迟
            Thread.sleep(200);

            // 实际项目中应该使用 Feign 调用真实 API
            // w3TodoFeignClient.push(request);

            return PushResult.success("W3代办推送成功");
        } catch (Exception e) {
            return PushResult.failure("W3代办推送失败: " + e.getMessage());
        }
    }

    @Override
    public String getPlatformCode() {
        return "W3_TODO";
    }
}
