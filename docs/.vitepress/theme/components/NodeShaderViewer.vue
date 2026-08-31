<template>
  <div class="ue-material-studio">
    <div class="studio-header">
      <span class="label">MATERIAL GRAPH Y VIEWPORT 3D</span>
      <span class="desc">Esquema Nodal Paramétrico PBR — Utah Teapot</span>
    </div>

    <!-- VIEWPORT 3D: UTAH TEAPOT -->
    <div class="canvas-wrapper" ref="canvasContainer"></div>

    <!-- BARRA DE CONTROL SOBRIA -->
    <div class="viewport-toolbar">
      <div class="toolbar-item">
        <label class="toolbar-label">Color Tint (Vector Parameter):</label>
        <div class="color-picker-wrapper">
          <input type="color" v-model="currentTint" @input="updateTintFromPicker" class="color-input" />
          <code class="hex-text">{{ currentTint.toUpperCase() }}</code>
        </div>
      </div>

      <div class="toolbar-presets">
        <span class="preset-label">Muestras:</span>
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

    <!-- ESQUEMA DEL MATERIAL GRAPH (ESTILO UNREAL ENGINE) -->
    <div class="graph-editor">
      <div class="graph-header">
        <span class="graph-title">Graph: M_Master_PBR</span>
        <span class="graph-tip">Estructura de conexiones (Texture Sample ──► Multiply ──► Base Color)</span>
      </div>

      <div class="graph-canvas">
        <svg class="wires-layer" width="100%" height="100%">
          <!-- Cable 1: Texture Sample RGB -> Multiply A -->
          <path d="M 195 58 C 225 58, 225 72, 255 72" fill="none" stroke="#d4d4d8" stroke-width="1.8" />
          
          <!-- Cable 2: Color Tint RGB -> Multiply B -->
          <path d="M 195 150 C 225 150, 225 90, 255 90" fill="none" stroke="#d4d4d8" stroke-width="1.8" />

          <!-- Cable 3: Multiply Result -> Master Node Base Color -->
          <path d="M 355 81 C 395 81, 395 62, 435 62" fill="none" stroke="#d4d4d8" stroke-width="1.8" />

          <!-- Cable 4: Metallic Scalar -> Master Node Metallic -->
          <path d="M 195 228 C 315 228, 315 86, 435 86" fill="none" stroke="#a1a1aa" stroke-width="1.5" />

          <!-- Cable 5: Roughness Scalar -> Master Node Roughness -->
          <path d="M 195 304 C 315 304, 315 110, 435 110" fill="none" stroke="#a1a1aa" stroke-width="1.5" />

          <!-- Cable 6: Normal Scale -> Master Node Normal -->
          <path d="M 195 380 C 315 380, 315 158, 435 158" fill="none" stroke="#a1a1aa" stroke-width="1.5" />
        </svg>

        <div class="nodes-container">
          
          <!-- COLUMNA IZQUIERDA -->
          <div class="nodes-col left-col">
            
            <!-- NODO 1: TEXTURE SAMPLE -->
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

            <!-- NODO 2: VECTOR PARAMETER -->
            <div class="ue-node">
              <div class="node-titlebar title-param">Vector Parameter</div>
              <div class="node-content">
                <div class="node-param-name">Color_Tint</div>
                <div class="color-swatch-box" :style="{ background: currentTint }"></div>
                <div class="pin-row right">
                  <span class="pin-name">RGB</span>
                  <span class="pin-dot white"></span>
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
                  <span class="pin-dot gray"></span>
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
                  <span class="pin-dot gray"></span>
                </div>
              </div>
            </div>

            <!-- NODO 5: NORMAL STRENGTH -->
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
                  <span class="pin-dot gray"></span>
                </div>
              </div>
            </div>

          </div>

          <!-- COLUMNA CENTRAL: MULTIPLY -->
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
                      <span class="pin-dot white"></span>
                      <span class="pin-name">B</span>
                    </div>
                  </div>
                  <div class="right-pins">
                    <div class="pin-row right">
                      <span class="pin-name">Result</span>
                      <span class="pin-dot white"></span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- COLUMNA DERECHA: MASTER MATERIAL NODE -->
          <div class="nodes-col right-col">
            <div class="ue-node master-node">
              <div class="node-titlebar title-master">M_Master_PBR</div>
              <div class="node-content">
                <div class="pin-row left active-input">
                  <span class="pin-dot white"></span>
                  <span class="pin-name highlight">Base Color</span>
                </div>
                <div class="pin-row left active-input">
                  <span class="pin-dot gray"></span>
                  <span class="pin-name highlight">Metallic</span>
                </div>
                <div class="pin-row left">
                  <span class="pin-dot dark-dot"></span>
                  <span class="pin-name dim">Specular</span>
                </div>
                <div class="pin-row left active-input">
                  <span class="pin-dot gray"></span>
                  <span class="pin-name highlight">Roughness</span>
                </div>
                <div class="pin-row left">
                  <span class="pin-dot dark-dot"></span>
                  <span class="pin-name dim">Emissive Color</span>
                </div>
                <div class="pin-row left">
                  <span class="pin-dot dark-dot"></span>
                  <span class="pin-name dim">Opacity</span>
                </div>
                <div class="pin-row left active-input">
                  <span class="pin-dot gray"></span>
                  <span class="pin-name highlight">Normal</span>
                </div>
                <div class="pin-row left">
                  <span class="pin-dot dark-dot"></span>
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
const currentTint = ref('#e5e7eb'); // Cerámica / metal neutro
const roughness = ref(0.35);
const metallic = ref(0.65);
const normalStrength = ref(1.5);

