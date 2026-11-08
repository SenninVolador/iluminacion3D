<template>
  <div class="technical-figure">
    <div class="figure-header">
      <div class="header-left">
        <span class="label">LABORATORIO INTERACTIVO 03</span>
        <span class="desc">Cuantización de Luz en NPR: De Producto Punto (N · L) a Rampas Cel Shading y Halftone</span>
      </div>
      <span class="viewport-hint">Arrastra para rotar · Observa la rampa matemática inferior</span>
    </div>

    <!-- PRESETS DE ESTILO NPR DE LA INDUSTRIA -->
    <div class="presets-bar">
      <div class="bar-group">
        <span class="preset-title">Arquitectura de Shader NPR:</span>
        <div class="preset-buttons">
          <button
            :class="['preset-btn', { active: stylePreset === 'anime2' }]"
            @click="applyStylePreset('anime2')"
          >
            Anime 2 Tonos (Guilty Gear / Genshin)
          </button>
          <button
            :class="['preset-btn', { active: stylePreset === 'toon3' }]"
            @click="applyStylePreset('toon3')"
          >
            Cel Shading 3 Bandas (Zelda Wind Waker / BotW)
          </button>
          <button
            :class="['preset-btn', { active: stylePreset === 'comic' }]"
            @click="applyStylePreset('comic')"
          >
            Halftone / Cómic (Hi-Fi Rush / Spider-Verse)
          </button>
          <button
            :class="['preset-btn', { active: stylePreset === 'pbr' }]"
            @click="applyStylePreset('pbr')"
          >
            Comparativa: Gradiente Continuo (PBR)
          </button>
        </div>
      </div>
    </div>

    <!-- VIEWPORT 3D -->
    <div class="canvas-wrapper" ref="canvasContainer"></div>

    <!-- COMPARADOR VISUAL DE LA RAMPA (N · L CONTINUO VS. CUANTIZADO) -->
    <div class="ramp-panel">
      <div class="ramp-row">
        <span class="ramp-label">1. Entrada Física <code>dot(N, L)</code> Continua (-1 a +1):</span>
        <div class="ramp-bar continuous-gradient"></div>
      </div>
      <div class="ramp-row">
        <span class="ramp-label">2. Salida del Shader NPR (Rampa / Step Aplicado):</span>
        <canvas ref="rampCanvas" class="ramp-bar" width="500" height="22"></canvas>
      </div>
    </div>

    <!-- CONTROLES PARAMÉTRICOS -->
    <div class="controls-grid">
      <!-- 1. SUAVIDAD DEL CORTE (STEP VS SMOOTHSTEP) -->
      <div class="control-card">
        <div class="control-label">
          <span>1. Dureza del Corte (Terminator Smoothness):</span>
          <code>{{ edgeSoftness.toFixed(3) }}</code>
        </div>
        <div class="toggle-row">
          <input type="range" min="0.002" max="0.35" step="0.005" v-model.number="edgeSoftness" @input="onParamChange" />
        </div>
        <div class="hints">
          <span>0.005 = Corte duro tipo <code>Step</code> (Cel puro) · 0.25 = Transición suave <code>Smoothstep</code>.</span>
        </div>
      </div>

      <!-- 2. POSICIÓN DEL CORTE PRINCIPAL -->
      <div class="control-card">
        <div class="control-label">
          <span>2. Posición del Umbral de Sombra (Shadow Cut):</span>
          <code>{{ shadowCut.toFixed(2) }}</code>
        </div>
        <div class="toggle-row">
          <input type="range" min="-0.4" max="0.5" step="0.02" v-model.number="shadowCut" @input="onParamChange" />
        </div>
        <div class="hints">
          <span>Desplaza la frontera entre la zona iluminada y la sombra proyectada.</span>
        </div>
      </div>

      <!-- 3. SPECULAR ESTILIZADO (STEPPED SPECULAR) -->
      <div class="control-card">
        <div class="control-label">
          <span>3. Brillo Especular Recortado (Stepped Specular):</span>
          <code>{{ specIntensity > 0.01 ? (specIntensity * 100).toFixed(0) + '%' : 'Apagado' }}</code>
        </div>
        <div class="toggle-row">
          <input type="range" min="0" max="1" step="0.05" v-model.number="specIntensity" @input="onParamChange" />
        </div>
        <div class="hints">
          <span>Convierte el reflejo Blinn-Phong en una mancha de luz sólida de bordes nítidos.</span>
        </div>
      </div>

      <!-- 4. SOMBRA CÁLIDA / COLOREADA (TINTED SHADOWS) -->
      <div class="control-card">
        <div class="control-label">
          <span>4. Saturación Cromática de la Sombra (No usar Negro):</span>
          <code>{{ (shadowSaturation * 100).toFixed(0) }}%</code>
        </div>
        <div class="toggle-row">
          <input type="range" min="0" max="1.2" step="0.05" v-model.number="shadowSaturation" @input="onParamChange" />
        </div>
        <div class="hints">
          <span>Regla de oro NPR: las sombras estilizadas nunca se multiplican por negro puro (0,0,0), sino por tonos violeta/azul/coral.</span>
        </div>
      </div>
    </div>

    <div class="methodology-note">
      <strong>Matemática del Sombreado No-Fotorrealista (NPR):</strong>
      Tanto un shader realista (PBR) como un shader de anime (Cel Shading) parten exactamente de la misma operación vectorial: el producto punto <code>dot(VertexNormal, LightVector)</code>. La diferencia radica en que el shader realista usa ese valor como una rampa lineal continua, mientras que el shader NPR pasa el resultado por funciones escalonadas (<code>Step</code>, <code>Smoothstep</code> o una textura <strong>Color Ramp 1D / LUT</strong>) y reemplaza la sombra negra por un color artístico saturado.
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';

