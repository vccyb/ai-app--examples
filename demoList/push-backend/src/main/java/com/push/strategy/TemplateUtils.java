package com.push.strategy;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.push.entity.GroupMember;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * 推送模板工具类
 */
public class TemplateUtils {

    private static final ObjectMapper objectMapper = new ObjectMapper();

    /**
     * 基于模板构建推送请求
     * @param template 配置模板（完整 JSON）
     * @param dynamicParams 前端传递的动态参数
     * @return 最终推送请求
     */
    public static Map<String, Object> buildFromTemplate(
            Map<String, Object> template,
            Map<String, Object> dynamicParams) {

        // 1. 深拷贝模板
        Map<String, Object> result = deepCopy(template);

        // 2. 用前端参数覆盖模板字段
        if (dynamicParams != null) {
            dynamicParams.forEach((key, value) -> {
                if (value != null) {
                    result.put(key, value);
                }
            });
        }

        return result;
    }

    /**
     * 深拷贝 Map
     */
    @SuppressWarnings("unchecked")
    private static Map<String, Object> deepCopy(Map<String, Object> original) {
        if (original == null || original.isEmpty()) {
            return new HashMap<>();
        }

        try {
            // 使用 Jackson 序列化再反序列化实现深拷贝
            String json = objectMapper.writeValueAsString(original);
            return objectMapper.readValue(json, Map.class);
        } catch (JsonProcessingException e) {
            // 如果序列化失败，返回浅拷贝
            return new HashMap<>(original);
        }
    }

    /**
     * 从群组成员列表中提取工号
     */
    public static List<String> extractEmployeeNos(List<GroupMember> members) {
        if (members == null || members.isEmpty()) {
            return new ArrayList<>();
        }
        return members.stream()
                .map(GroupMember::getEmployeeNo)
                .toList();
    }
}
