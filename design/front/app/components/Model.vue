<template>
  <div class="model-background">
    <TresCanvas ref="canvasRef" clear-color="#000000" shadows @ready="onCanvasReady" style="filter: contrast(1)">
      <TresPerspectiveCamera :position="[60, 90, 70]" />
      <OrbitControls :enable-damping="true" :damping-factor="0.05" />
      <!-- Big softbox simulation using RectAreaLight -->
      <TresRectAreaLight
        :position="[25, 10, -40]"
        :width="100"
        :height="100"
        :intensity="30"
        color="#ffffff"
        :lookAt="[0, 0, 0]"
      />
      <Environment preset="sunset" />

      <primitive v-if="model" :object="model" />
    </TresCanvas>
  </div>
</template>

<script setup lang="ts">
import { shallowRef, onMounted, watch, ref } from 'vue'
import { TresCanvas, useTresContext } from '@tresjs/core'
import { OrbitControls, Environment } from '@tresjs/cientos'
import { STLLoader } from 'three/examples/jsm/loaders/STLLoader.js'
import { EffectComposer } from 'three/examples/jsm/postprocessing/EffectComposer.js'
import { RenderPass } from 'three/examples/jsm/postprocessing/RenderPass.js'
import * as THREE from 'three'
import { useModelColor } from '~/composables/useModelColor'

const { modelColor } = useModelColor()
const model = shallowRef<THREE.Group | null>(null)
const materialRef = shallowRef<THREE.MeshPhysicalMaterial | null>(null)
const canvasRef = ref<InstanceType<typeof TresCanvas> | null>(null)
const meshRef = shallowRef<THREE.Mesh | null>(null)
const isSpinning = ref(false)
const baseRotationY = Math.PI / 8
const currentColor = shallowRef<THREE.Color>(new THREE.Color('#5500ff'))

onMounted(() => {
  const loader = new STLLoader()
  loader.load('/model.stl', (geometry) => {
    geometry.center()
    geometry.computeVertexNormals()

    const material = new THREE.MeshPhysicalMaterial({
      color: modelColor.value,
      metalness: 0.2,
      roughness: 1,
      clearcoat: 1,
      clearcoatRoughness: 0.4,
      reflectivity: 0.1,
      envMapIntensity: 0.1,
      sheen: 0,
      sheenRoughness: 0.8,
      sheenColor: new THREE.Color(0x9955ff),
      transparent: true,
      opacity: 1
    })
    materialRef.value = material

    const mesh = new THREE.Mesh(geometry, material)
    mesh.castShadow = true
    mesh.receiveShadow = true
    mesh.rotation.x = -Math.PI / 6
    mesh.rotation.y = baseRotationY
    mesh.rotation.z = 0
    meshRef.value = mesh

    // Add a floor plane to receive shadows
    const floorGeometry = new THREE.PlaneGeometry(500, 500)
    const floorMaterial = new THREE.ShadowMaterial({ opacity: 0.4 })
    const floor = new THREE.Mesh(floorGeometry, floorMaterial)
    floor.rotation.x = -Math.PI / 2
    floor.position.y = -50
    floor.receiveShadow = true

    const group = new THREE.Group()
    group.add(mesh)
    group.add(floor)
    model.value = group
  })
})

// Watch for color changes and trigger spin
watch(modelColor, (newColor) => {
  // Trigger full 360 spin with overshoot and subtle bounce back
  if (meshRef.value && !isSpinning.value) {
    isSpinning.value = true
    const mesh = meshRef.value
    const material = materialRef.value
    const duration = 700 // ms
    const startTime = performance.now()
    const fullRotation = Math.PI * 2

    // Store start and target colors
    const startColor = currentColor.value.clone()
    const targetColor = new THREE.Color(newColor)

    const spin = () => {
      const elapsed = performance.now() - startTime
      const progress = Math.min(elapsed / duration, 1)

      // Smooth ease for color (simple ease-in-out)
      const colorEased = (1 - Math.cos(progress * Math.PI)) / 2

      // Lerp color
      if (material) {
        material.color.copy(startColor).lerp(targetColor, colorEased)
      }

      // Smooth ease-out (quartic for more gradual deceleration)
      const rotationEased = 1 - Math.pow(1 - progress, 4)

      mesh.rotation.y = baseRotationY + fullRotation * rotationEased

      if (progress < 1) {
        requestAnimationFrame(spin)
      } else {
        mesh.rotation.y = baseRotationY
        currentColor.value = targetColor.clone()
        isSpinning.value = false
      }
    }

    requestAnimationFrame(spin)
  }
})

// Setup post-processing with SAO (Ambient Occlusion)
function onCanvasReady({
  scene,
  camera,
  renderer
}: {
  scene: THREE.Scene
  camera: THREE.Camera
  renderer: THREE.WebGLRenderer
}) {
  const composer = new EffectComposer(renderer)

  const renderPass = new RenderPass(scene, camera)
  composer.addPass(renderPass)

  // Override the render loop
  const animate = () => {
    requestAnimationFrame(animate)
    composer.render()
  }

  // Disable default rendering
  renderer.setAnimationLoop(null)
  animate()
}
</script>

<style scoped>
.model-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 0;
  pointer-events: auto;
}
</style>
