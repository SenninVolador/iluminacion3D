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
            :class="['preset-btn', { active: currentModel === 'head' && showHair }]"
            @click="setModel('head', true)"
          >
            Personaje Anime (Con Cabello)
          </button>
          <button
            :class="['preset-btn', { active: currentModel === 'head' && !showHair }]"
            @click="setModel('head', false)"
          >
            Cabeza Anime (Sin Cabello / Malla Facial)
          </button>
          <button
            :class="['preset-btn', { active: currentModel === 'cylinder' }]"
            @click="setModel('cylinder', false)"
          >
            Cilindro Biselado (Hard vs. Soft)
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
            Soft Edges (Topología sin Transferir)
          </button>
          <button
            :class="['preset-btn', { active: normalMode === 'proxy' }]"
            @click="setNormalMode('proxy')"
          >
            Normal Transfer (Esfera Proxy Anime)
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
          <span>Vertex Normal ({{ normalMode === 'hard' ? 'Separadas en esquinas' : normalMode === 'smooth' ? 'Topológicas con pliegues' : 'Transferidas desde Esfera' }})</span>
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
          <span>Activa "Cabeza Anime (Sin Cabello)" para inspeccionar con claridad los vectores sobre la cara.</span>
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
            min="0.008"
            max="0.065"
            step="0.002"
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
            min="-0.35"
            max="0.55"
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
        Cada triángulo de la malla conserva su propia orientación plana perpendicular. En los bordes, el motor duplica los vértices y asigna <em>múltiples Vertex Normals</em> divergentes. Bajo <strong>Cel Shading</strong> el rostro anime queda facetado en polígonos duros, y en el <strong>Cilindro Biselado</strong> el contorno <em>Inverted Hull</em> se abre dejando grietas vacías en las esquinas.
      </template>
      <template v-else-if="normalMode === 'smooth'">
        <strong>Diagnóstico Técnico — Soft Edges (Topología sin Transferir):</strong>
        Las caras vecinas promedian sus normales automáticamente según la geometría real. Aunque los polígonos ya no se ven facetados, los hundimientos anatómicos de los pómulos, surco nasogeniano, comisura labial y puente nasal desvían las normales y generan <strong>manchas e islas de sombra irregulares en la mejilla</strong> bajo el corte duro del <em>Cel Shading</em>.
      </template>
      <template v-else>
        <strong>Diagnóstico Técnico — Normal Transfer (Esfera Proxy / Estilo Anime):</strong>
        La malla 3D del personaje mantiene intactos su nariz, boca, ojos y mejillas, pero las <strong>Vertex Normals de la piel facial han sido transferidas desde un elipsoide limpio frontal</strong>. El cálculo <code>dot(N, L)</code> ignora las hendiduras topológicas y dibuja un corte de sombra limpio y continuo de oreja a mentón, idéntico al estándar de <em>Guilty Gear Strive</em>, <em>Genshin Impact</em> y <em>VRoid</em>.
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { withBase } from 'vitepress';

const canvasContainer = ref(null);

const currentModel = ref('head'); // 'head' | 'cylinder'
const showHair = ref(true);
const normalMode = ref('proxy');  // 'hard' | 'smooth' | 'proxy'
const shadeMode = ref('toon');    // 'toon' | 'lit' | 'rgb'

const showFaceNormals = ref(false);
const showVertexNormals = ref(false);

const outlineEnabled = ref(true);
const outlineWidth = ref(0.022);
const forceSmoothOutline = ref(false);

const lightAngle = ref(0.68);
const autoRotateLight = ref(false);
const toonThreshold = ref(0.04);

let THREE = null;
let scene, camera, renderer, animId;
let mainMesh, outlineMesh, helperGroup, lightIndicatorGroup;
let cachedAnimeData = null;
let isDragging = false;
let prevMouse = { x: 0, y: 0 };
let camOrbit = { theta: 0.22, phi: 0.12, radius: 3.1 };

