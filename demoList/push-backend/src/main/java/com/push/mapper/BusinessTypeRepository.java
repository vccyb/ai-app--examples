package com.push.mapper;

import com.push.entity.BusinessType;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

/**
 * 业务类型Repository
 */
@Repository
public interface BusinessTypeRepository extends JpaRepository<BusinessType, Long> {
    BusinessType findByBusinessCode(String businessCode);
}
