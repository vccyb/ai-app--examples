package com.push.mapper;

import com.push.entity.PushPlatform;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

/**
 * 推送平台Repository
 */
@Repository
public interface PushPlatformRepository extends JpaRepository<PushPlatform, Long> {
    PushPlatform findByPlatformCode(String platformCode);

    /**
     * 根据平台编码查询已启用的平台
     */
    Optional<PushPlatform> findByPlatformCodeAndEnabled(String platformCode, Integer enabled);

    /**
     * 查询所有已启用的平台
     */
    List<PushPlatform> findByEnabled(Integer enabled);
}