const canvasContainer = ref(null);
const rampCanvas = ref(null);

const stylePreset = ref('anime2'); // 'anime2' | 'toon3' | 'comic' | 'pbr'
const edgeSoftness = ref(0.015);
const shadowCut = ref(0.05);
const specIntensity = ref(0.75);
const shadowSaturation = ref(0.95);

let THREE = null;
let scene, camera, renderer, animId, clock;
let knotMesh, outlineMesh;
let isDragging = false;
let prevMouse = { x: 0, y: 0 };
let camOrbit = { theta: 0.4, phi: 0.2, radius: 3.7 };

function getStyleModeInt() {
  return stylePreset.value === 'anime2' ? 0 :
         stylePreset.value === 'toon3' ? 1 :
         stylePreset.value === 'comic' ? 2 : 3;
}

function draw2DRampPreview() {
  const cvs = rampCanvas.value;
  if (!cvs) return;
  const ctx = cvs.getContext('2d');
  const w = cvs.width;
  const h = cvs.height;

  const mode = getStyleModeInt();
  const soft = edgeSoftness.value;
  const cut = shadowCut.value;
  const sat = shadowSaturation.value;

  const smoothstep = (edge0, edge1, x) => {
    const t = Math.max(0, Math.min(1, (x - edge0) / (edge1 - edge0)));
    return t * t * (3 - 2 * t);
  };

  for (let x = 0; x < w; x++) {
    // Mapear x de [0, w] a NdotL [-1, +1]
    const ndotl = (x / w) * 2.0 - 1.0;

    // Color de sombra (gris si sat=0, violeta/índigo rico si sat=1)
    const shR = 0.22 * (1 - sat) + 0.36 * sat;
    const shG = 0.22 * (1 - sat) + 0.24 * sat;
    const shB = 0.22 * (1 - sat) + 0.48 * sat;

    const midR = 0.55 * (1 - sat) + 0.72 * sat;
    const midG = 0.55 * (1 - sat) + 0.46 * sat;
    const midB = 0.55 * (1 - sat) + 0.54 * sat;

    const litR = 0.96;
    const litG = 0.88;
    const litB = 0.78;

    let r = litR, g = litG, b = litB;

    if (mode === 3) {
      // PBR continuo
      const t = Math.max(0, Math.min(1, ndotl * 0.5 + 0.5));
      r = shR + (litR - shR) * t;
      g = shG + (litG - shG) * t;
      b = shB + (litB - shB) * t;
    } else if (mode === 1) {
      // 3 Bandas
      const b1 = smoothstep(cut - 0.25 - soft, cut - 0.25 + soft, ndotl);
      const b2 = smoothstep(cut + 0.15 - soft, cut + 0.15 + soft, ndotl);
      r = shR * (1 - b1) + midR * b1;
      g = shG * (1 - b1) + midG * b1;
      b = shB * (1 - b1) + midB * b1;
      r = r * (1 - b2) + litR * b2;
      g = g * (1 - b2) + litG * b2;
      b = b * (1 - b2) + litB * b2;
    } else {
      // 2 Tonos o Comic
      const b1 = smoothstep(cut - soft, cut + soft, ndotl);
      r = shR * (1 - b1) + litR * b1;
      g = shG * (1 - b1) + litG * b1;
      b = shB * (1 - b1) + litB * b1;
    }

    ctx.fillStyle = `rgb(${Math.round(r * 255)}, ${Math.round(g * 255)}, ${Math.round(b * 255)})`;
    ctx.fillRect(x, 0, 1, h);
  }
}