const tintPresets = [
  { name: 'Cerámica Blanca', color: '#e5e7eb' },
  { name: 'Oro Pulido', color: '#d4af37' },
  { name: 'Cobre Rojo', color: '#b85d38' },
  { name: 'Bronce Clásico', color: '#cd7f32' },
  { name: 'Acero Oscuro', color: '#4b5563' },
  { name: 'Gris Grafito', color: '#27272a' }
];

let scene, camera, renderer, teapotMesh, animId, proceduralNormal, proceduralAlbedo;

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

function createTeapotBaseTexture(THREE) {
  const size = 256;
  const canvas = document.createElement('canvas');
  canvas.width = size;
  canvas.height = size;
  const ctx = canvas.getContext('2d');

  ctx.fillStyle = '#ffffff';
  ctx.fillRect(0, 0, size, size);

  ctx.fillStyle = '#e5e7eb';
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
  scene.background = new THREE.Color(0x18181b);

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

  // Pedestal neutro
  const pedGeo = new THREE.CylinderGeometry(1.3, 1.4, 0.2, 48);
  const pedMat = new THREE.MeshStandardMaterial({ color: 0x27272a, roughness: 0.85 });
  const pedestal = new THREE.Mesh(pedGeo, pedMat);
  pedestal.position.y = -0.7;
  pedestal.receiveShadow = true;
  scene.add(pedestal);

  proceduralNormal = createTeapotNormalMap(THREE);
  proceduralAlbedo = createTeapotBaseTexture(THREE);

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

  // Iluminación 3 puntos sobria
  const keyLight = new THREE.DirectionalLight(0xfffaed, 2.8);
  keyLight.position.set(2.5, 2.5, 2.0);
  keyLight.castShadow = true;
  scene.add(keyLight);

  const fillLight = new THREE.DirectionalLight(0xd4d4d8, 0.8);
  fillLight.position.set(-2.5, 0.5, 1.5);
  scene.add(fillLight);

  const rimLight = new THREE.DirectionalLight(0xffffff, 2.5);
  rimLight.position.set(0, 2.0, -2.5);
  scene.add(rimLight);

  const ambient = new THREE.AmbientLight(0x27272a, 0.4);
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
  border: 1px solid #d1d5db;
  border-radius: 4px;
  margin: 18px 0;
  overflow: hidden;
  background: #ffffff;
  color: #111827;
}

.studio-header {
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

/* TOOLBAR CON COLOR PICKER */
.viewport-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 16px;
  background: #f9fafb;
  border-top: 1px solid #e5e7eb;
  border-bottom: 1px solid #e5e7eb;
}

.toolbar-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.toolbar-label {
  font-size: 11.5px;
  font-weight: 600;
  color: #111827;
}

.color-picker-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
}

