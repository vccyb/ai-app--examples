package com.push.mapper;

import com.push.entity.GroupMember;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * 群组成员Repository
 */
@Repository
public interface GroupMemberRepository extends JpaRepository<GroupMember, Long> {
    List<GroupMember> findByGroupId(Long groupId);
    void deleteByGroupId(Long groupId);
    void deleteByGroupIdAndId(Long groupId, Long memberId);
}
