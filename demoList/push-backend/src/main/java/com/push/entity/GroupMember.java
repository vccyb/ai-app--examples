package com.push.entity;

import jakarta.persistence.*;
import lombok.Data;
import java.time.LocalDateTime;

/**
 * 群组成员表
 */
@Data
@Entity
@Table(name = "group_member",
    uniqueConstraints = {
        @UniqueConstraint(columnNames = {"group_id", "employee_no"})
    }
)
public class GroupMember {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "group_id", nullable = false)
    private Long groupId;

    @Column(name = "employee_no", nullable = false, length = 50)
    private String employeeNo;

    @Column(name = "employee_name", length = 100)
    private String employeeName;

    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt = LocalDateTime.now();
}