.color-input {
  -webkit-appearance: none;
  border: 1px solid #d1d5db;
  width: 26px;
  height: 26px;
  border-radius: 3px;
  cursor: pointer;
  background: none;
  padding: 0;
}
.color-input::-webkit-color-swatch-wrapper { padding: 0; }
.color-input::-webkit-color-swatch { border: none; border-radius: 2px; }

.hex-text {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  color: #111827;
  background: #ffffff;
  padding: 2px 6px;
  border-radius: 3px;
  border: 1px solid #d1d5db;
}

.toolbar-presets {
  display: flex;
  align-items: center;
  gap: 6px;
}

.preset-label {
  font-size: 11px;
  color: #6b7280;
}

.preset-btn {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 1px solid #9ca3af;
  cursor: pointer;
  transition: transform 0.15s, border-color 0.15s;
}
.preset-btn.selected {
  border: 2px solid #111827;
  transform: scale(1.15);
}

/* MATERIAL GRAPH EN UNREAL ENGINE (ESTILO AUTÉNTICO) */
.graph-editor {
  background: #18181b;
  padding: 12px;
  position: relative;
  color: #f4f4f5;
}

.graph-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 8px;
  padding-bottom: 4px;
  border-bottom: 1px solid #27272a;
}

.graph-title {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  font-weight: 700;
  color: #f4f4f5;
}

.graph-tip {
  font-size: 10.5px;
  color: #a1a1aa;
}

.graph-canvas {
  position: relative;
  min-height: 430px;
  background-color: #121214;
  background-image: 
    linear-gradient(#1f1f23 1px, transparent 1px),
    linear-gradient(90deg, #1f1f23 1px, transparent 1px);
  background-size: 20px 20px;
  border: 1px solid #27272a;
  border-radius: 3px;
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
  grid-template-columns: 190px 150px 220px;
  gap: 45px;
}

.nodes-col {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

/* NODO UNREAL ENGINE */
.ue-node {
  background: #1e1e24;
  border: 1px solid #333338;
  border-radius: 3px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
  font-size: 9.5px;
}

.node-titlebar {
  padding: 3px 6px;
  font-weight: 700;
  font-size: 9.5px;
  border-top-left-radius: 2px;
  border-top-right-radius: 2px;
  color: #f4f4f5;
}

/* TONOS SUTILES AUTÉNTICOS DE UNREAL ENGINE */
.title-texture { background: #16382c; border-bottom: 1px solid #1f4e3d; }
.title-param { background: #1b2a4a; border-bottom: 1px solid #263c68; }
.title-scalar { background: #26262b; border-bottom: 1px solid #383840; }
.title-normal { background: #2f1d44; border-bottom: 1px solid #432961; }
.title-math { background: #2a2a30; border-bottom: 1px solid #3a3a42; text-align: center; }
.title-master { background: #4a1924; border-bottom: 1px solid #662232; }

.node-content {
  padding: 5px 7px;
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.node-param-name {
  font-family: 'JetBrains Mono', monospace;
  font-size: 8.5px;
  color: #a1a1aa;
  margin-bottom: 2px;
}

.color-swatch-box {
  width: 100%;
  height: 12px;
  border-radius: 2px;
  border: 1px solid #52525b;
  margin-bottom: 2px;
}

.inline-slider {
  display: flex;
  align-items: center;
  gap: 5px;
}

.inline-slider input {
  flex: 1;
  accent-color: #d4d4d8;
  height: 3px;
  cursor: pointer;
}

.inline-slider code {
  font-family: 'JetBrains Mono', monospace;
  font-size: 8.5px;
  color: #e4e4e7;
  width: 26px;
  text-align: right;
}

/* PINS & DOTS */
.pin-row {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 9px;
  color: #d4d4d8;
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
  color: #52525b;
}

.pin-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  display: inline-block;
  border: 1px solid rgba(255,255,255,0.3);
}

.pin-dot.white { background: #e4e4e7; }
.pin-dot.red { background: #ef4444; }
.pin-dot.green { background: #22c55e; }
.pin-dot.blue { background: #3b82f6; }
.pin-dot.gray { background: #9ca3af; }
.pin-dot.dark-dot { background: #3f3f46; border-color: #27272a; }

.pins-split {
  display: flex;
  justify-content: space-between;
  gap: 10px;
}

@media (max-width: 900px) {
  .nodes-container {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  .wires-layer {
    display: none;
  }
}
</style>
