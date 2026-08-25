<template>
  <div class="lighting-widget">
    <div class="widget-header">
      <span class="badge">ESTUDIO DE ILUMINACIÓN EN VIVO</span>
      <span class="title">Esquema de 3 Puntos Interactivo</span>
    </div>

    <div class="canvas-box" ref="canvasBox"></div>

    <div class="lights-grid">
      <!-- KEY LIGHT -->
      <div class="light-card" :class="{ active: keyActive }">
        <div class="card-top">
          <label class="switch">
            <input type="checkbox" v-model="keyActive" @change="updateLights" />
            <span class="slider"></span>
          </label>
          <span class="name">Key Light (100%)</span>
        </div>
        <span class="desc">Luz Principal a 45°. Define el contraste y la sombra dominante.</span>
      </div>

      <!-- FILL LIGHT -->
      <div class="light-card" :class="{ active: fillActive }">
        <div class="card-top">
          <label class="switch">
            <input type="checkbox" v-model="fillActive" @change="updateLights" />
            <span class="slider"></span>
          </label>
          <span class="name">Fill Light (30%)</span>
        </div>
        <span class="desc">Relleno difuso. Suaviza sombras oscuras sin competir.</span>
      </div>

      <!-- RIM LIGHT -->
      <div class="light-card" :class="{ active: rimActive }">
        <div class="card-top">
          <label class="switch">
            <input type="checkbox" v-model="rimActive" @change="updateLights" />
            <span class="slider"></span>
          </label>
          <span class="name">Rim Light (Contraluz)</span>
        </div>
        <span class="desc">Luz trasera. Dibuja un filo en la silueta para despegar del fondo.</span>
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
  const height = 280;

  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x0a0c10);

  camera = new THREE.PerspectiveCamera(40, width / height, 0.1, 100);
  camera.position.set(0, 0, 3.4);

  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(width, height);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  container.innerHTML = '';
  container.appendChild(renderer.domElement);

  // Escultura / Busto 3D geométrico
  const geo = new THREE.IcosahedronGeometry(1.05, 4);
  const mat = new THREE.MeshStandardMaterial({
    color: 0x94a3b8,
    roughness: 0.45,
    metalness: 0.1
  });
  headMesh = new THREE.Mesh(geo, mat);
  scene.add(headMesh);

  // Luces
  keyLight = new THREE.DirectionalLight(0xfff3d6, 3.0);
  keyLight.position.set(2.5, 2.0, 2.0);
  scene.add(keyLight);

  fillLight = new THREE.DirectionalLight(0x93c5fd, 0.9);
  fillLight.position.set(-2.5, 0.5, 1.5);
  scene.add(fillLight);

  rimLight = new THREE.DirectionalLight(0xffffff, 3.5);
  rimLight.position.set(0, 2.5, -2.8);
  scene.add(rimLight);

  const ambient = new THREE.AmbientLight(0x0f172a, 0.2);
  scene.add(ambient);

  const animate = () => {
    animId = requestAnimationFrame(animate);
    headMesh.rotation.y += 0.004;
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
.lighting-widget {
  background: #111827;
  border: 1px solid #1f2937;
  border-radius: 8px;
  margin: 20px 0;
  overflow: hidden;
  color: #f9fafb;
}

.widget-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 16px;
  background: #0f172a;
  border-bottom: 1px solid #1e293b;
}

.badge {
  font-family: monospace;
  font-size: 10px;
  background: #065f46;
  color: #34d399;
  padding: 2px 6px;
  border-radius: 3px;
  font-weight: bold;
}

.title {
  font-size: 12px;
  color: #94a3b8;
  font-weight: 500;
}

.canvas-box {
  width: 100%;
  height: 280px;
}

.lights-grid {
  padding: 14px;
  background: #161e2e;
  border-top: 1px solid #1f2937;
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 12px;
}

.light-card {
  background: #0f172a;
  border: 1px solid #334155;
  border-radius: 6px;
  padding: 10px 12px;
  transition: all 0.2s;
}

.light-card.active {
  border-color: #38bdf8;
  background: #1e293b;
}

.card-top {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.name {
  font-size: 12px;
  font-weight: 700;
  color: #f8fafc;
}

.desc {
  font-size: 10.5px;
  color: #94a3b8;
  line-height: 1.35;
  display: block;
}

/* SWITCH TOGGLE */
.switch {
  position: relative;
  display: inline-block;
  width: 32px;
  height: 18px;
}
.switch input { opacity: 0; width: 0; height: 0; }
.slider {
  position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0;
  background-color: #475569; transition: .2s; border-radius: 18px;
}
.slider:before {
  position: absolute; content: ""; height: 14px; width: 14px; left: 2px; bottom: 2px;
  background-color: white; transition: .2s; border-radius: 50%;
}
input:checked + .slider { background-color: #38bdf8; }
input:checked + .slider:before { transform: translateX(14px); }

@media (max-width: 768px) {
  .lights-grid {
    grid-template-columns: 1fr;
  }
}
</style>
