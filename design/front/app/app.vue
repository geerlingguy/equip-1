<template>
  <div id="app">
    <ClientOnly>
      <Model />
    </ClientOnly>
    <div class="equip-1">
      <header>
        <p>equip-1</p>
        <img src="/dv-recorder.png" />
      </header>
      <main></main>
      <footer>
        <div class="t">
          <div :class="{ active: modelColor === '#4e00eb' }" @click="setColor('#4e00eb')">Equip-1</div>
          <div :class="{ active: modelColor === '#4466ff' }" @click="setColor('#4466ff')">Firehat</div>
        </div>
        <div class="d">
          <div>
            <p>
              Equip-1 is designed to make capturing FireWire footage as easy and accessible as possible. It is a
              ready-to-use device that works out of the box. The system is fully open source — you are free to modify
              the operating system and utilize all available ports for your own purposes.
            </p>
          </div>
          <div>
            <p>
              Equip-1 is designed to make capturing FireWire footage as easy and accessible as possible. It is a
              ready-to-use device that works out of the box.
            </p>
          </div>
        </div>
        <div class="buttons">
          <button>Inspect</button>
          <div class="s">
            <a href="#">Discord</a>
            <a href="#">Github</a>
          </div>
        </div>
      </footer>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useModelColor } from '~/composables/useModelColor'

const { modelColor, setColor } = useModelColor()
</script>

<style>
@font-face {
  font-family: 'g';
  src: url('~/assets/fonts/g.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: 'w';
  src: url('~/assets/fonts/w.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
  font-display: swap;
}

* {
  box-sizing: border-box;
}

html,
body {
  margin: 0;
  padding: 0;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

body {
  font-size: 18px;
}

p {
  margin: 0;
  padding: 0;
  line-height: 1.3;
}

a,
a:visited {
  color: white;
  text-decoration: none;
}

#app {
  display: flex;
  flex-flow: column nowrap;
  /* justify-content: center; */
  align-items: center;
  height: 100vh;
  color: white;
  background: black;
}

.equip-1 {
  position: relative;
  z-index: 1;
  display: flex;
  flex-flow: column nowrap;
  justify-content: space-between;
  font-family: 'g', serif;
  max-width: 580px;
  height: 100vh;
  padding: 3rem 0;
  pointer-events: none;
}

.equip-1 * {
  pointer-events: auto;
}

header {
  display: flex;
  flex-flow: column nowrap;
  justify-content: center;
  align-items: center;
  font-family: 'w', monospace;
  font-size: 2.2rem;
}

header img {
  margin: 1rem 0 0 0;
  max-width: 230px;
}

footer {
  position: relative;
  display: flex;
  flex-flow: column nowrap;
  border: 1px solid rgba(255, 255, 255, 0.25);
  border-radius: 25px;
  background: black;
}

footer .d {
  display: flex;
}

footer .d div {
  padding: 2rem;
  color: rgba(255, 255, 255, 0.5);
}

footer .d div:first-of-type {
  flex-grow: 2;
  border-right: 1px solid rgba(255, 255, 255, 0.25);
  color: rgba(255, 255, 255, 1);
}

footer .buttons {
  position: relative;
  display: flex;
  justify-content: center;
  border-top: 1px solid rgba(255, 255, 255, 0.25);
  overflow: hidden;
}

footer .buttons .s {
  width: 100%;
  display: flex;
  justify-content: space-between;
}

footer .buttons a {
  flex-grow: 1;
  padding: 1rem 2.5rem;
  text-align: right;
  border-radius: 0 0 25px 25px;
}

footer .buttons a:first-of-type {
  text-align: left;
}

footer .buttons a:hover {
  background: rgba(255, 255, 255, 0.2);
}

footer button {
  position: absolute;
  padding: 1rem 2.5rem;
  font-family: 'w', monospace;
  font-size: 1rem;
  color: white;
  border: 1px solid rgba(140, 120, 255, 0.4);
  border-radius: 100px;
  cursor: pointer;
  transition: all 0.2s ease;
  background: linear-gradient(0deg, #5500ff 0%, rgba(0, 0, 0, 1) 100%);
}

footer button:hover {
  filter: saturate(1.3);
  padding: 1rem 2.666rem;
}

footer .t {
  position: absolute;
  right: 0;
  margin: -4rem -4rem 0 0;
  width: 100%;
  height: 100%;
  max-width: 125px;
  max-height: 125px;
  border-radius: 25px;
  overflow: hidden;
  background: black;
  border: 1px solid rgba(255, 255, 255, 0.25);
}

footer .t div {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1rem;
  height: 51%;
  cursor: pointer;
}

footer .t div:hover,
footer .t div.active {
  color: black;
  background: rgba(255, 255, 255, 0.9);
}

footer .t div:first-child {
  border-bottom: 1px solid rgba(255, 255, 255, 0.25);
}
</style>