function applyStylePreset(key) {
  stylePreset.value = key;
  if (key === 'anime2') {
    edgeSoftness.value = 0.012;
    shadowCut.value = 0.05;
    specIntensity.value = 0.75;
    shadowSaturation.value = 0.95;
  } else if (key === 'toon3') {
    edgeSoftness.value = 0.018;
    shadowCut.value = 0.05;
    specIntensity.value = 0.85;
    shadowSaturation.value = 1.0;
  } else if (key === 'comic') {
    edgeSoftness.value = 0.14;
    shadowCut.value = 0.08;
    specIntensity.value = 0.9;
    shadowSaturation.value = 1.0;
  } else if (key === 'pbr') {
    edgeSoftness.value = 0.35;
    shadowCut.value = 0.0;
    specIntensity.value = 0.35;
    shadowSaturation.value = 0.25;
  }
  onParamChange();
}

function onParamChange() {
  if (knotMesh) {
    knotMesh.material.uniforms.uMode.value = getStyleModeInt();
    knotMesh.material.uniforms.uSoftness.value = edgeSoftness.value;
    knotMesh.material.uniforms.uShadowCut.value = shadowCut.value;
    knotMesh.material.uniforms.uSpecIntensity.value = specIntensity.value;
    knotMesh.material.uniforms.uShadowSat.value = shadowSaturation.value;
  }
  if (outlineMesh) {
    outlineMesh.visible = stylePreset.value !== 'pbr';
  }
  draw2DRampPreview();
}

function updateCameraOrbit() {
  if (!camera) return;
  camera.position.x = camOrbit.radius * Math.sin(camOrbit.theta) * Math.cos(camOrbit.phi);
  camera.position.y = camOrbit.radius * Math.sin(camOrbit.phi);
  camera.position.z = camOrbit.radius * Math.cos(camOrbit.theta) * Math.cos(camOrbit.phi);
  camera.lookAt(0, 0, 0);
}

