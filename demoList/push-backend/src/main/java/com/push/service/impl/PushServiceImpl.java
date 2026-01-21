package com.push.service.impl;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.push.dto.*;
import com.push.entity.*;
import com.push.mapper.*;
import com.push.service.PushService;
import com.push.strategy.PushPlatformStrategy;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.*;
import java.util.stream.Collectors;

/**
 * 推送服务实现
 */
@Service
public class PushServiceImpl implements PushService {

    @Autowired
    private BusinessTypeRepository businessTypeRepository;

    @Autowired
    private PushConfigRepository pushConfigRepository;

    @Autowired
    private PushPlatformRepository pushPlatformRepository;

    @Autowired
    private PushHistoryRepository pushHistoryRepository;

    @Autowired
    private GroupMemberRepository groupMemberRepository;

    @Autowired
    private List<PushPlatformStrategy> strategies;

    private final ObjectMapper objectMapper = new ObjectMapper();

    @Override
    public PushPreviewResponse preview(PushPreviewRequest request) {
        BusinessType businessType = businessTypeRepository.findByBusinessCode(request.getBusinessCode());
        if (businessType == null) {
            throw new RuntimeException("业务类型不存在");
        }

        List<PushConfig> configs = pushConfigRepository.findByBusinessTypeId(businessType.getId());

        PushPreviewResponse response = new PushPreviewResponse();
        response.setBusinessCode(request.getBusinessCode());
        response.setPushPlatforms(new ArrayList<>());

        List<GroupMember> members = Collections.emptyList();
        if (request.getGroupId() != null) {
            members = groupMemberRepository.findByGroupId(request.getGroupId());
        }

        for (PushConfig config : configs) {
            if (config.getEnabled() == 0) continue;

            PushPlatform platform = pushPlatformRepository.findByPlatformCode(config.getPlatformCode());
            if (platform == null || platform.getEnabled() == 0) continue;

            PushPlatformStrategy strategy = getStrategy(config.getPlatformCode());
            if (strategy == null) continue;

            Map<String, Object> configJson = parseConfigJson(config.getConfigJson());
            Map<String, Object> requestParams = strategy.buildPushRequest(
                    configJson, request.getDynamicParams(), members);

            PushPreviewResponse.PushPlatformPreview preview = new PushPreviewResponse.PushPlatformPreview();
            preview.setPlatformCode(platform.getPlatformCode());
            preview.setPlatformName(platform.getPlatformName());
            preview.setRequestParams(requestParams);

            response.getPushPlatforms().add(preview);
        }

        return response;
    }

    @Override
    public PushResult execute(PushExecuteRequest request) {
        BusinessType businessType = businessTypeRepository.findByBusinessCode(request.getBusinessCode());
        if (businessType == null) {
            return PushResult.failure("业务类型不存在");
        }

        List<PushConfig> configs = pushConfigRepository.findByBusinessTypeId(businessType.getId());
        if (configs.isEmpty()) {
            return PushResult.failure("该业务未配置推送");
        }

        if (request.getGroupId() == null) {
            return PushResult.failure("请选择推送群组");
        }

        List<GroupMember> members = groupMemberRepository.findByGroupId(request.getGroupId());
        if (members.isEmpty()) {
            return PushResult.failure("群组中无成员");
        }

        // 执行推送
        for (PushConfig config : configs) {
            if (config.getEnabled() == 0) continue;

            PushPlatformStrategy strategy = getStrategy(config.getPlatformCode());
            if (strategy == null) continue;

            Map<String, Object> configJson = parseConfigJson(config.getConfigJson());
            Map<String, Object> requestParams = strategy.buildPushRequest(
                    configJson, request.getDynamicParams(), members);

            PushResult result = strategy.execute(requestParams);

            // 记录历史
            PushHistory history = new PushHistory();
            history.setBusinessTypeId(businessType.getId());
            history.setPlatformCode(config.getPlatformCode());
            history.setGroupId(request.getGroupId());
            history.setBusinessKey(request.getBusinessKey());
            try {
                history.setRequestJson(objectMapper.writeValueAsString(requestParams));
                history.setResponseJson(objectMapper.writeValueAsString(result));
            } catch (Exception e) {
                history.setRequestJson(requestParams.toString());
            }
            history.setStatus(result.isSuccess() ? 1 : 0);
            history.setErrorMessage(result.isSuccess() ? null : result.getMessage());

            pushHistoryRepository.save(history);
        }

        return PushResult.success("推送执行成功");
    }

    private PushPlatformStrategy getStrategy(String platformCode) {
        return strategies.stream()
                .filter(s -> s.getPlatformCode().equals(platformCode))
                .findFirst()
                .orElse(null);
    }

    private Map<String, Object> parseConfigJson(String json) {
        if (json == null || json.isEmpty()) {
            return new HashMap<>();
        }
        try {
            return objectMapper.readValue(json, new TypeReference<Map<String, Object>>() {});
        } catch (Exception e) {
            return new HashMap<>();
        }
    }
}
