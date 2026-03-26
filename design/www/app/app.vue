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
        <div class="d" :class="{ open: inspectOpen }">
          <div class="content">
            <p>
              Equip-1 is a digital video recorder, which allows users to capture video from their DV cameras via
              FireWire. It is based on a Radxa ROCK 2F, for which we developed the Firehat. This custom hat has a
              FireWire controller chip, which can be connected via the FPC cable, utilizing PCIe.
            </p>
            <div class="more">
              <p>
                The Equip-1 is built for camera enthusiasts, videographers, film schools, and archivists — anyone who
                wants to digitize footage from a camcorder with a FireWire port. Mount it to your camera, connect the
                cable, and press one button. Your footage records directly to microSD. Power it from any USB-C battery
                and you are good to go.
              </p>
            </div>
          </div>
          <div class="specs" :class="{ open: specsOpen }" @click="specsOpen = !specsOpen">
            <span class="specs-toggle">Specs</span>
            <p v-if="currentModel === 'equip-1'">
              60 × 70 × 25 mm, 100 g<br />
              USB-C power, 5V<br />
              MicroSD storage, HDMI<br />
              WiFi 6, Bluetooth 5.4<br />
              Tape deck control<br />
              Firehat included<br />
            </p>
            <p v-else>
              56 × 70 × 12 mm, 25 g<br />
              6-pin FireWire DVin port<br />
              VIA VT6315N FireWire<br />
              PCIe 2.0 x1 via FPC<br />
              OLED, 3× buttons, LED<br />
              RPi 4, RPi 5 compatible<br />
            </p>
          </div>
        </div>
        <div class="buttons">
          <div class="s">
            <a href="https://github.com/computerequipmentgroup/equip-1">Github</a>
            <a href="https://discord.gg/QEGVWvQaCJ">Discord</a>
          </div>
          <button @click="inspectOpen = !inspectOpen">Inspect</button>
        </div>
      </footer>
      <div class="logos">
        <img class="osh-logo" src="/osh.svg" alt="OSH" />
        <img class="ce-logo" src="/c-e.svg" alt="CE" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const { currentModel, setModel } = useModelColor()
const specsOpen = ref(false)
const inspectOpen = ref(false)
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

footer .content,
footer .specs {
  padding: 2rem 2rem 0 2rem;
  color: rgba(0, 0, 0, 1);
}

footer .content p:first-of-type,
footer .specs p:first-of-type {
  margin-bottom: 2rem;
}

footer .d .content:first-of-type {
  width: 64%;
  border-right: 1px solid rgba(0, 0, 0, 1);
  color: rgba(0, 0, 0, 1);
}

footer .more {
  margin-top: 2rem;
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.5s ease-in-out;
}

footer .d.open .more {
  max-height: 300px;
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
  padding: 1rem 1.5rem;
  font-family: 'w', monospace;
  font-size: 1rem;
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-top: none;
  border-bottom: none;
  border-radius: 15px;
  cursor: pointer;
  transition: all 300ms ease;
  background: linear-gradient(0deg, #50f, #000);
  filter: invert(1) saturate(2.5);
}

footer button:hover {
  padding: 1rem 2rem;
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

.specs-toggle {
  display: none;
}

.logos {
  position: fixed;
  bottom: 2rem;
  right: 3rem;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  opacity: 0.333;
}

.logos:hover {
  opacity: 1;
}

.osh-logo {
  width: 55px;
}

.ce-logo {
  width: 200px;
}

@media (max-width: 1055px) {
  .logos {
    display: none;
  }

  footer .content p:first-of-type,
  footer .specs p:first-of-type {
    margin-bottom: 0;
  }

  footer .content p:first-of-type {
    margin-bottom: 1.5rem;
  }

  body {
    font-size: 16px;
  }

  header {
    padding: 1.5rem;
    font-size: 1.4rem;
  }

  header img {
    max-width: 180px;
  }

  footer .d {
    flex-flow: column nowrap;
  }

  footer .d .content,
  footer .d .specs {
    padding: 1.5rem 1.5rem 0 1.5rem;
  }

  footer .d .content:first-of-type {
    width: 100%;
    border-right: none;
    border-bottom: 1px solid rgba(0, 0, 0, 1);
  }

  footer .d .more {
    margin-top: 1rem;
    padding: 0;
  }

  footer .t {
    left: 1rem;
    top: -2.5rem;
    margin: -3rem 0 0 0;
    max-width: 100px;
    max-height: 100px;
    font-size: 0.85rem;
  }

  footer .buttons {
    flex-direction: column;
  }

  footer .buttons .s {
    order: -1;
    border-bottom: 1px solid rgba(0, 0, 0, 1);
  }

  footer .buttons a {
    padding: 1rem 2rem;
  }

  footer button {
    position: static;
    height: auto;
    width: 100%;
    padding: 1rem 1.5rem;
    font-size: 0.85rem;
    border-radius: 0;
    border: none;
  }

  footer .d .specs {
    cursor: pointer;
    padding: 0;
    overflow: hidden;
  }

  footer .d .specs .specs-toggle {
    display: block;
    padding: 1rem 1.5rem;
  }

  footer .d .specs .specs-toggle::after {
    content: ' +';
  }

  footer .d .specs.open .specs-toggle::after {
    content: ' −';
  }

  footer .d .specs p {
    max-height: 0;
    padding: 0 1.5rem;
    transition:
      max-height 0.3s ease,
      padding 0.3s ease;
  }

  footer .d .specs.open p {
    max-height: 200px;
    padding: 0 1.5rem 1.5rem;
  }
}
</style>
