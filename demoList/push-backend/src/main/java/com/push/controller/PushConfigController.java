package com.push.controller;

import com.push.dto.ApiResponse;
import com.push.entity.BusinessType;
import com.push.entity.PushConfig;
import com.push.mapper.BusinessTypeRepository;
import com.push.service.PushConfigService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * 推送配置控制器
 */
@RestController
@RequestMapping("/api/push/config")
@CrossOrigin(origins = "*")
public class PushConfigController {

    @Autowired
    private PushConfigService pushConfigService;

    @Autowired
    private BusinessTypeRepository businessTypeRepository;

    /**
     * 获取业务配置
     */
    @GetMapping("/business/{businessCode}")
    public ApiResponse<List<PushConfig>> getBusinessConfig(@PathVariable String businessCode) {
        List<PushConfig> configs = pushConfigService.getByBusinessCode(businessCode);
        return ApiResponse.success(configs);
    }

    /**
     * 保存或更新配置
     */
    @PostMapping
    public ApiResponse<PushConfig> saveConfig(@RequestBody PushConfig config) {
        PushConfig saved = pushConfigService.saveOrUpdate(config);
        return ApiResponse.success(saved);
    }

    /**
     * 删除配置
     */
    @DeleteMapping("/{id}")
    public ApiResponse<Void> deleteConfig(@PathVariable Long id) {
        pushConfigService.delete(id);
        return ApiResponse.success(null);
    }

    /**
     * 获取所有业务类型
     */
    @GetMapping("/business-types")
    public ApiResponse<List<BusinessType>> getBusinessTypes() {
        return ApiResponse.success(pushConfigService.getAllBusinessTypes());
    }

    /**
     * 根据ID获取业务类型
     */
    @GetMapping("/business-types/{id}")
    public ApiResponse getBusinessTypeById(@PathVariable Long id) {
        BusinessType businessType = pushConfigService.getBusinessTypeById(id);
        if (businessType == null) {
            return ApiResponse.error("业务类型不存在");
        }
        return ApiResponse.success(businessType);
    }

    /**
     * 创建业务类型
     */
    @PostMapping("/business-types")
    public ApiResponse<BusinessType> createBusinessType(@RequestBody BusinessType businessType) {
        try {
            BusinessType created = pushConfigService.createBusinessType(businessType);
            return ApiResponse.success(created);
        } catch (RuntimeException e) {
            return ApiResponse.error( e.getMessage());
        }
    }

    /**
     * 更新业务类型
     */
    @PutMapping("/business-types/{id}")
    public ApiResponse<BusinessType> updateBusinessType(
            @PathVariable Long id,
            @RequestBody BusinessType businessType) {
        try {
            BusinessType updated = pushConfigService.updateBusinessType(id, businessType);
            return ApiResponse.success(updated);
        } catch (RuntimeException e) {
            return ApiResponse.error( e.getMessage());
        }
    }

    /**
     * 删除业务类型
     */
    @DeleteMapping("/business-types/{id}")
    public ApiResponse<Void> deleteBusinessType(@PathVariable Long id) {
        try {
            pushConfigService.deleteBusinessType(id);
            return ApiResponse.success(null);
        } catch (RuntimeException e) {
            return ApiResponse.error( e.getMessage());
        }
    }
}
