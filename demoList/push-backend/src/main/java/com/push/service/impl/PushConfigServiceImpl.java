package com.push.service.impl;

import com.push.entity.BusinessType;
import com.push.entity.PushConfig;
import com.push.mapper.BusinessTypeRepository;
import com.push.mapper.PushConfigRepository;
import com.push.service.PushConfigService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * 推送配置服务实现
 */
@Service
public class PushConfigServiceImpl implements PushConfigService {

    @Autowired
    private PushConfigRepository pushConfigRepository;

    @Autowired
    private BusinessTypeRepository businessTypeRepository;

    @Override
    public List<PushConfig> getByBusinessCode(String businessCode) {
        BusinessType businessType = businessTypeRepository.findByBusinessCode(businessCode);
        if (businessType == null) {
            return List.of();
        }
        return pushConfigRepository.findByBusinessTypeId(businessType.getId());
    }

    @Override
    public PushConfig saveOrUpdate(PushConfig config) {
        // 检查业务类型是否存在
        BusinessType businessType = businessTypeRepository.findById(config.getBusinessTypeId())
                .orElseThrow(() -> new RuntimeException("业务类型不存在"));

        return pushConfigRepository.save(config);
    }

    @Override
    public void delete(Long id) {
        pushConfigRepository.deleteById(id);
    }

    // ===== 业务类型管理 =====

    @Override
    public List<BusinessType> getAllBusinessTypes() {
        return businessTypeRepository.findAll();
    }

    @Override
    public BusinessType getBusinessTypeById(Long id) {
        return businessTypeRepository.findById(id).orElse(null);
    }

    @Override
    public BusinessType getBusinessTypeByCode(String businessCode) {
        return businessTypeRepository.findByBusinessCode(businessCode);
    }

    @Override
    public BusinessType createBusinessType(BusinessType businessType) {
        // 检查业务编码是否已存在
        BusinessType existing = businessTypeRepository.findByBusinessCode(businessType.getBusinessCode());
        if (existing != null) {
            throw new RuntimeException("业务编码已存在");
        }
        return businessTypeRepository.save(businessType);
    }

    @Override
    public BusinessType updateBusinessType(Long id, BusinessType businessType) {
        BusinessType existing = businessTypeRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("业务类型不存在"));

        // 检查业务编码是否被其他记录占用
        BusinessType duplicate = businessTypeRepository.findByBusinessCode(businessType.getBusinessCode());
        if (duplicate != null && !duplicate.getId().equals(id)) {
            throw new RuntimeException("业务编码已存在");
        }

        existing.setBusinessCode(businessType.getBusinessCode());
        existing.setBusinessName(businessType.getBusinessName());
        return businessTypeRepository.save(existing);
    }

    @Override
    public void deleteBusinessType(Long id) {
        BusinessType businessType = businessTypeRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("业务类型不存在"));

        // 检查是否有关联的推送配置
        List<PushConfig> configs = pushConfigRepository.findByBusinessTypeId(id);
        if (!configs.isEmpty()) {
            throw new RuntimeException("该业务类型存在推送配置，无法删除");
        }

        businessTypeRepository.deleteById(id);
    }
}
