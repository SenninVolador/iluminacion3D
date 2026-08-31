<template>
  <div class="technical-figure">
    <div class="figure-header">
      <span class="label">SIMULADOR INTERACTIVO</span>
      <span class="desc">Niebla Volumétrica y Rayos Crepusculares (God Rays / Media Scatter)</span>
    </div>
    
    <div class="canvas-wrapper" ref="canvasContainer"></div>

    <div class="controls-grid">
      <!-- CONTROL 1: DENSIDAD DE NIEBLA -->
      <div class="control-card">
        <div class="control-label">
          <span>1. Densidad de Niebla (Fog Density):</span>
          <code>{{ fogDensity.toFixed(2) }}</code>
        </div>
        <input type="range" min="0" max="0.35" step="0.01" v-model.number="fogDensity" @input="updateFog" />
        <div class="hints"><span>0.0 (Aire Limpio)</span><span>0.35 (Neblina Densa)</span></div>
      </div>

      <!-- CONTROL 2: ALTURA / FALLOFF -->
      <div class="control-card">
        <div class="control-label">
          <span>2. Altura de Niebla (Height Falloff):</span>
          <code>{{ fogHeight.toFixed(1) }}m</code>
        </div>
        <input type="range" min="0.5" max="4.0" step="0.1" v-model.number="fogHeight" @input="updateFog" />
        <div class="hints"><span>Concentrada en el suelo</span><span>Llena toda la escena</span></div>
      </div>

      <!-- CONTROL 3: COLOR DE ATMÓSFERA -->
      <div class="control-card">
        <div class="control-label">
          <span>3. Mood / Hora Atmosférica:</span>
        </div>
        <div class="mood-selector">
          <button 
            v-for="m in moodPresets" 
            :key="m.name" 
            :class="['mood-btn', { active: currentMood === m.id }]"
            @click="setMood(m.id)"
          >
            {{ m.name }}
          </button>
        </div>
      </div>

      <!-- CONTROL 4: DISPERSIÓN / RAYOS DE LUZ -->
      <div class="control-card">
        <div class="control-label">
          <span>4. Rayos de Luz (God Rays):</span>
          <code>{{ godRaysEnabled ? 'Visibles (Volumetric Fog ON)' : 'Desactivados' }}</code>
        </div>
        <label class="toggle-row">
          <input type="checkbox" v-model="godRaysEnabled" @change="updateFog" />
          <span>Calcular dispersión volumétrica de luz</span>
        </label>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';

const canvasContainer = ref(null);
const fogDensity = ref(0.18);
const fogHeight = ref(2.0);
const currentMood = ref('sunset');
const godRaysEnabled = ref(true);

const moodPresets = [
  { id: 'noon', name: 'Mediodía (Neutro)', sunColor: 0xfffaed, fogColor: 0xa5b4fc, skyColor: 0x38bdf8 },
  { id: 'sunset', name: 'Atardecer Dorado', sunColor: 0xfb923c, fogColor: 0x9a3412, skyColor: 0xc2410c },
  { id: 'night', name: 'Noche / Misterio', sunColor: 0x60a5fa, fogColor: 0x0f172a, skyColor: 0x020617 }
];

let scene, camera, renderer, sunLight, fogVolume, animId, pillarGroup;