const initThree = async () => {
  if (typeof window === 'undefined') return;
  THREE = await import('three');

  const container = canvasContainer.value;
  if (!container) return;

  const width = container.clientWidth || 680;
  const height = 290;

  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x141418);

  camera = new THREE.PerspectiveCamera(38, width / height, 0.1, 100);
  updateCameraOrbit();

  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(width, height);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  container.innerHTML = '';
  container.appendChild(renderer.domElement);

  const geo = new THREE.TorusKnotGeometry(0.72, 0.26, 128, 32);

  const mat = new THREE.ShaderMaterial({
    uniforms: {
      uTime: { value: 0 },
      uMode: { value: getStyleModeInt() },
      uSoftness: { value: edgeSoftness.value },
      uShadowCut: { value: shadowCut.value },
      uSpecIntensity: { value: specIntensity.value },
      uShadowSat: { value: shadowSaturation.value }
    },
    vertexShader: `
      varying vec3 vNormal;
      varying vec3 vViewDir;
      varying vec4 vScreenPos;
      void main() {
        vec4 worldPos = modelMatrix * vec4(position, 1.0);
        vNormal = normalize(mat3(modelMatrix) * normal);
        vViewDir = normalize(cameraPosition - worldPos.xyz);
        gl_Position = projectionMatrix * viewMatrix * worldPos;
        vScreenPos = gl_Position;
      }
    `,
    fragmentShader: `
      uniform float uTime;
      uniform int uMode;
      uniform float uSoftness;
      uniform float uShadowCut;
      uniform float uSpecIntensity;
      uniform float uShadowSat;

      varying vec3 vNormal;
      varying vec3 vViewDir;
      varying vec4 vScreenPos;

      void main() {
        vec3 N = normalize(vNormal);
        vec3 V = normalize(vViewDir);
        vec3 L = normalize(vec3(sin(uTime * 0.65) * 0.85, 0.55, cos(uTime * 0.65) * 0.85));

        float NdotL = dot(N, L);

        vec3 shadowCol = mix(vec3(0.22), vec3(0.36, 0.24, 0.48), uShadowSat);
        vec3 midCol = mix(vec3(0.55), vec3(0.72, 0.46, 0.54), uShadowSat);
        vec3 litCol = vec3(0.96, 0.88, 0.78);

        vec3 col = litCol;

        if (uMode == 3) {
          // PBR Gradiente Continuo
          float diff = clamp(NdotL * 0.5 + 0.5, 0.0, 1.0);
          col = mix(shadowCol, litCol, diff);
        } else if (uMode == 1) {
          // 3 Bandas (Zelda BotW / Wind Waker)
          float b1 = smoothstep(uShadowCut - 0.25 - uSoftness, uShadowCut - 0.25 + uSoftness, NdotL);
          float b2 = smoothstep(uShadowCut + 0.15 - uSoftness, uShadowCut + 0.15 + uSoftness, NdotL);
          col = mix(shadowCol, midCol, b1);
          col = mix(col, litCol, b2);
        } else if (uMode == 2) {
          // Halftone / Cómic (Hi-Fi Rush / Spider-Verse)
          vec2 screenUV = (vScreenPos.xy / vScreenPos.w) * vec2(85.0, 42.0);
          vec2 grid = fract(screenUV) - 0.5;
          float dotPattern = length(grid);
          float ramp = smoothstep(uShadowCut - 0.22, uShadowCut + 0.22, NdotL);
          float halftone = step(1.0 - ramp, dotPattern * 1.35);
          col = mix(shadowCol, litCol, halftone);
        } else {
          // Anime 2 Tonos
          float cel = smoothstep(uShadowCut - uSoftness, uShadowCut + uSoftness, NdotL);
          col = mix(shadowCol, litCol, cel);
        }

        // Specular recortado (Stepped Specular)
        vec3 H = normalize(L + V);
        float NdotH = max(dot(N, H), 0.0);
        if (uMode == 3) {
          float spec = pow(NdotH, 48.0) * uSpecIntensity;
          col += vec3(spec);
        } else {
          float specCut = smoothstep(0.86 - uSoftness * 0.5, 0.87 + uSoftness * 0.5, NdotH);
          col = mix(col, vec3(1.0, 0.98, 0.94), specCut * uSpecIntensity);
        }

        gl_FragColor = vec4(col, 1.0);
      }
    `
  });

  knotMesh = new THREE.Mesh(geo, mat);
  scene.add(knotMesh);

  const outMat = new THREE.ShaderMaterial({
    side: THREE.BackSide,
    vertexShader: `
      void main() {
        vec3 displaced = position + normalize(normal) * 0.038;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(displaced, 1.0);
      }
    `,
    fragmentShader: `
      void main() {
        gl_FragColor = vec4(0.07, 0.07, 0.09, 1.0);
      }
    `
  });
  outlineMesh = new THREE.Mesh(geo, outMat);
  scene.add(outlineMesh);

  clock = new THREE.Clock();
  draw2DRampPreview();

  const dom = renderer.domElement;
  dom.addEventListener('pointerdown', (e) => {
    isDragging = true;
    prevMouse = { x: e.clientX, y: e.clientY };
  });
  window.addEventListener('pointerup', () => {
    isDragging = false;
  });
  window.addEventListener('pointermove', (e) => {
    if (!isDragging) return;
    const dx = e.clientX - prevMouse.x;
    const dy = e.clientY - prevMouse.y;
    prevMouse = { x: e.clientX, y: e.clientY };
    camOrbit.theta -= dx * 0.008;
    camOrbit.phi = Math.max(-0.8, Math.min(0.85, camOrbit.phi + dy * 0.008));
    updateCameraOrbit();
  });

  const animate = () => {
    animId = requestAnimationFrame(animate);
    if (knotMesh && clock) {
      knotMesh.material.uniforms.uTime.value = clock.getElapsedTime();
    }
    renderer.render(scene, camera);
  };
  animate();
};

