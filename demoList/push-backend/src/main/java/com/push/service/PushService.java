package com.push.service;

import com.push.dto.*;

/**
 * 推送服务接口
 */
public interface PushService {
    /**
     * 预览推送内容
     */
    PushPreviewResponse preview(PushPreviewRequest request);

    /**
     * 执行推送
     */
    PushResult execute(PushExecuteRequest request);
}
