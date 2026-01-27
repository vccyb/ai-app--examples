package com.push.constants;

/**
 * 推送模块常量
 */
public class PushConstants {

    /**
     * 启用状态
     */
    public static final int ENABLED = 1;
    public static final int DISABLED = 0;

    /**
     * 推送状态
     */
    public static final int PUSH_STATUS_SUCCESS = 1;
    public static final int PUSH_STATUS_FAILURE = 0;

    /**
     * 默认值
     */
    public static final String DEFAULT_JSON = "{}";
    public static final String NULL_RESULT_JSON = "{\"success\":false,\"message\":\"result is null\"}";

    private PushConstants() {
        // 防止实例化
    }
}
