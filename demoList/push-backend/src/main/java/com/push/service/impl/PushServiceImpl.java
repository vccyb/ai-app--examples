package com.push.service.impl;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.push.constants.PushConstants;
import com.push.dto.*;
import com.push.dto.platform.BasePushRequest;
import com.push.entity.*;
import com.push.exception.PushException;
import com.push.mapper.*;
import com.push.service.PushService;
import com.push.strategy.PushPlatformStrategy;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.*;
import java.util.stream.Collectors;

/**
 * 推送服务实现
 */
@Service
public class PushServiceImpl implements PushService {

    private static final Logger log = LoggerFactory.getLogger(PushServiceImpl.class);

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
        log.info("开始预览推送，业务编码：{}，群组ID：{}", request.getBusinessCode(), request.getGroupId());

        // 1. 查询业务类型
        BusinessType businessType = businessTypeRepository.findByBusinessCode(request.getBusinessCode());
        if (businessType == null) {
            log.warn("业务类型不存在：{}", request.getBusinessCode());
            throw new PushException("业务类型不存在：" + request.getBusinessCode());
        }

        // 2. 查询已启用的推送配置
        List<PushConfig> configs = pushConfigRepository.findByBusinessTypeIdAndEnabled(
                businessType.getId(), PushConstants.ENABLED);
        if (configs.isEmpty()) {
            log.warn("业务类型【{}】未配置已启用的推送平台", businessType.getBusinessName());
        }

        // 3. 批量查询所有已启用的推送平台（避免N+1查询）
        List<String> platformCodes = configs.stream()
                .map(PushConfig::getPlatformCode)
                .distinct()
                .toList();
        List<PushPlatform> platforms = pushPlatformRepository.findByEnabled(PushConstants.ENABLED);
        Map<String, PushPlatform> platformMap = platforms.stream()
                .filter(p -> platformCodes.contains(p.getPlatformCode()))
                .collect(Collectors.toMap(PushPlatform::getPlatformCode, p -> p));

        // 4. 查询群组成员（如果指定了群组）
        List<GroupMember> members = Collections.emptyList();
        if (request.getGroupId() != null) {
            members = groupMemberRepository.findByGroupId(request.getGroupId());
            if (members.isEmpty()) {
                log.warn("群组【{}】中无成员", request.getGroupId());
            }
        }

        // 5. 构建预览响应
        PushPreviewResponse response = new PushPreviewResponse();
        response.setBusinessCode(request.getBusinessCode());
        response.setPushPlatforms(new ArrayList<>());

        int successCount = 0;
        int skipCount = 0;

        // 6. 遍历每个推送配置，构建预览
        for (PushConfig config : configs) {
            String platformCode = config.getPlatformCode();
            PushPlatform platform = platformMap.get(platformCode);

            if (platform == null) {
                log.warn("推送平台【{}】未启用或不存在", platformCode);
                skipCount++;
                continue;
            }

            // 获取推送策略
            PushPlatformStrategy strategy = getStrategy(platformCode);
            if (strategy == null) {
                log.warn("推送平台【{}】未实现对应的策略", platformCode);
                skipCount++;
                continue;
            }

            try {
                // 解析配置JSON
                Map<String, Object> configJson = parseConfigJson(config.getConfigJson());

                // 构建推送请求参数（强类型DTO）
                BasePushRequest baseRequest = strategy.buildPushRequest(
                        configJson, request.getDynamicParams(), members);

                // 转换为Map用于预览展示
                Map<String, Object> requestParams = baseRequest.toMap();

                // 添加到预览列表
                PushPreviewResponse.PushPlatformPreview preview = new PushPreviewResponse.PushPlatformPreview();
                preview.setPlatformCode(platform.getPlatformCode());
                preview.setPlatformName(platform.getPlatformName());
                preview.setRequestParams(requestParams);

                response.getPushPlatforms().add(preview);
                successCount++;

                log.debug("成功构建推送预览：平台【{}】", platform.getPlatformName());

            } catch (Exception e) {
                log.error("构建推送预览失败：平台【{}】", platform.getPlatformName(), e);
                skipCount++;
            }
        }

