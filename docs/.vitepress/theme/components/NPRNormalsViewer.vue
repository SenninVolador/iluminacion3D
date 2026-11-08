<template>
  <div class="technical-figure">
    <div class="figure-header">
      <div class="header-left">
        <span class="label">LABORATORIO INTERACTIVO 01</span>
        <span class="desc">Geometría de Normales (Face vs. Vertex), Normal Transfer e Inverted Hull en NPR</span>
      </div>
      <span class="viewport-hint">Arrastra en el visor para rotar la cámara</span>
    </div>

    <!-- BARRA DE MODELO Y PRESETS RÁPIDOS -->
    <div class="presets-bar">
      <div class="bar-group">
        <span class="preset-title">Modelo 3D:</span>
        <div class="preset-buttons">
          <button
            :class="['preset-btn', { active: currentModel === 'head' }]"
            @click="setModel('head')"
          >
            Rostro Estilizado (Anime / NPR)
          </button>
          <button
            :class="['preset-btn', { active: currentModel === 'cylinder' }]"
            @click="setModel('cylinder')"
          >
            Cilindro Biselado (Hard vs. Soft)
          </button>
          <button
            :class="['preset-btn', { active: currentModel === 'poly' }]"
            @click="setModel('poly')"
          >
            Esfera Facetada
          </button>
        </div>
      </div>

      <div class="bar-group">
        <span class="preset-title">Casos de Estudio:</span>
        <div class="preset-buttons">
          <button class="preset-btn preset-accent" @click="applyCase('dirty_toon')">
            1. Cel Shading Roto (Topología Cruda)
          </button>
          <button class="preset-btn preset-accent" @click="applyCase('clean_anime')">
            2. Normal Transfer (Estilo Guilty Gear)
          </button>
          <button class="preset-btn preset-accent" @click="applyCase('broken_hull')">
            3. Outline Roto vs. Sellado
          </button>
        </div>
      </div>
    </div>

    <!-- BARRA DE MODO DE NORMALES Y SHADER -->
    <div class="sub-bar">
      <div class="bar-group">
        <span class="preset-title">Cálculo de Normales:</span>
        <div class="preset-buttons">
          <button
            :class="['preset-btn', { active: normalMode === 'hard' }]"
            @click="setNormalMode('hard')"
          >
            Hard Edges (Split / Por Cara)
          </button>
          <button
            :class="['preset-btn', { active: normalMode === 'smooth' }]"
            @click="setNormalMode('smooth')"
          >
            Soft Edges (Vertex Promediado)
          </button>
          <button
            :class="['preset-btn', { active: normalMode === 'proxy' }]"
            @click="setNormalMode('proxy')"
          >
            Normal Transfer (Esfera Proxy)
          </button>
        </div>
      </div>

      <div class="bar-group">
        <span class="preset-title">Modo de Sombreado:</span>
        <div class="preset-buttons">
          <button
            :class="['preset-btn', { active: shadeMode === 'toon' }]"
            @click="setShadeMode('toon')"
          >
            Cel Shading (Step NPR)
          </button>
          <button
            :class="['preset-btn', { active: shadeMode === 'lit' }]"
            @click="setShadeMode('lit')"
          >
            Lambert Suave (PBR)
          </button>
          <button
            :class="['preset-btn', { active: shadeMode === 'rgb' }]"
            @click="setShadeMode('rgb')"
          >
            Debug Normales (RGB)
          </button>
        </div>
      </div>
    </div>

    <!-- VIEWPORT 3D + LEYENDA OVERLAY -->
    <div class="viewport-container">
      <div class="canvas-wrapper" ref="canvasContainer"></div>
      <div class="viewport-legend">
        <div class="legend-item" v-if="showFaceNormals">
          <span class="dot dot-face"></span>
          <span>Face Normal (1 por triángulo)</span>
        </div>
        <div class="legend-item" v-if="showVertexNormals">
          <span class="dot dot-vertex"></span>
          <span>Vertex Normal ({{ normalMode === 'hard' ? 'Separadas en esquinas' : normalMode === 'smooth' ? 'Unificadas / Promediadas' : 'Proyectadas desde Esfera' }})</span>
        </div>
        <div class="legend-item">
          <span class="dot dot-light"></span>
          <span>Dirección de Luz (Vector L)</span>
        </div>
      </div>
    </div>

    <!-- CONTROLES PARAMÉTRICOS -->
    <div class="controls-grid">
      <!-- 1. VISUALIZACIÓN DE VECTORES -->
      <div class="control-card">
        <div class="control-label">
          <span>1. Vectores Geométricos en Viewport:</span>
          <code>{{ (showFaceNormals || showVertexNormals) ? 'Visibles' : 'Ocultos' }}</code>
        </div>
        <div class="checkbox-group">
          <label class="check-item">
            <input type="checkbox" v-model="showFaceNormals" @change="rebuildHelpers" />
            <span>Mostrar <strong>Face Normals</strong> (Amarillo)</span>
          </label>
          <label class="check-item">
            <input type="checkbox" v-model="showVertexNormals" @change="rebuildHelpers" />
            <span>Mostrar <strong>Vertex Normals</strong> (Cian)</span>
          </label>
        </div>
        <div class="hints">
          <span>En Hard Edges, un mismo vértice dispara múltiples flechas cian divergentes.</span>
        </div>
      </div>

      <!-- 2. CONTORNO INVERTED HULL -->
      <div class="control-card">
        <div class="control-label">
          <span>2. Contorno Inverted Hull (Backface Extrusion):</span>
          <code>{{ outlineEnabled ? outlineWidth.toFixed(3) + ' u' : 'Desactivado' }}</code>
        </div>
        <div class="toggle-row">
          <input type="checkbox" v-model="outlineEnabled" @change="updateUniforms" />
          <input
            type="range"
            min="0.01"
            max="0.11"
            step="0.005"
            v-model.number="outlineWidth"
            :disabled="!outlineEnabled"
            @input="updateUniforms"
          />
        </div>
        <div class="checkbox-group" style="margin-top: 4px;">
          <label class="check-item">
            <input
              type="checkbox"
              v-model="forceSmoothOutline"
              :disabled="!outlineEnabled || normalMode !== 'hard'"
              @change="rebuildMesh"
            />
            <span>Reparar grietas del Outline usando Vertex Normals suavizadas en canal secundario</span>
          </label>
        </div>
      </div>

      <!-- 3. DIRECCIÓN DE LUZ (N · L) -->
      <div class="control-card">
        <div class="control-label">
          <span>3. Ángulo de la Luz Principal (Vector L):</span>
          <code>{{ Math.round((lightAngle * 180) / Math.PI) }}°</code>
        </div>
        <div class="toggle-row">
          <input
            type="range"
            min="-3.14"
            max="3.14"
            step="0.02"
            v-model.number="lightAngle"
            @input="onManualLightInput"
          />
        </div>
        <div class="checkbox-group" style="margin-top: 4px;">
          <label class="check-item">
            <input type="checkbox" v-model="autoRotateLight" />
            <span>Rotar luz automáticamente para inspeccionar el corte de sombra</span>
          </label>
        </div>
      </div>

      <!-- 4. UMBRAL Y TONOS DEL CEL SHADING -->
      <div class="control-card">
        <div class="control-label">
          <span>4. Corte de Sombra Toon (Threshold N · L):</span>
          <code>{{ toonThreshold.toFixed(2) }}</code>
        </div>
        <div class="toggle-row">
          <input
            type="range"
            min="-0.3"
            max="0.6"
            step="0.02"
            v-model.number="toonThreshold"
            :disabled="shadeMode === 'rgb'"
            @input="updateUniforms"
          />
        </div>
        <div class="hints">
          <span>Controla el punto exacto donde el producto punto N · L salta de luz a sombra.</span>
        </div>
      </div>
    </div>

    <!-- EXPLICACIÓN DINÁMICA SEGÚN ESTADO -->
    <div class="methodology-note">
      <template v-if="normalMode === 'hard'">
        <strong>Diagnóstico Técnico — Hard Edges (Split Normals):</strong>
        Cada triángulo conserva su propia orientación plana. En los bordes, el motor duplica los vértices y asigna <em>múltiples Vertex Normals</em> apuntando en direcciones distintas. Bajo <strong>Cel Shading</strong> el rostro se fragmenta en parches poligonales duros, y si activas el <strong>Inverted Hull Outline</strong> sin suavizar (desmarcando la casilla de reparación), verás cómo las caras extruidas se separan dejando brechas abiertas en las esquinas.
      </template>
      <template v-else-if="normalMode === 'smooth'">
        <strong>Diagnóstico Técnico — Soft Edges (Smooth Vertex Normals):</strong>
        Los vértices compartidos promedian las normales de las caras adyacentes en un solo vector continuo. Esto sella por completo las grietas del <strong>Inverted Hull Outline</strong> y suaviza cilindros o esferas. Sin embargo, en el <strong>Rostro Estilizado</strong> bajo <em>Cel Shading</em>, los pliegues topológicos de la nariz, pómulos y boca desvían las normales y generan sombras irregulares o "manchas" poco estéticas en la mejilla.
      </template>
      <template v-else>
        <strong>Diagnóstico Técnico — Normal Transfer (Esfera Proxy / Estilo Anime):</strong>
        La geometría 3D del rostro mantiene intactos su relieve de nariz, ojos y mentón, pero sus <strong>Vertex Normals han sido reemplazadas por las de un elipsoide limpio frontal</strong>. El cálculo <code>dot(N, L)</code> ignora las arrugas de los polígonos y dibuja un corte de sombra curvo y limpio a través de la cara, idéntico al dibujo 2D de <em>Guilty Gear Strive</em> o <em>Genshin Impact</em>.
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';

