package com.push.dto;

import lombok.Data;
import java.util.List;
import java.util.Map;

/**
 * 推送预览响应
 */
@Data
public class PushPreviewResponse {
    private String businessCode;
    private List<PushPlatformPreview> pushPlatforms;

    @Data
    public static class PushPlatformPreview {
        private String platformCode;
        private String platformName;
        private Map<String, Object> requestParams;
    }
}
