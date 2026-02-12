<script setup lang="ts">
import { ref } from 'vue'

const selectedLayer = ref<number | null>(null)

const layers = [
  { level: 36, name: '天庭核心', color: 'text-neon-gold', description: '十大宗门与八部正神的所在地' },
  { level: 10, name: '万法大学', color: 'text-neon-cyan', description: '高等修行学府，筑基资格证前置' },
  { level: 1, name: '嵩阳高中', color: 'text-neon-pink', description: '第一层重点高中，绝育+极限训练' },
  { level: -1, name: '地下1层', color: 'text-gray-400', description: '魂修区与工厂区' },
  { level: -18, name: '地下18层', color: 'text-gray-600', description: '最底层，危险区域' },
]

const systems = [
  {
    icon: '💰',
    title: '灵币体系',
    tagline: '锚定基础能源',
  },
  {
    icon: '🌐',
    title: '灵界网络',
    tagline: '精神互联网',
  },
  {
    icon: '💳',
    title: '法力贷',
    tagline: '借100年还150年',
  },
  {
    icon: '📚',
    title: '教育体系',
    tagline: '绝育+极限训练',
  },
]

function selectLayer(level: number) {
  selectedLayer.value = level
}
</script>

<template>
  <div class="world-info-panel">
    <!-- 标题 -->
    <div class="header">
      <h1 class="title neon-text-cyan">昆墟</h1>
      <p class="subtitle neon-text-pink">36层赛博修仙大金字塔</p>
    </div>

    <!-- 核心信息卡片 -->
    <div class="info-cards grid grid-cols-2 gap-8 mb-16">
      <div
        v-for="system in systems"
        :key="system.title"
        class="glass-card neon-border-cyan system-card p-8"
      >
        <div class="text-5xl mb-4">{{ system.icon }}</div>
        <h3 class="text-2xl font-bold neon-text-gold mb-3">{{ system.title }}</h3>
        <p class="text-base text-gray-300">{{ system.tagline }}</p>
      </div>
    </div>

    <!-- 层级结构 - 简化版 -->
    <div class="glass-card neon-border-pink p-10 mb-16">
      <h2 class="text-3xl font-bold neon-text-cyan mb-8">层级结构</h2>
      <div class="space-y-4">
        <div
          v-for="layer in layers"
          :key="layer.level"
          @click="selectLayer(layer.level)"
          :class="[
            'layer-item p-6 rounded-lg cursor-pointer transition-all',
            layer.color,
            selectedLayer === layer.level ? 'bg-white/10' : 'hover:bg-white/5'
          ]"
        >
          <div class="flex justify-between items-center mb-2">
            <span class="text-2xl font-bold">{{ layer.name }}</span>
            <span class="text-lg">第 {{ Math.abs(layer.level) }} 层</span>
          </div>
          <p class="text-base text-gray-400">{{ layer.description }}</p>
        </div>
      </div>
    </div>

    <!-- 核心规则 - 简化版 -->
    <div class="glass-card neon-border-gold p-10 mb-16">
      <h2 class="text-3xl font-bold neon-text-cyan mb-8">⚡ 核心规则</h2>
      <div class="space-y-6">
        <div class="flex items-center gap-4">
          <span class="text-neon-pink text-2xl">→</span>
          <p class="text-xl text-gray-300">升学 → 借贷 → 修仙 → 债务螺旋</p>
        </div>
        <div class="flex items-center gap-4">
          <span class="text-neon-cyan text-2xl">→</span>
          <p class="text-xl text-gray-300">一切价值用灵币与功率衡量</p>
        </div>
      </div>
    </div>

    <!-- 入口按钮 -->
    <div class="text-center">
      <button
        class="btn-neon px-12 py-5 rounded-xl text-2xl font-bold"
        @click="$router.push('/characters')"
      >
        进入角色展示 →
      </button>
    </div>
  </div>
</template>

<style scoped>
.world-info-panel {
  position: relative;
  z-index: 10;
  padding: 8rem 3rem 4rem 3rem;
  max-width: 1000px;
  margin: 0 auto;
}

.header {
  text-align: center;
  margin-bottom: 5rem;
}

.title {
  font-size: 6rem;
  font-weight: bold;
  margin-bottom: 1rem;
  letter-spacing: 0.5rem;
}

.subtitle {
  font-size: 2rem;
  letter-spacing: 0.3rem;
}

.system-card {
  min-height: 200px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  transition: all 0.3s ease;
}

.system-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 0 30px rgba(0, 245, 255, 0.3);
}

.layer-item {
  border: 1px solid transparent;
  transition: all 0.3s ease;
}

.layer-item:hover {
  border-color: rgba(0, 245, 255, 0.3);
  transform: translateX(10px);
}

.btn-neon {
  background: linear-gradient(135deg, rgba(0, 245, 255, 0.2), rgba(255, 0, 110, 0.2));
  border: 2px solid #00f5ff;
  color: #ffffff;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 0 15px rgba(0, 245, 255, 0.3);
}

.btn-neon:hover {
  background: linear-gradient(135deg, rgba(0, 245, 255, 0.4), rgba(255, 0, 110, 0.4));
  box-shadow: 0 0 30px rgba(0, 245, 255, 0.5), 0 0 30px rgba(255, 0, 110, 0.5);
  transform: translateY(-3px) scale(1.05);
}
</style>
