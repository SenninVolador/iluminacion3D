<template>
  <div class="technical-figure">
    <div class="figure-header">
      <div class="header-left">
        <span class="label">LABORATORIO INTERACTIVO 02</span>
        <span class="desc">Vertex Color y Empaquetado de 4 Máscaras Técnicas (RGBA) en Shaders</span>
      </div>
      <span class="viewport-hint">Arrastra para rotar · Inspecciona cada canal por separado</span>
    </div>

    <!-- BARRA DE ESCENARIO -->
    <div class="presets-bar">
      <div class="bar-group">
        <span class="preset-title">Caso de Producción:</span>
        <div class="preset-buttons">
          <button
            :class="['preset-btn', { active: scenario === 'npr' }]"
            @click="setScenario('npr')"
          >
            Caso A: Personaje Anime NPR (Outline + Sombra Bajo Mentón/Flequillo)
          </button>
          <button
            :class="['preset-btn', { active: scenario === 'env' }]"
            @click="setScenario('env')"
          >
            Caso B: Entorno 3D (Musgo + Humedad + Viento WPO)
          </button>
        </div>
      </div>
    </div>

    <!-- BARRA DE INSPECCIÓN DE CANALES (DEBUG VIEW) -->
    <div class="sub-bar">
      <div class="bar-group">
        <span class="preset-title">Vista de Diagnóstico:</span>
        <div class="preset-buttons">
          <button
            :class="['preset-btn', { active: viewChannel === 'final' }]"
            @click="setViewChannel('final')"
          >
            Shader Final (Render)
          </button>
          <button
            :class="['preset-btn', { active: viewChannel === 'rgb' }]"
            @click="setViewChannel('rgb')"
          >
            Vertex Color RGB (Raw)
          </button>
          <button
            :class="['preset-btn chan-r', { active: viewChannel === 'r' }]"
            @click="setViewChannel('r')"
          >
            Canal R ({{ scenario === 'npr' ? 'Grosor Outline' : 'Musgo' }})
          </button>
          <button
            :class="['preset-btn chan-g', { active: viewChannel === 'g' }]"
            @click="setViewChannel('g')"
          >
            Canal G ({{ scenario === 'npr' ? 'Sombra Fija' : 'Desgaste' }})
          </button>
          <button
            :class="['preset-btn chan-b', { active: viewChannel === 'b' }]"
            @click="setViewChannel('b')"
          >
            Canal B ({{ scenario === 'npr' ? 'Rim Cabello' : 'Humedad' }})
          </button>
          <button
            :class="['preset-btn chan-a', { active: viewChannel === 'a' }]"
            @click="setViewChannel('a')"
          >
            Canal A ({{ scenario === 'npr' ? 'Rubor Mejillas' : 'Peso de Viento' }})
          </button>
        </div>
      </div>
    </div>

    <!-- VIEWPORT 3D -->
    <div class="viewport-container">
      <div class="canvas-wrapper" ref="canvasContainer"></div>
      <div class="viewport-legend">
        <div class="legend-item" v-if="viewChannel !== 'final' && viewChannel !== 'rgb'">
          <span>Lectura de Máscara: <strong>Blanco = 1.0 (100%)</strong> · <strong>Negro = 0.0 (0%)</strong></span>
        </div>
        <div class="legend-item" v-else-if="viewChannel === 'rgb'">
          <span>Vista Raw: Cada vértice almacena <code>vec4(R, G, B, A)</code> sin usar memoria de texturas adicionales</span>
        </div>
        <div class="legend-item" v-else>
          <span>Shader Evaluando 4 Canales RGBA en Tiempo Real · Ángulo Solar: {{ Math.round((sunAngle * 180) / Math.PI) }}°</span>
        </div>
      </div>
    </div>

    <!-- CONTROLES DE LOS 4 CANALES -->
    <div class="controls-grid">
      <!-- CANAL R -->
      <div class="control-card">
        <div class="control-label">
          <span>
            <strong class="badge-r">R</strong>
            {{ scenario === 'npr' ? 'Canal Rojo — Multiplicador de Outline:' : 'Canal Rojo — Mezcla de Musgo Superior (Lerp):' }}
          </span>
          <code>{{ (channelRWeight * 100).toFixed(0) }}%</code>
        </div>
        <div class="toggle-row">
          <input type="range" min="0" max="1.5" step="0.05" v-model.number="channelRWeight" @input="updateUniforms" />
        </div>
        <div class="hints">
          <span v-if="scenario === 'npr'">
            En 0% el contorno infla también ojos y nariz; en 100% el Canal R adelgaza rasgos faciales internos (R=0) y engrosa cabello/hombros (R=1).
          </span>
          <span v-else>
            Controla el Alpha del nodo <code>Lerp(Piedra, Musgo, VertexColor.R)</code> en las caras superiores del pilar.
          </span>
        </div>
      </div>

      <!-- CANAL G -->
      <div class="control-card">
        <div class="control-label">
          <span>
            <strong class="badge-g">G</strong>
            {{ scenario === 'npr' ? 'Canal Verde — Sombra Permanente (Mentón y Flequillo):' : 'Canal Verde — Desgaste y Grietas Expuestas:' }}
          </span>
          <code>{{ (channelGWeight * 100).toFixed(0) }}%</code>
        </div>
        <div class="toggle-row">
          <input type="range" min="0" max="1.5" step="0.05" v-model.number="channelGWeight" @input="updateUniforms" />
        </div>
        <div class="hints">
          <span v-if="scenario === 'npr'">
            Desplaza el umbral <code>dot(N, L)</code> para forzar sombra fija bajo la barbilla y bajo el flequillo aunque la luz dé de frente.
          </span>
          <span v-else>
            Mezcla roca erosionada y oscurecimiento de cavidades en aristas y fisuras talladas.
          </span>
        </div>
      </div>

      <!-- CANAL B -->
      <div class="control-card">
        <div class="control-label">
          <span>
            <strong class="badge-b">B</strong>
            {{ scenario === 'npr' ? 'Canal Azul — Máscara de Rim Light en Cabello:' : 'Canal Azul — Humedad y Reflejo Especular en Base:' }}
          </span>
          <code>{{ (channelBWeight * 100).toFixed(0) }}%</code>
        </div>
        <div class="toggle-row">
          <input type="range" min="0" max="1.5" step="0.05" v-model.number="channelBWeight" @input="updateUniforms" />
        </div>
        <div class="hints">
          <span v-if="scenario === 'npr'">
            Restringe el brillo de borde (Fresnel Rim + Highlight) exclusivamente a los mechones del cabello y hombros.
          </span>
          <span v-else>
            Oscurece el Albedo por absorción de agua y eleva el brillo especular en la parte baja del monolito.
          </span>
        </div>
      </div>

      <!-- CANAL A -->
      <div class="control-card">
        <div class="control-label">
          <span>
            <strong class="badge-a">A</strong>
            {{ scenario === 'npr' ? 'Canal Alfa — Subsurface / Rubor Cálido en Mejillas:' : 'Canal Alfa — Animación de Viento (World Position Offset):' }}
          </span>
          <code>{{ (channelAWeight * 100).toFixed(0) }}%</code>
        </div>
        <div class="toggle-row">
          <input type="range" min="0" max="1.5" step="0.05" v-model.number="channelAWeight" @input="updateUniforms" />
        </div>
        <div class="hints">
          <span v-if="scenario === 'npr'">
            Inyecta calidez coral/rojiza en mejillas y puente nasal (Alpha = 1.0) sobre la piel anime.
          </span>
          <span v-else>
            Multiplica la onda sinusoidal de viento por <code>VertexColor.A</code>: la base (A=0) queda fija a la roca y la punta (A=1) oscila.
          </span>
        </div>
      </div>
    </div>

    <!-- EXPLICACIÓN DINÁMICA -->
    <div class="methodology-note">
      <template v-if="scenario === 'npr'">
        <strong>Flujo de Trabajo en Personajes Anime NPR (Arc System Works / HoYoverse):</strong>
        Inspecciona el botón <strong>Vertex Color RGB (Raw)</strong>: verás por qué los modelos de producción lucen como un mapa técnico multicolor. El <strong>Canal R</strong> protege ojos, pestañas y nariz para que el <em>Inverted Hull Outline</em> no los convierta en parches negros; el <strong>Canal G</strong> pinta sombra fija en el cuello bajo el mentón y bajo el flequillo; el <strong>Canal B</strong> concentra el <em>Rim Light</em> en el cabello; y el <strong>Canal A</strong> controla el rubor cálido de las mejillas.
      </template>
      <template v-else>
        <strong>Flujo de Trabajo en Entornos (Environment Blending & WPO):</strong>
        Diez pilares idénticos instanciados en Unreal Engine pueden verse completamente únicos sin crear diez texturas distintas. Pintando <strong>Vertex Color</strong> en el motor, cada canal actúa como el <em>Alpha</em> de un nodo <code>Lerp</code>: <strong>R</strong> añade musgo, <strong>G</strong> rompe bordes, <strong>B</strong> moja la base y <strong>A</strong> controla el <em>World Position Offset</em> del follaje para que las hojas se muevan con el viento sin despegar sus tallos del muro.
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { withBase } from 'vitepress';