const canvasContainer = ref(null);

const currentModel = ref('head'); // 'head' | 'cylinder' | 'poly'
const normalMode = ref('proxy');  // 'hard' | 'smooth' | 'proxy'
const shadeMode = ref('toon');    // 'toon' | 'lit' | 'rgb'

const showFaceNormals = ref(false);
const showVertexNormals = ref(true);

const outlineEnabled = ref(true);
const outlineWidth = ref(0.045);
const forceSmoothOutline = ref(false);

const lightAngle = ref(0.75);
const autoRotateLight = ref(false);
const toonThreshold = ref(0.08);

let THREE = null;
let scene, camera, renderer, animId;
let mainMesh, outlineMesh, helperGroup, lightIndicatorGroup;
let isDragging = false;
let prevMouse = { x: 0, y: 0 };
let camOrbit = { theta: 0.25, phi: 0.2, radius: 3.7 };

// Desplazamiento procedural para esculpir un rostro estilizado (nariz, arcos superciliares, pómulos y mentón)
function sculptStylizedFace(x, y, z) {
  // Base ovoidal del cráneo/mandíbula
  let sx = x * 0.88;
  let sy = y * 1.12;
  let sz = z * 0.92;

  // Afinar la mandíbula inferior hacia el mentón
  if (sy < 0) {
    const jawTaper = Math.max(0.55, 1.0 + sy * 0.36);
    sx *= jawTaper;
    sz *= Math.max(0.75, 1.0 + sy * 0.18);
  }

  // Solo esculpir rasgos faciales en el hemisferio frontal (z > 0)
  if (z > 0.05) {
    // Puente y punta de la nariz (prominencia aguda en el eje X=0)
    const noseBridge = Math.exp(-(x * x) / 0.022) * Math.exp(-Math.pow(y - 0.02, 2) / 0.09);
    const noseTip = Math.exp(-(x * x) / 0.018) * Math.exp(-Math.pow(y + 0.12, 2) / 0.025);
    sz += (noseBridge * 0.26 + noseTip * 0.18);

    // Cuencas oculares (hundimiento claro a ambos lados de la nariz)
    const leftEye = Math.exp(-Math.pow(x - 0.30, 2) / 0.032) * Math.exp(-Math.pow(y - 0.18, 2) / 0.024);
    const rightEye = Math.exp(-Math.pow(x + 0.30, 2) / 0.032) * Math.exp(-Math.pow(y - 0.18, 2) / 0.024);
    sz -= (leftEye + rightEye) * 0.22;

    // Arco superciliar / cejas
    const brow = Math.exp(-(x * x) / 0.38) * Math.exp(-Math.pow(y - 0.36, 2) / 0.018);
    sz += brow * 0.13;

    // Pómulos (cheekbones) y surco nasogeniano (crea sombras sucias en Smooth normal estándar)
    const leftCheek = Math.exp(-Math.pow(x - 0.38, 2) / 0.035) * Math.exp(-Math.pow(y + 0.08, 2) / 0.03);
    const rightCheek = Math.exp(-Math.pow(x + 0.38, 2) / 0.035) * Math.exp(-Math.pow(y + 0.08, 2) / 0.03);
    sz += (leftCheek + rightCheek) * 0.14;

    // Hendidura bajo los pómulos
    const leftHollow = Math.exp(-Math.pow(x - 0.34, 2) / 0.03) * Math.exp(-Math.pow(y + 0.30, 2) / 0.025);
    const rightHollow = Math.exp(-Math.pow(x + 0.34, 2) / 0.03) * Math.exp(-Math.pow(y + 0.30, 2) / 0.025);
    sz -= (leftHollow + rightHollow) * 0.11;

    // Labios y surco del mentón
    const mouth = Math.exp(-(x * x) / 0.05) * Math.exp(-Math.pow(y + 0.36, 2) / 0.01);
    const underLip = Math.exp(-(x * x) / 0.05) * Math.exp(-Math.pow(y + 0.48, 2) / 0.012);
    const chin = Math.exp(-(x * x) / 0.045) * Math.exp(-Math.pow(y + 0.68, 2) / 0.025);
    sz += mouth * 0.09 - underLip * 0.10 + chin * 0.14;
  }

  return [sx, sy, sz];
}

