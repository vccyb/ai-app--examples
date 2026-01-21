package com.push.controller;

import com.push.dto.ApiResponse;
import com.push.entity.PushHistory;
import com.push.service.PushHistoryService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.web.bind.annotation.*;

/**
 * 推送历史控制器
 */
@RestController
@RequestMapping("/api/push/history")
@CrossOrigin(origins = "*")
public class PushHistoryController {

    @Autowired
    private PushHistoryService pushHistoryService;

    /**
     * 分页查询历史记录
     */
    @GetMapping("/page")
    public ApiResponse<Page<PushHistory>> getPage(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size) {
        Page<PushHistory> pageData = pushHistoryService.getPage(page, size);
        return ApiResponse.success(pageData);
    }

    /**
     * 获取详情
     */
    @GetMapping("/{id}")
    public ApiResponse<PushHistory> getById(@PathVariable Long id) {
        PushHistory history = pushHistoryService.getById(id);
        return ApiResponse.success(history);
    }
}
