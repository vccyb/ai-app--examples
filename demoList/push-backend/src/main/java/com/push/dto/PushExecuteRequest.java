package com.push.dto;

import lombok.Data;
import java.util.Map;

/**
 * 推送执行请求
 */
@Data
public class PushExecuteRequest {
    private String businessCode;
    private Long groupId;
    private Map<String, Object> dynamicParams;
    private String businessKey;
}
