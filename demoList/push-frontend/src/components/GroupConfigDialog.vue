<template>
  <el-dialog
    v-model="dialogVisible"
    title="群组配置"
    width="900px"
  >
    <div class="group-config-container">
      <!-- 左侧：群组列表 -->
      <div class="group-list">
        <div class="list-header">
          <span>群组列表</span>
          <el-button type="primary" size="small" @click="handleCreateGroup">
            <el-icon><Plus /></el-icon>
            新建群组
          </el-button>
        </div>
        <el-table
          :data="groups"
          highlight-current-row
          @row-click="selectGroup"
          v-loading="loading"
        >
          <el-table-column prop="id" label="ID" width="60" />
          <el-table-column prop="groupName" label="群组名称" />
          <el-table-column prop="description" label="描述" show-overflow-tooltip />
          <el-table-column label="操作" width="120">
            <template #default="{ row }">
              <el-button link type="primary" @click.stop="handleEditGroup(row)">编辑</el-button>
              <el-button link type="danger" @click.stop="handleDeleteGroup(row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- 右侧：成员管理 -->
      <div class="member-list">
        <div class="list-header">
          <span>{{ selectedGroup ? `成员列表 - ${selectedGroup.groupName}` : '请选择群组' }}</span>
          <el-button
            v-if="selectedGroup"
            type="primary"
            size="small"
            @click="showAddMember"
          >
            <el-icon><Plus /></el-icon>
            添加成员
          </el-button>
        </div>
        <el-table
          :data="members"
          v-loading="membersLoading"
        >
          <el-table-column prop="id" label="ID" width="60" />
          <el-table-column prop="employeeNo" label="工号" width="120" />
          <el-table-column prop="employeeName" label="姓名" />
          <el-table-column prop="createdAt" label="加入时间" width="150">
            <template #default="{ row }">
              {{ formatTime(row.createdAt) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="80">
            <template #default="{ row }">
              <el-button
                link
                type="danger"
                @click="handleDeleteMember(row)"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>

    <!-- 群组编辑弹窗 -->
    <el-dialog
      v-model="groupFormVisible"
      :title="isEdit ? '编辑群组' : '新建群组'"
      width="500px"
      append-to-body
    >
      <el-form :model="groupForm" label-width="80px">
        <el-form-item label="群组名称" required>
          <el-input v-model="groupForm.groupName" placeholder="请输入群组名称" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input
            v-model="groupForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入群组描述"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="groupFormVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSaveGroup">确定</el-button>
      </template>
    </el-dialog>

    <!-- 添加成员弹窗 -->
    <el-dialog
      v-model="memberFormVisible"
      title="添加成员"
      width="400px"
      append-to-body
    >
      <el-form :model="memberForm" label-width="80px">
        <el-form-item label="工号" required>
          <el-input
            v-model="memberForm.employeeNo"
            placeholder="请输入工号，如：c00807372"
          />
        </el-form-item>
        <el-form-item label="姓名">
          <el-input v-model="memberForm.employeeName" placeholder="请输入姓名（可选）" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="memberFormVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSaveMember">确定</el-button>
      </template>
    </el-dialog>
  </el-dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import groupApi from '../api/group'

const props = defineProps({
  visible: Boolean
})

const emit = defineEmits(['update:visible'])

const dialogVisible = computed({
  get: () => props.visible,
  set: (val) => emit('update:visible', val)
})

const loading = ref(false)
const groups = ref([])
const selectedGroup = ref(null)
const members = ref([])
const membersLoading = ref(false)

// 群组表单
const groupFormVisible = ref(false)
const isEdit = ref(false)
const groupForm = ref({
  id: null,
  groupName: '',
  description: ''
})

// 成员表单
const memberFormVisible = ref(false)
const memberForm = ref({
  employeeNo: '',
  employeeName: ''
})

// 加载群组列表
const loadGroups = async () => {
  loading.value = true
  try {
    const res = await groupApi.getAll()
    groups.value = res.data || []
  } catch (error) {
    ElMessage.error('加载群组列表失败')
  } finally {
    loading.value = false
  }
}

// 选择群组
const selectGroup = (row) => {
  selectedGroup.value = row
  loadMembers()
}

// 加载成员列表
const loadMembers = async () => {
  if (!selectedGroup.value) return

  membersLoading.value = true
  try {
    const res = await groupApi.getMembers(selectedGroup.value.id)
    members.value = res.data || []
  } catch (error) {
    ElMessage.error('加载成员列表失败')
  } finally {
    membersLoading.value = false
  }
}

// 新建群组
const handleCreateGroup = () => {
  isEdit.value = false
  groupForm.value = { id: null, groupName: '', description: '' }
  groupFormVisible.value = true
}

// 编辑群组
const handleEditGroup = (row) => {
  isEdit.value = true
  groupForm.value = { ...row }
  groupFormVisible.value = true
}

// 保存群组
const handleSaveGroup = async () => {
  if (!groupForm.value.groupName) {
    ElMessage.warning('请输入群组名称')
    return
  }

  try {
    if (isEdit.value) {
      await groupApi.update(groupForm.value.id, groupForm.value)
      ElMessage.success('更新成功')
    } else {
      await groupApi.create(groupForm.value)
      ElMessage.success('创建成功')
    }
    groupFormVisible.value = false
    loadGroups()
  } catch (error) {
    ElMessage.error('保存失败')
  }
}

// 删除群组
const handleDeleteGroup = async (row) => {
  try {
    await ElMessageBox.confirm(`确定删除群组"${row.groupName}"吗？`, '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    await groupApi.delete(row.id)
    ElMessage.success('删除成功')

    if (selectedGroup.value?.id === row.id) {
      selectedGroup.value = null
      members.value = []
    }

    loadGroups()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 显示添加成员
const showAddMember = () => {
  memberForm.value = { employeeNo: '', employeeName: '' }
  memberFormVisible.value = true
}

// 保存成员
const handleSaveMember = async () => {
  if (!memberForm.value.employeeNo) {
    ElMessage.warning('请输入工号')
    return
  }

  try {
    await groupApi.addMember(
      selectedGroup.value.id,
      memberForm.value.employeeNo,
      memberForm.value.employeeName
    )
    ElMessage.success('添加成功')
    memberFormVisible.value = false
    loadMembers()
  } catch (error) {
    ElMessage.error('添加失败')
  }
}

// 删除成员
const handleDeleteMember = async (row) => {
  try {
    await ElMessageBox.confirm('确定删除该成员吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    await groupApi.deleteMember(selectedGroup.value.id, row.id)
    ElMessage.success('删除成功')
    loadMembers()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 格式化时间
const formatTime = (time) => {
  if (!time) return '-'
  return new Date(time).toLocaleString('zh-CN')
}

// 监听弹窗显示
watch(() => props.visible, (val) => {
  if (val) {
    loadGroups()
  }
})
</script>

<style scoped>
.group-config-container {
  display: flex;
  height: 500px;
  gap: 16px;
}

.group-list,
.member-list {
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
