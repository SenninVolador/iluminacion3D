<template>
  <div class="ue-material-studio">
    <div class="studio-header">
      <span class="label">UNREAL ENGINE 5 — MATERIAL GRAPH & VIEWPORT</span>
      <span class="desc">Shader Nodal Paramétrico PBR en Tiempo Real</span>
    </div>

    <!-- VIEWPORT 3D: UTAH TEAPOT -->
    <div class="canvas-wrapper" ref="canvasContainer"></div>

    <!-- PANEL DE CONTROL RÁPIDO CON COLOR PICKER -->
    <div class="viewport-toolbar">
      <div class="toolbar-item">
        <label class="toolbar-label">Color Tint (Vector Parameter):</label>
        <div class="color-picker-wrapper">
          <input type="color" v-model="currentTint" @input="updateTintFromPicker" class="color-input" />
          <code class="hex-text">{{ currentTint.toUpperCase() }}</code>
        </div>
      </div>

      <div class="toolbar-presets">
        <span class="preset-label">Presets:</span>
        <button 
          v-for="t in tintPresets" 
          :key="t.name" 
          :style="{ background: t.color }" 
          :title="t.name" 
          @click="setTint(t.color)" 
          :class="['preset-btn', { selected: currentTint.toLowerCase() === t.color.toLowerCase() }]"
        ></button>
      </div>
    </div>

    <!-- SIMULADOR DEL MATERIAL GRAPH DE UNREAL ENGINE -->
    <div class="graph-editor">
      <div class="graph-header">
        <span class="graph-title">Material Graph: M_Master_PBR</span>
        <span class="graph-tip">Lógica de conexiones en Unreal Engine (Texture ──► Multiply ──► Base Color)</span>
      </div>

      <div class="graph-canvas">
        <svg class="wires-layer" width="100%" height="100%">
          <!-- CABLE 1: Texture Sample RGB (salida) -> Multiply A (entrada) -->
          <path d="M 205 60 C 235 60, 235 75, 265 75" fill="none" stroke="#e2e8f0" stroke-width="2.5" />
          
          <!-- CABLE 2: Color Tint RGB (salida) -> Multiply B (entrada) -->
          <path d="M 205 155 C 235 155, 235 95, 265 95" fill="none" :stroke="currentTint" stroke-width="2.5" />

          <!-- CABLE 3: Multiply Result (salida) -> Master Node Base Color (entrada) -->
          <path d="M 370 85 C 410 85, 410 65, 450 65" fill="none" :stroke="currentTint" stroke-width="2.5" />

          <!-- CABLE 4: Metallic Scalar -> Master Node Metallic -->
          <path d="M 205 235 C 330 235, 330 90, 450 90" fill="none" stroke="#60a5fa" stroke-width="2" />

          <!-- CABLE 5: Roughness Scalar -> Master Node Roughness -->
          <path d="M 205 315 C 330 315, 330 115, 450 115" fill="none" stroke="#34d399" stroke-width="2" />

          <!-- CABLE 6: Normal Flatten -> Master Node Normal -->
          <path d="M 205 395 C 330 395, 330 165, 450 165" fill="none" stroke="#a78bfa" stroke-width="2" />
        </svg>

        <div class="nodes-container">
          
          <!-- COLUMNA IZQUIERDA DE NODOS -->
          <div class="nodes-col left-col">
            
            <!-- NODO 1: TEXTURE SAMPLE (ALBEDO) -->
            <div class="ue-node">
              <div class="node-titlebar title-texture">Texture Sample</div>
              <div class="node-content">
                <div class="node-param-name">T_Teapot_Albedo</div>
                <div class="pin-row right">
                  <span class="pin-name">RGB</span>
                  <span class="pin-dot white"></span>
                </div>
                <div class="pin-row right">
                  <span class="pin-name">R</span>
                  <span class="pin-dot red"></span>
                </div>
                <div class="pin-row right">
                  <span class="pin-name">G</span>
                  <span class="pin-dot green"></span>
                </div>
                <div class="pin-row right">
                  <span class="pin-name">B</span>
                  <span class="pin-dot blue"></span>
                </div>
              </div>
            </div>

            <!-- NODO 2: VECTOR PARAMETER (COLOR TINT) -->
            <div class="ue-node">
              <div class="node-titlebar title-param">Vector Parameter</div>
              <div class="node-content">
                <div class="node-param-name">Color_Tint</div>
                <div class="color-swatch-box" :style="{ background: currentTint }"></div>
                <div class="pin-row right">
                  <span class="pin-name">RGB</span>
                  <span class="pin-dot" :style="{ background: currentTint }"></span>
                </div>
              </div>
            </div>

            <!-- NODO 3: SCALAR PARAMETER METALLIC -->
            <div class="ue-node">
              <div class="node-titlebar title-scalar">Scalar Parameter</div>
              <div class="node-content">
                <div class="node-param-name">Metallic</div>
                <div class="inline-slider">
                  <input type="range" min="0" max="1" step="0.01" v-model.number="metallic" @input="updateShader" />
                  <code>{{ metallic.toFixed(2) }}</code>
                </div>
                <div class="pin-row right">
                  <span class="pin-name">Out</span>
                  <span class="pin-dot cyan"></span>
                </div>
              </div>
            </div>

            <!-- NODO 4: SCALAR PARAMETER ROUGHNESS -->
            <div class="ue-node">
              <div class="node-titlebar title-scalar">Scalar Parameter</div>
              <div class="node-content">
                <div class="node-param-name">Roughness</div>
                <div class="inline-slider">
                  <input type="range" min="0" max="1" step="0.01" v-model.number="roughness" @input="updateShader" />
                  <code>{{ roughness.toFixed(2) }}</code>
                </div>
                <div class="pin-row right">
                  <span class="pin-name">Out</span>
                  <span class="pin-dot green"></span>
                </div>
              </div>
            </div>

            <!-- NODO 5: NORMAL FLATTEN / STRENGTH -->
            <div class="ue-node">
              <div class="node-titlebar title-normal">Normal Strength (Flatten)</div>
              <div class="node-content">
                <div class="node-param-name">Normal_Scale</div>
                <div class="inline-slider">
                  <input type="range" min="0" max="3" step="0.1" v-model.number="normalStrength" @input="updateShader" />
                  <code>{{ normalStrength.toFixed(1) }}x</code>
                </div>
                <div class="pin-row right">
                  <span class="pin-name">Out</span>
                  <span class="pin-dot purple"></span>
                </div>
              </div>
            </div>

          </div>

          <!-- COLUMNA CENTRAL: NODO MULTIPLY -->
          <div class="nodes-col mid-col">
            <div class="ue-node math-node">
              <div class="node-titlebar title-math">Multiply</div>
              <div class="node-content">
                <div class="pins-split">
                  <div class="left-pins">
                    <div class="pin-row left">
                      <span class="pin-dot white"></span>
                      <span class="pin-name">A</span>
                    </div>
                    <div class="pin-row left">
                      <span class="pin-dot" :style="{ background: currentTint }"></span>
                      <span class="pin-name">B</span>
                    </div>
                  </div>
                  <div class="right-pins">
                    <div class="pin-row right">
                      <span class="pin-name">Result</span>
                      <span class="pin-dot" :style="{ background: currentTint }"></span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- COLUMNA DERECHA: MASTER MATERIAL NODE (ROOT) -->
          <div class="nodes-col right-col">
            <div class="ue-node master-node">
              <div class="node-titlebar title-master">M_Master_PBR (Material Attributes)</div>
              <div class="node-content">
                <div class="pin-row left active-input">
                  <span class="pin-dot" :style="{ background: currentTint }"></span>
                  <span class="pin-name highlight">Base Color</span>
                </div>
                <div class="pin-row left active-input">
                  <span class="pin-dot cyan"></span>
                  <span class="pin-name highlight">Metallic</span>
                </div>
                <div class="pin-row left">
                  <span class="pin-dot gray"></span>
                  <span class="pin-name dim">Specular</span>
                </div>
                <div class="pin-row left active-input">
                  <span class="pin-dot green"></span>
                  <span class="pin-name highlight">Roughness</span>
                </div>
                <div class="pin-row left">
                  <span class="pin-dot gray"></span>
                  <span class="pin-name dim">Emissive Color</span>
                </div>
                <div class="pin-row left">
                  <span class="pin-dot gray"></span>
                  <span class="pin-name dim">Opacity</span>
                </div>
                <div class="pin-row left active-input">
                  <span class="pin-dot purple"></span>
                  <span class="pin-name highlight">Normal</span>
                </div>
                <div class="pin-row left">
                  <span class="pin-dot gray"></span>
                  <span class="pin-name dim">Ambient Occlusion</span>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';

