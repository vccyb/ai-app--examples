package com.push.service;

import com.push.entity.BusinessType;
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

    // ===== 业务类型管理 =====

    /**
     * 获取所有业务类型
     */
    List<BusinessType> getAllBusinessTypes();

    /**
     * 根据ID获取业务类型
     */
    BusinessType getBusinessTypeById(Long id);

    /**
     * 根据编码获取业务类型
     */
    BusinessType getBusinessTypeByCode(String businessCode);

    /**
     * 创建业务类型
     */
    BusinessType createBusinessType(BusinessType businessType);

    /**
     * 更新业务类型
     */
    BusinessType updateBusinessType(Long id, BusinessType businessType);

    /**
     * 删除业务类型
     */
    void deleteBusinessType(Long id);
}