const initThree = async () => {
  if (typeof window === 'undefined') return;
  const THREE = await import('three');

  const container = canvasContainer.value;
  if (!container) return;

  const width = container.clientWidth || 600;
  const height = 260;

  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x0a0c10);

  camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 100);
  camera.position.set(0, 1.8, 5.0);
  camera.lookAt(0, 1.0, 0);

  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(width, height);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  container.innerHTML = '';
  container.appendChild(renderer.domElement);

  // Suelo
  const floorGeo = new THREE.PlaneGeometry(12, 12);
  const floorMat = new THREE.MeshStandardMaterial({ color: 0x27272a, roughness: 0.85 });
  const floor = new THREE.Mesh(floorGeo, floorMat);
  floor.rotation.x = -Math.PI / 2;
  floor.receiveShadow = true;
  scene.add(floor);

  // Columnata / Ventanales para proyectar rayos crepusculares
  pillarGroup = new THREE.Group();
  for (let i = -3; i <= 3; i += 1.5) {
    const colGeo = new THREE.BoxGeometry(0.35, 3.5, 0.35);
    const colMat = new THREE.MeshStandardMaterial({ color: 0x52525b, roughness: 0.7 });
    const col = new THREE.Mesh(colGeo, colMat);
    col.position.set(i, 1.75, -1.0);
    col.castShadow = true;
    col.receiveShadow = true;
    pillarGroup.add(col);
  }
  scene.add(pillarGroup);

  // Techo / Viga superior
  const beamGeo = new THREE.BoxGeometry(10, 0.5, 0.6);
  const beamMat = new THREE.MeshStandardMaterial({ color: 0x3f3f46, roughness: 0.7 });
  const beam = new THREE.Mesh(beamGeo, beamMat);
  beam.position.set(0, 3.25, -1.0);
  beam.castShadow = true;
  scene.add(beam);

  // Sol direccional
  sunLight = new THREE.DirectionalLight(0xfb923c, 3.5);
  sunLight.position.set(3, 4, -3);
  sunLight.castShadow = true;
  sunLight.shadow.mapSize.width = 1024;
  sunLight.shadow.mapSize.height = 1024;
  sunLight.shadow.camera.near = 0.5;
  sunLight.shadow.camera.far = 15;
  scene.add(sunLight);

  // Representación visual de niebla / haz volumétrico
  const fogGeo = new THREE.BoxGeometry(10, 3.5, 8);
  const fogMat = new THREE.MeshBasicMaterial({
    color: 0xfb923c,
    transparent: true,
    opacity: 0.15,
    side: THREE.BackSide
  });
  fogVolume = new THREE.Mesh(fogGeo, fogMat);
  fogVolume.position.set(0, 1.75, 0);
  scene.add(fogVolume);

  updateFog();

  const animate = () => {
    animId = requestAnimationFrame(animate);
    renderer.render(scene, camera);
  };
  animate();
};

const setMood = (moodId) => {
  currentMood.value = moodId;
  const m = moodPresets.find(p => p.id === moodId) || moodPresets[1];
  if (sunLight) {
    sunLight.color.setHex(m.sunColor);
  }
  if (scene) {
    scene.background.setHex(m.skyColor);
  }
  if (fogVolume) {
    fogVolume.material.color.setHex(m.fogColor);
  }
  updateFog();
};

const updateFog = () => {
  if (fogVolume) {
    fogVolume.visible = godRaysEnabled.value && fogDensity.value > 0.01;
    fogVolume.material.opacity = Math.min(0.35, fogDensity.value * (godRaysEnabled.value ? 1.0 : 0.0));
    fogVolume.scale.set(1, fogHeight.value / 2.0, 1);
  }
};

onMounted(() => {
  initThree();
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

.canvas-wrapper {
  width: 100%;
  height: 260px;
}

.controls-grid {
  padding: 14px;
  background: #f9fafb;
  border-top: 1px solid #e5e7eb;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}

.control-card {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.control-label {
  display: flex;
  justify-content: space-between;
  font-size: 11.5px;
  font-weight: 600;
  color: #111827;
}

.control-label code {
  color: #111827;
  font-size: 10.5px;
}

input[type="range"] {
  width: 100%;
  accent-color: #111827;
  cursor: pointer;
}

.hints {
  display: flex;
  justify-content: space-between;
  font-size: 9px;
  color: #6b7280;
}

.mood-selector {
  display: flex;
  gap: 6px;
}

.mood-btn {
  font-size: 10.5px;
  padding: 4px 8px;
  background: #ffffff;
  border: 1px solid #d1d5db;
  border-radius: 3px;
  cursor: pointer;
  color: #374151;
  transition: all 0.15s;
}

.mood-btn.active {
  background: #111827;
  color: #ffffff;
  border-color: #111827;
}

.toggle-row {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 11.5px;
  color: #111827;
  cursor: pointer;
  margin-top: 4px;
}

.toggle-row input {
  accent-color: #111827;
  width: 15px;
  height: 15px;
}

@media (max-width: 768px) {
  .controls-grid {
    grid-template-columns: 1fr;
  }
}
</style>