async function loadAnimeBinary() {
  if (cachedAnimeData) return cachedAnimeData;
  const resp = await fetch(withBase('/models/anime_bust.bin'));
  const buf = await resp.arrayBuffer();
  const header = new Uint32Array(buf, 0, 4);
  const [hVerts, hTris, hrVerts, hrTris] = header;

  let offset = 16;
  const hPos = new Float32Array(buf, offset, hVerts * 3);
  offset += hVerts * 3 * 4;
  const hRgba = new Uint8Array(buf, offset, hVerts * 4);
  offset += hVerts * 4;
  const hTriIdx = new Uint32Array(buf, offset, hTris * 3);
  offset += hTris * 3 * 4;

  const hrPos = new Float32Array(buf, offset, hrVerts * 3);
  offset += hrVerts * 3 * 4;
  const hrRgba = new Uint8Array(buf, offset, hrVerts * 4);
  offset += hrVerts * 4;
  const hrTriIdx = new Uint32Array(buf, offset, hrTris * 3);

  cachedAnimeData = { hVerts, hTris, hPos, hRgba, hTriIdx, hrVerts, hrTris, hrPos, hrRgba, hrTriIdx };
  return cachedAnimeData;
}

function buildAnimeBufferGeometry(data, includeHair, mode) {
  const totalTris = data.hTris + (includeHair ? data.hrTris : 0);
  const vCount = totalTris * 3;

  const posArr = new Float32Array(vCount * 3);
  const colArr = new Float32Array(vCount * 3);
  const partArr = new Float32Array(vCount);

  let ptr = 0;

  const appendSection = (pos, rgba, triIdx, triCount) => {
    for (let t = 0; t < triCount; t++) {
      for (let k = 0; k < 3; k++) {
        const vi = triIdx[t * 3 + k];
        posArr[ptr * 3] = pos[vi * 3];
        posArr[ptr * 3 + 1] = pos[vi * 3 + 1];
        posArr[ptr * 3 + 2] = pos[vi * 3 + 2];

        const pid = rgba[vi * 4 + 3];
        // Si el cabello está oculto, el casco craneal (pid == 4) toma color piel para ver el cráneo limpio
        if (!includeHair && pid === 4) {
          colArr[ptr * 3] = 0.98;
          colArr[ptr * 3 + 1] = 0.89;
          colArr[ptr * 3 + 2] = 0.84;
        } else {
          colArr[ptr * 3] = rgba[vi * 4] / 255.0;
          colArr[ptr * 3 + 1] = rgba[vi * 4 + 1] / 255.0;
          colArr[ptr * 3 + 2] = rgba[vi * 4 + 2] / 255.0;
        }
        partArr[ptr] = pid;
        ptr++;
      }
    }
  };

  appendSection(data.hPos, data.hRgba, data.hTriIdx, data.hTris);
  if (includeHair) {
    appendSection(data.hrPos, data.hrRgba, data.hrTriIdx, data.hrTris);
  }

  // 1. Calcular Face Normals por cada triángulo
  const faceNormals = new Float32Array(vCount * 3);
  const vA = new THREE.Vector3();
  const vB = new THREE.Vector3();
  const vC = new THREE.Vector3();
  const cb = new THREE.Vector3();
  const ab = new THREE.Vector3();

  for (let i = 0; i < vCount; i += 3) {
    vA.set(posArr[i * 3], posArr[i * 3 + 1], posArr[i * 3 + 2]);
    vB.set(posArr[(i + 1) * 3], posArr[(i + 1) * 3 + 1], posArr[(i + 1) * 3 + 2]);
    vC.set(posArr[(i + 2) * 3], posArr[(i + 2) * 3 + 1], posArr[(i + 2) * 3 + 2]);
    cb.subVectors(vC, vB);
    ab.subVectors(vA, vB);
    cb.cross(ab).normalize();
    for (let k = 0; k < 3; k++) {
      faceNormals[(i + k) * 3] = cb.x;
      faceNormals[(i + k) * 3 + 1] = cb.y;
      faceNormals[(i + k) * 3 + 2] = cb.z;
    }
  }

  // 2. Calcular Smooth Normals promediando por posición espacial
  const smoothMap = new Map();
  const keyOf = (x, y, z) => `${Math.round(x * 2000)},${Math.round(y * 2000)},${Math.round(z * 2000)}`;

  for (let i = 0; i < vCount; i++) {
    const k = keyOf(posArr[i * 3], posArr[i * 3 + 1], posArr[i * 3 + 2]);
    let acc = smoothMap.get(k);
    if (!acc) {
      acc = new THREE.Vector3(0, 0, 0);
      smoothMap.set(k, acc);
    }
    acc.x += faceNormals[i * 3];
    acc.y += faceNormals[i * 3 + 1];
    acc.z += faceNormals[i * 3 + 2];
  }

  const rawSmoothNormals = new Float32Array(vCount * 3);
  const topoNormals = new Float32Array(vCount * 3);
  const proxyNormals = new Float32Array(vCount * 3);
  const pVec = new THREE.Vector3();

  for (let i = 0; i < vCount; i++) {
    const x = posArr[i * 3];
    const y = posArr[i * 3 + 1];
    const z = posArr[i * 3 + 2];
    const pid = partArr[i];

    const k = keyOf(x, y, z);
    const avg = smoothMap.get(k);
    pVec.copy(avg).normalize();

    rawSmoothNormals[i * 3] = pVec.x;
    rawSmoothNormals[i * 3 + 1] = pVec.y;
    rawSmoothNormals[i * 3 + 2] = pVec.z;

    // En modo "Smooth Topológico sin Transferir", los rasgos faciales (surco nasogeniano, pómulo, cuenca ocular y comisura)
    // desvían la normal provocando las clásicas manchas de sombra en Cel Shading:
    if (pid === 0 && z > 0.1) {
      const tVec = pVec.clone();
      // Hundimiento bajo el pómulo / mejilla media y surco nasogeniano
      const cheekHollow =
        (Math.exp(-Math.pow(Math.abs(x) - 0.34, 2) / 0.018) * Math.exp(-Math.pow(y + 0.08, 2) / 0.022)) -
        (Math.exp(-Math.pow(Math.abs(x) - 0.20, 2) / 0.012) * Math.exp(-Math.pow(y + 0.18, 2) / 0.018));
      const mouthCrease =
        Math.exp(-Math.pow(Math.abs(x) - 0.15, 2) / 0.008) * Math.exp(-Math.pow(y + 0.30, 2) / 0.010);
      const noseSide =
        Math.exp(-Math.pow(Math.abs(x) - 0.09, 2) / 0.005) * Math.exp(-Math.pow(y - 0.02, 2) / 0.018);

      const signX = x >= 0 ? 1.0 : -1.0;
      tVec.x -= signX * (cheekHollow * 0.65 + mouthCrease * 0.55 + noseSide * 0.60);
      tVec.y -= ( Math.abs(cheekHollow) * 0.35 + mouthCrease * 0.45 );
      tVec.normalize();
      topoNormals[i * 3] = tVec.x;
      topoNormals[i * 3 + 1] = tVec.y;
      topoNormals[i * 3 + 2] = tVec.z;
    } else {
      topoNormals[i * 3] = pVec.x;
      topoNormals[i * 3 + 1] = pVec.y;
      topoNormals[i * 3 + 2] = pVec.z;
    }

    // En modo "Proxy / Normal Transfer", la cara (pid === 0 o 4) recibe las normales de un elipsoide frontal limpio:
    if (pid === 0 || pid === 4) {
      pVec.set(x * 1.15, (y - 0.12) * 0.72, z + 0.52).normalize();
      proxyNormals[i * 3] = pVec.x;
      proxyNormals[i * 3 + 1] = pVec.y;
      proxyNormals[i * 3 + 2] = pVec.z;
    } else {
      proxyNormals[i * 3] = rawSmoothNormals[i * 3];
      proxyNormals[i * 3 + 1] = rawSmoothNormals[i * 3 + 1];
      proxyNormals[i * 3 + 2] = rawSmoothNormals[i * 3 + 2];
    }
  }

  const activeNormals =
    mode === 'hard' ? faceNormals :
    mode === 'smooth' ? topoNormals :
    proxyNormals;

  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(posArr, 3));
  geo.setAttribute('normal', new THREE.BufferAttribute(activeNormals, 3));
  geo.setAttribute('aSmoothNormal', new THREE.BufferAttribute(rawSmoothNormals, 3));
  geo.setAttribute('aColor', new THREE.BufferAttribute(colArr, 3));
  geo.setAttribute('aPartId', new THREE.BufferAttribute(partArr, 1));
  geo.userData = { faceNormals, smoothNormals: rawSmoothNormals, proxyNormals };
  return geo;
}

