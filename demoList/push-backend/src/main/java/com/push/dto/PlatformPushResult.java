package com.push.dto;

import lombok.Data;
import java.time.LocalDateTime;

/**
 * 平台推送结果（包含完整的API响应信息）
 */
@Data
public class PlatformPushResult {
    /**
     * 是否成功
     */
    private boolean success;

    /**
     * 业务消息（用户友好的描述）
     */
    private String message;

    /**
     * HTTP状态码（如果是HTTP调用）
     */
    private Integer httpStatusCode;

    /**
     * 第三方平台返回的业务码
     */
    private String businessCode;

    /**
     * 第三方平台返回的业务消息
     */
    private String businessMessage;

    /**
     * 第三方平台的追踪ID（用于追溯）
     * 例如：W3的taskId、WeLink的msgId
     */
    private String traceId;

    /**
     * 完整的响应体（JSON字符串）
     */
    private String responseBody;

    /**
     * 响应时间
     */
    private LocalDateTime responseTime;

    /**
     * 异常堆栈（如果发生异常）
     */
    private String exceptionStack;

    public PlatformPushResult() {
        this.responseTime = LocalDateTime.now();
    }

    public static PlatformPushResult success(String message) {
        PlatformPushResult result = new PlatformPushResult();
        result.setSuccess(true);
        result.setMessage(message);
        return result;
    }

    public static PlatformPushResult failure(String message) {
        PlatformPushResult result = new PlatformPushResult();
        result.setSuccess(false);
        result.setMessage(message);
        return result;
    }

    public static PlatformPushResult success(String message, String traceId, String responseBody) {
        PlatformPushResult result = new PlatformPushResult();
        result.setSuccess(true);
        result.setMessage(message);
        result.setTraceId(traceId);
        result.setResponseBody(responseBody);
        return result;
    }

    public static PlatformPushResult failure(String message, String responseBody, String exceptionStack) {
        PlatformPushResult result = new PlatformPushResult();
        result.setSuccess(false);
        result.setMessage(message);
        result.setResponseBody(responseBody);
        result.setExceptionStack(exceptionStack);
        return result;
    }
}