        log.info("预览完成，成功：{}，跳过：{}", successCount, skipCount);
        return response;
    }

    @Override
    public PushResult execute(PushExecuteRequest request) {
        log.info("开始执行推送，业务编码：{}，群组ID：{}，业务主键：{}",
                request.getBusinessCode(), request.getGroupId(), request.getBusinessKey());

        // 1. 查询业务类型
        BusinessType businessType = businessTypeRepository.findByBusinessCode(request.getBusinessCode());
        if (businessType == null) {
            log.warn("业务类型不存在：{}", request.getBusinessCode());
            return PushResult.failure("业务类型不存在：" + request.getBusinessCode());
        }

        // 2. 查询已启用的推送配置
        List<PushConfig> configs = pushConfigRepository.findByBusinessTypeIdAndEnabled(
                businessType.getId(), PushConstants.ENABLED);
        if (configs.isEmpty()) {
            log.warn("业务类型【{}】未配置已启用的推送平台", businessType.getBusinessName());
            return PushResult.failure("该业务未配置已启用的推送平台");
        }

        // 3. 校验群组
        if (request.getGroupId() == null) {
            log.warn("未指定推送群组");
            return PushResult.failure("请选择推送群组");
        }

        // 4. 查询群组成员
        List<GroupMember> members = groupMemberRepository.findByGroupId(request.getGroupId());
        if (members.isEmpty()) {
            log.warn("群组【{}】中无成员", request.getGroupId());
            return PushResult.failure("群组中无成员");
        }

        // 5. 批量查询所有已启用的推送平台（避免N+1查询）
        List<String> platformCodes = configs.stream()
                .map(PushConfig::getPlatformCode)
                .distinct()
                .toList();
        List<PushPlatform> platforms = pushPlatformRepository.findByEnabled(PushConstants.ENABLED);
        Map<String, PushPlatform> platformMap = platforms.stream()
                .filter(p -> platformCodes.contains(p.getPlatformCode()))
                .collect(Collectors.toMap(PushPlatform::getPlatformCode, p -> p));

        log.info("群组成员数：{}，推送平台数：{}", members.size(), configs.size());

        // 6. 执行推送统计
        int successCount = 0;
        int failureCount = 0;
        List<String> failurePlatforms = new ArrayList<>();

        // 7. 遍历每个推送配置，执行推送
        for (PushConfig config : configs) {
            String platformCode = config.getPlatformCode();
            PushPlatform platform = platformMap.get(platformCode);

            if (platform == null) {
                log.warn("推送平台【{}】未启用或不存在，跳过", platformCode);
                failureCount++;
                failurePlatforms.add(platformCode + "(平台未启用)");
                continue;
            }

            // 获取推送策略
            PushPlatformStrategy strategy = getStrategy(platformCode);
            if (strategy == null) {
                log.warn("推送平台【{}】未实现对应的策略，跳过", platformCode);
                failureCount++;
                failurePlatforms.add(platformCode + "(策略未实现)");
                continue;
            }

            try {
                // 解析配置JSON
                Map<String, Object> configJson = parseConfigJson(config.getConfigJson());

                // 构建推送请求参数（强类型DTO）
                BasePushRequest baseRequest = strategy.buildPushRequest(
                        configJson, request.getDynamicParams(), members);

                // 转换为Map用于API调用
                Map<String, Object> requestParams = baseRequest.toMap();

                log.info("开始推送，平台：{}，接收人数：{}", platform.getPlatformName(), members.size());

                // 执行推送
                PlatformPushResult platformResult = strategy.execute(requestParams);

                // 转换为Service层使用的PushResult
                PushResult result = platformResult.isSuccess()
                    ? PushResult.success(platformResult.getMessage(), platformResult)
                    : PushResult.failure(platformResult.getMessage(), platformResult);

                // 记录推送历史（存储完整的平台响应）
                PushHistory history = new PushHistory();
                history.setBusinessTypeId(businessType.getId());
                history.setPlatformCode(platformCode);
                history.setGroupId(request.getGroupId());
                history.setBusinessKey(request.getBusinessKey());
                history.setRequestJson(serializeRequestParams(requestParams));
                history.setResponseJson(serializePlatformResult(platformResult));
                history.setStatus(platformResult.isSuccess() ? PushConstants.PUSH_STATUS_SUCCESS : PushConstants.PUSH_STATUS_FAILURE);
                history.setErrorMessage(platformResult.isSuccess() ? null : platformResult.getMessage());

                pushHistoryRepository.save(history);

                // 统计结果
                if (platformResult.isSuccess()) {
                    successCount++;
                    log.info("推送成功，平台：{}，traceId：{}",
                        platform.getPlatformName(), platformResult.getTraceId());
                } else {
                    failureCount++;
                    failurePlatforms.add(platformCode + "(" + platformResult.getMessage() + ")");
                    log.error("推送失败，平台：{}，错误：{}",
                        platform.getPlatformName(), platformResult.getMessage());
                }

            } catch (Exception e) {
                // 记录异常推送历史
                try {
                    BasePushRequest baseRequest = strategy.buildPushRequest(
                            parseConfigJson(config.getConfigJson()),
                            request.getDynamicParams(),
                            members);
                    Map<String, Object> requestParams = baseRequest.toMap();

                    PlatformPushResult errorResult = new PlatformPushResult();
                    errorResult.setSuccess(false);
                    errorResult.setMessage("执行异常: " + e.getMessage());
                    errorResult.setExceptionStack(getStackTrace(e));

                    PushHistory history = new PushHistory();
                    history.setBusinessTypeId(businessType.getId());
                    history.setPlatformCode(platformCode);
                    history.setGroupId(request.getGroupId());
                    history.setBusinessKey(request.getBusinessKey());
                    history.setRequestJson(serializeRequestParams(requestParams));
                    history.setResponseJson(serializePlatformResult(errorResult));
                    history.setStatus(PushConstants.PUSH_STATUS_FAILURE);
                    history.setErrorMessage("执行异常: " + e.getMessage());
                    pushHistoryRepository.save(history);
                } catch (Exception saveException) {
                    log.error("保存推送历史失败", saveException);
                }

                failureCount++;
                failurePlatforms.add(platformCode + "(执行异常)");
                log.error("推送执行异常，平台：{}", platform.getPlatformName(), e);
            }
        }

        // 8. 构建返回结果
        if (successCount == 0 && failureCount > 0) {
            String message = String.format("推送全部失败，失败平台：%s", String.join("、", failurePlatforms));
            log.error("推送执行结果：{}", message);
            return PushResult.failure(message);
        } else if (successCount > 0 && failureCount > 0) {
            String message = String.format("推送部分成功（成功：%d，失败：%d），失败平台：%s",
                    successCount, failureCount, String.join("、", failurePlatforms));
            log.warn("推送执行结果：{}", message);
            return PushResult.success(message);
        } else {
            String message = String.format("推送全部成功，成功：%d", successCount);
            log.info("推送执行结果：{}", message);
            return PushResult.success(message);
        }
    }

    private PushPlatformStrategy getStrategy(String platformCode) {
        return strategies.stream()
                .filter(s -> s.getPlatformCode().equals(platformCode))
                .findFirst()
                .orElse(null);
    }

    /**
     * 解析配置JSON
     */
    private Map<String, Object> parseConfigJson(String json) {
        if (json == null || json.isEmpty()) {
            log.debug("配置JSON为空，使用空配置");
            return new HashMap<>();
        }

        try {
            return objectMapper.readValue(json, new TypeReference<Map<String, Object>>() {});
        } catch (Exception e) {
            log.error("解析配置JSON失败，使用空配置。JSON：{}", json, e);
            return new HashMap<>();
        }
    }

    /**
     * 序列化请求参数为JSON字符串
     */
    private String serializeRequestParams(Map<String, Object> requestParams) {
        if (requestParams == null) {
            return PushConstants.DEFAULT_JSON;
        }

        try {
            return objectMapper.writeValueAsString(requestParams);
        } catch (Exception e) {
            log.error("序列化请求参数失败，降级为toString()", e);
            return requestParams.toString();
        }
    }

    /**
     * 序列化平台推送结果为JSON字符串
     */
    private String serializePlatformResult(PlatformPushResult platformResult) {
        if (platformResult == null) {
            return PushConstants.NULL_RESULT_JSON;
        }

        try {
            return objectMapper.writeValueAsString(platformResult);
        } catch (Exception e) {
            log.error("序列化平台推送结果失败，降级为toString()", e);
            return platformResult.toString();
        }
    }

    /**
     * 获取异常堆栈信息
     */
    private String getStackTrace(Exception e) {
        if (e == null) {
            return null;
        }
        java.io.StringWriter sw = new java.io.StringWriter();
        java.io.PrintWriter pw = new java.io.PrintWriter(sw);
        e.printStackTrace(pw);
        return sw.toString();
    }
}