const canvasContainer = ref(null);
const currentTint = ref('#e2e8f0'); // Cerámica neutra inicial
const roughness = ref(0.35);
const metallic = ref(0.65);
const normalStrength = ref(1.5);

const tintPresets = [
  { name: 'Cerámica Blanca', color: '#e2e8f0' },
  { name: 'Oro Pulido', color: '#d4af37' },
  { name: 'Cobre Rojo', color: '#b85d38' },
  { name: 'Bronce Clásico', color: '#cd7f32' },
  { name: 'Acero Azul', color: '#3b82f6' },
  { name: 'Carbón Mate', color: '#27272a' }
];

let scene, camera, renderer, teapotMesh, animId, proceduralNormal, proceduralAlbedo;

// Textura procedural de relieve (adornos geométricos en la tetera)
function createTeapotNormalMap(THREE) {
  const size = 256;
  const canvas = document.createElement('canvas');
  canvas.width = size;
  canvas.height = size;
  const ctx = canvas.getContext('2d');

  ctx.fillStyle = 'rgb(128, 128, 255)';
  ctx.fillRect(0, 0, size, size);

  ctx.strokeStyle = 'rgb(200, 128, 200)';
  ctx.lineWidth = 6;
  for (let y = 16; y < size; y += 32) {
    ctx.beginPath();
    ctx.arc(size / 2, y, 14, 0, Math.PI * 2);
    ctx.stroke();
  }

  const texture = new THREE.CanvasTexture(canvas);
  texture.wrapS = THREE.RepeatWrapping;
  texture.wrapT = THREE.RepeatWrapping;
  texture.repeat.set(4, 2);
  return texture;
}

