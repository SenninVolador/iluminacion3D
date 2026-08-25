<template>
  <div class="interactive-pbr-card">
    <div class="canvas-header">
      <span class="badge">SIMULADOR 3D INTERACTIVO</span>
      <span class="title">Respuesta de Materiales PBR en Tiempo Real</span>
    </div>
    
    <div class="canvas-wrapper" ref="canvasContainer"></div>

    <div class="controls-panel">
      <div class="control-group">
        <div class="control-label">
          <span>Roughness (Rugosidad):</span>
          <code>{{ roughness.toFixed(2) }}</code>
        </div>
        <input type="range" min="0" max="1" step="0.01" v-model.number="roughness" @input="updateMaterial" />
        <div class="hints"><span>0.0 (Espejo/Brillante)</span><span>1.0 (Mate/Disperso)</span></div>
      </div>

      <div class="control-group">
        <div class="control-label">
          <span>Metallic (Metalicidad):</span>
          <code>{{ metallic.toFixed(2) }}</code>
        </div>
        <input type="range" min="0" max="1" step="0.01" v-model.number="metallic" @input="updateMaterial" />
        <div class="hints"><span>0.0 (Dieléctrico / Madera)</span><span>1.0 (Metal Puro)</span></div>
      </div>

      <div class="control-group">
        <div class="control-label">
          <span>Color Base (Albedo):</span>
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
const roughness = ref(0.2);
const metallic = ref(0.8);
const baseColor = ref('#d4af37'); // Oro por defecto

const presets = [
  { name: 'Oro', color: '#d4af37' },
  { name: 'Cromo', color: '#e5e7eb' },
  { name: 'Cobre', color: '#b87333' },
  { name: 'Plástico Rojo', color: '#dc2626' },
  { name: 'Madera Oscura', color: '#452b1f' },
  { name: 'Piel / Cerámica', color: '#f3c5a8' }
];

let scene, camera, renderer, mesh, animId;
let keyLight, fillLight, rimLight;

const initThree = async () => {
  if (typeof window === 'undefined') return;
  const THREE = await import('three');

  const container = canvasContainer.value;
  if (!container) return;

  const width = container.clientWidth || 600;
  const height = 280;

  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x0f1117);

  camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 100);
  camera.position.set(0, 0, 3.2);

  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(width, height);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.0;
  container.innerHTML = '';
  container.appendChild(renderer.domElement);

  // Material PBR estándar
  const geometry = new THREE.SphereGeometry(1, 64, 64);
  const material = new THREE.MeshStandardMaterial({
    color: new THREE.Color(baseColor.value),
    roughness: roughness.value,
    metalness: metallic.value,
  });

  mesh = new THREE.Mesh(geometry, material);
  scene.add(mesh);

  // Luces de 3 Puntos
  keyLight = new THREE.DirectionalLight(0xfffaed, 2.5);
  keyLight.position.set(2, 2, 2);
  scene.add(keyLight);

  fillLight = new THREE.DirectionalLight(0x8bc34a, 0.6);
  fillLight.position.set(-2, 0, 1.5);
  fillLight.color.setHex(0x93c5fd); // Relleno azulado
  scene.add(fillLight);

  rimLight = new THREE.DirectionalLight(0xffffff, 2.0);
  rimLight.position.set(0, 2, -2.5);
  scene.add(rimLight);

  const ambient = new THREE.AmbientLight(0x1e293b, 0.5);
  scene.add(ambient);

  const animate = () => {
    animId = requestAnimationFrame(animate);
    mesh.rotation.y += 0.005;
    mesh.rotation.x += 0.002;
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
.interactive-pbr-card {
  background: #111827;
  border: 1px solid #1f2937;
  border-radius: 8px;
  margin: 20px 0;
  overflow: hidden;
  color: #f9fafb;
}

.canvas-header {
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
  background: #1e3a8a;
  color: #60a5fa;
  padding: 2px 6px;
  border-radius: 3px;
  font-weight: bold;
}

.title {
  font-size: 12px;
  color: #94a3b8;
  font-weight: 500;
}

.canvas-wrapper {
  width: 100%;
  height: 280px;
  cursor: grab;
}

.controls-panel {
  padding: 16px;
  background: #161e2e;
  border-top: 1px solid #1f2937;
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 16px;
}

.control-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.control-label {
  display: flex;
  justify-content: space-between;
  font-size: 11.5px;
  font-weight: 600;
  color: #e2e8f0;
}

.control-label code {
  color: #38bdf8;
  font-size: 11px;
}

input[type="range"] {
  width: 100%;
  accent-color: #38bdf8;
  cursor: pointer;
}

.hints {
  display: flex;
  justify-content: space-between;
  font-size: 9.5px;
  color: #64748b;
}

.color-presets {
  display: flex;
  gap: 8px;
  align-items: center;
}

.color-btn {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 2px solid #334155;
  cursor: pointer;
  transition: transform 0.15s, border-color 0.15s;
}

.color-btn:hover {
  transform: scale(1.15);
  border-color: #ffffff;
}

@media (max-width: 768px) {
  .controls-panel {
    grid-template-columns: 1fr;
  }
}
</style>
