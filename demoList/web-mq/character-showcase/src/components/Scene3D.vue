<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'
import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js'

const sceneContainer = ref<HTMLDivElement>()

// Scene variables
let scene: THREE.Scene
let camera: THREE.PerspectiveCamera
let renderer: THREE.WebGLRenderer
let controls: OrbitControls
let pyramid: THREE.Group
let particles: THREE.Points
let animationFrameId: number

onMounted(() => {
  initScene()
  createPyramid()
  createParticles()
  animate()

  window.addEventListener('resize', onWindowResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', onWindowResize)
  if (animationFrameId) {
    cancelAnimationFrame(animationFrameId)
  }
})

function initScene() {
  // Scene
  scene = new THREE.Scene()
  scene.background = new THREE.Color(0x0a0a0a)
  scene.fog = new THREE.Fog(0x0a0a0a, 15, 60)

  // Camera - adjusted for better view
  camera = new THREE.PerspectiveCamera(
    60,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
  )
  camera.position.set(0, 8, 18)
  camera.lookAt(0, 0, 0)

  // Renderer
  renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true })
  renderer.setSize(window.innerWidth, window.innerHeight)
  renderer.setPixelRatio(window.devicePixelRatio)
  sceneContainer.value?.appendChild(renderer.domElement)

  // Controls - more permissive
  controls = new OrbitControls(camera, renderer.domElement)
  controls.enableDamping = true
  controls.dampingFactor = 0.05
  controls.maxPolarAngle = Math.PI / 2
  controls.minDistance = 8
  controls.maxDistance = 35
  controls.autoRotate = true
  controls.autoRotateSpeed = 0.5

  // Lights
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.4)
  scene.add(ambientLight)

  const pointLight = new THREE.PointLight(0x00f5ff, 2, 100)
  pointLight.position.set(10, 15, 10)
  scene.add(pointLight)

  const pointLight2 = new THREE.PointLight(0xff006e, 2, 100)
  pointLight2.position.set(-10, 15, -10)
  scene.add(pointLight2)

  const pointLight3 = new THREE.PointLight(0xffd700, 1.5, 100)
  pointLight3.position.set(0, 20, 0)
  scene.add(pointLight3)

  // Grid floor
  const gridHelper = new THREE.GridHelper(40, 40, 0x00f5ff, 0x1a0a2e)
  gridHelper.position.y = -6
  gridHelper.material.transparent = true
  gridHelper.material.opacity = 0.3
  scene.add(gridHelper)
}

function createPyramid() {
  pyramid = new THREE.Group()

  // 金字塔参数
  const height = 8
  const baseRadius = 5
  const layers = 36

  // 创建每一层
  for (let i = 0; i < layers; i++) {
    const layerHeight = height / layers
    const currentY = (i - layers / 2) * layerHeight
    const currentRadius = baseRadius * (1 - i / layers)
    const color = getLayerColor(i)

    // 层级几何体
    const geometry = new THREE.ConeGeometry(currentRadius, layerHeight, 4)
    const material = new THREE.MeshBasicMaterial({
      color: color,
      transparent: true,
      opacity: 0.3,
      wireframe: false,
    })

    const mesh = new THREE.Mesh(geometry, material)
    mesh.position.y = currentY
    pyramid.add(mesh)

    // 边框线
    const edges = new THREE.EdgesGeometry(geometry)
    const lineMaterial = new THREE.LineBasicMaterial({
      color: color,
      transparent: true,
      opacity: 0.8,
    })
    const wireframe = new THREE.LineSegments(edges, lineMaterial)
    wireframe.position.y = currentY
    pyramid.add(wireframe)
  }

  // 地下18层
  for (let i = 0; i < 18; i++) {
    const layerHeight = height / 36
    const currentY = -((layers / 2) * layerHeight) - (i + 1) * layerHeight
    const currentRadius = baseRadius * (1 - (layers + i) / (layers + 18))
    const color = 0x333333 // 深灰色

    const geometry = new THREE.ConeGeometry(currentRadius, layerHeight, 4)
    const material = new THREE.MeshBasicMaterial({
      color: color,
      transparent: true,
      opacity: 0.2,
      wireframe: true,
    })

    const mesh = new THREE.Mesh(geometry, material)
    mesh.position.y = currentY
    pyramid.add(mesh)
  }

  scene.add(pyramid)
}

function getLayerColor(layerIndex: number): number {
  // 根据层级返回不同颜色
  if (layerIndex < 5) {
    return 0xffd700 // 金色（天庭层）
  } else if (layerIndex < 15) {
    return 0x00f5ff // 霓虹青（万法大学层）
  } else if (layerIndex < 30) {
    return 0xff006e // 霓虹粉（嵩阳高中层）
  } else {
    return 0x1a0a2e // 深紫（贫民窟层）
  }
}

function createParticles() {
  const particleCount = 1000
  const geometry = new THREE.BufferGeometry()
  const positions = new Float32Array(particleCount * 3)
  const colors = new Float32Array(particleCount * 3)

  for (let i = 0; i < particleCount; i++) {
    // 随机位置
    positions[i * 3] = (Math.random() - 0.5) * 30
    positions[i * 3 + 1] = (Math.random() - 0.5) * 30
    positions[i * 3 + 2] = (Math.random() - 0.5) * 30

    // 霓虹青色
    colors[i * 3] = 0
    colors[i * 3 + 1] = 0.96
    colors[i * 3 + 2] = 1
  }

  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3))
  geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3))

  const material = new THREE.PointsMaterial({
    size: 0.05,
    vertexColors: true,
    transparent: true,
    opacity: 0.6,
  })

  particles = new THREE.Points(geometry, material)
  scene.add(particles)
}

function animate() {
  animationFrameId = requestAnimationFrame(animate)

  // 旋转金字塔
  if (pyramid) {
    pyramid.rotation.y += 0.002
  }

  // 粒子运动
  if (particles) {
    const positions = particles.geometry.attributes.position.array as Float32Array
    for (let i = 0; i < positions.length; i += 3) {
      positions[i + 1] -= 0.02 // 向下移动
      if (positions[i + 1] < -15) {
        positions[i + 1] = 15 // 重置到顶部
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
  <div ref="sceneContainer" class="scene-container"></div>
</template>

<style scoped>
.scene-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
}
</style>