const handleResize = () => {
  if (!canvasContainer.value || !renderer || !camera) return;
  const width = canvasContainer.value.clientWidth;
  const height = 290;
  camera.aspect = width / height;
  camera.updateProjectionMatrix();
  renderer.setSize(width, height);
};

onMounted(() => {
  initThree();
  window.addEventListener('resize', handleResize);
});

onBeforeUnmount(() => {
  if (animId) cancelAnimationFrame(animId);
  window.removeEventListener('resize', handleResize);
  if (renderer) renderer.dispose();
});
</script>

<style scoped>
.technical-figure {
  border: 1px solid #d1d5db;
  border-radius: 4px;
  overflow: hidden;
  margin: 24px 0;
  background: #ffffff;
}

.figure-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 14px;
  background: #f9fafb;
  border-bottom: 1px solid #e5e7eb;
  flex-wrap: wrap;
  gap: 8px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  font-weight: 700;
  color: #111827;
  letter-spacing: 0.5px;
  background: #e5e7eb;
  padding: 2px 6px;
  border-radius: 2px;
}

.desc {
  font-size: 11.5px;
  color: #4b5563;
  font-weight: 600;
}

.viewport-hint {
  font-size: 10.5px;
  color: #6b7280;
  font-family: monospace;
}

.presets-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
  padding: 8px 14px;
  background: #f3f4f6;
  border-bottom: 1px solid #e5e7eb;
  flex-wrap: wrap;
}

.bar-group {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.preset-title {
  font-size: 11px;
  font-weight: 700;
  color: #374151;
}

.preset-buttons {
  display: flex;
  gap: 5px;
  flex-wrap: wrap;
}

.preset-btn {
  padding: 4px 9px;
  font-size: 11px;
  font-family: inherit;
  font-weight: 500;
  color: #374151;
  background: #ffffff;
  border: 1px solid #d1d5db;
  border-radius: 3px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.preset-btn:hover {
  background: #f3f4f6;
  border-color: #9ca3af;
  color: #111827;
}

.preset-btn.active {
  background: #111827;
  color: #ffffff;
  border-color: #111827;
}

.canvas-wrapper {
  width: 100%;
  height: 290px;
  cursor: grab;
}

.canvas-wrapper:active {
  cursor: grabbing;
}

.ramp-panel {
  padding: 10px 14px;
  background: #18181b;
  border-top: 1px solid #27272a;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.ramp-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
}

.ramp-label {
  font-size: 11px;
  color: #d4d4d8;
  min-width: 270px;
}

.ramp-label code {
  color: #f4f4f5;
  background: #27272a;
  padding: 1px 4px;
  border-radius: 2px;
}

.ramp-bar {
  flex: 1;
  height: 18px;
  border-radius: 3px;
  border: 1px solid #3f3f46;
  min-width: 200px;
}

.continuous-gradient {
  background: linear-gradient(to right, #09090b 0%, #71717a 50%, #fafafa 100%);
}

.controls-grid {
  padding: 14px;
  background: #ffffff;
  border-top: 1px solid #e5e7eb;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}

.control-card {
  display: flex;
  flex-direction: column;
  gap: 5px;
  padding: 10px;
  border: 1px solid #e5e7eb;
  border-radius: 3px;
  background: #fafafa;
}

.control-label {
  display: flex;
  justify-content: space-between;
  font-size: 11.5px;
  font-weight: 700;
  color: #111827;
}

.control-label code {
  color: #111827;
  font-size: 10.5px;
  background: #e5e7eb;
  padding: 1px 5px;
  border-radius: 2px;
}

.toggle-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.toggle-row input[type="range"] {
  flex: 1;
  accent-color: #111827;
  cursor: pointer;
}

.hints {
  font-size: 10px;
  color: #6b7280;
  line-height: 1.35;
}

.methodology-note {
  background: #f9fafb;
  border-top: 1px solid #e5e7eb;
  padding: 12px 14px;
  font-size: 11.5px;
  color: #374151;
  line-height: 1.5;
}

.methodology-note strong {
  color: #111827;
}

@media (max-width: 768px) {
  .controls-grid {
    grid-template-columns: 1fr;
  }
}
</style>
