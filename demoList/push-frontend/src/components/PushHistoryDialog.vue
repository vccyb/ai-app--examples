<template>
  <el-dialog
    v-model="dialogVisible"
    title="推送历史记录"
    width="900px"
  >
    <el-table :data="historyList" v-loading="loading" stripe>
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="businessCode" label="业务类型" width="120">
        <template #default="{ row }">
          <el-tag size="small">{{ getBusinessName(row.businessTypeId) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="platformCode" label="平台" width="120">
        <template #default="{ row }">
          <el-tag size="small" type="info">{{ row.platformCode }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="row.status === 1 ? 'success' : 'danger'" size="small">
            {{ row.status === 1 ? '成功' : '失败' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="createdAt" label="推送时间" width="180">
        <template #default="{ row }">
          {{ formatTime(row.createdAt) }}
        </template>
      </el-table-column>
      <el-table-column prop="errorMessage" label="错误信息" show-overflow-tooltip>
        <template #default="{ row }">
          <span v-if="row.status === 0" style="color: #f56c6c">{{ row.errorMessage }}</span>
          <span v-else style="color: #909399">-</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="80" fixed="right">
        <template #default="{ row }">
          <el-button link type="primary" @click="showDetail(row)">详情</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      v-model:current-page="currentPage"
      v-model:page-size="pageSize"
      :total="total"
      :page-sizes="[10, 20, 50, 100]"
      layout="total, sizes, prev, pager, next, jumper"
      @size-change="loadHistory"
      @current-change="loadHistory"
      style="margin-top: 16px; justify-content: flex-end"
    />

    <!-- 详情弹窗 -->
    <el-dialog
      v-model="detailVisible"
      title="推送详情"
      width="700px"
      append-to-body
    >
      <el-descriptions :column="1" border v-if="currentHistory">
        <el-descriptions-item label="ID">{{ currentHistory.id }}</el-descriptions-item>
        <el-descriptions-item label="业务类型">{{ getBusinessName(currentHistory.businessTypeId) }}</el-descriptions-item>
        <el-descriptions-item label="平台">{{ currentHistory.platformCode }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="currentHistory.status === 1 ? 'success' : 'danger'" size="small">
            {{ currentHistory.status === 1 ? '成功' : '失败' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="推送时间">{{ formatTime(currentHistory.createdAt) }}</el-descriptions-item>
        <el-descriptions-item v-if="currentHistory.errorMessage" label="错误信息">
          <span style="color: #f56c6c">{{ currentHistory.errorMessage }}</span>
        </el-descriptions-item>
      </el-descriptions>

      <el-divider content-position="left">请求参数</el-divider>
      <el-input
        type="textarea"
        :model-value="formatJson(currentHistory?.requestJson)"
        :rows="8"
        readonly
      />

      <el-divider content-position="left">响应结果</el-divider>
      <el-input
        type="textarea"
        :model-value="formatJson(currentHistory?.responseJson)"
        :rows="8"
        readonly
      />
    </el-dialog>
  </el-dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import historyApi from '../api/history'

const props = defineProps({
  visible: Boolean
})

const emit = defineEmits(['update:visible'])

const dialogVisible = computed({
  get: () => props.visible,
  set: (val) => emit('update:visible', val)
})

const loading = ref(false)
const historyList = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const detailVisible = ref(false)
const currentHistory = ref(null)

// 业务类型映射
const businessTypeMap = {
  1: 'QA报告',
  2: '测试报告'
}

const getBusinessName = (typeId) => {
  return businessTypeMap[typeId] || `业务类型${typeId}`
}

// 加载历史记录
const loadHistory = async () => {
  loading.value = true
  try {
    const res = await historyApi.getPage(currentPage.value - 1, pageSize.value)
    historyList.value = res.data.content || []
    total.value = res.data.totalElements || 0
  } catch (error) {
    ElMessage.error('加载历史记录失败')
  } finally {
    loading.value = false
  }
}

// 显示详情
const showDetail = (row) => {
  currentHistory.value = row
  detailVisible.value = true
}

// 格式化时间
const formatTime = (time) => {
  if (!time) return '-'
  return new Date(time).toLocaleString('zh-CN')
}

// 格式化JSON
const formatJson = (json) => {
  if (!json) return '-'
  try {
    return JSON.stringify(JSON.parse(json), null, 2)
  } catch {
    return json
  }
}

// 监听弹窗显示
watch(() => props.visible, (val) => {
  if (val) {
    loadHistory()
  }
})
</script>
