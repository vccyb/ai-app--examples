<template>
  <el-dialog
    v-model="dialogVisible"
    title="推送预览"
    width="900px"
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

    <div v-loading="loading" class="preview-container">
      <!-- 顶部信息栏 -->
      <div class="top-bar">
        <div class="business-info">
          <span class="label">业务类型：</span>
          <span class="value">{{ businessName }}</span>
        </div>
        <div class="group-selector">
          <span class="label">推送群组：</span>
          <el-select
            v-model="selectedGroupId"
            placeholder="请选择推送群组"
            style="width: 200px"
            @change="refreshPreview"
          >
            <el-option
              v-for="group in groups"
              :key="group.id"
              :label="group.groupName"
              :value="group.id"
            />
          </el-select>
        </div>
      </div>

      <!-- 空状态 -->
      <el-empty v-if="!previewData.pushPlatforms || previewData.pushPlatforms.length === 0"
                description="该业务未配置推送"
                :image-size="120" />

      <!-- 标签页展示多个推送平台 -->
      <el-tabs v-else v-model="activeTab" type="card" class="platform-tabs">
        <el-tab-pane
          v-for="platform in previewData.pushPlatforms"
          :key="platform.platformCode"
          :label="platform.platformName"
          :name="platform.platformCode"
        >
          <template #label>
            <span class="tab-label">
              <span>{{ platform.platformName }}</span>
              <el-tag size="small" type="info" effect="plain">{{ platform.platformCode }}</el-tag>
            </span>
          </template>

          <div class="platform-content">
            <!-- 参数来源图例 -->
            <div class="legend">
              <span class="legend-title">参数来源：</span>
              <el-tag size="small" type="success">配置（静态）</el-tag>
              <el-tag size="small" type="primary">动态（业务+群组）</el-tag>
            </div>

            <!-- 参数表格 -->
            <el-table :data="getTableData(platform.requestParams)"
                      class="params-table"
                      stripe
                      border
                      style="width: 100%">
              <el-table-column width="100" label="来源">
                <template #default="{ row }">
                  <el-tag :type="getParamSourceType(row.key).tagType" size="small" effect="plain">
                    {{ getParamSourceType(row.key).label }}
                  </el-tag>
                </template>
              </el-table-column>

              <el-table-column width="180" label="参数 Key">
                <template #default="{ row }">
                  <code class="param-key">{{ row.key }}</code>
                </template>
              </el-table-column>

              <el-table-column width="150" label="参数说明">
                <template #default="{ row }">
                  <span class="param-label">{{ formatParamLabel(row.key) }}</span>
                </template>
              </el-table-column>

              <el-table-column label="参数值" min-width="200">
                <template #default="{ row }">
                  <div class="param-value-cell">
                    <pre class="param-value">{{ formatValue(row.value) }}</pre>
                    <el-button
                      v-if="isLongValue(row.value)"
                      link
                      type="primary"
                      size="small"
                      @click="copyValue(row.value)"
                    >
                      复制
                    </el-button>
                  </div>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-tab-pane>
      </el-tabs>
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
const activeTab = ref('')
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

/**
 * 判断参数来源
 * 规则：
 * - 动态：业务传入的 dynamicParams + 群组信息
 * - 静态：数据库配置 + 后端自动生成
 */
const getParamSourceType = (key) => {
  const dynamicParams = props.dynamicParams || {}

  // 1. 业务传入的动态参数
  if (key in dynamicParams) {
    return { label: '动态', tagType: 'primary', type: 'dynamic' }
  }

  // 2. 群组信息（接收人相关）
  if (/^(handler|to_user_account|userIds|receivers?)$/i.test(key)) {
    return { label: '动态', tagType: 'primary', type: 'dynamic' }
  }

  // 3. 其他都是静态（数据库配置 + 后端自动生成）
  return { label: '配置', tagType: 'success', type: 'static' }
}

/**
 * 将参数对象转换为表格数据
 */
const getTableData = (params) => {
  return Object.entries(params || {}).map(([key, value]) => ({
    key,
    value,
    source: getParamSourceType(key)
  }))
}

/**
 * 判断是否为长文本值
 */
