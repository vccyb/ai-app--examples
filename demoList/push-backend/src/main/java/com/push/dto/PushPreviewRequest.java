package com.push.dto;

import lombok.Data;
import java.util.Map;

/**
 * 推送预览请求
 */
@Data
public class PushPreviewRequest {
    private String businessCode;
    private Map<String, Object> dynamicParams;
    private Long groupId;
}