// Textura base de patrón cuadriculado sutil
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
  scene.background = new THREE.Color(0x0f1117);

  camera = new THREE.PerspectiveCamera(40, width / height, 0.1, 100);
  camera.position.set(0, 1.3, 4.0);
  camera.lookAt(0, 0, 0);

  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(width, height);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.shadowMap.enabled = true;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  container.innerHTML = '';
  container.appendChild(renderer.domElement);

  // Pedestal
  const pedGeo = new THREE.CylinderGeometry(1.3, 1.4, 0.2, 48);
  const pedMat = new THREE.MeshStandardMaterial({ color: 0x27272a, roughness: 0.85 });
  const pedestal = new THREE.Mesh(pedGeo, pedMat);
  pedestal.position.y = -0.7;
  pedestal.receiveShadow = true;
  scene.add(pedestal);

  proceduralNormal = createTeapotNormalMap(THREE);
  proceduralAlbedo = createTeapotBaseTexture(THREE);

  // Utah Teapot
  const teapotGeo = new TeapotGeometry(0.75, 20, true, true, true, true, true);
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

  // Luces de 3 Puntos
  const keyLight = new THREE.DirectionalLight(0xfffaed, 2.8);
  keyLight.position.set(2.5, 2.5, 2.0);
  keyLight.castShadow = true;
  scene.add(keyLight);

  const fillLight = new THREE.DirectionalLight(0x93c5fd, 0.8);
  fillLight.position.set(-2.5, 0.5, 1.5);
  scene.add(fillLight);

  const rimLight = new THREE.DirectionalLight(0xffffff, 2.5);
  rimLight.position.set(0, 2.0, -2.5);
  scene.add(rimLight);

  const ambient = new THREE.AmbientLight(0x18181b, 0.4);
  scene.add(ambient);

  const animate = () => {
    animId = requestAnimationFrame(animate);
    teapotMesh.rotation.y += 0.005;
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

const updateTintFromPicker = () => {
  if (teapotMesh && teapotMesh.material) {
    teapotMesh.material.color.set(currentTint.value);
    teapotMesh.material.needsUpdate = true;
  }
};

const setTint = (hex) => {
  currentTint.value = hex;
  updateTintFromPicker();
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
.ue-material-studio {
  border: 1px solid #334155;
  border-radius: 6px;
  margin: 20px 0;
  overflow: hidden;
  background: #0f172a;
  color: #f8fafc;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

.studio-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 14px;
  background: #090d16;
  border-bottom: 1px solid #1e293b;
}

.label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  font-weight: 700;
  color: #38bdf8;
  letter-spacing: 0.5px;
}

.desc {
  font-size: 11px;
  color: #94a3b8;
}

.canvas-wrapper {
  width: 100%;
  height: 280px;
}

/* TOOLBAR CON COLOR PICKER */
.viewport-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 16px;
  background: #1e293b;
  border-top: 1px solid #334155;
  border-bottom: 1px solid #334155;
}

.toolbar-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.toolbar-label {
  font-size: 11.5px;
  font-weight: 600;
  color: #f1f5f9;
}

.color-picker-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
}

