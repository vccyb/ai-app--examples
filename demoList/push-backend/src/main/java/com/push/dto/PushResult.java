package com.push.dto;

import lombok.Data;

/**
 * 推送结果（简化版，用于Service层返回）
 */
@Data
public class PushResult {
    private boolean success;
    private String message;

    /**
     * 详细的平台推送结果（包含完整的API响应）
     */
    private PlatformPushResult platformResult;

    public PushResult() {
    }

    public PushResult(boolean success, String message) {
        this.success = success;
        this.message = message;
    }

    public static PushResult success(String message) {
        return new PushResult(true, message);
    }

    public static PushResult failure(String message) {
        return new PushResult(false, message);
    }

    public static PushResult success(String message, PlatformPushResult platformResult) {
        PushResult result = new PushResult(true, message);
        result.setPlatformResult(platformResult);
        return result;
    }

    public static PushResult failure(String message, PlatformPushResult platformResult) {
        PushResult result = new PushResult(false, message);
        result.setPlatformResult(platformResult);
        return result;
    }
}
