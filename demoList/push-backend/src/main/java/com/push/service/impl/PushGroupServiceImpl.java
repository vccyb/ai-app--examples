package com.push.service.impl;

import com.push.entity.GroupMember;
import com.push.entity.PushGroup;
import com.push.mapper.GroupMemberRepository;
import com.push.mapper.PushGroupRepository;
import com.push.service.PushGroupService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

/**
 * 推送群组服务实现
 */
@Service
public class PushGroupServiceImpl implements PushGroupService {

    @Autowired
    private PushGroupRepository pushGroupRepository;

    @Autowired
    private GroupMemberRepository groupMemberRepository;

    @Override
    public List<PushGroup> getAll() {
        return pushGroupRepository.findAll();
    }

    @Override
    public PushGroup create(PushGroup group) {
        return pushGroupRepository.save(group);
    }

    @Override
    public PushGroup update(Long id, PushGroup group) {
        PushGroup existing = pushGroupRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("群组不存在"));
        existing.setGroupName(group.getGroupName());
        existing.setDescription(group.getDescription());
        return pushGroupRepository.save(existing);
    }

    @Override
    @Transactional
    public void delete(Long id) {
        groupMemberRepository.deleteByGroupId(id);
        pushGroupRepository.deleteById(id);
    }

    @Override
    public List<GroupMember> getMembers(Long groupId) {
        return groupMemberRepository.findByGroupId(groupId);
    }

    @Override
    public GroupMember addMember(Long groupId, String employeeNo, String employeeName) {
        GroupMember member = new GroupMember();
        member.setGroupId(groupId);
        member.setEmployeeNo(employeeNo);
        member.setEmployeeName(employeeName);
        return groupMemberRepository.save(member);
    }

    @Override
    public void deleteMember(Long groupId, Long memberId) {
        groupMemberRepository.deleteByGroupIdAndId(groupId, memberId);
    }
}
