package com.push.dto;

import lombok.Data;

/**
 * 推送结果
 */
@Data
public class PushResult {
    private boolean success;
    private String message;
    private Object data;

    public static PushResult success(String message) {
        PushResult result = new PushResult();
        result.setSuccess(true);
        result.setMessage(message);
        return result;
    }

    public static PushResult failure(String message) {
        PushResult result = new PushResult();
        result.setSuccess(false);
        result.setMessage(message);
        return result;
    }
}
