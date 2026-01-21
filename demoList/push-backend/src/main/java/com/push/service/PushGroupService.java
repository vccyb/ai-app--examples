package com.push.service;

import com.push.entity.GroupMember;
import com.push.entity.PushGroup;

import java.util.List;

/**
 * 推送群组服务接口
 */
public interface PushGroupService {
    /**
     * 获取所有群组
     */
    List<PushGroup> getAll();

    /**
     * 创建群组
     */
    PushGroup create(PushGroup group);

    /**
     * 更新群组
     */
    PushGroup update(Long id, PushGroup group);

    /**
     * 删除群组
     */
    void delete(Long id);

    /**
     * 获取群组成员
     */
    List<GroupMember> getMembers(Long groupId);

    /**
     * 添加成员
     */
    GroupMember addMember(Long groupId, String employeeNo, String employeeName);

    /**
     * 删除成员
     */
    void deleteMember(Long groupId, Long memberId);
}
