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
}
