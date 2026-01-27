package com.push.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Data;
import java.util.Map;

/**
 * 推送预览请求
 */
@Data
public class PushPreviewRequest {

    @NotBlank(message = "业务编码不能为空")
    private String businessCode;

    @NotNull(message = "动态参数不能为空")
    private Map<String, Object> dynamicParams;

    @NotNull(message = "群组ID不能为空")
    private Long groupId;
}
