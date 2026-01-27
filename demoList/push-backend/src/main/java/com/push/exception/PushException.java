package com.push.exception;

/**
 * 推送业务异常
 */
public class PushException extends RuntimeException {

    private final Integer code;

    public PushException(String message) {
        super(message);
        this.code = 500;
    }

    public PushException(Integer code, String message) {
        super(message);
        this.code = code;
    }

    public PushException(String message, Throwable cause) {
        super(message, cause);
        this.code = 500;
    }

    public Integer getCode() {
        return code;
    }
}