// Construye una geometría indexada con costuras selladas y normales calculadas según modo
function createModelGeometry(modelType, mode) {
  let baseIndexedGeo;

  if (modelType === 'head') {
    baseIndexedGeo = new THREE.IcosahedronGeometry(1.0, 3);
    const pos = baseIndexedGeo.attributes.position;
    for (let i = 0; i < pos.count; i++) {
      const [nx, ny, nz] = sculptStylizedFace(pos.getX(i), pos.getY(i), pos.getZ(i));
      pos.setXYZ(i, nx, ny, nz);
    }
  } else if (modelType === 'cylinder') {
    baseIndexedGeo = new THREE.CylinderGeometry(0.85, 0.85, 1.65, 14, 1, false);
  } else {
    baseIndexedGeo = new THREE.IcosahedronGeometry(1.08, 1);
  }

  // Convertimos a non-indexed para poder controlar con exactitud matemática Face vs Smooth vs Proxy
  const geo = baseIndexedGeo.toNonIndexed();
  const posAttr = geo.attributes.position;
  const vertexCount = posAttr.count;

  // 1. Calcular Face Normals por cada triángulo
  const faceNormals = new Float32Array(vertexCount * 3);
  const vA = new THREE.Vector3();
  const vB = new THREE.Vector3();
  const vC = new THREE.Vector3();
  const cb = new THREE.Vector3();
  const ab = new THREE.Vector3();

  for (let i = 0; i < vertexCount; i += 3) {
    vA.fromBufferAttribute(posAttr, i);
    vB.fromBufferAttribute(posAttr, i + 1);
    vC.fromBufferAttribute(posAttr, i + 2);
    cb.subVectors(vC, vB);
    ab.subVectors(vA, vB);
    cb.cross(ab).normalize();

    for (let k = 0; k < 3; k++) {
      faceNormals[(i + k) * 3] = cb.x;
      faceNormals[(i + k) * 3 + 1] = cb.y;
      faceNormals[(i + k) * 3 + 2] = cb.z;
    }
  }

  // 2. Calcular Smooth Vertex Normals (promediando todos los vértices que comparten la misma posición espacial)
  const smoothMap = new Map();
  const keyOf = (x, y, z) => `${Math.round(x * 10000)},${Math.round(y * 10000)},${Math.round(z * 10000)}`;

  for (let i = 0; i < vertexCount; i++) {
    const k = keyOf(posAttr.getX(i), posAttr.getY(i), posAttr.getZ(i));
    if (!smoothMap.has(k)) {
      smoothMap.set(k, new THREE.Vector3(0, 0, 0));
    }
    smoothMap.get(k).add(new THREE.Vector3(
      faceNormals[i * 3],
      faceNormals[i * 3 + 1],
      faceNormals[i * 3 + 2]
    ));
  }

  const smoothNormals = new Float32Array(vertexCount * 3);
  for (let i = 0; i < vertexCount; i++) {
    const k = keyOf(posAttr.getX(i), posAttr.getY(i), posAttr.getZ(i));
    const avg = smoothMap.get(k).clone().normalize();
    smoothNormals[i * 3] = avg.x;
    smoothNormals[i * 3 + 1] = avg.y;
    smoothNormals[i * 3 + 2] = avg.z;
  }

  // 3. Calcular Proxy Sphere / Normal Transfer (proyección desde un elipsoide frontal limpio)
  const proxyNormals = new Float32Array(vertexCount * 3);
  const pVec = new THREE.Vector3();
  for (let i = 0; i < vertexCount; i++) {
    pVec.set(
      posAttr.getX(i) * 1.15,
      posAttr.getY(i) * 0.85,
      posAttr.getZ(i) + 0.35 // Sesgo frontal tipo anime para aplanar sutilmente el corte en mejillas
    ).normalize();
    proxyNormals[i * 3] = pVec.x;
    proxyNormals[i * 3 + 1] = pVec.y;
    proxyNormals[i * 3 + 2] = pVec.z;
  }

  // Seleccionar el buffer activo según normalMode
  const activeNormals =
    mode === 'hard' ? faceNormals :
    mode === 'smooth' ? smoothNormals :
    proxyNormals;

  geo.setAttribute('normal', new THREE.BufferAttribute(activeNormals, 3));
  geo.setAttribute('aSmoothNormal', new THREE.BufferAttribute(smoothNormals, 3));
  geo.userData = { faceNormals, smoothNormals, proxyNormals };

  return geo;
}

