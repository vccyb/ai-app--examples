package com.push.mapper;

import com.push.entity.PushGroup;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * 推送群组Repository
 */
@Repository
public interface PushGroupRepository extends JpaRepository<PushGroup, Long> {
}
