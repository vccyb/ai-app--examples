<script setup lang="ts">
import { onMounted, onUnmounted, ref, watch } from 'vue'
import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js'
import gsap from 'gsap'

const props = defineProps<{
  currentCharacter: string
}>()

const sceneContainer = ref<HTMLDivElement>()

// Scene variables
let scene: THREE.Scene
let camera: THREE.PerspectiveCamera
let renderer: THREE.WebGLRenderer
let controls: OrbitControls
let characterStandee: THREE.Mesh
let particles: THREE.Points
let animationFrameId: number
let isAnimating = false // 防止动画冲突

// Character colors
const characterColors: Record<string, { top: string; bottom: string }> = {
  zhang_yu: { top: '#00f5ff', bottom: '#1a0a2e' }, // Blue-cyan gradient
  bai_zhenzhen: { top: '#ff006e', bottom: '#1a0a2e' }, // Pink-purple gradient
}

onMounted(() => {
  initScene()
  createGridFloor()
  createParticles()
  createCharacterStandee(props.currentCharacter)
  animate()

  window.addEventListener('resize', onWindowResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', onWindowResize)
  if (animationFrameId) {
    cancelAnimationFrame(animationFrameId)
  }
})

// Watch for character changes
watch(() => props.currentCharacter, (newChar) => {
  updateCharacterStandee(newChar)
})

function initScene() {
  // Scene
  scene = new THREE.Scene()
  scene.background = new THREE.Color(0x0a0a0a)
  scene.fog = new THREE.Fog(0x0a0a0a, 10, 50)

  // Camera
  camera = new THREE.PerspectiveCamera(
    60,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
  )
  camera.position.set(0, 3, 8)
  camera.lookAt(0, 2, 0)

  // Renderer
  renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true })
  renderer.setSize(window.innerWidth, window.innerHeight)
  renderer.setPixelRatio(window.devicePixelRatio)
  sceneContainer.value?.appendChild(renderer.domElement)

  // Controls
  controls = new OrbitControls(camera, renderer.domElement)
  controls.enableDamping = true
  controls.dampingFactor = 0.05
  controls.maxPolarAngle = Math.PI / 2 - 0.1
  controls.minDistance = 5
  controls.maxDistance = 15
  controls.target.set(0, 2, 0)

  // Lights
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.4)
  scene.add(ambientLight)

  // Main light (from top-left)
  const mainLight = new THREE.DirectionalLight(0xffffff, 1)
  mainLight.position.set(5, 10, 5)
  scene.add(mainLight)

  // Rim light (cyan, from right)
  const rimLight = new THREE.PointLight(0x00f5ff, 2, 20)
  rimLight.position.set(-5, 5, 5)
  scene.add(rimLight)

  // Fill light (pink, from front)
  const fillLight = new THREE.PointLight(0xff006e, 1.5, 20)
  fillLight.position.set(0, 3, 8)
  scene.add(fillLight)
}

function createGridFloor() {
  // Create Tron-style grid
  const gridSize = 40
  const gridDivisions = 40

  // Main grid (cyan)
  const gridHelper = new THREE.GridHelper(gridSize, gridDivisions, 0x00f5ff, 0x1a0a2e)
  gridHelper.position.y = 0
  scene.add(gridHelper)

  // Reflection plane (mirror-like floor)
  const planeGeometry = new THREE.PlaneGeometry(100, 100)
  const planeMaterial = new THREE.MeshStandardMaterial({
    color: 0x0a0a0a,
    metalness: 0.8,
    roughness: 0.2,
    transparent: true,
    opacity: 0.8,
  })
  const plane = new THREE.Mesh(planeGeometry, planeMaterial)
  plane.rotation.x = -Math.PI / 2
  plane.position.y = -0.01
  scene.add(plane)
}

