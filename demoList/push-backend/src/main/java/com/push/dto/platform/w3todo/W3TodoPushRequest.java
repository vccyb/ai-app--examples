package com.push.dto.platform.w3todo;

import com.push.dto.platform.BasePushRequest;
import lombok.Data;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * W3代办推送请求DTO
 *
 * 接口文档：http(s)://w3-beta.huawei.com/task/rest/todotaskmanagement/v2/createtask4w3
 */
@Data
public class W3TodoPushRequest implements BasePushRequest {

    // ========== 静态参数（从配置获取） ==========

    /**
     * 应用英文名
     */
    private String appName;

    /**
     * 应用URL
     */
    private String appURL;

    /**
     * 类型（固定为 J2EE）
     */
    private String type;

    /**
     * 备用字段1
     */
    private String reserve1;

    /**
     * 备用字段2（区分任务类型）
     */
    private String reserve2;

    /**
     * 是否支持移动审批（0-不支持，1-支持）
     */
    private String reserve10;

    // ========== 动态参数（从前端传入） ==========

    /**
     * 任务描述（建议加上标题、流程和状态）
     */
    private String taskDesc;

    /**
     * 任务跳转URL（绝对地址）
     */
    private String taskURL;

    /**
     * 任务全局唯一标识符（建议拼接应用名英文简写）
     */
    private String taskUUID;

    /**
     * 任务标题
     */
    private String taskTitle;

    /**
     * 任务创建时间（格式：yyyy-MM-dd HH:mm:ss）
     */
    private String taskCreateTime;

    /**
     * 任务状态
     */
    private String taskState;

    /**
     * 任务创建人工号
     */
    private String taskCreateUser;

    /**
     * 任务创建人姓名
     */
    private String taskCreateUserName;

    /**
     * 接收人工号列表
     */
    private List<String> receiverUserAccounts;

    /**
     * 任务抄送人工号列表
     */
    private List<String> copyUserAccounts;

    /**
     * 转换为Map格式（用于预览展示、历史记录存储）
     */
    @Override
    public Map<String, Object> toMap() {
        Map<String, Object> map = new HashMap<>();

        // 静态参数
        map.put("appName", appName);
        map.put("appURL", appURL);
        map.put("type", type);
        map.put("reserve1", reserve1);
        map.put("reserve2", reserve2);
        map.put("reserve10", reserve10);

        // 动态参数
        map.put("taskDesc", taskDesc);
        map.put("taskURL", taskURL);
        map.put("taskUUID", taskUUID);
        map.put("taskTitle", taskTitle);
        map.put("taskCreateTime", taskCreateTime);
        map.put("taskState", taskState);
        map.put("taskCreateUser", taskCreateUser);
        map.put("taskCreateUserName", taskCreateUserName);

        // 接收人和抄送人
        map.put("receiverUserAccounts", receiverUserAccounts);
        map.put("copyUserAccounts", copyUserAccounts);

        return map;
    }
}
