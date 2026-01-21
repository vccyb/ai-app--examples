package com.push.mapper;

import com.push.entity.PushConfig;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * 推送配置Repository
 */
@Repository
public interface PushConfigRepository extends JpaRepository<PushConfig, Long> {
    List<PushConfig> findByBusinessTypeId(Long businessTypeId);
    PushConfig findByBusinessTypeIdAndPlatformCode(Long businessTypeId, String platformCode);
}
