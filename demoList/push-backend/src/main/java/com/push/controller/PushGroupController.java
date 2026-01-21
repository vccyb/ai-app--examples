package com.push.controller;

import com.push.dto.ApiResponse;
import com.push.entity.GroupMember;
import com.push.entity.PushGroup;
import com.push.service.PushGroupService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * 推送群组控制器
 */
@RestController
@RequestMapping("/api/push/groups")
@CrossOrigin(origins = "*")
public class PushGroupController {

    @Autowired
    private PushGroupService pushGroupService;

    /**
     * 获取群组列表
     */
    @GetMapping
    public ApiResponse<List<PushGroup>> getAll() {
        return ApiResponse.success(pushGroupService.getAll());
    }

    /**
     * 创建群组
     */
    @PostMapping
    public ApiResponse<PushGroup> create(@RequestBody PushGroup group) {
        PushGroup created = pushGroupService.create(group);
        return ApiResponse.success(created);
    }

    /**
     * 更新群组
     */
    @PutMapping("/{id}")
    public ApiResponse<PushGroup> update(@PathVariable Long id, @RequestBody PushGroup group) {
        PushGroup updated = pushGroupService.update(id, group);
        return ApiResponse.success(updated);
    }

    /**
     * 删除群组
     */
    @DeleteMapping("/{id}")
    public ApiResponse<Void> delete(@PathVariable Long id) {
        pushGroupService.delete(id);
        return ApiResponse.success(null);
    }

    /**
     * 获取群组成员
     */
    @GetMapping("/{id}/members")
    public ApiResponse<List<GroupMember>> getMembers(@PathVariable Long id) {
        return ApiResponse.success(pushGroupService.getMembers(id));
    }

    /**
     * 添加成员
     */
    @PostMapping("/{id}/members")
    public ApiResponse<GroupMember> addMember(
            @PathVariable Long id,
            @RequestParam String employeeNo,
            @RequestParam(required = false) String employeeName) {
        GroupMember member = pushGroupService.addMember(id, employeeNo, employeeName);
        return ApiResponse.success(member);
    }

    /**
     * 删除成员
     */
    @DeleteMapping("/{id}/members/{memberId}")
    public ApiResponse<Void> deleteMember(
            @PathVariable Long id,
            @PathVariable Long memberId) {
        pushGroupService.deleteMember(id, memberId);
        return ApiResponse.success(null);
    }
}