function createParticles() {
  const particleCount = 1500
  const geometry = new THREE.BufferGeometry()
  const positions = new Float32Array(particleCount * 3)
  const colors = new Float32Array(particleCount * 3)
  const velocities = new Float32Array(particleCount * 3) // Track velocity

  for (let i = 0; i < particleCount; i++) {
    // Spawn particles from outside edges
    const angle = Math.random() * Math.PI * 2
    const radius = 15 + Math.random() * 10

    positions[i * 3] = Math.cos(angle) * radius
    positions[i * 3 + 1] = Math.random() * 10 // Height: 0-10
    positions[i * 3 + 2] = Math.sin(angle) * radius

    // Velocity towards center
    velocities[i * 3] = -Math.cos(angle) * 0.02 // x velocity
    velocities[i * 3 + 1] = (Math.random() - 0.5) * 0.01 // y velocity (slight drift)
    velocities[i * 3 + 2] = -Math.sin(angle) * 0.02 // z velocity

    // Neon colors (cyan and pink)
    if (Math.random() > 0.5) {
      colors[i * 3] = 0 // R
      colors[i * 3 + 1] = 0.96 // G
      colors[i * 3 + 2] = 1 // B (cyan)
    } else {
      colors[i * 3] = 1 // R
      colors[i * 3 + 1] = 0 // G
      colors[i * 3 + 2] = 0.43 // B (pink)
    }
  }

  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3))
  geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3))
  geometry.setAttribute('velocity', new THREE.BufferAttribute(velocities, 3))

  const material = new THREE.PointsMaterial({
    size: 0.05,
    vertexColors: true,
    transparent: true,
    opacity: 0.8,
    blending: THREE.AdditiveBlending,
  })

  particles = new THREE.Points(geometry, material)
  scene.add(particles)
}

function createCharacterStandee(characterId: string) {
  const colors = characterColors[characterId] || { top: '#00f5ff', bottom: '#1a0a2e' }

  // Create gradient texture
  const canvas = document.createElement('canvas')
  canvas.width = 512
  canvas.height = 1024
  const ctx = canvas.getContext('2d')!

  // Draw gradient
  const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height)
  gradient.addColorStop(0, colors.top)
  gradient.addColorStop(1, colors.bottom)

  ctx.fillStyle = gradient
  ctx.fillRect(0, 0, canvas.width, canvas.height)

  // Add border glow
  ctx.strokeStyle = colors.top
  ctx.lineWidth = 10
  ctx.strokeRect(5, 5, canvas.width - 10, canvas.height - 10)

  // Add character silhouette (simple shape)
  ctx.fillStyle = 'rgba(255, 255, 255, 0.1)'
  ctx.beginPath()
  ctx.arc(canvas.width / 2, canvas.height / 3, 120, 0, Math.PI * 2) // Head
  ctx.fill()

  ctx.beginPath()
  ctx.moveTo(canvas.width / 2 - 80, canvas.height / 3 + 120)
  ctx.lineTo(canvas.width / 2 + 80, canvas.height / 3 + 120)
  ctx.lineTo(canvas.width / 2 + 100, canvas.height / 3 + 350)
  ctx.lineTo(canvas.width / 2 - 100, canvas.height / 3 + 350)
  ctx.closePath()
  ctx.fill()

  // Create texture from canvas
  const texture = new THREE.CanvasTexture(canvas)

  // Create standee geometry
  const geometry = new THREE.PlaneGeometry(4, 8)
  const material = new THREE.MeshBasicMaterial({
    map: texture,
    transparent: true,
    side: THREE.DoubleSide,
  })

  characterStandee = new THREE.Mesh(geometry, material)
  characterStandee.position.set(0, 4, 0) // Centered in the scene
  scene.add(characterStandee)
}

