<template>
  <div id="app">
    <ClientOnly>
      <Model />
    </ClientOnly>
    <div class="equip-1">
      <header>
        <p>equip-1<!-- <br /><span style="font-size: 1.2rem; line-height: 1">dv recorder</span> --></p>
        <img src="/dv-recorder.png" />
      </header>
      <main></main>
      <footer>
        <div class="t">
          <div :class="{ active: currentModel === 'equip-1' }" @click="setModel('equip-1')">Equip-1</div>
          <div :class="{ active: currentModel === 'firehat' }" @click="setModel('firehat')">Firehat</div>
        </div>
        <div class="d">
          <div>
            <p>
              Equip-1 is a digital video recorder, which allows users to capture video from their DV cameras via
              FireWire. It is based on a Radxa ROCK 2F, for which we developed the Firehat. This custom hat has a
              FireWire controller chip, which can be connected via the FPC cable, utilizing PCIe.
            </p>
          </div>
          <div>
            <p v-if="currentModel === 'equip-1'">
              60mm × 70mm × 25mm<br />
              Saves to MicroSD<br />
              FireWire DVin Port<br />
              WiFi, HDMI, USB<br />
              USB-C Power<br />
              Open Source Hardware<br />
            </p>
            <p v-else>
              60mm × 70mm × 25mm<br />
              FireWire DVin Port<br />
              VIA VT6315N FireWire<br />
              Compatible with RPi 5<br />
              3 Buttons + Buzzer<br />
              Open Source Hardware<br />
            </p>
          </div>
        </div>
        <div class="buttons">
          <button>Inspect</button>
          <div class="s">
            <a href="https://github.com/computerequipmentgroup/equip-1">Github</a>
            <a href="https://discord.gg/QEGVWvQaCJ">Discord</a>
          </div>
        </div>
      </footer>
    </div>
  </div>
</template>

<script setup lang="ts">
const { currentModel, setModel } = useModelColor()
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
}

a,
a:visited {
  color: black;
  text-decoration: none;
}

#app {
  display: flex;
  flex-flow: column nowrap;
  /* justify-content: center; */
  /* align-items: center; */
  height: 100vh;
  color: black;
  background: white;
}

.equip-1 {
  position: relative;
  z-index: 1;
  display: flex;
  flex-flow: column nowrap;
  justify-content: space-between;
  font-family: 'g', serif;
  max-width: 680px;
  height: 100vh;
  /* padding: 3rem; */
  pointer-events: none;
}

.equip-1 * {
  pointer-events: auto;
}

header {
  display: flex;
  flex-flow: column nowrap;
  justify-content: center;
  /* align-items: center; */
  font-family: 'w', monospace;
  font-size: 2.2rem;
  padding: 3rem;
}

header img {
  margin: 1rem 0 0 0;
  max-width: 230px;
  filter: invert(1);
}

footer {
  position: relative;
  display: flex;
  flex-flow: column nowrap;
  border-top: 1px solid rgba(0, 0, 0, 1);
  border-right: 1px solid rgba(0, 0, 0, 1);
  /* border-radius: 25px; */
  background: white;
  line-height: 1.3;
}

footer .d {
  display: flex;
}

footer .d div {
  padding: 2rem;
  color: rgba(0, 0, 0, 1);
}

footer .d div:first-of-type {
  width: 64%;
  border-right: 1px solid rgba(0, 0, 0, 1);
  color: rgba(0, 0, 0, 1);
}

footer .buttons {
  position: relative;
  display: flex;
  justify-content: center;
  border-top: 1px solid rgba(0, 0, 0, 1);
  overflow: hidden;
}

footer .buttons .s {
  width: 100%;
  display: flex;
  justify-content: space-between;
}

footer .buttons a {
  flex-grow: 1;
  padding: 1rem 4rem;
  text-align: right;
}

footer .buttons a:first-of-type {
  text-align: left;
}

footer .buttons a:hover {
  color: white;
  background: rgba(0, 0, 0, 1);
}

footer button {
  position: absolute;
  height: 100%;
  padding: 1rem 2.5rem;
  font-family: 'w', monospace;
  font-size: 1rem;
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-top: none;
  border-bottom: none;
  border-radius: 15px;
  cursor: pointer;
  transition: all 0.2s ease;
  background: linear-gradient(0deg, #5500ff 0%, rgba(0, 0, 0, 1) 100%);
  filter: invert(1) saturate(2.5);
}

footer button:hover {
  padding: 1rem 3rem;
}

footer .t {
  position: absolute;
  left: 2rem;
  top: -3rem;
  margin: -4rem -4rem 0 0;
  width: 100%;
  height: 100%;
  max-width: 125px;
  max-height: 125px;
  border-radius: 15px;
  overflow: hidden;
  background: white;
  border: 1px solid rgba(0, 0, 0, 1);
}

footer .t div {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1rem;
  height: 50%;
  cursor: pointer;
}

footer .t div:hover,
footer .t div.active {
  color: white;
  background: rgba(0, 0, 0, 1);
}
</style>
