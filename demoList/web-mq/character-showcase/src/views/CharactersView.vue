<script setup lang="ts">
import { ref } from 'vue'
import { characters } from '../data'
import CharacterScene3D from '../components/CharacterScene3D.vue'
import CharacterInfoPanel from '../components/CharacterInfoPanel.vue'
import CharacterSelector from '../components/CharacterSelector.vue'

// Start with the first main character (张羽)
const currentCharacterId = ref('zhang_yu')

function selectCharacter(characterId: string) {
  currentCharacterId.value = characterId
}
</script>

<template>
  <div class="characters-view">
    <!-- 3D Scene (Left side - 60%) -->
    <div class="scene-section">
      <CharacterScene3D :current-character="currentCharacterId" />
    </div>

    <!-- Info Panel (Right side - 40%) -->
    <div class="info-section">
      <CharacterInfoPanel :current-character="currentCharacterId" />
    </div>

    <!-- Character Selector (Bottom center) -->
    <CharacterSelector
      :current-character="currentCharacterId"
      @select="selectCharacter"
    />

    <!-- Scan line effect -->
    <div class="scan-line"></div>
  </div>
</template>

<style scoped>
.characters-view {
  position: relative;
  width: 100%;
  height: 100vh;
  display: grid;
  grid-template-columns: 60fr 40fr;
  overflow: hidden;
  padding-top: 5rem; /* Account for fixed navigation bar */
}

.scene-section {
  position: relative;
  width: 100%;
  height: 100%;
}

.info-section {
  position: relative;
  width: 100%;
  height: 100%;
  overflow-y: auto;
  background: rgba(10, 10, 10, 0.5);
  backdrop-filter: blur(5px);
}

/* Responsive design */
@media (max-width: 1024px) {
  .characters-view {
    grid-template-columns: 1fr;
    grid-template-rows: 50fr 50fr;
  }

  .info-section {
    order: 2;
  }

  .scene-section {
    order: 1;
  }
}
</style>
