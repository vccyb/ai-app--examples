package com.push.service;

import com.push.entity.PushHistory;
import org.springframework.data.domain.Page;

/**
 * 推送历史服务接口
 */
public interface PushHistoryService {
    /**
     * 分页查询历史记录
     */
    Page<PushHistory> getPage(int page, int size);

    /**
     * 获取详情
     */
    PushHistory getById(Long id);
}
