package com.push.strategy;

import com.push.dto.PlatformPushResult;
import com.push.dto.platform.BasePushRequest;
import com.push.entity.GroupMember;

import java.util.List;
import java.util.Map;

/**
 * 推送平台策略接口
 */
public interface PushPlatformStrategy {
    /**
     * 构建推送参数（强类型）
     * @param config 配置参数
     * @param dynamicParams 动态参数
     * @param groupMembers 群组成员
     * @return 强类型的推送请求包装器
     */
    BasePushRequest buildPushRequest(Map<String, Object> config,
                                      Map<String, Object> dynamicParams,
                                      List<GroupMember> groupMembers);

    /**
     * 执行推送
     * @param request 推送请求（Map格式，用于实际API调用）
     * @return 详细的推送结果（包含HTTP状态码、响应体、traceId等）
     */
    PlatformPushResult execute(Map<String, Object> request);

    /**
     * 执行推送（强类型重载方法）
     * @param request 强类型的推送请求
     * @return 详细的推送结果
     */
    default PlatformPushResult execute(BasePushRequest request) {
        return execute(request.toMap());
    }

    /**
     * 获取平台编码
     */
    String getPlatformCode();
}