function buildCylinderGeometry(mode) {
  const base = new THREE.CylinderGeometry(0.78, 0.78, 1.55, 14, 1, false).toNonIndexed();
  const posAttr = base.attributes.position;
  const vCount = posAttr.count;

  const faceNormals = new Float32Array(vCount * 3);
  const colArr = new Float32Array(vCount * 3);
  const partArr = new Float32Array(vCount);

  const vA = new THREE.Vector3();
  const vB = new THREE.Vector3();
  const vC = new THREE.Vector3();
  const cb = new THREE.Vector3();
  const ab = new THREE.Vector3();

  for (let i = 0; i < vCount; i += 3) {
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
      colArr[(i + k) * 3] = 0.90;
      colArr[(i + k) * 3 + 1] = 0.86;
      colArr[(i + k) * 3 + 2] = 0.82;
      partArr[i + k] = 0;
    }
  }

  const smoothMap = new Map();
  const keyOf = (x, y, z) => `${Math.round(x * 1000)},${Math.round(y * 1000)},${Math.round(z * 1000)}`;
  for (let i = 0; i < vCount; i++) {
    const k = keyOf(posAttr.getX(i), posAttr.getY(i), posAttr.getZ(i));
    if (!smoothMap.has(k)) smoothMap.set(k, new THREE.Vector3());
    smoothMap.get(k).add(new THREE.Vector3(faceNormals[i * 3], faceNormals[i * 3 + 1], faceNormals[i * 3 + 2]));
  }

  const smoothNormals = new Float32Array(vCount * 3);
  const proxyNormals = new Float32Array(vCount * 3);
  for (let i = 0; i < vCount; i++) {
    const k = keyOf(posAttr.getX(i), posAttr.getY(i), posAttr.getZ(i));
    const avg = smoothMap.get(k).clone().normalize();
    smoothNormals[i * 3] = avg.x;
    smoothNormals[i * 3 + 1] = avg.y;
    smoothNormals[i * 3 + 2] = avg.z;

    const sph = new THREE.Vector3(posAttr.getX(i), posAttr.getY(i) * 0.4, posAttr.getZ(i)).normalize();
    proxyNormals[i * 3] = sph.x;
    proxyNormals[i * 3 + 1] = sph.y;
    proxyNormals[i * 3 + 2] = sph.z;
  }

  const active = mode === 'hard' ? faceNormals : mode === 'smooth' ? smoothNormals : proxyNormals;
  base.setAttribute('normal', new THREE.BufferAttribute(active, 3));
  base.setAttribute('aSmoothNormal', new THREE.BufferAttribute(smoothNormals, 3));
  base.setAttribute('aColor', new THREE.BufferAttribute(colArr, 3));
  base.setAttribute('aPartId', new THREE.BufferAttribute(partArr, 1));
  base.userData = { faceNormals, smoothNormals, proxyNormals };
  return base;
}