const canvasContainer = ref(null);

const scenario = ref('npr');       // 'npr' | 'env'
const viewChannel = ref('final');  // 'final' | 'rgb' | 'r' | 'g' | 'b' | 'a'

const channelRWeight = ref(1.0);
const channelGWeight = ref(1.0);
const channelBWeight = ref(1.0);
const channelAWeight = ref(1.0);

const sunAngle = ref(0.58);

let THREE = null;
let scene, camera, renderer, animId, clock;
let mainMesh, outlineMesh;
let cachedAnimeData = null;
let isDragging = false;
let prevMouse = { x: 0, y: 0 };
let camOrbit = { theta: 0.25, phi: 0.14, radius: 3.15 };

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

async function createNPRBustGeometry() {
  const data = await loadAnimeBinary();
  const totalTris = data.hTris + data.hrTris;
  const vCount = totalTris * 3;

  const posArr = new Float32Array(vCount * 3);
  const baseColArr = new Float32Array(vCount * 3);
  const partArr = new Float32Array(vCount);

  let ptr = 0;
  const appendSection = (pos, rgba, triIdx, triCount) => {
    for (let t = 0; t < triCount; t++) {
      for (let k = 0; k < 3; k++) {
        const vi = triIdx[t * 3 + k];
        posArr[ptr * 3] = pos[vi * 3];
        posArr[ptr * 3 + 1] = pos[vi * 3 + 1];
        posArr[ptr * 3 + 2] = pos[vi * 3 + 2];

        baseColArr[ptr * 3] = rgba[vi * 4] / 255.0;
        baseColArr[ptr * 3 + 1] = rgba[vi * 4 + 1] / 255.0;
        baseColArr[ptr * 3 + 2] = rgba[vi * 4 + 2] / 255.0;
        partArr[ptr] = rgba[vi * 4 + 3];
        ptr++;
      }
    }
  };

  appendSection(data.hPos, data.hRgba, data.hTriIdx, data.hTris);
  appendSection(data.hrPos, data.hrRgba, data.hrTriIdx, data.hrTris);

  // Calcular normales por cara y promediarlas por posición espacial
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

  const smoothMap = new Map();
  const keyOf = (x, y, z) => `${Math.round(x * 2000)},${Math.round(y * 2000)},${Math.round(z * 2000)}`;
  for (let i = 0; i < vCount; i++) {
    const k = keyOf(posArr[i * 3], posArr[i * 3 + 1], posArr[i * 3 + 2]);
    let acc = smoothMap.get(k);
    if (!acc) {
      acc = new THREE.Vector3();
      smoothMap.set(k, acc);
    }
    acc.x += faceNormals[i * 3];
    acc.y += faceNormals[i * 3 + 1];
    acc.z += faceNormals[i * 3 + 2];
  }

  const finalNormals = new Float32Array(vCount * 3);
  const smoothHullNormals = new Float32Array(vCount * 3);
  const rgbaMask = new Float32Array(vCount * 4);
  const pVec = new THREE.Vector3();

  for (let i = 0; i < vCount; i++) {
    const x = posArr[i * 3];
    const y = posArr[i * 3 + 1];
    const z = posArr[i * 3 + 2];
    const pid = partArr[i];

    const avg = smoothMap.get(keyOf(x, y, z));
    pVec.copy(avg).normalize();
    smoothHullNormals[i * 3] = pVec.x;
    smoothHullNormals[i * 3 + 1] = pVec.y;
    smoothHullNormals[i * 3 + 2] = pVec.z;

    // En la cara (pid === 0 o 4), usamos Normal Transfer limpio
    if (pid === 0 || pid === 4) {
      pVec.set(x * 1.15, (y - 0.12) * 0.72, z + 0.52).normalize();
    }
    finalNormals[i * 3] = pVec.x;
    finalNormals[i * 3 + 1] = pVec.y;
    finalNormals[i * 3 + 2] = pVec.z;

    // 1. CANAL R (Grosor de Outline):
    // 0.0 en ojos/cejas/pestañas (pid === 1) y centro facial (nariz/labios)
    // 1.0 en silueta exterior, cabello (pid === 3) y cuello/hombros
    let r = 1.0;
    if (pid === 1) {
      r = 0.0;
    } else if (pid === 0 && z > 0.25) {
      const innerFace = Math.exp(-(x * x) / 0.12) * Math.exp(-Math.pow(y + 0.05, 2) / 0.14);
      r = Math.max(0.12, 1.0 - innerFace * 0.88);
    }

    // 2. CANAL G (Sombra Permanente / Oclusión):
    // Negro (0.0) en el cuello alto bajo el mentón y en la frente bajo el flequillo
    let g = 1.0;
    if (pid === 2 && y > -0.82 && y < -0.36 && z > -0.15) {
      const underChin = Math.exp(-(x * x) / 0.10) * Math.exp(-Math.pow(y + 0.52, 2) / 0.025);
      g = Math.max(0.0, 1.0 - underChin * 1.35);
    } else if (pid === 0 && z > 0.15) {
      const bangsShadow = Math.exp(-(x * x) / 0.28) * Math.exp(-Math.pow(y - 0.34, 2) / 0.022);
      const eyeSocket =
        (Math.exp(-Math.pow(Math.abs(x) - 0.25, 2) / 0.012)) * Math.exp(-Math.pow(y - 0.05, 2) / 0.008);
      g = Math.max(0.0, 1.0 - Math.min(1.0, bangsShadow * 1.15 + eyeSocket * 0.9));
    }

    // 3. CANAL B (Máscara de Rim Light / Specular en Cabello y Hombros):
    let b = 0.0;
    if (pid === 3 || pid === 4) {
      b = Math.max(0.2, Math.min(1.0, (y + 0.4) * 0.85));
    } else if (pid === 2 && Math.abs(x) > 0.32) {
      b = 0.75;
    }

    // 4. CANAL A (Rubor / Subsurface Cálido en Mejillas y Nariz):
    let a = 0.0;
    if (pid === 0 && z > 0.25) {
      const blush =
        (Math.exp(-Math.pow(Math.abs(x) - 0.28, 2) / 0.018) +
         Math.exp(-(x * x) / 0.012) * 0.7) *
        Math.exp(-Math.pow(y + 0.10, 2) / 0.016);
      a = Math.max(0.0, Math.min(1.0, blush * 1.15));
    }

    rgbaMask[i * 4] = r;
    rgbaMask[i * 4 + 1] = g;
    rgbaMask[i * 4 + 2] = b;
    rgbaMask[i * 4 + 3] = a;
  }

  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(posArr, 3));
  geo.setAttribute('normal', new THREE.BufferAttribute(finalNormals, 3));
  geo.setAttribute('aSmoothNormal', new THREE.BufferAttribute(smoothHullNormals, 3));
  geo.setAttribute('aBaseColor', new THREE.BufferAttribute(baseColArr, 3));
  geo.setAttribute('aPartId', new THREE.BufferAttribute(partArr, 1));
  geo.setAttribute('aVertexRGBA', new THREE.BufferAttribute(rgbaMask, 4));
  return geo;
}

