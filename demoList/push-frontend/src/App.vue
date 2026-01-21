<template>
  <div id="app">
    <el-container>
      <el-header>
        <h1>推送系统演示</h1>
      </el-header>
      <el-main>
        <el-card>
          <template #header>
            <div class="card-header">
              <span>推送演示 - QA报告</span>
            </div>
          </template>

          <el-table :data="reportList" stripe>
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="reportName" label="报告名称" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="row.status === 'pending' ? 'warning' : 'success'" size="small">
                  {{ row.status === 'pending' ? '待审核' : '已完成' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="createdAt" label="创建时间" width="180" />
            <el-table-column label="操作" width="120">
              <template #default="{ row }">
                <el-button type="primary" size="small" @click="handlePush(row)">
                  推送
                </el-button>
              </template>
            </el-table-column>
          </el-table>

          <template #footer>
            <div class="footer-hint">
              <el-icon><InfoFilled /></el-icon>
              <span>点击"推送"按钮打开推送预览弹窗，可选择群组并执行推送</span>
            </div>
          </template>
        </el-card>

        <!-- 测试报告表格 -->
        <el-card style="margin-top: 20px">
          <template #header>
            <div class="card-header">
              <span>推送演示 - 测试报告</span>
            </div>
          </template>

          <el-table :data="testReportList" stripe>
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="testName" label="测试名称" />
            <el-table-column prop="result" label="测试结果" width="100">
              <template #default="{ row }">
                <el-tag :type="row.result === 'pass' ? 'success' : 'danger'" size="small">
                  {{ row.result === 'pass' ? '通过' : '失败' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="createdAt" label="创建时间" width="180" />
            <el-table-column label="操作" width="120">
              <template #default="{ row }">
                <el-button type="primary" size="small" @click="handleTestPush(row)">
                  推送
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-main>
    </el-container>

    <!-- 推送弹窗 -->
    <PushDialog
      v-model:visible="pushVisible"
      :business-code="pushBusinessCode"
      :dynamic-params="pushParams"
      :business-key="currentBusinessKey"
      @success="handlePushSuccess"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { InfoFilled } from '@element-plus/icons-vue'
import PushDialog from './components/PushDialog.vue'

// QA报告数据
const reportList = ref([
  {
    id: 1,
    reportName: '2024-Q1-QA审核报告',
    status: 'pending',
    createdAt: '2024-01-20 10:00:00'
  },
  {
    id: 2,
    reportName: '2024-Q2-QA审核报告',
    status: 'completed',
    createdAt: '2024-01-21 15:30:00'
  }
])

// 测试报告数据
const testReportList = ref([
  {
    id: 101,
    testName: '功能模块回归测试',
    result: 'pass',
    createdAt: '2024-01-21 09:00:00'
  },
  {
    id: 102,
    testName: '性能压力测试',
    result: 'fail',
    createdAt: '2024-01-21 14:00:00'
  }
])

// 推送弹窗状态
const pushVisible = ref(false)
const pushBusinessCode = ref('')
const pushParams = ref({})
const currentBusinessKey = ref('')

// QA报告推送
const handlePush = (row) => {
  pushBusinessCode.value = 'QA_REPORT'
  currentBusinessKey.value = String(row.id)
  pushParams.value = {
    title: row.reportName,
    content: `请审核QA报告: ${row.reportName}`,
    jumpUrl: `/qa/report/${row.id}`
  }
  pushVisible.value = true
}

// 测试报告推送
const handleTestPush = (row) => {
  pushBusinessCode.value = 'TEST_REPORT'
  currentBusinessKey.value = String(row.id)
  pushParams.value = {
    title: row.testName,
    content: `测试结果: ${row.result === 'pass' ? '通过' : '失败'}`,
    jumpUrl: `/test/report/${row.id}`
  }
  pushVisible.value = true
}

// 推送成功回调
const handlePushSuccess = () => {
  ElMessage.success('推送操作已完成')
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  min-height: 100vh;
  background: #f5f7fa;
}

.el-header {
  background: #409eff;
  color: white;
  display: flex;
  align-items: center;
  padding: 0 20px;
}

.el-header h1 {
  font-size: 24px;
  margin: 0;
}

.el-main {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 16px;
  font-weight: 500;
}

.footer-hint {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #909399;
  font-size: 13px;
}
</style>
