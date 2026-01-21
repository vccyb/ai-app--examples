package com.push.mapper;

import com.push.entity.PushPlatform;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

/**
 * 推送平台Repository
 */
@Repository
public interface PushPlatformRepository extends JpaRepository<PushPlatform, Long> {
    PushPlatform findByPlatformCode(String platformCode);
}