// Construir un Pilar de Ruina + Tallos de Follaje en un mismo BufferGeometry para el Caso B (Entorno)
function createEnvironmentGeometry() {
  const pillar = new THREE.BoxGeometry(1.15, 1.9, 1.15, 14, 22, 14).toNonIndexed();
  const leaves = [];
  const leafConfigs = [
    { x: 0.58, y: 0.25, z: 0.2, dirX: 1, dirZ: 0.2 },
    { x: 0.58, y: -0.15, z: -0.25, dirX: 1, dirZ: -0.2 },
    { x: -0.58, y: 0.35, z: 0.15, dirX: -1, dirZ: 0.15 },
    { x: -0.58, y: -0.05, z: -0.2, dirX: -1, dirZ: -0.2 },
    { x: 0.15, y: 0.1, z: 0.58, dirX: 0.2, dirZ: 1 },
    { x: -0.25, y: 0.45, z: 0.58, dirX: -0.2, dirZ: 1 }
  ];

  leafConfigs.forEach((cfg) => {
    const blade = new THREE.PlaneGeometry(0.65, 0.24, 10, 2).toNonIndexed();
    const bPos = blade.attributes.position;
    for (let i = 0; i < bPos.count; i++) {
      const u = (bPos.getX(i) + 0.325) / 0.65;
      const v = bPos.getY(i);
      const worldX = cfg.x + cfg.dirX * (u * 0.62);
      const worldY = cfg.y + Math.sin(u * Math.PI) * 0.12 - u * u * 0.18 + v * 0.35;
      const worldZ = cfg.z + cfg.dirZ * (u * 0.62) + v * 0.7;
      bPos.setXYZ(i, worldX, worldY, worldZ);
    }
    blade.computeVertexNormals();
    leaves.push(blade);
  });

  const allGeos = [pillar, ...leaves];
  let totalVerts = 0;
  allGeos.forEach((g) => {
    totalVerts += g.attributes.position.count;
  });

  const mergedPos = new Float32Array(totalVerts * 3);
  const mergedNorm = new Float32Array(totalVerts * 3);
  const mergedBaseCol = new Float32Array(totalVerts * 3);
  const mergedPartId = new Float32Array(totalVerts);
  const mergedRGBA = new Float32Array(totalVerts * 4);

  let offset = 0;
  allGeos.forEach((g, idx) => {
    const p = g.attributes.position;
    const n = g.attributes.normal;
    const isLeaf = idx > 0;

    for (let i = 0; i < p.count; i++) {
      let x = p.getX(i);
      let y = p.getY(i);
      let z = p.getZ(i);
      let nx = n.getX(i);
      let ny = n.getY(i);
      let nz = n.getZ(i);

      if (!isLeaf) {
        const bevel = Math.sin(y * 7.0) * 0.025 + Math.cos(x * 5.0 + z * 5.0) * 0.02;
        x += nx * bevel;
        z += nz * bevel;
      }

      const vi = offset + i;
      mergedPos[vi * 3] = x;
      mergedPos[vi * 3 + 1] = y;
      mergedPos[vi * 3 + 2] = z;
      mergedNorm[vi * 3] = nx;
      mergedNorm[vi * 3 + 1] = ny;
      mergedNorm[vi * 3 + 2] = nz;
      mergedBaseCol[vi * 3] = 0.54;
      mergedBaseCol[vi * 3 + 1] = 0.53;
      mergedBaseCol[vi * 3 + 2] = 0.50;
      mergedPartId[vi] = 0;

      if (isLeaf) {
        const radialDist = Math.max(Math.abs(x), Math.abs(z));
        const windWeight = Math.max(0.0, Math.min(1.0, (radialDist - 0.56) / 0.55));
        mergedRGBA[vi * 4] = 1.0;
        mergedRGBA[vi * 4 + 1] = 0.0;
        mergedRGBA[vi * 4 + 2] = 0.2;
        mergedRGBA[vi * 4 + 3] = windWeight;
      } else {
        const mossNoise = 0.5 + 0.5 * Math.sin(x * 4.5 + z * 3.8);
        const r = Math.max(0.0, Math.min(1.0, (y - 0.15) * 1.15 + mossNoise * 0.35 * (y > -0.1 ? 1 : 0)));

        const cornerDist = Math.abs(x) * Math.abs(z);
        const crackZone = Math.exp(-Math.pow(y - 0.05 + x * 0.35, 2) / 0.025);
        const gVal = Math.max(0.0, Math.min(1.0, cornerDist * 2.2 + crackZone * 0.75));

        const b = Math.max(0.0, Math.min(1.0, (-y - 0.1) * 1.35));
        const a = 0.0;

        mergedRGBA[vi * 4] = r;
        mergedRGBA[vi * 4 + 1] = gVal;
        mergedRGBA[vi * 4 + 2] = b;
        mergedRGBA[vi * 4 + 3] = a;
      }
    }
    offset += p.count;
  });

  const finalGeo = new THREE.BufferGeometry();
  finalGeo.setAttribute('position', new THREE.BufferAttribute(mergedPos, 3));
  finalGeo.setAttribute('normal', new THREE.BufferAttribute(mergedNorm, 3));
  finalGeo.setAttribute('aSmoothNormal', new THREE.BufferAttribute(mergedNorm, 3));
  finalGeo.setAttribute('aBaseColor', new THREE.BufferAttribute(mergedBaseCol, 3));
  finalGeo.setAttribute('aPartId', new THREE.BufferAttribute(mergedPartId, 1));
  finalGeo.setAttribute('aVertexRGBA', new THREE.BufferAttribute(mergedRGBA, 4));
  return finalGeo;
}

