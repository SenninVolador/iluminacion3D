<template>
  <div class="technical-figure">
    <div class="figure-header">
      <span class="label">SIMULADOR INTERACTIVO</span>
      <span class="desc">Shader Nodal Paramétrico PBR — Utah Teapot</span>
    </div>
    
    <div class="canvas-wrapper" ref="canvasContainer"></div>

    <!-- DIAGRAMA DE NODOS VISUAL -->
    <div class="node-graph-panel">
      <div class="node-graph-title">Estructura del Shader Nodal (Lógica Universal de Motores)</div>
      <div class="nodes-flow">
        <div class="node-box">
          <div class="node-header">Texture Sample (Albedo)</div>
          <div class="node-body">Textura Base 2D</div>
        </div>
        <div class="node-connector">──►</div>
        <div class="node-box active">
          <div class="node-header">Multiply (Tinte)</div>
          <div class="node-body">Color Tint Parameter</div>
        </div>
        <div class="node-connector">──►</div>
        <div class="node-box master">
          <div class="node-header">Master PBR Node</div>
          <div class="node-body">
            <div>• Base Color</div>
            <div>• Metallic: {{ metallic.toFixed(2) }}</div>
            <div>• Roughness: {{ roughness.toFixed(2) }}</div>
            <div>• Normal Strength: {{ normalStrength.toFixed(1) }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- CONTROLES PARAMÉTRICOS -->
    <div class="controls-grid">
      <!-- CONTROL 1: TINTE DE TEXTURA -->
      <div class="control-card">
        <div class="control-label">
          <span>1. Tinte de Color (Multiply):</span>
        </div>
        <div class="color-presets">
          <button 
            v-for="t in tintPresets" 
            :key="t.name" 
            :style="{ background: t.color }" 
            :title="t.name" 
            @click="setTint(t.color)" 
            :class="['color-btn', { selected: currentTint === t.color }]"
          ></button>
        </div>
      </div>

      <!-- CONTROL 2: ROUGHNESS -->
      <div class="control-card">
        <div class="control-label">
          <span>2. Roughness (Rugosidad):</span>
          <code>{{ roughness.toFixed(2) }}</code>
        </div>
        <input type="range" min="0" max="1" step="0.01" v-model.number="roughness" @input="updateShader" />
        <div class="hints"><span>0.0 (Espejo)</span><span>1.0 (Mate)</span></div>
      </div>

      <!-- CONTROL 3: METALLIC -->
      <div class="control-card">
        <div class="control-label">
          <span>3. Metallic (Metalicidad):</span>
          <code>{{ metallic.toFixed(2) }}</code>
        </div>
        <input type="range" min="0" max="1" step="0.01" v-model.number="metallic" @input="updateShader" />
        <div class="hints"><span>0.0 (Dieléctrico)</span><span>1.0 (Metal Puro)</span></div>
      </div>

      <!-- CONTROL 4: NORMAL STRENGTH -->
      <div class="control-card">
        <div class="control-label">
          <span>4. Normal Strength (Relieve):</span>
          <code>{{ normalStrength.toFixed(1) }}x</code>
        </div>
        <input type="range" min="0" max="3" step="0.1" v-model.number="normalStrength" @input="updateShader" />
        <div class="hints"><span>0.0 (Plano)</span><span>3.0 (Relieve Profundo)</span></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';

const canvasContainer = ref(null);
const currentTint = ref('#e2e8f0'); // Blanco/Plateado neutro
const roughness = ref(0.35);
const metallic = ref(0.7);
const normalStrength = ref(1.5);

const tintPresets = [
  { name: 'Cerámica Blanca', color: '#e2e8f0' },
  { name: 'Bronce Antiguo', color: '#cd7f32' },
  { name: 'Oro Real', color: '#d4af37' },
  { name: 'Cobre Rojo', color: '#b85d38' },
  { name: 'Acero Oscuro', color: '#334155' },
  { name: 'Esmalte Azul', color: '#2563eb' }
];

let scene, camera, renderer, teapotMesh, animId, proceduralNormal, proceduralAlbedo;

// Textura procedural de relieve (grabado ornamental para la tetera)
function createTeapotNormalMap(THREE) {
  const size = 256;
  const canvas = document.createElement('canvas');
  canvas.width = size;
  canvas.height = size;
  const ctx = canvas.getContext('2d');

  ctx.fillStyle = 'rgb(128, 128, 255)';
  ctx.fillRect(0, 0, size, size);

  // Patrón geométrico decorativo
  ctx.strokeStyle = 'rgb(200, 128, 200)';
  ctx.lineWidth = 4;
  for (let y = 16; y < size; y += 32) {
    ctx.beginPath();
    ctx.arc(size / 2, y, 12, 0, Math.PI * 2);
    ctx.stroke();
  }

  const texture = new THREE.CanvasTexture(canvas);
  texture.wrapS = THREE.RepeatWrapping;
  texture.wrapT = THREE.RepeatWrapping;
  texture.repeat.set(4, 2);
  return texture;
}

// Textura base de patrón
function createTeapotBaseTexture(THREE) {
  const size = 256;
  const canvas = document.createElement('canvas');
  canvas.width = size;
  canvas.height = size;
  const ctx = canvas.getContext('2d');

  ctx.fillStyle = '#ffffff';
  ctx.fillRect(0, 0, size, size);

  ctx.fillStyle = '#e2e8f0';
  for (let y = 0; y < size; y += 16) {
    for (let x = 0; x < size; x += 16) {
      if ((x + y) % 32 === 0) {
        ctx.fillRect(x, y, 16, 16);
      }
    }
  }

  const texture = new THREE.CanvasTexture(canvas);
  texture.wrapS = THREE.RepeatWrapping;
  texture.wrapT = THREE.RepeatWrapping;
  texture.repeat.set(4, 2);
  return texture;
}

const initThree = async () => {
  if (typeof window === 'undefined') return;
  const THREE = await import('three');
  const { TeapotGeometry } = await import('three/examples/jsm/geometries/TeapotGeometry.js');

  const container = canvasContainer.value;
  if (!container) return;

  const width = container.clientWidth || 600;
  const height = 280;

  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x111217);

  camera = new THREE.PerspectiveCamera(40, width / height, 0.1, 100);
  camera.position.set(0, 1.2, 3.8);
  camera.lookAt(0, 0, 0);

  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(width, height);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.shadowMap.enabled = true;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  container.innerHTML = '';
  container.appendChild(renderer.domElement);

  // Pedestal
  const pedGeo = new THREE.CylinderGeometry(1.2, 1.3, 0.2, 48);
  const pedMat = new THREE.MeshStandardMaterial({ color: 0x27272a, roughness: 0.8 });
  const pedestal = new THREE.Mesh(pedGeo, pedMat);
  pedestal.position.y = -0.7;
  pedestal.receiveShadow = true;
  scene.add(pedestal);

  proceduralNormal = createTeapotNormalMap(THREE);
  proceduralAlbedo = createTeapotBaseTexture(THREE);

  // Utah Teapot
  const teapotGeo = new TeapotGeometry(0.7, 18, true, true, true, true, true);
  const teapotMat = new THREE.MeshStandardMaterial({
    map: proceduralAlbedo,
    color: new THREE.Color(currentTint.value),
    roughness: roughness.value,
    metalness: metallic.value,
    normalMap: proceduralNormal,
    normalScale: new THREE.Vector2(normalStrength.value, normalStrength.value)
  });

  teapotMesh = new THREE.Mesh(teapotGeo, teapotMat);
  teapotMesh.position.y = -0.15;
  teapotMesh.castShadow = true;
  teapotMesh.receiveShadow = true;
  scene.add(teapotMesh);

  // Luces de estudio (Key, Fill, Rim)
  const keyLight = new THREE.DirectionalLight(0xfffaed, 2.5);
  keyLight.position.set(2.5, 2.5, 2.0);
  keyLight.castShadow = true;
  scene.add(keyLight);

  const fillLight = new THREE.DirectionalLight(0x93c5fd, 0.7);
  fillLight.position.set(-2.5, 0.5, 1.5);
  scene.add(fillLight);

  const rimLight = new THREE.DirectionalLight(0xffffff, 2.2);
  rimLight.position.set(0, 2.0, -2.5);
  scene.add(rimLight);

  const ambient = new THREE.AmbientLight(0x18181b, 0.4);
  scene.add(ambient);

  const animate = () => {
    animId = requestAnimationFrame(animate);
    teapotMesh.rotation.y += 0.006;
    renderer.render(scene, camera);
  };
  animate();
};

