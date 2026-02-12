<script setup lang="ts">
import { computed } from 'vue'
import { characters } from '../data'

const props = defineProps<{
  currentCharacter: string
}>()

const emit = defineEmits<{
  (e: 'select', characterId: string): void
}>()

// Get only the main characters (张羽 and 白真真)
const mainCharacters = computed(() => {
  return characters.filter(c => c.id === 'zhang_yu' || c.id === 'bai_zhenzhen')
})

function selectCharacter(characterId: string) {
  emit('select', characterId)
}
</script>

<template>
  <div class="character-selector">
    <div class="selector-container">
      <button
        v-for="character in mainCharacters"
        :key="character.id"
        @click="selectCharacter(character.id)"
        :class="[
          'character-button',
          currentCharacter === character.id ? 'active' : ''
        ]"
        :title="character.name"
      >
        <div class="avatar-circle">
          <span class="avatar-text">{{ character.name.charAt(0) }}</span>
        </div>
        <div v-if="currentCharacter === character.id" class="active-ring"></div>
      </button>
    </div>
  </div>
</template>

<style scoped>
.character-selector {
  position: fixed;
  bottom: 2rem;
  left: 50%;
  transform: translateX(-50%);
  z-index: 50;
}

.selector-container {
  display: flex;
  gap: 2rem;
  align-items: center;
  justify-content: center;
  padding: 1rem 2rem;
  background: rgba(10, 10, 10, 0.8);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 245, 255, 0.3);
  border-radius: 50px;
  box-shadow: 0 0 20px rgba(0, 245, 255, 0.2);
}

.character-button {
  position: relative;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  transition: all 0.3s ease;
}

.avatar-circle {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(0, 245, 255, 0.2), rgba(255, 0, 110, 0.2));
  border: 2px solid rgba(255, 255, 255, 0.3);
  transition: all 0.3s ease;
}

.character-button:hover .avatar-circle {
  transform: scale(1.1);
  border-color: rgba(0, 245, 255, 0.8);
  box-shadow: 0 0 15px rgba(0, 245, 255, 0.5);
}

.character-button.active .avatar-circle {
  transform: scale(1.2);
  border-color: #00f5ff;
  box-shadow: 0 0 20px rgba(0, 245, 255, 0.8);
}

.avatar-text {
  font-size: 1.5rem;
  font-weight: bold;
  color: #ffffff;
  text-shadow: 0 0 10px rgba(0, 245, 255, 0.8);
}

.active-ring {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 70px;
  height: 70px;
  border-radius: 50%;
  border: 2px solid #00f5ff;
  animation: pulse-ring 2s ease-in-out infinite;
  pointer-events: none;
}

@keyframes pulse-ring {
  0% {
    transform: translate(-50%, -50%) scale(1);
    opacity: 1;
  }
  100% {
    transform: translate(-50%, -50%) scale(1.5);
    opacity: 0;
  }
}
</style>