function getLightDirectionVector() {
  if (!THREE) return null;
  return new THREE.Vector3(
    Math.sin(lightAngle.value) * 0.9,
    0.32,
    Math.cos(lightAngle.value) * 0.9
  ).normalize();
}

function buildShaders() {
  const lightDir = getLightDirectionVector();

  const mainMaterial = new THREE.ShaderMaterial({
    uniforms: {
      uLightDir: { value: lightDir },
      uShadeMode: { value: shadeMode.value === 'toon' ? 0 : shadeMode.value === 'lit' ? 1 : 2 },
      uThreshold: { value: toonThreshold.value }
    },
    vertexShader: `
      varying vec3 vNormal;
      varying vec3 vViewDir;
      void main() {
        // Transformar normal al espacio de mundo (sin escala no uniforme)
        vNormal = normalize(mat3(modelMatrix) * normal);
        vec4 worldPos = modelMatrix * vec4(position, 1.0);
        vViewDir = normalize(cameraPosition - worldPos.xyz);
        gl_Position = projectionMatrix * viewMatrix * worldPos;
      }
    `,
    fragmentShader: `
      uniform vec3 uLightDir;
      uniform int uShadeMode;
      uniform float uThreshold;
      varying vec3 vNormal;
      varying vec3 vViewDir;

      void main() {
        vec3 N = normalize(vNormal);
        vec3 L = normalize(uLightDir);
        vec3 V = normalize(vViewDir);

        // Modo 2: Debug RGB de Normales
        if (uShadeMode == 2) {
          vec3 rgbNorm = N * 0.5 + 0.5;
          gl_FragColor = vec4(rgbNorm, 1.0);
          return;
        }

        float NdotL = dot(N, L);

        // Modo 1: Sombreado Suave Lambert PBR
        if (uShadeMode == 1) {
          float diff = clamp(NdotL * 0.5 + 0.5, 0.0, 1.0);
          vec3 shadowCol = vec3(0.27, 0.25, 0.36);
          vec3 litCol = vec3(0.95, 0.87, 0.82);
          vec3 col = mix(shadowCol, litCol, smoothstep(0.15, 0.85, diff));
          gl_FragColor = vec4(col, 1.0);
          return;
        }

        // Modo 0: Cel Shading NPR (2 tonos + Rim estilizado)
        float celCut = smoothstep(uThreshold - 0.015, uThreshold + 0.015, NdotL);
        vec3 animeShadow = vec3(0.42, 0.34, 0.44);
        vec3 animeLit = vec3(0.98, 0.90, 0.85);
        vec3 finalCol = mix(animeShadow, animeLit, celCut);

        // Pequeño toque de Rim Light estilizado en la zona iluminada
        float fresnel = pow(1.0 - max(dot(N, V), 0.0), 3.8);
        float rimMask = step(0.65, fresnel) * celCut;
        finalCol += vec3(0.18, 0.20, 0.25) * rimMask;

        gl_FragColor = vec4(finalCol, 1.0);
      }
    `
  });

  const outlineMaterial = new THREE.ShaderMaterial({
    side: THREE.BackSide,
    uniforms: {
      uOutlineWidth: { value: outlineWidth.value },
      uUseSmoothNormal: { value: (normalMode.value === 'hard' && forceSmoothOutline.value) ? 1.0 : 0.0 }
    },
    vertexShader: `
      attribute vec3 aSmoothNormal;
      uniform float uOutlineWidth;
      uniform float uUseSmoothNormal;
      void main() {
        vec3 extrudeDir = normalize(mix(normal, aSmoothNormal, uUseSmoothNormal));
        vec3 displaced = position + extrudeDir * uOutlineWidth;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(displaced, 1.0);
      }
    `,
    fragmentShader: `
      void main() {
        gl_FragColor = vec4(0.07, 0.07, 0.09, 1.0);
      }
    `
  });

  return { mainMaterial, outlineMaterial };
}

