package com.push.strategy;

import com.push.dto.PlatformPushResult;
import com.push.dto.platform.BasePushRequest;
import com.push.dto.platform.w3todo.W3TodoPushRequest;
import com.push.entity.GroupMember;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
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

    private static final Logger log = LoggerFactory.getLogger(W3TodoPushStrategy.class);
    private static final DateTimeFormatter DATE_FORMATTER = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

    @Override
    public BasePushRequest buildPushRequest(Map<String, Object> config,
                                              Map<String, Object> dynamicParams,
                                              List<GroupMember> groupMembers) {
        W3TodoPushRequest request = new W3TodoPushRequest();

        // ========== 静态参数（从 config 获取） ==========
        request.setAppName((String) config.get("appName"));
        request.setAppURL((String) config.get("appURL"));
        request.setType((String) config.get("type"));
        request.setReserve1((String) config.getOrDefault("reserve1", ""));
        request.setReserve2((String) config.get("reserve2"));
        request.setReserve10((String) config.getOrDefault("reserve10", "0"));

        // ========== 动态参数（从 dynamicParams 获取） ==========
        request.setTaskDesc((String) dynamicParams.getOrDefault("taskDesc", ""));
        request.setTaskURL((String) dynamicParams.getOrDefault("taskURL", ""));

        // 任务UUID（建议拼接应用名英文简写）
        String taskUUID = (String) dynamicParams.get("taskUUID");
        if (taskUUID == null || taskUUID.isEmpty()) {
            String appName = (String) config.get("appName");
            taskUUID = appName + "_" + UUID.randomUUID().toString().substring(0, 8);
        }
        request.setTaskUUID(taskUUID);

        request.setTaskTitle((String) dynamicParams.getOrDefault("taskTitle", ""));
        request.setTaskCreateTime(dynamicParams.containsKey("taskCreateTime")
                ? (String) dynamicParams.get("taskCreateTime")
                : LocalDateTime.now().format(DATE_FORMATTER));
        request.setTaskState((String) dynamicParams.getOrDefault("taskState", "1"));
        request.setTaskCreateUser((String) dynamicParams.getOrDefault("taskCreateUser", ""));
        request.setTaskCreateUserName((String) dynamicParams.getOrDefault("taskCreateUserName", ""));

        // ========== 接收人（从 groupMembers 获取） ==========
        request.setReceiverUserAccounts(groupMembers.stream()
                .map(GroupMember::getEmployeeNo)
                .collect(Collectors.toList()));

        // 抄送人（可选）
        // request.setCopyUserAccounts(...);

        return request;
    }

    @Override
    public PlatformPushResult execute(Map<String, Object> request) {
        log.info("=== W3代办推送（模拟） ====");
        log.info("接口路径: http(s)://w3-beta.huawei.com/task/rest/todotaskmanagement/v2/createtask4w3");
        log.info("请求参数: {}", request);

        try {
            // 模拟网络延迟
            Thread.sleep(200);

            // 模拟成功响应
            // 实际项目中应该使用 Feign 调用真实 API
            // ResponseEntity<W3TodoResponse> response = w3TodoFeignClient.createTask(request);

            // ========== 模拟W3 API响应 ==========
            String mockTaskId = "W3_TASK_" + UUID.randomUUID().toString().substring(0, 8);
            String mockResponseBody = String.format(
                    "{\"code\":\"0\",\"message\":\"成功\",\"data\":{\"taskId\":\"%s\",\"taskStatus\":\"created\"}}",
                    mockTaskId);

            log.info("W3 API响应: {}", mockResponseBody);

            // 构建详细的推送结果
            PlatformPushResult result = PlatformPushResult.success(
                    "W3代办推送成功",
                    mockTaskId,  // W3返回的taskId作为traceId
                    mockResponseBody
            );
            result.setHttpStatusCode(200);
            result.setBusinessCode("0");
            result.setBusinessMessage("成功");

            return result;

        } catch (Exception e) {
            log.error("W3代办推送失败", e);

            // 构建失败结果
            PlatformPushResult result = PlatformPushResult.failure(
                    "W3代办推送失败: " + e.getMessage(),
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
        return "W3_TODO";
    }
}
