package com.push.entity;

import jakarta.persistence.*;
import lombok.Data;
import java.time.LocalDateTime;

/**
 * 推送历史表
 */
@Data
@Entity
@Table(name = "push_history",
    indexes = {
        @Index(name = "idx_business_type", columnList = "business_type_id"),
        @Index(name = "idx_platform", columnList = "platform_code"),
        @Index(name = "idx_created_at", columnList = "created_at")
    }
)
public class PushHistory {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "business_type_id", nullable = false)
    private Long businessTypeId;

    @Column(name = "platform_code", nullable = false, length = 50)
    private String platformCode;

    @Column(name = "group_id")
    private Long groupId;

    @Column(name = "business_key", length = 100)
    private String businessKey;

    @Lob
    @Column(name = "request_json", nullable = false)
    private String requestJson;

    @Lob
    @Column(name = "response_json")
    private String responseJson;

    private Integer status = 0;

    @Lob
    @Column(name = "error_message")
    private String errorMessage;

    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt = LocalDateTime.now();
}
