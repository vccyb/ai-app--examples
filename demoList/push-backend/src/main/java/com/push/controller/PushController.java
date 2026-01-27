package com.push.controller;

import com.push.dto.ApiResponse;
import com.push.dto.*;
import com.push.entity.PushPlatform;
import com.push.mapper.PushPlatformRepository;
import com.push.service.PushService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * 推送控制器
 */
@RestController
@RequestMapping("/api/push")
@CrossOrigin(origins = "*")
public class PushController {

    @Autowired
    private PushService pushService;

    @Autowired
    private PushPlatformRepository pushPlatformRepository;

    /**
     * 预览推送内容
     */
    @PostMapping("/preview")
    public ApiResponse<PushPreviewResponse> preview(@Valid @RequestBody PushPreviewRequest request) {
        PushPreviewResponse response = pushService.preview(request);
        return ApiResponse.success(response);
    }

    /**
     * 执行推送
     */
    @PostMapping("/execute")
    public ApiResponse<PushResult> execute(@Valid @RequestBody PushExecuteRequest request) {
        PushResult result = pushService.execute(request);
        if (result.isSuccess()) {
            return ApiResponse.success(result.getMessage(), result);
        } else {
            return ApiResponse.error(result.getMessage());
        }
    }

    /**
     * 获取所有推送平台
     */
    @GetMapping("/platforms")
    public ApiResponse<List<PushPlatform>> getPlatforms() {
        return ApiResponse.success(pushPlatformRepository.findAll());
    }
}