const isLongValue = (value) => {
  if (value === null || value === undefined) return false
  const str = String(value)
  return str.length > 50
}

/**
 * 复制值到剪贴板
 */
const copyValue = async (value) => {
  try {
    const str = typeof value === 'object' ? JSON.stringify(value, null, 2) : String(value)
    await navigator.clipboard.writeText(str)
    ElMessage.success('已复制到剪贴板')
  } catch (error) {
    ElMessage.error('复制失败')
  }
}

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

    // 自动切换到第一个平台
    if (previewData.value.pushPlatforms?.length > 0) {
      activeTab.value = previewData.value.pushPlatforms[0].platformCode
    }
  } catch (error) {
    ElMessage.error('预览失败')
  } finally {
    loading.value = false
  }
}

// 格式化参数标签
const formatParamLabel = (key) => {
  const map = {
    // W3 参数
    appName: '应用名称',
    appURL: '应用URL',
    type: '任务类型',
    taskDesc: '任务描述',
    taskURL: '任务链接',
    taskUUID: '任务ID',
    time: '发送时间',
    handler: '责任人',
    applicant: '申请人',
    reserve1: '保留字段1',
    reserve2: '任务类型标识',
    reserve3: '申请详情链接',
    reserve10: '移动审批支持',

    // WeLink 参数
    app_id: '应用ID',
    theme_id: '主题ID',
    templateNo: '模板编号',
    from_user_account: '发送人',
    templateTitleParams: '标题参数',
    templateContentParams: '内容参数',
    to_user_account: '接收人',
    jump_url: '跳转链接',
    displayType: '显示类型',
    noticeType: '通知类型'
  }
  return map[key] || key
}

// 格式化值
const formatValue = (value) => {
  if (value === null || value === undefined) {
    return '-'
  }
  if (Array.isArray(value)) {
    return value.join(', ')
  }
  if (typeof value === 'object') {
    return JSON.stringify(value, null, 2)
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
  activeTab.value = ''
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

.preview-container {
  min-height: 400px;
}

/* 顶部信息栏 */
.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 8px;
  margin-bottom: 20px;
  color: white;
}

.business-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.business-info .label {
  opacity: 0.9;
  font-size: 14px;
}

.business-info .value {
  font-size: 16px;
  font-weight: 600;
}

.group-selector {
  display: flex;
  align-items: center;
  gap: 8px;
}

.group-selector .label {
  opacity: 0.9;
  font-size: 14px;
}

/* 标签页样式 */
.platform-tabs {
  margin-top: 20px;
}

.tab-label {
  display: flex;
  align-items: center;
  gap: 8px;
}

.platform-content {
  padding: 20px 0;
}

/* 参数来源图例 */
.legend {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: #f8f9fa;
  border-radius: 6px;
  margin-bottom: 20px;
  border-left: 4px solid #667eea;
}

.legend-title {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
  margin-right: 8px;
}

/* 参数表格 */
.params-table {
  margin-top: 16px;
}

.param-key {
  font-size: 12px;
  color: #606266;
  background: #f5f7fa;
  padding: 2px 6px;
  border-radius: 3px;
  font-family: 'Consolas', 'Monaco', monospace;
}

.param-label {
  font-size: 13px;
  color: #303133;
  font-weight: 500;
}

.param-value-cell {
  display: flex;
  align-items: flex-start;
  gap: 8px;
}

.param-value {
  margin: 0;
  padding: 8px 12px;
  background: #fafbfc;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  font-size: 13px;
  color: #303133;
  word-break: break-all;
  line-height: 1.6;
  font-family: 'Consolas', 'Monaco', monospace;
  flex: 1;
  white-space: pre-wrap;
  max-height: 200px;
  overflow-y: auto;
}

/* 表格样式优化 */
:deep(.el-table) {
  font-size: 13px;
}

:deep(.el-table th) {
  background: #f5f7fa;
  font-weight: 600;
}

:deep(.el-table__row:hover) {
  background-color: #f8f9fa;
}

/* 空状态优化 */
:deep(.el-empty) {
  padding: 60px 0;
}

/* 响应式 */
@media (max-width: 768px) {
  .top-bar {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }

  :deep(.el-table) {
    font-size: 12px;
  }
}
</style>
