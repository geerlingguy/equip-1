<template>
  <div class="model-background" :style="{ backgroundImage: `url(/${currentModel}.png)` }"></div>
</template>

<script setup lang="ts">
const { currentModel } = useModelColor()
</script>

<style scoped>
.model-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 0;
  pointer-events: none;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  filter: contrast(1.2);
}

@media (max-width: 680px) {
  .model-background {
    background-size: contain;
  }
}
</style>
