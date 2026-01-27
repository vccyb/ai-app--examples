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

    /**
     * 查询业务类型下所有已启用的推送配置
     */
    List<PushConfig> findByBusinessTypeIdAndEnabled(Long businessTypeId, Integer enabled);

    PushConfig findByBusinessTypeIdAndPlatformCode(Long businessTypeId, String platformCode);
}
