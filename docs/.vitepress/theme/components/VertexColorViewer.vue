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
            Caso A: Personaje NPR (Outline + Sombras Forzadas)
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
            Canal B ({{ scenario === 'npr' ? 'Rim Light' : 'Humedad' }})
          </button>
          <button
            :class="['preset-btn chan-a', { active: viewChannel === 'a' }]"
            @click="setViewChannel('a')"
          >
            Canal A ({{ scenario === 'npr' ? 'Tinte Cálido' : 'Peso de Viento' }})
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
            En 0% el contorno tiene grosor uniforme; en 100% el Canal R adelgaza trazos faciales internos (R=0) y engrosa hombros (R=1).
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
            {{ scenario === 'npr' ? 'Canal Verde — Sombra Permanente (Bajo Mentón/Cuello):' : 'Canal Verde — Desgaste y Grietas Expuestas:' }}
          </span>
          <code>{{ (channelGWeight * 100).toFixed(0) }}%</code>
        </div>
        <div class="toggle-row">
          <input type="range" min="0" max="1.5" step="0.05" v-model.number="channelGWeight" @input="updateUniforms" />
        </div>
        <div class="hints">
          <span v-if="scenario === 'npr'">
            Desplaza el umbral <code>N · L</code> para forzar sombra fija bajo la barbilla y cuencas oculares aunque la luz dé de frente.
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
            {{ scenario === 'npr' ? 'Canal Azul — Máscara de Rim Light / Specular:' : 'Canal Azul — Humedad y Reflejo Especular en Base:' }}
          </span>
          <code>{{ (channelBWeight * 100).toFixed(0) }}%</code>
        </div>
        <div class="toggle-row">
          <input type="range" min="0" max="1.5" step="0.05" v-model.number="channelBWeight" @input="updateUniforms" />
        </div>
        <div class="hints">
          <span v-if="scenario === 'npr'">
            Restringe el recorte de luz de borde (Fresnel Rim) únicamente a la zona superior de la cabeza y hombros.
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
            {{ scenario === 'npr' ? 'Canal Alfa — Subsurface / Tinte Cálido en Mejillas:' : 'Canal Alfa — Animación de Viento (World Position Offset):' }}
          </span>
          <code>{{ (channelAWeight * 100).toFixed(0) }}%</code>
        </div>
        <div class="toggle-row">
          <input type="range" min="0" max="1.5" step="0.05" v-model.number="channelAWeight" @input="updateUniforms" />
        </div>
        <div class="hints">
          <span v-if="scenario === 'npr'">
            Inyecta calidez rojiza en la transición luz-sombra sobre mejillas, nariz y orejas (Alpha = 1.0).
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
        <strong>Flujo de Trabajo en Personajes NPR (Arc System Works / Hoyoverse):</strong>
        En lugar de dejar que la matemática pura decida dónde cae cada línea y sombra, el artista técnico pinta los canales <strong>RGBA</strong> directamente en los vértices del modelo: el <strong>Canal R</strong> afina el contorno <em>Inverted Hull</em> en nariz y labios para que no parezcan manchones negros; el <strong>Canal G</strong> asegura que bajo el mentón siempre exista sombra estética; el <strong>Canal B</strong> acota el brillo de borde (Rim Light); y el <strong>Canal A</strong> suaviza la transición rojiza en la piel.
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

const canvasContainer = ref(null);

const scenario = ref('npr');       // 'npr' | 'env'
const viewChannel = ref('final');  // 'final' | 'rgb' | 'r' | 'g' | 'b' | 'a'

const channelRWeight = ref(1.0);
const channelGWeight = ref(1.0);
const channelBWeight = ref(1.0);
const channelAWeight = ref(1.0);

const sunAngle = ref(0.65);

let THREE = null;
let scene, camera, renderer, animId, clock;
let mainMesh, outlineMesh;
let isDragging = false;
let prevMouse = { x: 0, y: 0 };
let camOrbit = { theta: 0.35, phi: 0.22, radius: 3.9 };

