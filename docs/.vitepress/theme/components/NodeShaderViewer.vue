<template>
  <div class="technical-figure">
    <div class="figure-header">
      <span class="label">SIMULADOR INTERACTIVO</span>
      <span class="desc">Shader Nodal Paramétrico PBR — Utah Teapot</span>
    </div>
    
    <!-- VIEWPORT 3D: UTAH TEAPOT -->
    <div class="canvas-wrapper" ref="canvasContainer"></div>

    <!-- CONTROLES PARAMÉTRICOS EN FORMATO BLANCO Y NEGRO -->
    <div class="controls-grid">
      
      <!-- CONTROL 1: COLOR TINT (VECTOR PARAMETER) -->
      <div class="control-card">
        <div class="control-label">
          <span>1. Tinte de Color (Vector Parameter):</span>
          <code>{{ currentTint.toUpperCase() }}</code>
        </div>
        <div class="picker-row">
          <input type="color" v-model="currentTint" @input="updateTintFromPicker" class="color-picker" />
          <div class="preset-list">
            <button 
              v-for="t in tintPresets" 
              :key="t.name" 
              :style="{ background: t.color }" 
              :title="t.name" 
              @click="setTint(t.color)" 
              :class="['preset-circle', { active: currentTint.toLowerCase() === t.color.toLowerCase() }]"
            ></button>
          </div>
        </div>
        <div class="hints"><span>Multiplicación directa sobre la textura base</span></div>
      </div>

      <!-- CONTROL 2: ROUGHNESS -->
      <div class="control-card">
        <div class="control-label">
          <span>2. Rugosidad (Roughness):</span>
          <code>{{ roughness.toFixed(2) }}</code>
        </div>
        <input type="range" min="0" max="1" step="0.01" v-model.number="roughness" @input="updateShader" />
        <div class="hints"><span>0.0 (Especular liso)</span><span>1.0 (Difuso mate)</span></div>
      </div>

      <!-- CONTROL 3: METALLIC -->
      <div class="control-card">
        <div class="control-label">
          <span>3. Metalicidad (Metallic):</span>
          <code>{{ metallic.toFixed(2) }}</code>
        </div>
        <input type="range" min="0" max="1" step="0.01" v-model.number="metallic" @input="updateShader" />
        <div class="hints"><span>0.0 (Dieléctrico)</span><span>1.0 (Conductor puro)</span></div>
      </div>

      <!-- CONTROL 4: NORMAL STRENGTH -->
      <div class="control-card">
        <div class="control-label">
          <span>4. Intensidad de Normales:</span>
          <code>{{ normalStrength.toFixed(1) }}x</code>
        </div>
        <input type="range" min="0" max="3" step="0.1" v-model.number="normalStrength" @input="updateShader" />
        <div class="hints"><span>0.0 (Plano)</span><span>3.0 (Relieve pronunciado)</span></div>
      </div>

    </div>

    <!-- ESQUEMA TÉCNICO DE NODOS (ESTILO DIAGRAMA DE INGENIERÍA / UNREAL ENGINE) -->
    <div class="schematic-section">
      <div class="schematic-header">
        <span>Esquema Nodal en Unreal Engine (M_Master_PBR)</span>
      </div>

      <div class="schematic-canvas">
        <svg class="wires-svg" viewBox="0 0 760 300" width="100%" height="280">
          
          <!-- CABLE 1: Texture Sample RGB -> Multiply A -->
          <path d="M 210 50 C 255 50, 255 65, 290 65" fill="none" stroke="#111827" stroke-width="2" />
          
          <!-- CABLE 2: Color Tint RGB -> Multiply B -->
          <path d="M 210 135 C 255 135, 255 85, 290 85" fill="none" stroke="#111827" stroke-width="2" />

          <!-- CABLE 3: Multiply Result -> Master Node Base Color -->
          <path d="M 410 75 C 470 75, 470 60, 520 60" fill="none" stroke="#111827" stroke-width="2" />

          <!-- CABLE 4: Metallic -> Master Node Metallic -->
          <path d="M 210 195 C 380 195, 380 85, 520 85" fill="none" stroke="#4b5563" stroke-width="1.8" />

          <!-- CABLE 5: Roughness -> Master Node Roughness -->
          <path d="M 210 245 C 380 245, 380 110, 520 110" fill="none" stroke="#4b5563" stroke-width="1.8" />

          <!-- CABLE 6: Normal Flatten -> Master Node Normal -->
          <path d="M 210 285 C 380 285, 380 155, 520 155" fill="none" stroke="#4b5563" stroke-width="1.8" />

          <!-- ================= NODOS IZQUIERDA ================= -->

          <!-- NODO 1: TEXTURE SAMPLE -->
          <g transform="translate(10, 20)">
            <rect width="200" height="60" rx="3" fill="#ffffff" stroke="#111827" stroke-width="1.2"/>
            <rect width="200" height="18" rx="3" fill="#1f2937"/>
            <text x="8" y="13" font-family="Inter, sans-serif" font-size="9" font-weight="700" fill="#ffffff">Texture Sample</text>
            <text x="8" y="32" font-family="JetBrains Mono, monospace" font-size="8" fill="#4b5563">T_Teapot_Albedo</text>
            <text x="175" y="52" font-family="JetBrains Mono, monospace" font-size="8" font-weight="700" fill="#111827">RGB</text>
            <circle cx="195" cy="49" r="4" fill="#111827"/>
          </g>

          <!-- NODO 2: VECTOR PARAMETER (COLOR TINT) -->
          <g transform="translate(10, 95)">
            <rect width="200" height="65" rx="3" fill="#ffffff" stroke="#111827" stroke-width="1.2"/>
            <rect width="200" height="18" rx="3" fill="#1f2937"/>
            <text x="8" y="13" font-family="Inter, sans-serif" font-size="9" font-weight="700" fill="#ffffff">Vector Parameter</text>
            <text x="8" y="32" font-family="JetBrains Mono, monospace" font-size="8" fill="#4b5563">Color_Tint</text>
            <!-- Muestra de color actual -->
            <rect x="8" y="40" width="130" height="14" rx="2" :fill="currentTint" stroke="#9ca3af" stroke-width="0.8"/>
            <text x="175" y="52" font-family="JetBrains Mono, monospace" font-size="8" font-weight="700" fill="#111827">RGB</text>
            <circle cx="195" cy="49" r="4" fill="#111827"/>
          </g>

          <!-- NODO 3: SCALAR PARAMETER (METALLIC) -->
          <g transform="translate(10, 175)">
            <rect width="200" height="38" rx="3" fill="#ffffff" stroke="#9ca3af" stroke-width="1"/>
            <rect width="200" height="16" rx="3" fill="#374151"/>
            <text x="8" y="12" font-family="Inter, sans-serif" font-size="8.5" font-weight="700" fill="#ffffff">Scalar: Metallic</text>
            <text x="8" y="29" font-family="JetBrains Mono, monospace" font-size="8" fill="#111827">Valor: {{ metallic.toFixed(2) }}</text>
            <circle cx="195" cy="27" r="3.5" fill="#4b5563"/>
          </g>

          <!-- NODO 4: SCALAR PARAMETER (ROUGHNESS) -->
          <g transform="translate(10, 222)">
            <rect width="200" height="38" rx="3" fill="#ffffff" stroke="#9ca3af" stroke-width="1"/>
            <rect width="200" height="16" rx="3" fill="#374151"/>
            <text x="8" y="12" font-family="Inter, sans-serif" font-size="8.5" font-weight="700" fill="#ffffff">Scalar: Roughness</text>
            <text x="8" y="29" font-family="JetBrains Mono, monospace" font-size="8" fill="#111827">Valor: {{ roughness.toFixed(2) }}</text>
            <circle cx="195" cy="27" r="3.5" fill="#4b5563"/>
          </g>

          <!-- NODO 5: NORMAL FLATTEN / STRENGTH -->
          <g transform="translate(10, 267)">
            <rect width="200" height="30" rx="3" fill="#ffffff" stroke="#9ca3af" stroke-width="1"/>
            <rect width="200" height="14" rx="3" fill="#374151"/>
            <text x="8" y="11" font-family="Inter, sans-serif" font-size="8" font-weight="700" fill="#ffffff">Normal Strength</text>
            <text x="8" y="24" font-family="JetBrains Mono, monospace" font-size="7.5" fill="#111827">Escala: {{ normalStrength.toFixed(1) }}x</text>
            <circle cx="195" cy="22" r="3.5" fill="#4b5563"/>
          </g>

          <!-- ================= NODO CENTRAL: MULTIPLY ================= -->
          <g transform="translate(290, 40)">
            <rect width="120" height="65" rx="3" fill="#ffffff" stroke="#111827" stroke-width="1.2"/>
            <rect width="120" height="18" rx="3" fill="#111827"/>
            <text x="60" y="13" font-family="Inter, sans-serif" font-size="9" font-weight="700" text-anchor="middle" fill="#ffffff">Multiply</text>
            <!-- Entrada A -->
            <circle cx="10" cy="30" r="4" fill="#111827"/>
            <text x="20" y="33" font-family="JetBrains Mono, monospace" font-size="8" fill="#111827">A (Textura)</text>
            <!-- Entrada B -->
            <circle cx="10" cy="50" r="4" fill="#111827"/>
            <text x="20" y="53" font-family="JetBrains Mono, monospace" font-size="8" fill="#111827">B (Tinte)</text>
            <!-- Salida Result -->
            <circle cx="110" cy="40" r="4" fill="#111827"/>
            <text x="75" y="43" font-family="JetBrains Mono, monospace" font-size="8" fill="#111827">Out</text>
          </g>

          <!-- ================= NODO DERECHA: MASTER NODE ================= -->
          <g transform="translate(520, 20)">
            <rect width="230" height="240" rx="3" fill="#ffffff" stroke="#111827" stroke-width="1.5"/>
            <rect width="230" height="22" rx="3" fill="#111827"/>
            <text x="115" y="15" font-family="Inter, sans-serif" font-size="9.5" font-weight="700" text-anchor="middle" fill="#ffffff">M_Master_PBR (Root)</text>
            
            <!-- Pines de entrada -->
            <g transform="translate(10, 40)">
              <circle cx="4" cy="0" r="4" fill="#111827"/>
              <text x="14" y="3" font-family="JetBrains Mono, monospace" font-size="8.5" font-weight="700" fill="#111827">Base Color</text>
            </g>

            <g transform="translate(10, 65)">
              <circle cx="4" cy="0" r="4" fill="#4b5563"/>
              <text x="14" y="3" font-family="JetBrains Mono, monospace" font-size="8.5" font-weight="700" fill="#111827">Metallic</text>
            </g>

            <g transform="translate(10, 90)">
              <circle cx="4" cy="0" r="3" fill="#d1d5db"/>
              <text x="14" y="3" font-family="JetBrains Mono, monospace" font-size="8" fill="#9ca3af">Specular</text>
            </g>

            <g transform="translate(10, 115)">
              <circle cx="4" cy="0" r="4" fill="#4b5563"/>
              <text x="14" y="3" font-family="JetBrains Mono, monospace" font-size="8.5" font-weight="700" fill="#111827">Roughness</text>
            </g>

            <g transform="translate(10, 140)">
              <circle cx="4" cy="0" r="3" fill="#d1d5db"/>
              <text x="14" y="3" font-family="JetBrains Mono, monospace" font-size="8" fill="#9ca3af">Emissive Color</text>
            </g>

            <g transform="translate(10, 165)">
              <circle cx="4" cy="0" r="4" fill="#4b5563"/>
              <text x="14" y="3" font-family="JetBrains Mono, monospace" font-size="8.5" font-weight="700" fill="#111827">Normal</text>
            </g>

            <g transform="translate(10, 190)">
              <circle cx="4" cy="0" r="3" fill="#d1d5db"/>
              <text x="14" y="3" font-family="JetBrains Mono, monospace" font-size="8" fill="#9ca3af">Ambient Occlusion</text>
            </g>
          </g>

        </svg>
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
  const height = 260;

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
.technical-figure {
  border: 1px solid #d1d5db;
  border-radius: 4px;
  margin: 18px 0;
  overflow: hidden;
  background: #ffffff;
  color: #111827;
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

/* PANEL DE CONTROLES: EXACTO AL FORMATO DE IMAGEN 2 */
.controls-grid {
  padding: 14px;
  background: #ffffff;
  border-top: 1px solid #e5e7eb;
  border-bottom: 1px solid #e5e7eb;
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

.picker-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.color-picker {
  -webkit-appearance: none;
  border: 1px solid #d1d5db;
  width: 26px;
  height: 26px;
  border-radius: 3px;
  cursor: pointer;
  background: none;
  padding: 0;
}
.color-picker::-webkit-color-swatch-wrapper { padding: 0; }
.color-picker::-webkit-color-swatch { border: none; border-radius: 2px; }

.preset-list {
  display: flex;
  align-items: center;
  gap: 6px;
}

.preset-circle {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  border: 1px solid #9ca3af;
  cursor: pointer;
  transition: transform 0.15s, border-color 0.15s;
}

.preset-circle.active {
  border: 2px solid #111827;
  transform: scale(1.15);
}

/* ESQUEMA TÉCNICO DE NODOS BLANCO Y NEGRO */
.schematic-section {
  background: #f9fafb;
  padding: 12px 14px;
}

.schematic-header {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #111827;
  margin-bottom: 8px;
}

.schematic-canvas {
  background: #ffffff;
  border: 1px solid #d1d5db;
  border-radius: 3px;
  padding: 8px;
  overflow-x: auto;
}

.wires-svg {
  display: block;
}

@media (max-width: 768px) {
  .controls-grid {
    grid-template-columns: 1fr;
  }
}
</style>
