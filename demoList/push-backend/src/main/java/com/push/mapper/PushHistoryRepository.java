package com.push.mapper;

import com.push.entity.PushHistory;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

/**
 * 推送历史Repository
 */
@Repository
public interface PushHistoryRepository extends JpaRepository<PushHistory, Long> {
    Page<PushHistory> findByOrderByCreatedAtDesc(Pageable pageable);
}
