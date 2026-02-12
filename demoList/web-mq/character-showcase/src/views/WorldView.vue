<script setup lang="ts">
import Scene3D from '../components/Scene3D.vue'
import WorldInfoPanel from '../components/WorldInfoPanel.vue'
</script>

<template>
  <div class="world-view">
    <!-- 3D 场景 -->
    <Scene3D />

    <!-- 信息面板 -->
    <WorldInfoPanel />

    <!-- 扫描线效果 -->
    <div class="scan-line"></div>
  </div>
</template>

<style scoped>
.world-view {
  position: relative;
  width: 100%;
  min-height: 100vh;
  overflow-x: hidden;
}
</style>