const updateShader = () => {
  if (teapotMesh && teapotMesh.material) {
    teapotMesh.material.roughness = roughness.value;
    teapotMesh.material.metalness = metallic.value;
    teapotMesh.material.normalScale.set(normalStrength.value, normalStrength.value);
    teapotMesh.material.needsUpdate = true;
  }
};

const setTint = (hex) => {
  currentTint.value = hex;
  if (teapotMesh && teapotMesh.material) {
    teapotMesh.material.color.set(hex);
    teapotMesh.material.needsUpdate = true;
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
  height: 280px;
}

/* DIAGRAMA DE NODOS */
.node-graph-panel {
  background: #18181b;
  color: #f4f4f5;
  padding: 12px 14px;
  border-top: 1px solid #e5e7eb;
  border-bottom: 1px solid #27272a;
}

.node-graph-title {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #a1a1aa;
  margin-bottom: 8px;
}

.nodes-flow {
  display: flex;
  align-items: center;
  gap: 8px;
  overflow-x: auto;
}

.node-box {
  background: #27272a;
  border: 1px solid #3f3f46;
  border-radius: 3px;
  padding: 6px 8px;
  font-size: 10px;
  min-width: 120px;
}

.node-box.active {
  border-color: #38bdf8;
}

.node-box.master {
  border-color: #34d399;
  min-width: 140px;
}

.node-header {
  font-weight: 700;
  border-bottom: 1px solid #3f3f46;
  padding-bottom: 3px;
  margin-bottom: 3px;
  color: #f4f4f5;
}

.node-body {
  font-size: 9.5px;
  color: #a1a1aa;
  line-height: 1.3;
}

.node-connector {
  color: #71717a;
  font-family: monospace;
  font-size: 11px;
}

/* PANEL DE CONTROLES */
.controls-grid {
  padding: 14px;
  background: #f9fafb;
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

.color-presets {
  display: flex;
  gap: 6px;
  align-items: center;
}

.color-btn {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  border: 1px solid #9ca3af;
  cursor: pointer;
  transition: transform 0.15s, border-color 0.15s;
}

.color-btn.selected {
  border: 2px solid #111827;
  transform: scale(1.15);
}

@media (max-width: 768px) {
  .controls-grid {
    grid-template-columns: 1fr;
  }
}
</style>
