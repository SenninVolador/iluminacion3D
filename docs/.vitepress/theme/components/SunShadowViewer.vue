<template>
  <div class="technical-figure">
    <div class="figure-header">
      <span class="label">SIMULADOR INTERACTIVO</span>
      <span class="desc">Simulador de Sol (Directional Light) y Sombras en Tiempo Real</span>
    </div>
    
    <div class="canvas-wrapper" ref="canvasContainer"></div>

    <div class="controls-panel">
      <div class="control-group">
        <div class="control-label">
          <span>Hora Solar / Ángulo del Sol:</span>
          <code>{{ sunTimeLabel }} ({{ sunAngle }}°)</code>
        </div>
        <input type="range" min="10" max="170" step="1" v-model.number="sunAngle" @input="updateSun" />
        <div class="hints">
          <span>Amanecer (10°)</span>
          <span>Mediodía (90°)</span>
          <span>Atardecer (170°)</span>
        </div>
      </div>

      <div class="control-group">
        <div class="control-label">
          <span>Sky Light (Luz de Cielo):</span>
          <code>{{ skyLightEnabled ? 'Activa (Relleno Azul)' : 'Apagada (Negro Puro)' }}</code>
        </div>
        <label class="toggle-row">
          <input type="checkbox" v-model="skyLightEnabled" @change="updateSun" />
          <span>Activar luz difusa del cielo</span>
        </label>
        <div class="hints">
          <span>Observa cómo cambian las sombras cuando apagas la Sky Light</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';

const canvasContainer = ref(null);
const sunAngle = ref(45);
const skyLightEnabled = ref(true);

let scene, camera, renderer, sunLight, skyAmbient, animId, pillarMesh;

const sunTimeLabel = computed(() => {
  const a = sunAngle.value;
  if (a < 35) return 'Amanecer · Sombras largas doradas';
  if (a < 75) return 'Media Mañana · Ángulo 45° clásico';
  if (a < 105) return 'Mediodía · Sombras cortas y duras';
  if (a < 145) return 'Media Tarde';
  return 'Atardecer · Luz rasante cálida';
});

const initThree = async () => {
  if (typeof window === 'undefined') return;
  const THREE = await import('three');

  const container = canvasContainer.value;
  if (!container) return;

  const width = container.clientWidth || 600;
  const height = 260;

  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x18181b);

  camera = new THREE.PerspectiveCamera(40, width / height, 0.1, 100);
  camera.position.set(0, 2.2, 5.0);
  camera.lookAt(0, 0.3, 0);

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
  const floorMat = new THREE.MeshStandardMaterial({ color: 0x52525b, roughness: 0.85 });
  const floor = new THREE.Mesh(floorGeo, floorMat);
  floor.rotation.x = -Math.PI / 2;
  floor.receiveShadow = true;
  scene.add(floor);

  // Columna central (Pilar)
  const pillarGeo = new THREE.CylinderGeometry(0.35, 0.4, 2.0, 32);
  const pillarMat = new THREE.MeshStandardMaterial({ color: 0xd4d4d8, roughness: 0.4, metalness: 0.1 });
  pillarMesh = new THREE.Mesh(pillarGeo, pillarMat);
  pillarMesh.position.y = 1.0;
  pillarMesh.castShadow = true;
  pillarMesh.receiveShadow = true;
  scene.add(pillarMesh);

  // Sol (Directional Light)
  sunLight = new THREE.DirectionalLight(0xfff3d6, 2.5);
  sunLight.castShadow = true;
  sunLight.shadow.mapSize.width = 1024;
  sunLight.shadow.mapSize.height = 1024;
  sunLight.shadow.camera.near = 0.5;
  sunLight.shadow.camera.far = 15;
  sunLight.shadow.camera.left = -4;
  sunLight.shadow.camera.right = 4;
  sunLight.shadow.camera.top = 4;
  sunLight.shadow.camera.bottom = -4;
  scene.add(sunLight);

  // Sky Light (Luz difusa ambiental hemisférica)
  skyAmbient = new THREE.HemisphereLight(0x93c5fd, 0x1e293b, 0.6);
  scene.add(skyAmbient);

  updateSun();

  const animate = () => {
    animId = requestAnimationFrame(animate);
    renderer.render(scene, camera);
  };
  animate();
};

const updateSun = () => {
  if (sunLight) {
    const rad = (sunAngle.value * Math.PI) / 180;
    const x = Math.cos(rad) * 6;
    const y = Math.sin(rad) * 6;
    sunLight.position.set(x, Math.max(0.5, y), 2.5);

    // Ajuste de color según hora solar (más cálido al amanecer/atardecer)
    if (sunAngle.value < 40 || sunAngle.value > 140) {
      sunLight.color.setHex(0xfb923c); // Naranja cálido
      sunLight.intensity = 2.0;
    } else {
      sunLight.color.setHex(0xfffaed); // Blanco solar
      sunLight.intensity = 2.8;
    }
  }

  if (skyAmbient) {
    skyAmbient.intensity = skyLightEnabled.value ? 0.65 : 0.02;
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
  margin: 16px 0;
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

.controls-panel {
  padding: 12px 16px;
  background: #f9fafb;
  border-top: 1px solid #e5e7eb;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.control-group {
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
  font-size: 9.5px;
  color: #6b7280;
}

.toggle-row {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 11.5px;
  color: #111827;
  cursor: pointer;
}

.toggle-row input {
  accent-color: #111827;
  width: 15px;
  height: 15px;
}

@media (max-width: 768px) {
  .controls-panel {
    grid-template-columns: 1fr;
  }
}
</style>