function updateCharacterStandee(characterId: string) {
  if (isAnimating || !characterStandee) return

  isAnimating = true

  // 创建GSAP动画时间线
  const tl = gsap.timeline({
    onComplete: () => {
      isAnimating = false
    }
  })

  // 1. 当前角色淡出 + 缩小 + 旋转 (0.75秒)
  tl.to(characterStandee.scale, {
    x: 0.5,
    y: 0.5,
    z: 0.5,
    duration: 0.75,
    ease: 'power2.in'
  }, 0)
  .to(characterStandee.rotation, {
    y: characterStandee.rotation.y + Math.PI * 0.5,
    duration: 0.75,
    ease: 'power2.in'
  }, 0)
  .to(characterStandee.material, {
    opacity: 0,
    duration: 0.75,
    ease: 'power2.in'
  }, 0)

  // 2. 相机运镜 (0.5秒，与上面同时开始但稍晚结束)
  tl.to(camera.position, {
    x: camera.position.x + 2,
    y: camera.position.y + 1,
    z: camera.position.z + 2,
    duration: 0.5,
    ease: 'power1.inOut'
  }, 0.25)

  // 3. 移除旧角色，创建新角色（瞬间完成，在0.75秒时）
  tl.call(() => {
    scene.remove(characterStandee)
    characterStandee.geometry.dispose()
    ;(characterStandee.material as THREE.Material).dispose()

    createCharacterStandee(characterId)

    // 设置新角色初始状态（从下方、透明、缩小）
    characterStandee.position.y = 2 // 从下方开始
    characterStandee.scale.set(0.5, 0.5, 0.5)
    ;(characterStandee.material as THREE.Material).opacity = 0
  }, null, 0.75)

  // 4. 新角色从下方升起 + 淡入 + 放大 (0.75秒)
  tl.to(characterStandee.position, {
    y: 4, // 升到正常位置
    duration: 0.75,
    ease: 'back.out(1.7)' // 回弹效果
  }, 0.75)
  .to(characterStandee.scale, {
    x: 1,
    y: 1,
    z: 1,
    duration: 0.75,
    ease: 'back.out(1.7)'
  }, 0.75)
  .to(characterStandee.material, {
    opacity: 1,
    duration: 0.75,
    ease: 'power2.out'
  }, 0.75)

  // 5. 相机回到原位 (0.5秒)
  tl.to(camera.position, {
    x: 0,
    y: 3,
    z: 8,
    duration: 0.5,
    ease: 'power2.inOut'
  }, 1.25) // 在新角色动画开始后0.5秒开始
}

function animate() {
  animationFrameId = requestAnimationFrame(animate)

  // Rotate character standee slightly
  if (characterStandee) {
    characterStandee.rotation.y = Math.sin(Date.now() * 0.0005) * 0.1
  }

  // Update particles (flow towards center)
  if (particles) {
    const positions = particles.geometry.attributes.position.array as Float32Array
    const velocities = particles.geometry.attributes.velocity.array as Float32Array

    for (let i = 0; i < positions.length / 3; i++) {
      // Move towards center
      positions[i * 3] += velocities[i * 3]
      positions[i * 3 + 1] += velocities[i * 3 + 1]
      positions[i * 3 + 2] += velocities[i * 3 + 2]

      // Reset if too close to center
      const dist = Math.sqrt(
        positions[i * 3] ** 2 +
        positions[i * 3 + 2] ** 2
      )
      if (dist < 2) {
        const angle = Math.random() * Math.PI * 2
        const radius = 15 + Math.random() * 10
        positions[i * 3] = Math.cos(angle) * radius
        positions[i * 3 + 1] = Math.random() * 10
        positions[i * 3 + 2] = Math.sin(angle) * radius

        velocities[i * 3] = -Math.cos(angle) * 0.02
        velocities[i * 3 + 1] = (Math.random() - 0.5) * 0.01
        velocities[i * 3 + 2] = -Math.sin(angle) * 0.02
      }
    }

    particles.geometry.attributes.position.needsUpdate = true
  }

  controls.update()
  renderer.render(scene, camera)
}

function onWindowResize() {
  camera.aspect = window.innerWidth / window.innerHeight
  camera.updateProjectionMatrix()
  renderer.setSize(window.innerWidth, window.innerHeight)
}
</script>

<template>
  <div ref="sceneContainer" class="character-scene-container"></div>
</template>

<style scoped>
.character-scene-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
}
</style>
