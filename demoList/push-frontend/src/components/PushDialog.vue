<template>
  <el-dialog
    v-model="dialogVisible"
    title="推送预览"
    width="700px"
    @close="handleClose"
  >
    <template #header>
      <div class="dialog-header">
        <span>推送预览</span>
        <div class="header-actions">
          <el-button link @click="showHistory">历史记录</el-button>
          <el-button link @click="showGroupConfig">群组配置</el-button>
          <el-button link @click="showBusinessTypeConfig">业务类型配置</el-button>
        </div>
      </div>
    </template>

    <div v-loading="loading">
      <el-descriptions :column="1" border>
        <el-descriptions-item label="业务类型">
          {{ businessName }}
        </el-descriptions-item>
      </el-descriptions>

      <el-divider />

      <div v-if="previewData.pushPlatforms && previewData.pushPlatforms.length > 0">
        <div v-for="platform in previewData.pushPlatforms" :key="platform.platformCode" class="platform-card">
          <el-card shadow="never">
            <template #header>
              <div class="platform-header">
                <span>{{ platform.platformName }}</span>
                <el-tag type="info" size="small">{{ platform.platformCode }}</el-tag>
              </div>
            </template>

            <el-form label-width="120px">
              <el-form-item label="群组">
                <el-select
                  v-model="selectedGroupId"
                  placeholder="请选择推送群组"
                  style="width: 100%"
                  @change="refreshPreview"
                >
                  <el-option
                    v-for="group in groups"
                    :key="group.id"
                    :label="group.groupName"
                    :value="group.id"
                  />
                </el-select>
              </el-form-item>

              <el-divider />

              <div v-for="(value, key) in platform.requestParams" :key="key" class="param-item">
                <div class="param-label">{{ formatParamLabel(key) }}</div>
                <div class="param-value">{{ formatValue(value) }}</div>
              </div>
            </el-form>
          </el-card>
        </div>
      </div>
      <el-empty v-else description="该业务未配置推送" />
    </div>

    <template #footer>
      <el-button @click="dialogVisible = false">取消</el-button>
      <el-button type="primary" :loading="submitting" @click="handleConfirm">
        确定推送
      </el-button>
    </template>

    <!-- 历史记录弹窗 -->
    <PushHistoryDialog v-model:visible="historyVisible" />

    <!-- 群组配置弹窗 -->
    <GroupConfigDialog v-model:visible="groupConfigVisible" />

    <!-- 业务类型配置弹窗 -->
    <BusinessTypeConfigDialog v-model:visible="businessTypeConfigVisible" />
  </el-dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import pushApi from '../api/push'
import groupApi from '../api/group'
import PushHistoryDialog from './PushHistoryDialog.vue'
import GroupConfigDialog from './GroupConfigDialog.vue'
import BusinessTypeConfigDialog from './BusinessTypeConfigDialog.vue'

const props = defineProps({
  visible: Boolean,
  businessCode: String,
  dynamicParams: Object,
  businessKey: String
})

const emit = defineEmits(['update:visible', 'success'])

const dialogVisible = computed({
  get: () => props.visible,
  set: (val) => emit('update:visible', val)
})

const loading = ref(false)
const submitting = ref(false)
const previewData = ref({ pushPlatforms: [] })
const groups = ref([])
const selectedGroupId = ref(null)
const historyVisible = ref(false)
const groupConfigVisible = ref(false)
const businessTypeConfigVisible = ref(false)

const businessName = computed(() => {
  const map = {
    'QA_REPORT': 'QA报告',
    'TEST_REPORT': '测试报告'
  }
  return map[props.businessCode] || props.businessCode
})

// 加载群组列表
const loadGroups = async () => {
  try {
    const res = await groupApi.getAll()
    groups.value = res.data || []
  } catch (error) {
    ElMessage.error('加载群组失败')
  }
}

// 刷新预览
const refreshPreview = async () => {
  if (!props.businessCode) return

  loading.value = true
  try {
    const res = await pushApi.preview({
      businessCode: props.businessCode,
      dynamicParams: props.dynamicParams || {},
      groupId: selectedGroupId.value
    })
    previewData.value = res.data
  } catch (error) {
    ElMessage.error('预览失败')
  } finally {
    loading.value = false
  }
}

// 格式化参数标签
const formatParamLabel = (key) => {
  const map = {
    title: '标题',
    content: '内容',
    jumpUrl: '跳转链接',
    receivers: '接收人',
    userIds: '接收人',
    type: '类型',
    source: '来源',
    category: '分类'
  }
  return map[key] || key
}

// 格式化值
const formatValue = (value) => {
  if (Array.isArray(value)) {
    return value.join(', ')
  }
  if (typeof value === 'object') {
    return JSON.stringify(value)
  }
  return String(value)
}

// 确认推送
const handleConfirm = async () => {
  if (!selectedGroupId.value) {
    ElMessage.warning('请选择推送群组')
    return
  }

  try {
    await ElMessageBox.confirm('确认执行推送吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    submitting.value = true
    const res = await pushApi.execute({
      businessCode: props.businessCode,
      groupId: selectedGroupId.value,
      dynamicParams: props.dynamicParams || {},
      businessKey: props.businessKey
    })

    if (res.code === 200) {
      ElMessage.success('推送成功')
      dialogVisible.value = false
      emit('success')
    } else {
      ElMessage.error(res.message || '推送失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('推送失败')
    }
  } finally {
    submitting.value = false
  }
}

// 显示历史记录
const showHistory = () => {
  historyVisible.value = true
}

// 显示群组配置
const showGroupConfig = () => {
  groupConfigVisible.value = true
}

// 显示业务类型配置
const showBusinessTypeConfig = () => {
  businessTypeConfigVisible.value = true
}

const handleClose = () => {
  previewData.value = { pushPlatforms: [] }
  selectedGroupId.value = null
}

watch(() => props.visible, (val) => {
  if (val) {
    loadGroups()
    refreshPreview()
  }
})
</script>

<style scoped>
.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
  gap: 8px;
}

.platform-card {
  margin-bottom: 16px;
}

.platform-card:last-child {
  margin-bottom: 0;
}

.platform-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.param-item {
  margin-bottom: 12px;
  padding: 8px;
  background: #f5f7fa;
  border-radius: 4px;
}

.param-label {
  font-size: 13px;
  color: #606266;
  margin-bottom: 4px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.param-tag {
  font-size: 11px;
}

.param-value {
  font-size: 14px;
  color: #303133;
  word-break: break-all;
}
</style>
