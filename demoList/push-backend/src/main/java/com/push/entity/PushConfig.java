package com.push.entity;

import jakarta.persistence.*;
import lombok.Data;
import java.time.LocalDateTime;

/**
 * 推送配置表
 */
@Data
@Entity
@Table(name = "push_config", uniqueConstraints = {
    @UniqueConstraint(columnNames = {"business_type_id", "platform_code"})
})
public class PushConfig {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "business_type_id", nullable = false)
    private Long businessTypeId;

    @Column(name = "platform_code", nullable = false, length = 50)
    private String platformCode;

    private Integer enabled = 1;

    @Lob
    @Column(name = "config_json")
    private String configJson;

    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt = LocalDateTime.now();

    @Column(name = "updated_at")
    private LocalDateTime updatedAt = LocalDateTime.now();

    @PreUpdate
    public void preUpdate() {
        this.updatedAt = LocalDateTime.now();
    }
}