// Esculpir busto estilizado con cabeza, cuello y hombros para mostrar las 4 máscaras NPR
function createNPRBustGeometry() {
  const base = new THREE.IcosahedronGeometry(1.0, 4);
  const pos = base.attributes.position;

  for (let i = 0; i < pos.count; i++) {
    let x = pos.getX(i);
    let y = pos.getY(i);
    let z = pos.getZ(i);

    if (y < -0.35) {
      // Cuello y apertura hacia los hombros en la base
      const t = Math.min(1.0, (-y - 0.35) / 0.65);
      const neckNarrow = 0.52;
      const shoulderWide = 1.45;
      const widthFactor = neckNarrow * (1.0 - t) + shoulderWide * (t * t);
      x *= widthFactor;
      z *= 0.55 * (1.0 - t * 0.25);
      y *= 1.18;
    } else {
      // Cabeza y rasgos faciales
      x *= 0.82;
      y *= 1.05;
      z *= 0.86;

      if (z > 0.05) {
        const nose = Math.exp(-(x * x) / 0.02) * Math.exp(-Math.pow(y - 0.05, 2) / 0.06);
        const eyes =
          Math.exp(-Math.pow(x - 0.26, 2) / 0.025) * Math.exp(-Math.pow(y - 0.18, 2) / 0.02) +
          Math.exp(-Math.pow(x + 0.26, 2) / 0.025) * Math.exp(-Math.pow(y - 0.18, 2) / 0.02);
        const chin = Math.exp(-(x * x) / 0.04) * Math.exp(-Math.pow(y + 0.32, 2) / 0.02);
        z += nose * 0.24 - eyes * 0.18 + chin * 0.12;
      }
    }

    pos.setXYZ(i, x, y, z);
  }

  base.computeVertexNormals();

  // Asignar los 4 canales RGBA de Vertex Color y normales proxy suaves
  const vCount = pos.count;
  const rgba = new Float32Array(vCount * 4);
  const proxyNorms = new Float32Array(vCount * 3);
  const pVec = new THREE.Vector3();

  for (let i = 0; i < vCount; i++) {
    const x = pos.getX(i);
    const y = pos.getY(i);
    const z = pos.getZ(i);

    // Normal suave estilo anime
    pVec.set(x * 1.1, y * 0.85, z + 0.28).normalize();
    proxyNorms[i * 3] = pVec.x;
    proxyNorms[i * 3 + 1] = pVec.y;
    proxyNorms[i * 3 + 2] = pVec.z;

    // CANAL R (Grosor de Outline):
    // Fino (0.15) en centro del rostro (nariz, ojos, boca); Grueso (1.0) en silueta exterior, cráneo y hombros
    const faceCenterMask =
      z > 0.2 ? Math.exp(-(x * x) / 0.16) * Math.exp(-Math.pow(y - 0.02, 2) / 0.14) : 0.0;
    const r = Math.max(0.12, Math.min(1.0, 1.0 - faceCenterMask * 0.88));

    // CANAL G (Sombra Permanente / Oclusión):
    // Negro (0.0) bajo el mentón/cuello alto y cuencas oculares; Blanco (1.0) en el resto
    const underChin =
      z > -0.1 && y < -0.18 && y > -0.68
        ? Math.exp(-(x * x) / 0.22) * Math.exp(-Math.pow(y + 0.42, 2) / 0.035)
        : 0.0;
    const eyeSockets =
      z > 0.15
        ? (Math.exp(-Math.pow(x - 0.26, 2) / 0.025) + Math.exp(-Math.pow(x + 0.26, 2) / 0.025)) *
          Math.exp(-Math.pow(y - 0.18, 2) / 0.02)
        : 0.0;
    const g = Math.max(0.0, Math.min(1.0, 1.0 - Math.min(1.0, underChin * 1.15 + eyeSockets * 0.85)));

    // CANAL B (Máscara de Rim Light):
    // Blanco (1.0) en coronilla, laterales superiores y hombros; Negro (0.0) en cuello/bajo mentón
    const b = Math.max(0.0, Math.min(1.0, (y + 0.25) * 0.85 + Math.abs(x) * 0.45 - underChin));

    // CANAL A (Subsurface / Rubor Cálido en mejillas y nariz):
    const cheeks =
      z > 0.2
        ? (Math.exp(-Math.pow(x - 0.32, 2) / 0.035) +
            Math.exp(-Math.pow(x + 0.32, 2) / 0.035) +
            Math.exp(-(x * x) / 0.025)) *
          Math.exp(-Math.pow(y - 0.02, 2) / 0.04)
        : 0.0;
    const a = Math.max(0.0, Math.min(1.0, cheeks));

    rgba[i * 4] = r;
    rgba[i * 4 + 1] = g;
    rgba[i * 4 + 2] = b;
    rgba[i * 4 + 3] = a;
  }

  base.setAttribute('normal', new THREE.BufferAttribute(proxyNorms, 3));
  base.setAttribute('aVertexRGBA', new THREE.BufferAttribute(rgba, 4));
  return base;
}

