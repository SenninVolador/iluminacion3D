<template>
  <div class="technical-figure">
    <div class="figure-header">
      <span class="label">FIGURA INTERACTIVA</span>
      <span class="desc">Aislamiento de fuentes en el esquema de 3 puntos</span>
    </div>

    <div class="canvas-box" ref="canvasBox"></div>

    <div class="lights-grid">
      <!-- KEY LIGHT -->
      <div class="light-card" :class="{ active: keyActive }">
        <div class="card-top">
          <input type="checkbox" id="key-check" v-model="keyActive" @change="updateLights" />
          <label for="key-check" class="name">Key Light (100%)</label>
        </div>
        <span class="desc">Luz principal a 45°. Define el contraste y la sombra dominante.</span>
      </div>

      <!-- FILL LIGHT -->
      <div class="light-card" :class="{ active: fillActive }">
        <div class="card-top">
          <input type="checkbox" id="fill-check" v-model="fillActive" @change="updateLights" />
          <label for="fill-check" class="name">Fill Light (30%)</label>
        </div>
        <span class="desc">Relleno difuso lateral. Suaviza sombras oscuras sin competir.</span>
      </div>

      <!-- RIM LIGHT -->
      <div class="light-card" :class="{ active: rimActive }">
        <div class="card-top">
          <input type="checkbox" id="rim-check" v-model="rimActive" @change="updateLights" />
          <label for="rim-check" class="name">Rim Light (Contraluz)</label>
        </div>
        <span class="desc">Luz trasera. Genera el contorno luminoso que separa al sujeto del fondo.</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';

const canvasBox = ref(null);
const keyActive = ref(true);
const fillActive = ref(true);
const rimActive = ref(true);

let scene, camera, renderer, headMesh, animId;
let keyLight, fillLight, rimLight;

const initStudio = async () => {
  if (typeof window === 'undefined') return;
  const THREE = await import('three');

  const container = canvasBox.value;
  if (!container) return;

  const width = container.clientWidth || 600;
  const height = 260;

  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x18181b);

  camera = new THREE.PerspectiveCamera(40, width / height, 0.1, 100);
  camera.position.set(0, 0, 3.4);

  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(width, height);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  container.innerHTML = '';
  container.appendChild(renderer.domElement);

  const geo = new THREE.IcosahedronGeometry(1.05, 4);
  const mat = new THREE.MeshStandardMaterial({
    color: 0xd4d4d8,
    roughness: 0.5,
    metalness: 0.05
  });
  headMesh = new THREE.Mesh(geo, mat);
  scene.add(headMesh);

  keyLight = new THREE.DirectionalLight(0xfff8ee, 3.0);
  keyLight.position.set(2.5, 2.0, 2.0);
  scene.add(keyLight);

  fillLight = new THREE.DirectionalLight(0xa5b4fc, 0.9);
  fillLight.position.set(-2.5, 0.5, 1.5);
  scene.add(fillLight);

  rimLight = new THREE.DirectionalLight(0xffffff, 3.5);
  rimLight.position.set(0, 2.5, -2.8);
  scene.add(rimLight);

  const ambient = new THREE.AmbientLight(0x27272a, 0.2);
  scene.add(ambient);

  const animate = () => {
    animId = requestAnimationFrame(animate);
    headMesh.rotation.y += 0.003;
    renderer.render(scene, camera);
  };
  animate();
};

const updateLights = () => {
  if (keyLight) keyLight.visible = keyActive.value;
  if (fillLight) fillLight.visible = fillActive.value;
  if (rimLight) rimLight.visible = rimActive.value;
};

onMounted(() => {
  initStudio();
});

onBeforeUnmount(() => {
  if (animId) cancelAnimationFrame(animId);
  if (renderer) renderer.dispose();
});
</script>

<style scoped>
.technical-figure {
  border: 1px solid #d1d5db;
  border-radius: 4px;
  margin: 18px 0;
  overflow: hidden;
  background: #ffffff;
}

.figure-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 14px;
  background: #f9fafb;
  border-bottom: 1px solid #e5e7eb;
}

.label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  font-weight: 700;
  color: #111827;
  letter-spacing: 0.5px;
}

.desc {
  font-size: 11.5px;
  color: #6b7280;
}

.canvas-box {
  width: 100%;
  height: 260px;
}

.lights-grid {
  padding: 12px;
  background: #f9fafb;
  border-top: 1px solid #e5e7eb;
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 12px;
}

.light-card {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  padding: 10px;
}

.light-card.active {
  border-color: #111827;
}

.card-top {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 4px;
}

.card-top input {
  accent-color: #111827;
  cursor: pointer;
}

.name {
  font-size: 11.5px;
  font-weight: 600;
  color: #111827;
  cursor: pointer;
}

.desc {
  font-size: 10.5px;
  color: #6b7280;
  line-height: 1.35;
  display: block;
}

@media (max-width: 768px) {
  .lights-grid {
    grid-template-columns: 1fr;
  }
}
</style>
