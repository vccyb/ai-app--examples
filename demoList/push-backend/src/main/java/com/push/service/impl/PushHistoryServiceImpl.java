package com.push.service.impl;

import com.push.entity.PushHistory;
import com.push.mapper.PushHistoryRepository;
import com.push.service.PushHistoryService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;

import java.util.Optional;

/**
 * 推送历史服务实现
 */
@Service
public class PushHistoryServiceImpl implements PushHistoryService {

    @Autowired
    private PushHistoryRepository pushHistoryRepository;

    @Override
    public Page<PushHistory> getPage(int page, int size) {
        PageRequest pageRequest = PageRequest.of(page, size, Sort.by(Sort.Direction.DESC, "createdAt"));
        return pushHistoryRepository.findAll(pageRequest);
    }

    @Override
    public PushHistory getById(Long id) {
        return pushHistoryRepository.findById(id).orElse(null);
    }
}
