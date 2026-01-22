package com.push.strategy;

import com.push.dto.PushResult;
import com.push.entity.GroupMember;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.stream.Collectors;

/**
 * W3代办推送策略实现（模拟）
 *
 * 接口文档：http(s)://w3-beta.huawei.com/task/rest/todotaskmanagement/v2/createtask4w3
 */
@Component
public class W3TodoPushStrategy implements PushPlatformStrategy {

    private static final DateTimeFormatter DATE_FORMATTER = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

    @Override
    public Map<String, Object> buildPushRequest(Map<String, Object> config,
                                                 Map<String, Object> dynamicParams,
                                                 List<GroupMember> groupMembers) {
        Map<String, Object> request = new HashMap<>();

        // ========== 静态参数（从 config 获取） ==========
        request.put("appName", config.get("appName"));
        request.put("appURL", config.get("appURL"));
        request.put("type", config.get("type"));  // 固定为 J2EE
        request.put("reserve1", config.getOrDefault("reserve1", ""));
        request.put("reserve2", config.get("reserve2"));  // 备用字段，区分任务类型
        request.put("reserve10", config.getOrDefault("reserve10", "0"));  // 是否支持移动审批

        // ========== 动态参数（从 dynamicParams 获取） ==========
        // 任务描述（建议加上标题、流程和状态）
        request.put("taskDesc", dynamicParams.getOrDefault("taskDesc", ""));

        // 任务跳转 URL（绝对地址）
        request.put("taskURL", dynamicParams.getOrDefault("taskURL", ""));

        // 任务全局唯一标识符（建议拼接应用名英文简写）
        String taskUUID = (String) dynamicParams.get("taskUUID");
        if (taskUUID == null || taskUUID.isEmpty()) {
            String appName = (String) config.get("appName");
            String appNameEn = extractAppNameEn(appName);
            taskUUID = appNameEn + "_" + UUID.randomUUID().toString().replace("-", "");
        }
        request.put("taskUUID", taskUUID);

        // 业务系统发送待办的时间
        String time = (String) dynamicParams.get("time");
        if (time == null || time.isEmpty()) {
            time = LocalDateTime.now().format(DATE_FORMATTER);
        }
        request.put("time", time);

        // 申请人（可选，默认使用系统账号）
        request.put("applicant", dynamicParams.getOrDefault("applicant", "system 00000000"));

        // reserve3（可选，默认使用 taskURL）
        request.put("reserve3", dynamicParams.getOrDefault("reserve3", request.get("taskURL")));

        // ========== 接收人（从 groupMembers 获取） ==========
        // handler 格式：zhangsan 00124563,lishi WX123456（工号前面加前缀，用逗号分隔）
        String handler = groupMembers.stream()
                .map(member -> formatEmployeeNo(member.getEmployeeNo()))
                .collect(Collectors.joining(","));
        request.put("handler", handler);

        return request;
    }

    @Override
    public PushResult execute(Map<String, Object> request) {
        // 模拟推送成功（实际项目中调用真实API）
        System.out.println("=== W3代办推送（模拟） ====");
        System.out.println("接口路径: http(s)://w3-beta.huawei.com/task/rest/todotaskmanagement/v2/createtask4w3");
        System.out.println("请求参数: " + request);
        try {
            // 模拟网络延迟
            Thread.sleep(200);

            // 实际项目中应该使用 Feign 调用真实 API
            // w3TodoFeignClient.createTask(request);

            return PushResult.success("W3代办推送成功");
        } catch (Exception e) {
            return PushResult.failure("W3代办推送失败: " + e.getMessage());
        }
    }

    @Override
    public String getPlatformCode() {
        return "W3_TODO";
    }

    /**
     * 格式化工号
     * W3 要求格式：zhangsan 00124563 或 lishi WX123456
     * 如果工号已经是正确格式，直接使用；否则添加 z 前缀
     */
    private String formatEmployeeNo(String employeeNo) {
        if (employeeNo == null || employeeNo.isEmpty()) {
            return "z 00000000";
        }

        // 如果已经包含空格（已经是正确格式），直接返回
        if (employeeNo.contains(" ")) {
            return employeeNo;
        }

        // 如果以 z 或 Z 开头，直接在后面加空格
        if (employeeNo.toLowerCase().startsWith("z")) {
            return employeeNo.substring(0, 1) + " " + employeeNo.substring(1);
        }

        // 其他情况，添加 z 前缀和空格
        return "z " + employeeNo;
    }

    /**
     * 从应用名称提取英文简写
     * 例如："QA报告系统" -> "qa"
     */
    private String extractAppNameEn(String appName) {
        if (appName == null || appName.isEmpty()) {
            return "app";
        }

        // 提取英文字母和数字
        String en = appName.replaceAll("[^a-zA-Z0-9]", "");
        return en.isEmpty() ? "app" : en.toLowerCase();
    }
}