function rebuildHelpers() {
  if (!THREE || !scene || !mainMesh) return;

  if (helperGroup) {
    scene.remove(helperGroup);
  }
  helperGroup = new THREE.Group();

  const geo = mainMesh.geometry;
  const pos = geo.attributes.position;
  const norm = geo.attributes.normal;
  const count = pos.count;

  // 1. Flechas de Face Normals (amarillas, 1 por centro de triángulo)
  if (showFaceNormals.value) {
    const facePts = [];
    const faceNorms = geo.userData.faceNormals;
    const stride = currentModel.value === 'head' ? 9 : 3; // Submuestreo en el rostro para lectura limpia

    for (let i = 0; i < count; i += stride) {
      const cx = (pos.getX(i) + pos.getX(i + 1) + pos.getX(i + 2)) / 3;
      const cy = (pos.getY(i) + pos.getY(i + 1) + pos.getY(i + 2)) / 3;
      const cz = (pos.getZ(i) + pos.getZ(i + 1) + pos.getZ(i + 2)) / 3;

      const nx = faceNorms[i * 3];
      const ny = faceNorms[i * 3 + 1];
      const nz = faceNorms[i * 3 + 2];

      const len = 0.19;
      facePts.push(cx, cy, cz, cx + nx * len, cy + ny * len, cz + nz * len);
    }

    const lineGeo = new THREE.BufferGeometry();
    lineGeo.setAttribute('position', new THREE.Float32BufferAttribute(facePts, 3));
    const lineMat = new THREE.LineBasicMaterial({ color: 0xfacc15 });
    helperGroup.add(new THREE.LineSegments(lineGeo, lineMat));
  }

  // 2. Flechas de Vertex Normals (cian, desde cada vértice)
  if (showVertexNormals.value) {
    const vertPts = [];
    const seenPairs = new Set();

    for (let i = 0; i < count; i++) {
      const vx = pos.getX(i);
      const vy = pos.getY(i);
      const vz = pos.getZ(i);
      const nx = norm.getX(i);
      const ny = norm.getY(i);
      const nz = norm.getZ(i);

      // En rostro denso filtramos algunos vértices para evitar saturar la vista
      if (currentModel.value === 'head' && (Math.abs(vx) * 100 + Math.abs(vy) * 100) % 3 > 1.2) {
        continue;
      }

      // Evitar dibujar dos veces exactamente la misma flecha en el mismo punto
      const key = `${Math.round(vx * 100)},${Math.round(vy * 100)},${Math.round(vz * 100)}_${Math.round(nx * 50)},${Math.round(ny * 50)},${Math.round(nz * 50)}`;
      if (seenPairs.has(key)) continue;
      seenPairs.add(key);

      const len = 0.22;
      vertPts.push(vx, vy, vz, vx + nx * len, vy + ny * len, vz + nz * len);
    }

    const vGeo = new THREE.BufferGeometry();
    vGeo.setAttribute('position', new THREE.Float32BufferAttribute(vertPts, 3));
    const vMat = new THREE.LineBasicMaterial({ color: 0x38bdf8 });
    helperGroup.add(new THREE.LineSegments(vGeo, vMat));
  }

  scene.add(helperGroup);
}