// Construir un Pilar de Ruina + Tallos de Follaje en un mismo BufferGeometry para el Caso B (Entorno)
function createEnvironmentGeometry() {
  // 1. Pilar de piedra subdividido
  const pillar = new THREE.BoxGeometry(1.15, 1.9, 1.15, 14, 22, 14).toNonIndexed();
  // 2. Placas de hojas/tallos de vegetación que salen de los costados del pilar
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
      // u va de 0 (tallo pegado al pilar) a 1 (punta exterior de la hoja)
      const u = (bPos.getX(i) + 0.325) / 0.65;
      const v = bPos.getY(i);

      // Curvar la hoja hacia afuera y ligeramente hacia abajo en la punta
      const worldX = cfg.x + cfg.dirX * (u * 0.62);
      const worldY = cfg.y + Math.sin(u * Math.PI) * 0.12 - u * u * 0.18 + v * 0.35;
      const worldZ = cfg.z + cfg.dirZ * (u * 0.62) + v * 0.7;

      bPos.setXYZ(i, worldX, worldY, worldZ);
    }
    blade.computeVertexNormals();
    blade.userData.isFoliage = true;
    leaves.push(blade);
  });

  // Fusionar pilar + hojas en un solo BufferGeometry
  const allGeos = [pillar, ...leaves];
  let totalVerts = 0;
  allGeos.forEach((g) => {
    totalVerts += g.attributes.position.count;
  });

  const mergedPos = new Float32Array(totalVerts * 3);
  const mergedNorm = new Float32Array(totalVerts * 3);
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
        // Deformación orgánica sutil en los bloques del pilar de piedra
        const bevel =
          Math.sin(y * 7.0) * 0.025 +
          Math.cos(x * 5.0 + z * 5.0) * 0.02;
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

      if (isLeaf) {
        // En las hojas:
        // R = 1.0 (color verde vegetación)
        // G = 0.0
        // B = 0.2
        // A = Peso de viento: 0.0 en la raíz pegada al pilar (dist <= 0.59) hasta 1.0 en la punta exterior
        const radialDist = Math.max(Math.abs(x), Math.abs(z));
        const windWeight = Math.max(0.0, Math.min(1.0, (radialDist - 0.56) / 0.55));
        mergedRGBA[vi * 4] = 1.0;
        mergedRGBA[vi * 4 + 1] = 0.0;
        mergedRGBA[vi * 4 + 2] = 0.2;
        mergedRGBA[vi * 4 + 3] = windWeight;
      } else {
        // En el pilar de piedra:
        // CANAL R (Musgo): Blanco (1.0) en el tope superior y hombros altos con ruido orgánico
        const mossNoise = 0.5 + 0.5 * Math.sin(x * 4.5 + z * 3.8);
        const r = Math.max(0.0, Math.min(1.0, (y - 0.15) * 1.15 + mossNoise * 0.35 * (y > -0.1 ? 1 : 0)));

        // CANAL G (Desgaste / Grietas): Blanco (1.0) en las esquinas verticales y grieta central
        const cornerDist = Math.abs(x) * Math.abs(z);
        const crackZone = Math.exp(-Math.pow(y - 0.05 + x * 0.35, 2) / 0.025);
        const g = Math.max(0.0, Math.min(1.0, cornerDist * 2.2 + crackZone * 0.75));

        // CANAL B (Humedad / Agua en la base): Blanco (1.0) en el tercio inferior del pilar
        const b = Math.max(0.0, Math.min(1.0, (-y - 0.1) * 1.35));

        // CANAL A (Peso de Viento): 0.0 absoluto en toda la piedra para que el pilar sea rígido
        const a = 0.0;

        mergedRGBA[vi * 4] = r;
        mergedRGBA[vi * 4 + 1] = g;
        mergedRGBA[vi * 4 + 2] = b;
        mergedRGBA[vi * 4 + 3] = a;
      }
    }
    offset += p.count;
  });

  const finalGeo = new THREE.BufferGeometry();
  finalGeo.setAttribute('position', new THREE.BufferAttribute(mergedPos, 3));
  finalGeo.setAttribute('normal', new THREE.BufferAttribute(mergedNorm, 3));
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