function getLightDirectionVector() {
  if (!THREE) return null;
  return new THREE.Vector3(
    Math.sin(lightAngle.value) * 0.92,
    0.26,
    Math.cos(lightAngle.value) * 0.92
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
      attribute vec3 aColor;
      attribute float aPartId;
      varying vec3 vNormal;
      varying vec3 vViewDir;
      varying vec3 vColor;
      varying float vPartId;
      void main() {
        vColor = aColor;
        vPartId = aPartId;
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
      varying vec3 vColor;
      varying float vPartId;

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

        // Ojos, cejas y pestañas mantienen alta legibilidad tipo anime
        if (vPartId > 0.5 && vPartId < 1.5) {
          gl_FragColor = vec4(vColor, 1.0);
          return;
        }

        float NdotL = dot(N, L);

        // Color de sombra estilizado (multiplicando el color base por un tono frío/malva anime)
        vec3 shadowTint = vec3(0.68, 0.57, 0.69);
        vec3 shadowCol = vColor * shadowTint;
        vec3 litCol = vColor;

        // Modo 1: Sombreado Suave Lambert PBR
        if (uShadeMode == 1) {
          float diff = clamp(NdotL * 0.5 + 0.5, 0.0, 1.0);
          vec3 col = mix(shadowCol, litCol, smoothstep(0.12, 0.88, diff));
          gl_FragColor = vec4(col, 1.0);
          return;
        }

        // Modo 0: Cel Shading NPR (Corte nítido Step + Rim Light en cabello/bordes)
        float celCut = smoothstep(uThreshold - 0.015, uThreshold + 0.015, NdotL);
        vec3 finalCol = mix(shadowCol, litCol, celCut);

        float fresnel = pow(1.0 - max(dot(N, V), 0.0), 3.6);
        float rimMask = step(0.68, fresnel) * celCut;
        finalCol += vec3(0.14, 0.16, 0.22) * rimMask;

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
      attribute float aPartId;
      uniform float uOutlineWidth;
      uniform float uUseSmoothNormal;
      void main() {
        // No extruir ojos/pestañas (aPartId == 1) para mantener limpios los rasgos internos
        float partMask = (aPartId > 0.5 && aPartId < 1.5) ? 0.0 : 1.0;
        vec3 extrudeDir = normalize(mix(normal, aSmoothNormal, uUseSmoothNormal));
        vec3 displaced = position + extrudeDir * (uOutlineWidth * partMask);
        gl_Position = projectionMatrix * modelViewMatrix * vec4(displaced, 1.0);
      }
    `,
    fragmentShader: `
      void main() {
        gl_FragColor = vec4(0.08, 0.07, 0.10, 1.0);
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

  // Submuestreo inteligente en el modelo anime para que las flechas sean limpias y legibles
  const triStep = currentModel.value === 'head' ? 45 : 3;

  if (showFaceNormals.value) {
    const facePts = [];
    const faceNorms = geo.userData.faceNormals;

    for (let i = 0; i < count; i += triStep) {
      const cx = (pos.getX(i) + pos.getX(i + 1) + pos.getX(i + 2)) / 3;
      const cy = (pos.getY(i) + pos.getY(i + 1) + pos.getY(i + 2)) / 3;
      const cz = (pos.getZ(i) + pos.getZ(i + 1) + pos.getZ(i + 2)) / 3;

      const nx = faceNorms[i * 3];
      const ny = faceNorms[i * 3 + 1];
      const nz = faceNorms[i * 3 + 2];

      const len = currentModel.value === 'head' ? 0.14 : 0.20;
      facePts.push(cx, cy, cz, cx + nx * len, cy + ny * len, cz + nz * len);
    }

    const lineGeo = new THREE.BufferGeometry();
    lineGeo.setAttribute('position', new THREE.Float32BufferAttribute(facePts, 3));
    const lineMat = new THREE.LineBasicMaterial({ color: 0xfacc15 });
    helperGroup.add(new THREE.LineSegments(lineGeo, lineMat));
  }

  if (showVertexNormals.value) {
    const vertPts = [];
    const seenPairs = new Set();
    const vStride = currentModel.value === 'head' ? 14 : 1;

    for (let i = 0; i < count; i += vStride) {
      const vx = pos.getX(i);
      const vy = pos.getY(i);
      const vz = pos.getZ(i);
      const nx = norm.getX(i);
      const ny = norm.getY(i);
      const nz = norm.getZ(i);

      const key = `${Math.round(vx * 100)},${Math.round(vy * 100)},${Math.round(vz * 100)}_${Math.round(nx * 40)},${Math.round(ny * 40)},${Math.round(nz * 40)}`;
      if (seenPairs.has(key)) continue;
      seenPairs.add(key);

      const len = currentModel.value === 'head' ? 0.15 : 0.22;
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
  const origin = dir.clone().multiplyScalar(1.85);
  const target = dir.clone().multiplyScalar(1.25);

  const lineGeo = new THREE.BufferGeometry().setFromPoints([origin, target]);
  const lineMat = new THREE.LineBasicMaterial({ color: 0xf97316 });
  lightIndicatorGroup.add(new THREE.Line(lineGeo, lineMat));

  const bulbGeo = new THREE.SphereGeometry(0.055, 12, 12);
  const bulbMat = new THREE.MeshBasicMaterial({ color: 0xf97316 });
  const bulb = new THREE.Mesh(bulbGeo, bulbMat);
  bulb.position.copy(origin);
  lightIndicatorGroup.add(bulb);
}

async function rebuildMesh() {
  if (!THREE || !scene) return;

  let geo;
  if (currentModel.value === 'head') {
    const data = await loadAnimeBinary();
    geo = buildAnimeBufferGeometry(data, showHair.value, normalMode.value);
  } else {
    geo = buildCylinderGeometry(normalMode.value);
  }

  if (mainMesh) {
    scene.remove(mainMesh);
    mainMesh.geometry.dispose();
    mainMesh.material.dispose();
  }
  if (outlineMesh) {
    scene.remove(outlineMesh);
    outlineMesh.material.dispose();
  }

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

function setModel(modelKey, hairFlag) {
  currentModel.value = modelKey;
  showHair.value = hairFlag;
  if (modelKey === 'cylinder') {
    outlineWidth.value = 0.055;
  } else {
    outlineWidth.value = 0.022;
  }
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
    showHair.value = true;
    normalMode.value = 'smooth';
    shadeMode.value = 'toon';
    showFaceNormals.value = false;
    showVertexNormals.value = false;
    outlineEnabled.value = true;
    outlineWidth.value = 0.022;
    lightAngle.value = 0.68;
    rebuildMesh();
  } else if (caseKey === 'clean_anime') {
    currentModel.value = 'head';
    showHair.value = true;
    normalMode.value = 'proxy';
    shadeMode.value = 'toon';
    showFaceNormals.value = false;
    showVertexNormals.value = false;
    outlineEnabled.value = true;
    outlineWidth.value = 0.022;
    lightAngle.value = 0.68;
    rebuildMesh();
  } else if (caseKey === 'broken_hull') {
    currentModel.value = 'cylinder';
    showHair.value = false;
    normalMode.value = 'hard';
    shadeMode.value = 'toon';
    showFaceNormals.value = true;
    showVertexNormals.value = true;
    outlineEnabled.value = true;
    outlineWidth.value = 0.06;
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
  camera.position.y = camOrbit.radius * Math.sin(camOrbit.phi) + 0.08;
  camera.position.z = camOrbit.radius * Math.cos(camOrbit.theta) * Math.cos(camOrbit.phi);
  camera.lookAt(0, 0.08, 0);
}

const initThree = async () => {
  if (typeof window === 'undefined') return;
  THREE = await import('three');

  const container = canvasContainer.value;
  if (!container) return;

  const width = container.clientWidth || 680;
  const height = 360;

  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x141418);

  camera = new THREE.PerspectiveCamera(36, width / height, 0.1, 100);
  updateCameraOrbit();

  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(width, height);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  container.innerHTML = '';
  container.appendChild(renderer.domElement);

  const grid = new THREE.GridHelper(5, 10, 0x27272a, 0x1f1f23);
  grid.position.y = -1.25;
  scene.add(grid);

  await rebuildMesh();

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
    camOrbit.phi = Math.max(-0.7, Math.min(0.85, camOrbit.phi + dy * 0.008));
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
  const height = 360;
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
  height: 360px;
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
