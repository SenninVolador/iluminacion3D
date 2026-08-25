<template>
  <div class="technical-figure">
    <div class="figure-header">
      <span class="label">FIGURA INTERACTIVA</span>
      <span class="desc">Respuesta de superficie PBR (Ecuación de Microfacetas)</span>
    </div>
    
    <div class="canvas-wrapper" ref="canvasContainer"></div>

    <div class="controls-panel">
      <div class="control-group">
        <div class="control-label">
          <span>Rugosidad (Roughness):</span>
          <code>{{ roughness.toFixed(2) }}</code>
        </div>
        <input type="range" min="0" max="1" step="0.01" v-model.number="roughness" @input="updateMaterial" />
        <div class="hints"><span>0.0 (Especular nítido)</span><span>1.0 (Difuso mate)</span></div>
      </div>

      <div class="control-group">
        <div class="control-label">
          <span>Metalicidad (Metallic):</span>
          <code>{{ metallic.toFixed(2) }}</code>
        </div>
        <input type="range" min="0" max="1" step="0.01" v-model.number="metallic" @input="updateMaterial" />
        <div class="hints"><span>0.0 (Dieléctrico)</span><span>1.0 (Conductor puro)</span></div>
      </div>

      <div class="control-group">
        <div class="control-label">
          <span>Muestra de Material:</span>
        </div>
        <div class="color-presets">
          <button v-for="c in presets" :key="c.name" :style="{ background: c.color }" :title="c.name" @click="setColor(c.color)" class="color-btn"></button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';

const canvasContainer = ref(null);
const roughness = ref(0.25);
const metallic = ref(0.8);
const baseColor = ref('#cfcfcf'); // Neutro plateado/metal

const presets = [
  { name: 'Metal Neutro', color: '#cfcfcf' },
  { name: 'Oro', color: '#d4af37' },
  { name: 'Cobre', color: '#b87333' },
  { name: 'Dieléctrico Oscuro', color: '#2b2b2b' },
  { name: 'Cerámica / Piel', color: '#dfc0ad' }
];

let scene, camera, renderer, mesh, animId;

const initThree = async () => {
  if (typeof window === 'undefined') return;
  const THREE = await import('three');

  const container = canvasContainer.value;
  if (!container) return;

  const width = container.clientWidth || 600;
  const height = 260;

  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x18181b);

  camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 100);
  camera.position.set(0, 0, 3.2);

  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(width, height);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.0;
  container.innerHTML = '';
  container.appendChild(renderer.domElement);

  const geometry = new THREE.SphereGeometry(1, 64, 64);
  const material = new THREE.MeshStandardMaterial({
    color: new THREE.Color(baseColor.value),
    roughness: roughness.value,
    metalness: metallic.value,
  });

  mesh = new THREE.Mesh(geometry, material);
  scene.add(mesh);

  const keyLight = new THREE.DirectionalLight(0xfff8ee, 2.5);
  keyLight.position.set(2, 2, 2);
  scene.add(keyLight);

  const fillLight = new THREE.DirectionalLight(0xa5b4fc, 0.6);
  fillLight.position.set(-2, 0, 1.5);
  scene.add(fillLight);

  const rimLight = new THREE.DirectionalLight(0xffffff, 2.0);
  rimLight.position.set(0, 2, -2.5);
  scene.add(rimLight);

  const ambient = new THREE.AmbientLight(0x27272a, 0.5);
  scene.add(ambient);

  const animate = () => {
    animId = requestAnimationFrame(animate);
    mesh.rotation.y += 0.005;
    renderer.render(scene, camera);
  };
  animate();
};

const updateMaterial = () => {
  if (mesh && mesh.material) {
    mesh.material.roughness = roughness.value;
    mesh.material.metalness = metallic.value;
    mesh.material.needsUpdate = true;
  }
};

const setColor = (hex) => {
  baseColor.value = hex;
  if (mesh && mesh.material) {
    mesh.material.color.set(hex);
    mesh.material.needsUpdate = true;
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

.controls-panel {
  padding: 14px;
  background: #f9fafb;
  border-top: 1px solid #e5e7eb;
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
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
  font-size: 11px;
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

.color-presets {
  display: flex;
  gap: 8px;
  align-items: center;
}

.color-btn {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 1px solid #9ca3af;
  cursor: pointer;
}

@media (max-width: 768px) {
  .controls-panel {
    grid-template-columns: 1fr;
  }
}
</style>
