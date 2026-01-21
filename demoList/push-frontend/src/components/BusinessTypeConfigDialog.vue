<template>
  <el-dialog
    v-model="dialogVisible"
    title="业务类型配置"
    width="900px"
    @close="handleClose"
  >
    <div class="config-container">
      <!-- 左侧：业务类型列表 -->
      <div class="business-type-list">
        <div class="list-header">
          <span>业务类型</span>
          <el-button type="primary" size="small" @click="handleCreate">
            <el-icon><Plus /></el-icon>
            新建
          </el-button>
        </div>
        <el-table
          :data="businessTypes"
          highlight-current-row
          @row-click="selectType"
          v-loading="loading"
        >
          <el-table-column prop="id" label="ID" width="60" />
          <el-table-column prop="businessCode" label="编码" width="120" />
          <el-table-column prop="businessName" label="名称" />
          <el-table-column label="操作" width="120">
            <template #default="{ row }">
              <el-button link type="primary" @click.stop="handleEdit(row)">编辑</el-button>
              <el-button link type="danger" @click.stop="handleDelete(row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- 右侧：推送平台配置 -->
      <div class="platform-config-list">
        <div class="list-header">
          <span>{{ selectedType ? `推送平台配置 - ${selectedType.businessName}` : '请选择业务类型' }}</span>
          <el-button v-if="selectedType" type="primary" size="small" @click="showAddConfig">
            <el-icon><Plus /></el-icon>
            添加平台配置
          </el-button>
        </div>
        <el-table :data="pushConfigs" v-loading="configsLoading">
          <el-table-column prop="platformCode" label="平台编码" width="120" />
          <el-table-column prop="enabled" label="启用状态" width="100">
            <template #default="{ row }">
              <el-switch
                v-model="row.enabled"
                :active-value="1"
                :inactive-value="0"
                @change="updateEnabled(row)"
              />
            </template>
          </el-table-column>
          <el-table-column prop="configJson" label="配置JSON" show-overflow-tooltip />
          <el-table-column label="操作" width="120">
            <template #default="{ row }">
              <el-button link type="primary" @click="handleEditConfig(row)">编辑配置</el-button>
              <el-button link type="danger" @click="handleDeleteConfig(row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>

    <!-- 业务类型编辑弹窗 -->
    <el-dialog
      v-model="typeFormVisible"
      :title="isEditType ? '编辑业务类型' : '新建业务类型'"
      width="500px"
      append-to-body
    >
      <el-form :model="typeForm" label-width="80px">
        <el-form-item label="业务编码" required>
          <el-input
            v-model="typeForm.businessCode"
            placeholder="如：QA_REPORT"
            :disabled="isEditType"
          />
        </el-form-item>
        <el-form-item label="业务名称" required>
          <el-input v-model="typeForm.businessName" placeholder="如：QA报告" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="typeFormVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSaveType">确定</el-button>
      </template>
    </el-dialog>

    <!-- 推送平台配置编辑弹窗 -->
    <el-dialog
      v-model="configFormVisible"
      title="编辑推送配置"
      width="600px"
      append-to-body
    >
      <el-form :model="configForm" label-width="100px">
        <el-form-item label="平台编码">
          <el-input v-model="configForm.platformCode" disabled />
        </el-form-item>
        <el-form-item label="是否启用">
          <el-switch
            v-model="configForm.enabled"
            :active-value="1"
            :inactive-value="0"
          />
        </el-form-item>
        <el-form-item label="配置JSON">
          <el-input
            v-model="configForm.configJson"
            type="textarea"
            :rows="8"
            placeholder='例如：{"type": "QA", "source": "QA系统"}'
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="configFormVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSaveConfig">确定</el-button>
      </template>
    </el-dialog>

    <!-- 添加平台配置弹窗 -->
    <el-dialog
      v-model="addConfigVisible"
      title="添加推送平台配置"
      width="500px"
      append-to-body
    >
      <el-form :model="addConfigForm" label-width="100px">
        <el-form-item label="选择平台" required>
          <el-select
            v-model="addConfigForm.platformCode"
            placeholder="请选择推送平台"
            style="width: 100%"
          >
            <el-option
              v-for="platform in platforms"
              :key="platform.platformCode"
              :label="`${platform.platformName} (${platform.platformCode})`"
              :value="platform.platformCode"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="配置JSON">
          <el-input
            v-model="addConfigForm.configJson"
            type="textarea"
            :rows="6"
            placeholder='例如：{"type": "QA", "source": "QA系统"}'
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="addConfigVisible = false">取消</el-button>
        <el-button type="primary" @click="handleAddConfig">确定</el-button>
      </template>
    </el-dialog>
  </el-dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import configApi from '../api/config'
import pushApi from '../api/push'

const props = defineProps({
  visible: Boolean
})

const emit = defineEmits(['update:visible'])

// 弹窗控制
const dialogVisible = computed({
  get: () => props.visible,
  set: (val) => emit('update:visible', val)
})

// 数据加载
const loading = ref(false)
const configsLoading = ref(false)
const businessTypes = ref([])
const pushConfigs = ref([])
const platforms = ref([])
const selectedType = ref(null)

