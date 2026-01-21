package com.push.strategy;

import com.push.dto.PushResult;
import com.push.entity.GroupMember;

import java.util.List;
import java.util.Map;

/**
 * 推送平台策略接口
 */
public interface PushPlatformStrategy {
    /**
     * 构建推送参数
     * @param config 配置参数
     * @param dynamicParams 动态参数
     * @param groupMembers 群组成员
     * @return 完整的推送参数
     */
    Map<String, Object> buildPushRequest(Map<String, Object> config,
                                          Map<String, Object> dynamicParams,
                                          List<GroupMember> groupMembers);

    /**
     * 执行推送
     * @param request 推送请求
     * @return 推送结果
     */
    PushResult execute(Map<String, Object> request);

    /**
     * 获取平台编码
     */
    String getPlatformCode();
}