function updateLightIndicator() {
  if (!THREE || !scene) return;
  if (!lightIndicatorGroup) {
    lightIndicatorGroup = new THREE.Group();
    scene.add(lightIndicatorGroup);
  }
  lightIndicatorGroup.clear();

  const dir = getLightDirectionVector();
  const origin = dir.clone().multiplyScalar(2.1);
  const target = dir.clone().multiplyScalar(1.35);

  const lineGeo = new THREE.BufferGeometry().setFromPoints([origin, target]);
  const lineMat = new THREE.LineBasicMaterial({ color: 0xf97316 });
  lightIndicatorGroup.add(new THREE.Line(lineGeo, lineMat));

  const bulbGeo = new THREE.SphereGeometry(0.06, 12, 12);
  const bulbMat = new THREE.MeshBasicMaterial({ color: 0xf97316 });
  const bulb = new THREE.Mesh(bulbGeo, bulbMat);
  bulb.position.copy(origin);
  lightIndicatorGroup.add(bulb);
}

function rebuildMesh() {
  if (!THREE || !scene) return;

  if (mainMesh) {
    scene.remove(mainMesh);
    mainMesh.geometry.dispose();
    mainMesh.material.dispose();
  }
  if (outlineMesh) {
    scene.remove(outlineMesh);
    outlineMesh.material.dispose();
  }

  const geo = createModelGeometry(currentModel.value, normalMode.value);
  const { mainMaterial, outlineMaterial } = buildShaders();

  mainMesh = new THREE.Mesh(geo, mainMaterial);
  scene.add(mainMesh);

  outlineMesh = new THREE.Mesh(geo, outlineMaterial);
  outlineMesh.visible = outlineEnabled.value;
  scene.add(outlineMesh);

  rebuildHelpers();
  updateLightIndicator();
}