function getChannelModeInt() {
  return viewChannel.value === 'final' ? 0 :
         viewChannel.value === 'rgb' ? 1 :
         viewChannel.value === 'r' ? 2 :
         viewChannel.value === 'g' ? 3 :
         viewChannel.value === 'b' ? 4 : 5;
}

async function buildSceneMeshes() {
  if (!THREE || !scene) return;

  const isNPR = scenario.value === 'npr';
  const geo = isNPR ? await createNPRBustGeometry() : createEnvironmentGeometry();

  if (mainMesh) {
    scene.remove(mainMesh);
    mainMesh.geometry.dispose();
    mainMesh.material.dispose();
  }
  if (outlineMesh) {
    scene.remove(outlineMesh);
    outlineMesh.material.dispose();
    outlineMesh = null;
  }

  const mat = new THREE.ShaderMaterial({
    side: THREE.DoubleSide,
    uniforms: {
      uTime: { value: 0 },
      uScenario: { value: isNPR ? 0 : 1 },
      uViewChannel: { value: getChannelModeInt() },
      uWeights: {
        value: new THREE.Vector4(
          channelRWeight.value,
          channelGWeight.value,
          channelBWeight.value,
          channelAWeight.value
        )
      },
      uLightDir: {
        value: new THREE.Vector3(Math.sin(sunAngle.value), 0.32, Math.cos(sunAngle.value)).normalize()
      }
    },
    vertexShader: `
      attribute vec4 aVertexRGBA;
      attribute vec3 aBaseColor;
      attribute float aPartId;
      uniform float uTime;
      uniform int uScenario;
      uniform vec4 uWeights;

      varying vec4 vRGBA;
      varying vec3 vBaseColor;
      varying float vPartId;
      varying vec3 vNormal;
      varying vec3 vViewDir;

      void main() {
        vRGBA = aVertexRGBA;
        vBaseColor = aBaseColor;
        vPartId = aPartId;
        vec3 pos = position;

        // En Caso B (Entorno), el Canal A controla el World Position Offset (Viento)
        if (uScenario == 1) {
          float windMask = aVertexRGBA.a * uWeights.w;
          float wave = sin(uTime * 3.4 + position.y * 4.0 + position.x * 3.0);
          pos.x += wave * 0.08 * windMask;
          pos.y += cos(uTime * 2.8 + position.z * 4.0) * 0.09 * windMask;
          pos.z += wave * 0.06 * windMask;
        }

        vec4 worldPos = modelMatrix * vec4(pos, 1.0);
        vNormal = normalize(mat3(modelMatrix) * normal);
        vViewDir = normalize(cameraPosition - worldPos.xyz);
        gl_Position = projectionMatrix * viewMatrix * worldPos;
      }
    `,
    fragmentShader: `
      uniform int uScenario;
      uniform int uViewChannel;
      uniform vec4 uWeights;
      uniform vec3 uLightDir;

      varying vec4 vRGBA;
      varying vec3 vBaseColor;
      varying float vPartId;
      varying vec3 vNormal;
      varying vec3 vViewDir;

      void main() {
        // Vistas de Diagnóstico (Raw RGB o Canales Individuales)
        if (uViewChannel == 1) {
          gl_FragColor = vec4(vRGBA.rgb, 1.0);
          return;
        }
        if (uViewChannel == 2) {
          float val = clamp(vRGBA.r * uWeights.x, 0.0, 1.0);
          gl_FragColor = vec4(vec3(val), 1.0);
          return;
        }
        if (uViewChannel == 3) {
          float val = clamp(1.0 - (1.0 - vRGBA.g) * uWeights.y, 0.0, 1.0);
          if (uScenario == 1) val = clamp(vRGBA.g * uWeights.y, 0.0, 1.0);
          gl_FragColor = vec4(vec3(val), 1.0);
          return;
        }
        if (uViewChannel == 4) {
          float val = clamp(vRGBA.b * uWeights.z, 0.0, 1.0);
          gl_FragColor = vec4(vec3(val), 1.0);
          return;
        }
        if (uViewChannel == 5) {
          float val = clamp(vRGBA.a * uWeights.w, 0.0, 1.0);
          gl_FragColor = vec4(vec3(val), 1.0);
          return;
        }

        vec3 N = normalize(vNormal);
        vec3 L = normalize(uLightDir);
        vec3 V = normalize(vViewDir);
        float NdotL = dot(N, L);

        // CASO A: PERSONAJE ANIME NPR
        if (uScenario == 0) {
          if (vPartId > 0.5 && vPartId < 1.5) {
            gl_FragColor = vec4(vBaseColor, 1.0);
            return;
          }

          // Canal G empuja el producto punto hacia sombra donde G < 1.0 (bajo mentón y flequillo)
          float shadowBias = (vRGBA.g - 1.0) * 0.95 * uWeights.y;
          float effectiveLight = NdotL + shadowBias;
          float cel = smoothstep(0.01, 0.04, effectiveLight);

          vec3 litColor = vBaseColor;
          vec3 shadowColor = vBaseColor * vec3(0.68, 0.56, 0.68);

          // Canal A añade rubor coral en mejillas y nariz
          vec3 blushCol = vec3(0.96, 0.50, 0.48);
          float blushMask = clamp(vRGBA.a * uWeights.w, 0.0, 1.0);
          litColor = mix(litColor, blushCol, blushMask * 0.42);
          shadowColor = mix(shadowColor, blushCol * 0.75, blushMask * 0.35);

          vec3 col = mix(shadowColor, litColor, cel);

          // Canal B controla dónde aparece la Rim Light / Specular en el cabello
          float fresnel = pow(1.0 - max(dot(N, V), 0.0), 2.8);
          float rimMask = step(0.48, fresnel) * clamp(vRGBA.b * uWeights.z, 0.0, 1.0);
          col += vec3(0.28, 0.34, 0.48) * rimMask;

          gl_FragColor = vec4(col, 1.0);
          return;
        }

        // CASO B: ENTORNO 3D (Lerp de Materiales PBR mediante Vertex Color)
        vec3 baseStone = vec3(0.54, 0.53, 0.50);
        vec3 mossCol = vec3(0.22, 0.48, 0.20);
        vec3 wornRock = vec3(0.28, 0.24, 0.21);

        float wearMask = clamp(vRGBA.g * uWeights.y, 0.0, 1.0);
        vec3 albedo = mix(baseStone, wornRock, wearMask * 0.78);

        float mossMask = clamp(vRGBA.r * uWeights.x, 0.0, 1.0);
        albedo = mix(albedo, mossCol, smoothstep(0.25, 0.75, mossMask));

        float wetMask = clamp(vRGBA.b * uWeights.z, 0.0, 1.0);
        albedo *= mix(1.0, 0.45, wetMask);

        float diff = clamp(NdotL * 0.5 + 0.5, 0.15, 1.0);
        vec3 H = normalize(L + V);
        float specPower = mix(12.0, 96.0, wetMask);
        float specStrength = mix(0.06, 0.65, wetMask);
        float spec = pow(max(dot(N, H), 0.0), specPower) * specStrength;

        vec3 envColor = albedo * diff + vec3(0.85, 0.92, 1.0) * spec;
        gl_FragColor = vec4(envColor, 1.0);
      }
    `
  });

  mainMesh = new THREE.Mesh(geo, mat);
  scene.add(mainMesh);

  if (isNPR) {
    const outMat = new THREE.ShaderMaterial({
      side: THREE.BackSide,
      uniforms: {
        uWeightR: { value: channelRWeight.value },
        uHideInDebug: { value: viewChannel.value === 'final' ? 1.0 : 0.0 }
      },
      vertexShader: `
        attribute vec4 aVertexRGBA;
        attribute vec3 aSmoothNormal;
        uniform float uWeightR;
        uniform float uHideInDebug;
        void main() {
          // Si uWeightR == 0, usa grosor uniforme (inflando incluso ojos y pestañas); si uWeightR == 1, modula por Canal R
          float maskFactor = mix(1.0, aVertexRGBA.r, clamp(uWeightR, 0.0, 1.5));
          float thickness = 0.025 * maskFactor * uHideInDebug;
          vec3 displaced = position + normalize(aSmoothNormal) * thickness;
          gl_Position = projectionMatrix * modelViewMatrix * vec4(displaced, 1.0);
        }
      `,
      fragmentShader: `
        void main() {
          gl_FragColor = vec4(0.08, 0.07, 0.10, 1.0);
        }
      `
    });
    outlineMesh = new THREE.Mesh(geo, outMat);
    scene.add(outlineMesh);
  }
}