// 业务类型表单
const typeFormVisible = ref(false)
const isEditType = ref(false)
const typeForm = ref({ id: null, businessCode: '', businessName: '' })

// 推送配置表单
const configFormVisible = ref(false)
const configForm = ref({ id: null, businessTypeId: null, platformCode: '', enabled: 1, configJson: '' })

// 添加配置表单
const addConfigVisible = ref(false)
const addConfigForm = ref({ platformCode: '', configJson: '' })

// 加载业务类型列表
const loadBusinessTypes = async () => {
  loading.value = true
  try {
    const res = await configApi.getBusinessTypes()
    businessTypes.value = res.data || []
  } catch (error) {
    ElMessage.error('加载业务类型失败')
  } finally {
    loading.value = false
  }
}

// 加载推送平台列表
const loadPlatforms = async () => {
  try {
    const res = await pushApi.getPlatforms()
    platforms.value = res.data || []
  } catch (error) {
    ElMessage.error('加载推送平台失败')
  }
}

// 选择业务类型
const selectType = (row) => {
  selectedType.value = row
  loadPushConfigs()
}

// 加载推送配置
const loadPushConfigs = async () => {
  if (!selectedType.value) return

  configsLoading.value = true
  try {
    const res = await configApi.getBusinessConfig(selectedType.value.businessCode)
    pushConfigs.value = res.data || []
  } catch (error) {
    ElMessage.error('加载推送配置失败')
  } finally {
    configsLoading.value = false
  }
}

// 新建业务类型
const handleCreate = () => {
  isEditType.value = false
  typeForm.value = { id: null, businessCode: '', businessName: '' }
  typeFormVisible.value = true
}

// 编辑业务类型
const handleEdit = (row) => {
  isEditType.value = true
  typeForm.value = { ...row }
  typeFormVisible.value = true
}

// 保存业务类型
const handleSaveType = async () => {
  if (!typeForm.value.businessCode || !typeForm.value.businessName) {
    ElMessage.warning('请填写完整信息')
    return
  }

  try {
    if (isEditType.value) {
      await configApi.updateBusinessType(typeForm.value.id, typeForm.value)
      ElMessage.success('更新成功')
    } else {
      await configApi.createBusinessType(typeForm.value)
      ElMessage.success('创建成功')
    }
    typeFormVisible.value = false
    loadBusinessTypes()
  } catch (error) {
    ElMessage.error(error.response?.data?.message || '保存失败')
  }
}

// 删除业务类型
const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(`确定删除业务类型"${row.businessName}"吗？`, '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    await configApi.deleteBusinessType(row.id)
    ElMessage.success('删除成功')

    if (selectedType.value?.id === row.id) {
      selectedType.value = null
      pushConfigs.value = []
    }

    loadBusinessTypes()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.response?.data?.message || '删除失败')
    }
  }
}

// 更新启用状态
const updateEnabled = async (row) => {
  try {
    await configApi.saveConfig(row)
    ElMessage.success('更新成功')
  } catch (error) {
    ElMessage.error('更新失败')
    // 回滚状态
    row.enabled = row.enabled === 1 ? 0 : 1
  }
}

// 显示添加配置
const showAddConfig = () => {
  addConfigForm.value = { platformCode: '', configJson: '' }
  addConfigVisible.value = true
}

// 添加配置
const handleAddConfig = async () => {
  if (!addConfigForm.value.platformCode) {
    ElMessage.warning('请选择推送平台')
    return
  }

  try {
    await configApi.saveConfig({
      businessTypeId: selectedType.value.id,
      platformCode: addConfigForm.value.platformCode,
      enabled: 1,
      configJson: addConfigForm.value.configJson
    })
    ElMessage.success('添加成功')
    addConfigVisible.value = false
    loadPushConfigs()
  } catch (error) {
    ElMessage.error(error.response?.data?.message || '添加失败')
  }
}

// 编辑配置
const handleEditConfig = (row) => {
  configForm.value = { ...row }
  configFormVisible.value = true
}

// 保存配置
const handleSaveConfig = async () => {
  try {
    await configApi.saveConfig(configForm.value)
    ElMessage.success('更新成功')
    configFormVisible.value = false
    loadPushConfigs()
  } catch (error) {
    ElMessage.error('更新失败')
  }
}

// 删除配置
const handleDeleteConfig = async (row) => {
  try {
    await ElMessageBox.confirm('确定删除该推送配置吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    await configApi.deleteConfig(row.id)
    ElMessage.success('删除成功')
    loadPushConfigs()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const handleClose = () => {
  selectedType.value = null
  pushConfigs.value = []
}

// 监听弹窗显示
watch(() => props.visible, (val) => {
  if (val) {
    loadBusinessTypes()
    loadPlatforms()
  }
})
</script>

<style scoped>
.config-container {
  display: flex;
  height: 500px;
  gap: 16px;
}

.business-type-list,
.platform-config-list {
  flex: 1;
  display: flex;
  flex-direction: column;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  overflow: hidden;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: #f5f7fa;
  border-bottom: 1px solid #ebeef5;
  font-weight: 500;
}

:deep(.el-table) {
  flex: 1;
  overflow: auto;
}
</style>