function updateUniforms() {
  if (!mainMesh || !outlineMesh) return;
  mainMesh.material.uniforms.uLightDir.value.copy(getLightDirectionVector());
  mainMesh.material.uniforms.uShadeMode.value =
    shadeMode.value === 'toon' ? 0 : shadeMode.value === 'lit' ? 1 : 2;
  mainMesh.material.uniforms.uThreshold.value = toonThreshold.value;

  outlineMesh.visible = outlineEnabled.value;
  outlineMesh.material.uniforms.uOutlineWidth.value = outlineWidth.value;
  outlineMesh.material.uniforms.uUseSmoothNormal.value =
    normalMode.value === 'hard' && forceSmoothOutline.value ? 1.0 : 0.0;

  updateLightIndicator();
}

function setModel(modelKey) {
  currentModel.value = modelKey;
  rebuildMesh();
}

function setNormalMode(modeKey) {
  normalMode.value = modeKey;
  rebuildMesh();
}

function setShadeMode(modeKey) {
  shadeMode.value = modeKey;
  updateUniforms();
}

function applyCase(caseKey) {
  if (caseKey === 'dirty_toon') {
    currentModel.value = 'head';
    normalMode.value = 'smooth';
    shadeMode.value = 'toon';
    showFaceNormals.value = false;
    showVertexNormals.value = true;
    outlineEnabled.value = true;
    outlineWidth.value = 0.04;
    lightAngle.value = 0.72;
    rebuildMesh();
  } else if (caseKey === 'clean_anime') {
    currentModel.value = 'head';
    normalMode.value = 'proxy';
    shadeMode.value = 'toon';
    showFaceNormals.value = false;
    showVertexNormals.value = true;
    outlineEnabled.value = true;
    outlineWidth.value = 0.04;
    lightAngle.value = 0.72;
    rebuildMesh();
  } else if (caseKey === 'broken_hull') {
    currentModel.value = 'cylinder';
    normalMode.value = 'hard';
    shadeMode.value = 'toon';
    showFaceNormals.value = true;
    showVertexNormals.value = true;
    outlineEnabled.value = true;
    outlineWidth.value = 0.085;
    forceSmoothOutline.value = false;
    rebuildMesh();
  }
}