function updateUniforms() {
  if (!mainMesh) return;
  mainMesh.material.uniforms.uViewChannel.value = getChannelModeInt();
  mainMesh.material.uniforms.uWeights.value.set(
    channelRWeight.value,
    channelGWeight.value,
    channelBWeight.value,
    channelAWeight.value
  );

  if (outlineMesh) {
    outlineMesh.visible = viewChannel.value === 'final';
    outlineMesh.material.uniforms.uWeightR.value = channelRWeight.value;
    outlineMesh.material.uniforms.uHideInDebug.value = viewChannel.value === 'final' ? 1.0 : 0.0;
  }
}

function setScenario(key) {
  scenario.value = key;
  camOrbit.radius = key === 'npr' ? 3.15 : 3.85;
  updateCameraOrbit();
  buildSceneMeshes();
}

function setViewChannel(ch) {
  viewChannel.value = ch;
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
  grid.position.y = -1.2;
  scene.add(grid);

  clock = new THREE.Clock();
  await buildSceneMeshes();

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
    if (mainMesh && clock) {
      mainMesh.material.uniforms.uTime.value = clock.getElapsedTime();
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
  gap: 10px;
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
  background: rgba(17, 24, 39, 0.84);
  padding: 5px 10px;
  border-radius: 3px;
  border: 1px solid rgba(255, 255, 255, 0.12);
  pointer-events: none;
}

.legend-item {
  font-size: 10.5px;
  color: #e5e7eb;
  font-family: monospace;
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
  align-items: center;
  font-size: 11.5px;
  font-weight: 700;
  color: #111827;
  gap: 6px;
}

.control-label code {
  color: #111827;
  font-size: 10.5px;
  background: #e5e7eb;
  padding: 1px 5px;
  border-radius: 2px;
}

.badge-r,
.badge-g,
.badge-b,
.badge-a {
  display: inline-block;
  font-family: monospace;
  font-size: 10px;
  padding: 1px 5px;
  border-radius: 2px;
  color: #ffffff;
  margin-right: 4px;
}

.badge-r {
  background: #dc2626;
}
.badge-g {
  background: #16a34a;
}
.badge-b {
  background: #2563eb;
}
.badge-a {
  background: #4b5563;
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