function buildSceneMeshes() {
  if (!THREE || !scene) return;

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

  const isNPR = scenario.value === 'npr';
  const geo = isNPR ? createNPRBustGeometry() : createEnvironmentGeometry();

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
        value: new THREE.Vector3(Math.sin(sunAngle.value), 0.45, Math.cos(sunAngle.value)).normalize()
      }
    },
    vertexShader: `
      attribute vec4 aVertexRGBA;
      uniform float uTime;
      uniform int uScenario;
      uniform vec4 uWeights;

      varying vec4 vRGBA;
      varying vec3 vNormal;
      varying vec3 vWorldPos;
      varying vec3 vViewDir;

      void main() {
        vRGBA = aVertexRGBA;
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
        vWorldPos = worldPos.xyz;
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
      varying vec3 vNormal;
      varying vec3 vWorldPos;
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
          float val = clamp(vRGBA.g * uWeights.y, 0.0, 1.0);
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

        // CASO A: PERSONAJE NPR (Cel Shading + Sombras Forzadas G + Rim B + Subsurface A)
        if (uScenario == 0) {
          // Canal G empuja la iluminación hacia sombra donde G es cercano a 0.0
          float shadowBias = (vRGBA.g - 1.0) * 0.85 * uWeights.y;
          float effectiveLight = NdotL + shadowBias;

          float cel = smoothstep(0.02, 0.06, effectiveLight);

          vec3 shadowColor = vec3(0.40, 0.32, 0.43);
          vec3 litColor = vec3(0.98, 0.90, 0.85);

          // Canal A añade rubor / dispersión cálida en mejillas y nariz
          vec3 blushColor = vec3(0.95, 0.56, 0.52);
          float blushMask = clamp(vRGBA.a * uWeights.w, 0.0, 1.0);
          litColor = mix(litColor, blushColor, blushMask * 0.42);
          shadowColor = mix(shadowColor, vec3(0.55, 0.32, 0.38), blushMask * 0.35);

          vec3 col = mix(shadowColor, litColor, cel);

          // Canal B controla dónde aparece la Rim Light estilizada
          float fresnel = pow(1.0 - max(dot(N, V), 0.0), 3.2);
          float rimMask = step(0.52, fresnel) * clamp(vRGBA.b * uWeights.z, 0.0, 1.0);
          col += vec3(0.28, 0.36, 0.48) * rimMask;

          gl_FragColor = vec4(col, 1.0);
          return;
        }

        // CASO B: ENTORNO 3D (Lerp de Materiales PBR mediante Vertex Color)
        vec3 baseStone = vec3(0.54, 0.53, 0.50);
        vec3 mossCol = vec3(0.22, 0.48, 0.20);
        vec3 wornRock = vec3(0.28, 0.24, 0.21);

        // 1. Canal G: Desgaste de bordes y grietas
        float wearMask = clamp(vRGBA.g * uWeights.y, 0.0, 1.0);
        vec3 albedo = mix(baseStone, wornRock, wearMask * 0.78);

        // 2. Canal R: Capa de musgo / follaje
        float mossMask = clamp(vRGBA.r * uWeights.x, 0.0, 1.0);
        albedo = mix(albedo, mossCol, smoothstep(0.25, 0.75, mossMask));

        // 3. Canal B: Humedad en la base (oscurece el Albedo y genera reflejo especular fuerte)
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

  // En el Caso A (NPR), añadimos el contorno Inverted Hull cuyo grosor es modulado por el Canal R
  if (isNPR) {
    const outMat = new THREE.ShaderMaterial({
      side: THREE.BackSide,
      uniforms: {
        uWeightR: { value: channelRWeight.value },
        uHideInDebug: { value: viewChannel.value === 'final' ? 1.0 : 0.0 }
      },
      vertexShader: `
        attribute vec4 aVertexRGBA;
        uniform float uWeightR;
        uniform float uHideInDebug;
        void main() {
          // Si uWeightR == 0, usa grosor uniforme; si aumenta, modula el grosor con aVertexRGBA.r
          float maskFactor = mix(1.0, aVertexRGBA.r, clamp(uWeightR, 0.0, 1.5));
          float thickness = 0.048 * maskFactor * uHideInDebug;
          vec3 displaced = position + normalize(normal) * thickness;
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
  buildSceneMeshes();
}

function setViewChannel(ch) {
  viewChannel.value = ch;
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

  const grid = new THREE.GridHelper(5, 10, 0x27272a, 0x1f1f23);
  grid.position.y = -1.2;
  scene.add(grid);

  clock = new THREE.Clock();
  buildSceneMeshes();

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