.color-input {
  -webkit-appearance: none;
  border: none;
  width: 28px;
  height: 28px;
  border-radius: 4px;
  cursor: pointer;
  background: none;
}
.color-input::-webkit-color-swatch-wrapper { padding: 0; }
.color-input::-webkit-color-swatch { border: 1.5px solid #ffffff; border-radius: 4px; }

.hex-text {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  color: #38bdf8;
  background: #0f172a;
  padding: 2px 6px;
  border-radius: 3px;
  border: 1px solid #334155;
}

.toolbar-presets {
  display: flex;
  align-items: center;
  gap: 6px;
}

.preset-label {
  font-size: 11px;
  color: #94a3b8;
}

.preset-btn {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 1px solid #64748b;
  cursor: pointer;
  transition: transform 0.15s, border-color 0.15s;
}
.preset-btn.selected {
  border: 2px solid #ffffff;
  transform: scale(1.2);
}

/* MATERIAL GRAPH EN UNREAL ENGINE */
.graph-editor {
  background: #0b0f19;
  padding: 12px;
  position: relative;
}

.graph-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 8px;
  padding-bottom: 4px;
  border-bottom: 1px solid #1e293b;
}

.graph-title {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  font-weight: 700;
  color: #f1f5f9;
}

.graph-tip {
  font-size: 10px;
  color: #94a3b8;
}

.graph-canvas {
  position: relative;
  min-height: 440px;
  background: radial-gradient(circle, #1e293b 1px, transparent 1px);
  background-size: 16px 16px;
  border: 1px solid #1e293b;
  border-radius: 4px;
  padding: 12px;
  overflow-x: auto;
}

.wires-layer {
  position: absolute;
  top: 0;
  left: 0;
  pointer-events: none;
  z-index: 1;
}

.nodes-container {
  position: relative;
  z-index: 2;
  display: grid;
  grid-template-columns: 200px 160px 240px;
  gap: 50px;
}

.nodes-col {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* NODO UNREAL ENGINE */
.ue-node {
  background: #181e29;
  border: 1px solid #334155;
  border-radius: 5px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.4);
  font-size: 10px;
}

.node-titlebar {
  padding: 4px 8px;
  font-weight: 700;
  font-size: 10px;
  border-top-left-radius: 4px;
  border-top-right-radius: 4px;
  color: #ffffff;
}

.title-texture { background: #065f46; border-bottom: 1px solid #047857; }
.title-param { background: #1e3a8a; border-bottom: 1px solid #1d4ed8; }
.title-scalar { background: #075985; border-bottom: 1px solid #0284c7; }
.title-normal { background: #581c87; border-bottom: 1px solid #7e22ce; }
.title-math { background: #374151; border-bottom: 1px solid #4b5563; text-align: center; }
.title-master { background: #831843; border-bottom: 1px solid #9d174d; }

.node-content {
  padding: 6px 8px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.node-param-name {
  font-family: 'JetBrains Mono', monospace;
  font-size: 9px;
  color: #94a3b8;
  margin-bottom: 2px;
}

.color-swatch-box {
  width: 100%;
  height: 14px;
  border-radius: 2px;
  border: 1px solid #475569;
  margin-bottom: 2px;
}

.inline-slider {
  display: flex;
  align-items: center;
  gap: 6px;
}

.inline-slider input {
  flex: 1;
  accent-color: #38bdf8;
  height: 4px;
  cursor: pointer;
}

.inline-slider code {
  font-family: 'JetBrains Mono', monospace;
  font-size: 9px;
  color: #38bdf8;
  width: 28px;
  text-align: right;
}

/* PINS & DOTS */
.pin-row {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 9.5px;
  color: #cbd5e1;
}

.pin-row.right {
  justify-content: flex-end;
}

.pin-row.left {
  justify-content: flex-start;
}

.pin-row.active-input .pin-name {
  color: #ffffff;
  font-weight: 600;
}

.pin-row .dim {
  color: #64748b;
}

.pin-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  display: inline-block;
  border: 1px solid rgba(255,255,255,0.4);
}

.pin-dot.white { background: #ffffff; }
.pin-dot.red { background: #ef4444; }
.pin-dot.green { background: #22c55e; }
.pin-dot.blue { background: #3b82f6; }
.pin-dot.cyan { background: #06b6d4; }
.pin-dot.purple { background: #a855f7; }
.pin-dot.gray { background: #475569; }

.pins-split {
  display: flex;
  justify-content: space-between;
  gap: 12px;
}

@media (max-width: 900px) {
  .nodes-container {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  .wires-layer {
    display: none;
  }
}
</style>