function onManualLightInput() {
  autoRotateLight.value = false;
  updateUniforms();
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
  const height = 340;

  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x141418);

  camera = new THREE.PerspectiveCamera(38, width / height, 0.1, 100);
  updateCameraOrbit();

  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(width, height);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  container.innerHTML = '';
  container.appendChild(renderer.domElement);

  // Grilla sutil de piso para referencia espacial
  const grid = new THREE.GridHelper(5, 10, 0x27272a, 0x1f1f23);
  grid.position.y = -1.25;
  scene.add(grid);

  rebuildMesh();

  // Eventos de órbita con mouse / touch
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
    camOrbit.phi = Math.max(-0.8, Math.min(0.9, camOrbit.phi + dy * 0.008));
    updateCameraOrbit();
  });

  const animate = () => {
    animId = requestAnimationFrame(animate);
    if (autoRotateLight.value) {
      lightAngle.value += 0.015;
      if (lightAngle.value > 3.14) lightAngle.value = -3.14;
      updateUniforms();
    }
    renderer.render(scene, camera);
  };
  animate();
};

const handleResize = () => {
  if (!canvasContainer.value || !renderer || !camera) return;
  const width = canvasContainer.value.clientWidth;
  const height = 340;
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

.presets-bar,
.sub-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  padding: 8px 14px;
  background: #f3f4f6;
  border-bottom: 1px solid #e5e7eb;
  flex-wrap: wrap;
}

.sub-bar {
  background: #f9fafb;
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

.preset-btn.preset-accent {
  border-color: #9ca3af;
  font-weight: 600;
}

.viewport-container {
  position: relative;
  width: 100%;
}

.canvas-wrapper {
  width: 100%;
  height: 340px;
  cursor: grab;
}

.canvas-wrapper:active {
  cursor: grabbing;
}

.viewport-legend {
  position: absolute;
  bottom: 10px;
  left: 12px;
  display: flex;
  gap: 14px;
  background: rgba(17, 24, 39, 0.82);
  padding: 5px 10px;
  border-radius: 3px;
  border: 1px solid rgba(255, 255, 255, 0.12);
  pointer-events: none;
  flex-wrap: wrap;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 10.5px;
  color: #e5e7eb;
  font-family: monospace;
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  display: inline-block;
}

.dot-face {
  background: #facc15;
}

.dot-vertex {
  background: #38bdf8;
}

.dot-light {
  background: #f97316;
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

.toggle-row input[type="checkbox"],
.check-item input[type="checkbox"] {
  accent-color: #111827;
  width: 14px;
  height: 14px;
  cursor: pointer;
}

.toggle-row input[type="range"] {
  flex: 1;
  accent-color: #111827;
  cursor: pointer;
}

.checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.check-item {
  display: flex;
  align-items: center;
  gap: 7px;
  font-size: 11px;
  color: #374151;
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
