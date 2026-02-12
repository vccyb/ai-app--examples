<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

function goToCharacters() {
  router.push('/characters')
}

function goToWorld() {
  router.push('/')
}
</script>

<template>
  <div class="min-h-screen bg-cyber-black text-white">
    <!-- 导航栏 -->
    <nav class="fixed top-0 left-0 right-0 z-50 glass-card border-b border-neon-cyan/30">
      <div class="container mx-auto px-6 py-4 flex justify-between items-center">
        <h1 class="text-2xl font-bold neon-text-cyan cursor-pointer tracking-wider" @click="goToWorld">
          没钱修什么仙
        </h1>
        <div class="flex gap-6">
          <button
            @click="goToWorld"
            class="px-6 py-2 rounded-lg text-base font-medium transition-all"
            :class="router.currentRoute.value?.name === 'world' ? 'bg-neon-cyan/20 text-neon-cyan border border-neon-cyan/50' : 'hover:bg-white/5 hover:border hover:border-white/10'"
          >
            世界观
          </button>
          <button
            @click="goToCharacters"
            class="px-6 py-2 rounded-lg text-base font-medium transition-all"
            :class="router.currentRoute.value?.name === 'characters' ? 'bg-neon-cyan/20 text-neon-cyan border border-neon-cyan/50' : 'hover:bg-white/5 hover:border hover:border-white/10'"
          >
            角色
          </button>
        </div>
      </div>
    </nav>

    <!-- 路由视图 -->
    <router-view />

    <!-- 扫描线效果 -->
    <div class="scan-line"></div>
  </div>
</template>

<style scoped>
/* 组件特定样式 */
</style>
