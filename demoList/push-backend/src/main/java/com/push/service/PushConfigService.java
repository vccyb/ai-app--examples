package com.push.service;

import com.push.entity.PushConfig;

import java.util.List;

/**
 * 推送配置服务接口
 */
public interface PushConfigService {
    /**
     * 获取业务配置
     */
    List<PushConfig> getByBusinessCode(String businessCode);

    /**
     * 保存或更新配置
     */
    PushConfig saveOrUpdate(PushConfig config);

    /**
     * 删除配置
     */
    void delete(Long id);
}
