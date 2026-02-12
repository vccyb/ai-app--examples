<script setup lang="ts">
import { computed } from 'vue'
import { characters } from '../data'

const props = defineProps<{
  currentCharacter: string
}>()

const currentChar = computed(() => {
  return characters.find(c => c.id === props.currentCharacter)
})

// Format debt number with commas
const formatDebt = (value: number) => {
  return value.toLocaleString('zh-CN')
}

// Format power system path
const formatPowerSystemPath = (abilities: any) => {
  if (!abilities || !abilities.path) return ''
  return abilities.path
}
</script>

<template>
  <div v-if="currentChar" class="character-info-panel">
    <!-- Header Section -->
    <div class="panel-header mb-8">
      <h1 class="character-name neon-text-cyan">
        {{ currentChar.name }}
      </h1>
      <p class="character-identity neon-text-pink">
        {{ currentChar.identity }}
      </p>
    </div>

    <!-- Debt Counter -->
    <div class="glass-card neon-border-gold debt-card mb-8 p-6">
      <div class="debt-label text-gray-400 mb-2">当前债务</div>
      <div class="debt-amount neon-text-gold">
        {{ formatDebt(currentChar.debt.total) }} 灵币
      </div>
      <div class="debt-breakdown mt-4 space-y-2">
        <div
          v-for="(item, index) in currentChar.debt.breakdown"
          :key="index"
          class="flex justify-between text-sm"
        >
          <span class="text-gray-300">{{ item.type }}</span>
          <span class="text-neon-cyan">{{ formatDebt(item.amount) }} 灵币</span>
        </div>
      </div>
    </div>

    <!-- Tags -->
    <div class="tags-container mb-8">
      <div
        v-for="(tag, index) in currentChar.tags"
        :key="index"
        class="tag-item"
      >
        {{ tag }}
      </div>
    </div>

    <!-- Cultivation Path -->
    <div class="glass-card neon-border-cyan mb-8 p-6">
      <h2 class="section-title neon-text-cyan mb-4">修行路线</h2>
      <p class="text-gray-300 text-lg">
        {{ formatPowerSystemPath(currentChar.abilities) }}
      </p>
    </div>

    <!-- Cultivation Abilities -->
    <div class="glass-card neon-border-pink mb-8 p-6">
      <h2 class="section-title neon-text-pink mb-4">核心功法</h2>
      <div class="abilities-list space-y-3">
        <div
          v-for="(ability, index) in currentChar.abilities.list.slice(0, 5)"
          :key="index"
          class="ability-item"
        >
          <div class="ability-icon text-neon-cyan">⚡</div>
          <div class="ability-content">
            <div class="ability-name text-white font-medium">{{ ability }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Key Events -->
    <div class="glass-card neon-border-gold mb-8 p-6">
      <h2 class="section-title neon-text-gold mb-4">关键事件</h2>
      <div class="events-timeline space-y-4">
        <div
          v-for="(event, index) in currentChar.key_events"
          :key="index"
          class="event-item"
        >
          <div class="event-marker">●</div>
          <div class="event-content">
            <div class="event-title text-white font-medium">
              {{ event.title }}
            </div>
            <div class="event-description text-gray-400 text-sm mt-1">
              {{ event.description }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Relationships -->
    <div class="glass-card neon-border-cyan p-6">
      <h2 class="section-title neon-text-cyan mb-4">人物关系</h2>
      <div class="relationships-list space-y-3">
        <div
          v-for="(rel, index) in currentChar.relationships"
          :key="index"
          class="relationship-item"
        >
          <div class="relationship-label text-neon-pink mb-1">
            {{ rel.label }}
          </div>
          <div class="relationship-target text-white font-medium">
            {{ rel.target }}
          </div>
          <div class="relationship-description text-gray-400 text-sm mt-1">
            {{ rel.description }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.character-info-panel {
  position: relative;
  z-index: 10;
  padding: 2rem;
  max-height: calc(100vh - 8rem);
  overflow-y: auto;
}

/* Custom scrollbar */
.character-info-panel::-webkit-scrollbar {
  width: 8px;
}

.character-info-panel::-webkit-scrollbar-track {
  background: rgba(26, 10, 46, 0.3);
}

.character-info-panel::-webkit-scrollbar-thumb {
  background: rgba(0, 245, 255, 0.5);
  border-radius: 4px;
}

.character-info-panel::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 245, 255, 0.8);
}

.panel-header {
  text-align: center;
}

.character-name {
  font-size: 3rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
  letter-spacing: 0.3rem;
}

.character-identity {
  font-size: 1.25rem;
  font-weight: 300;
}

.debt-card {
  text-align: center;
}

.debt-label {
  font-size: 0.875rem;
  letter-spacing: 0.2rem;
}

.debt-amount {
  font-size: 2.5rem;
  font-weight: bold;
  letter-spacing: 0.2rem;
}

.debt-breakdown {
  border-top: 1px solid rgba(255, 215, 0, 0.2);
  padding-top: 1rem;
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  justify-content: center;
}

.tag-item {
  padding: 0.5rem 1rem;
  background: rgba(0, 245, 255, 0.1);
  border: 1px solid rgba(0, 245, 255, 0.3);
  border-radius: 20px;
  color: #00f5ff;
  font-size: 0.875rem;
  transition: all 0.3s ease;
}

.tag-item:hover {
  background: rgba(0, 245, 255, 0.2);
  border-color: rgba(0, 245, 255, 0.6);
  transform: translateY(-2px);
}

.section-title {
  font-size: 1.5rem;
  font-weight: bold;
  letter-spacing: 0.2rem;
}

.ability-item {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background: rgba(255, 0, 110, 0.05);
  border: 1px solid rgba(255, 0, 110, 0.2);
  border-radius: 8px;
  transition: all 0.3s ease;
}

.ability-item:hover {
  background: rgba(255, 0, 110, 0.1);
  border-color: rgba(255, 0, 110, 0.4);
  transform: translateX(5px);
}

.ability-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.ability-content {
  flex: 1;
}

.ability-name {
  font-size: 1.125rem;
  margin-bottom: 0.25rem;
}

.event-item {
  display: flex;
  gap: 1rem;
  position: relative;
}

.event-marker {
  color: #ffd700;
  font-size: 1.5rem;
  flex-shrink: 0;
  text-shadow: 0 0 10px rgba(255, 215, 0, 0.8);
}

.event-content {
  flex: 1;
  padding-bottom: 0.5rem;
  border-left: 2px solid rgba(255, 215, 0, 0.3);
  padding-left: 1rem;
}

.event-title {
  font-size: 1.125rem;
}

.relationship-item {
  padding: 1rem;
  background: rgba(0, 245, 255, 0.05);
  border: 1px solid rgba(0, 245, 255, 0.2);
  border-radius: 8px;
  transition: all 0.3s ease;
}

.relationship-item:hover {
  background: rgba(0, 245, 255, 0.1);
  border-color: rgba(0, 245, 255, 0.4);
  transform: translateX(5px);
}

.relationship-label {
  font-size: 0.875rem;
  letter-spacing: 0.1rem;
  margin-bottom: 0.5rem;
}

.relationship-target {
  font-size: 1.125rem;
  margin-bottom: 0.5rem;
}

.relationship-description {
  line-height: 1.6;
}
</style>
