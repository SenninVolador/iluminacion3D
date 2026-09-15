<template>
  <div class="technical-figure">
    <div class="figure-header">
      <div class="header-left">
        <span class="label">ESTUDIO DE CASO 3D</span>
        <span class="desc">Desglose de Iluminación — Prólogo Nocturno (Inspirado en The Last of Us)</span>
      </div>
      <span class="viewport-hint">Arrastra para rotar la cámara</span>
    </div>

    <!-- PRESETS DE ANÁLISIS -->
    <div class="presets-bar">
      <span class="preset-title">Capas de referencia:</span>
      <div class="preset-buttons">
        <button
          :class="['preset-btn', { active: currentPreset === 'full' }]"
          @click="applyPreset('full')"
        >
          Setup Completo TLOU
        </button>
        <button
          :class="['preset-btn', { active: currentPreset === 'moonlight' }]"
          @click="applyPreset('moonlight')"
        >
          Solo Luna Exterior
        </button>
        <button
          :class="['preset-btn', { active: currentPreset === 'tv' }]"
          @click="applyPreset('tv')"
        >
          Solo Pantalla de TV
        </button>
        <button
          :class="['preset-btn', { active: currentPreset === 'thermal' }]"
          @click="applyPreset('thermal')"
        >
          Contraste Frío / Cálido
        </button>
      </div>
    </div>
    
    <!-- VIEWPORT 3D -->
    <div class="canvas-wrapper" ref="canvasContainer"></div>

    <!-- CONTROLES PARAMÉTRICOS POR CAPAS -->
    <div class="controls-grid">
      
      <!-- CAPA 1: LUZ NATURAL (LUNA Y EXTERIOR) -->
      <div class="control-card">
        <div class="control-label">
          <span>1. Luz Natural (Luna y Noche Exterior):</span>
          <code>{{ moonEnabled ? moonIntensity.toFixed(1) + ' lux' : 'Apagada' }}</code>
        </div>
        <div class="toggle-row">
          <input type="checkbox" v-model="moonEnabled" @change="onManualChange" />
          <input type="range" min="0" max="4" step="0.1" v-model.number="moonIntensity" :disabled="!moonEnabled" @input="onManualChange" />
        </div>
        <div class="hints"><span>Azul frío desaturado (~7.500K) que entra por el ventanal</span></div>
      </div>

      <!-- CAPA 2: PRACTICAL LIGHT (PANTALLA DE TELEVISOR) -->
      <div class="control-card">
        <div class="control-label">
          <span>2. Luz Práctica (Pantalla de TV):</span>
          <code>{{ tvEnabled ? tvIntensity.toFixed(1) + ' cd' : 'Apagada' }}</code>
        </div>
        <div class="toggle-row">
          <input type="checkbox" v-model="tvEnabled" @change="onManualChange" />
          <input type="range" min="0" max="4" step="0.1" v-model.number="tvIntensity" :disabled="!tvEnabled" @input="onManualChange" />
        </div>
        <div class="hints"><span>Emisión blanco-celeste que proyecta sombras duras en la sala</span></div>
      </div>

      <!-- CAPA 3: LUZ CÁLIDA DE PASILLO -->
      <div class="control-card">
        <div class="control-label">
          <span>3. Luz de Pasillo / Puerta Entreabierta:</span>
          <code>{{ hallEnabled ? hallIntensity.toFixed(1) + ' cd' : 'Apagada' }}</code>
        </div>
        <div class="toggle-row">
          <input type="checkbox" v-model="hallEnabled" @change="onManualChange" />
          <input type="range" min="0" max="3" step="0.1" v-model.number="hallIntensity" :disabled="!hallEnabled" @input="onManualChange" />
        </div>
        <div class="hints"><span>Tungsteno cálido (~2.700K) que crea contraste térmico</span></div>
      </div>

      <!-- CAPA 4: DRAMATIC LIGHT (RECORTE DE SILUETA) -->
      <div class="control-card">
        <div class="control-label">
          <span>4. Luz Dramática (Silueta / Rim Light):</span>
          <code>{{ rimEnabled ? rimIntensity.toFixed(1) + ' cd' : 'Apagada' }}</code>
        </div>
        <div class="toggle-row">
          <input type="checkbox" v-model="rimEnabled" @change="onManualChange" />
          <input type="range" min="0" max="4" step="0.1" v-model.number="rimIntensity" :disabled="!rimEnabled" @input="onManualChange" />
        </div>
        <div class="hints"><span>Luz invisible que despega al sujeto de la oscuridad</span></div>
      </div>

    </div>

    <!-- NOTA METODOLÓGICA -->
    <div class="methodology-note">
      <strong>Análisis Naughty Dog:</strong> Observa cómo la escena genera dramatismo no inundando la habitación de luz, sino mediante <em>contraste de claroscuro y temperatura</em>: el azul frío de la luna exterior baña el suelo, el televisor genera un foco frío intenso en la oscuridad, y la luz cálida del pasillo añade tensión narrativa al sugerir presencia en otra habitación. La luz dramática sutil permite leer la silueta del personaje sin lavar las sombras profundas.
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';

const canvasContainer = ref(null);

const moonEnabled = ref(true);
const moonIntensity = ref(2.0);

const tvEnabled = ref(true);
const tvIntensity = ref(2.8);

const hallEnabled = ref(true);
const hallIntensity = ref(1.6);

const rimEnabled = ref(true);
const rimIntensity = ref(2.2);

const currentPreset = ref('full');

let scene, camera, renderer, animId;
let moonLight, moonFill, tvLight, tvScreenMesh, hallLight, rimLight, shaftMesh;
let isDragging = false;
let previousMousePosition = { x: 0, y: 0 };
let cameraAngle = { theta: 0.15, phi: 0.25 };

const applyPreset = (presetKey) => {
  currentPreset.value = presetKey;
  if (presetKey === 'full') {
    moonEnabled.value = true;
    moonIntensity.value = 2.0;
    tvEnabled.value = true;
    tvIntensity.value = 2.8;
    hallEnabled.value = true;
    hallIntensity.value = 1.6;
    rimEnabled.value = true;
    rimIntensity.value = 2.2;
  } else if (presetKey === 'moonlight') {
    moonEnabled.value = true;
    moonIntensity.value = 2.8;
    tvEnabled.value = false;
    tvIntensity.value = 0.0;
    hallEnabled.value = false;
    hallIntensity.value = 0.0;
    rimEnabled.value = false;
    rimIntensity.value = 0.0;
  } else if (presetKey === 'tv') {
    moonEnabled.value = false;
    moonIntensity.value = 0.0;
    tvEnabled.value = true;
    tvIntensity.value = 3.5;
    hallEnabled.value = false;
    hallIntensity.value = 0.0;
    rimEnabled.value = false;
    rimIntensity.value = 0.0;
  } else if (presetKey === 'thermal') {
    moonEnabled.value = true;
    moonIntensity.value = 2.2;
    tvEnabled.value = false;
    tvIntensity.value = 0.0;
    hallEnabled.value = true;
    hallIntensity.value = 2.6;
    rimEnabled.value = false;
    rimIntensity.value = 0.0;
  }
  updateLights();
};

const onManualChange = () => {
  currentPreset.value = 'custom';
  updateLights();
};

const initThree = async () => {
  if (typeof window === 'undefined') return;
  const THREE = await import('three');

  const container = canvasContainer.value;
  if (!container) return;

  const width = container.clientWidth || 600;
  const height = 300;

  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x080a10);

  camera = new THREE.PerspectiveCamera(36, width / height, 0.1, 100);
  updateCameraPos();

  renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
  renderer.setSize(width, height);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.0;
  container.innerHTML = '';
  container.appendChild(renderer.domElement);

  // ================= MATERIALES =================
  const wallMat = new THREE.MeshStandardMaterial({ color: 0x1c1f26, roughness: 0.9 });
  const floorMat = new THREE.MeshStandardMaterial({ color: 0x12141a, roughness: 0.65 });
  const woodMat = new THREE.MeshStandardMaterial({ color: 0x181716, roughness: 0.5 });
  const sofaMat = new THREE.MeshStandardMaterial({ color: 0x242b35, roughness: 0.85 });
  const frameMat = new THREE.MeshStandardMaterial({ color: 0x0a0c10, roughness: 0.4 });

  // 1. Suelo de la sala
  const floor = new THREE.Mesh(new THREE.PlaneGeometry(9, 7), floorMat);
  floor.rotation.x = -Math.PI / 2;
  floor.position.y = -0.6;
  floor.receiveShadow = true;
  scene.add(floor);

  // 2. Pared de Fondo
  const backWall = new THREE.Mesh(new THREE.PlaneGeometry(9, 4.5), wallMat);
  backWall.position.set(0, 1.4, -2.5);
  backWall.receiveShadow = true;
  scene.add(backWall);

  // 3. Pared Izquierda con Ventanal Alto
  const leftWallUpper = new THREE.Mesh(new THREE.BoxGeometry(0.2, 1.2, 7), wallMat);
  leftWallUpper.position.set(-3.6, 2.2, 0);
  scene.add(leftWallUpper);

  const leftWallLower = new THREE.Mesh(new THREE.BoxGeometry(0.2, 0.7, 7), wallMat);
  leftWallLower.position.set(-3.6, -0.25, 0);
  leftWallLower.receiveShadow = true;
  scene.add(leftWallLower);

  // Marco de Ventana
  const windowGroup = new THREE.Group();
  windowGroup.position.set(-3.5, 1.0, -0.2);
  const outerWindow = new THREE.Mesh(new THREE.BoxGeometry(0.08, 1.7, 2.2), frameMat);
  windowGroup.add(outerWindow);

  const divH = new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.05, 2.16), frameMat);
  windowGroup.add(divH);

  const divV = new THREE.Mesh(new THREE.BoxGeometry(0.1, 1.66, 0.05), frameMat);
  windowGroup.add(divV);

  // Vidrio azulado
  const glass = new THREE.Mesh(
    new THREE.PlaneGeometry(2.16, 1.66),
    new THREE.MeshBasicMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.12 })
  );
  glass.rotation.y = Math.PI / 2;
  windowGroup.add(glass);
  scene.add(windowGroup);

  // Haz de luz de luna
  const shaftGeo = new THREE.CylinderGeometry(0.5, 2.6, 5.2, 16, 1, true);
  const shaftMat = new THREE.MeshBasicMaterial({
    color: 0x38bdf8,
    transparent: true,
    opacity: 0.06,
    blending: THREE.AdditiveBlending,
    side: THREE.DoubleSide,
    depthWrite: false
  });
  shaftMesh = new THREE.Mesh(shaftGeo, shaftMat);
  shaftMesh.rotation.z = Math.PI / 3.4;
  shaftMesh.rotation.y = -Math.PI / 8;
  shaftMesh.position.set(-1.8, 0.7, -0.2);
  scene.add(shaftMesh);

  // 4. Puerta a Pasillo en la Pared Derecha
  const rightWall = new THREE.Mesh(new THREE.BoxGeometry(0.2, 4.5, 4.5), wallMat);
  rightWall.position.set(3.6, 1.4, 1.25);
  scene.add(rightWall);

  // Hueco de puerta en la pared derecha (fondo)
  const doorFrame = new THREE.Mesh(new THREE.BoxGeometry(0.25, 2.4, 1.2), frameMat);
  doorFrame.position.set(3.5, 0.6, -1.5);
  scene.add(doorFrame);

  // Luz que se cuela por la puerta del pasillo
  const hallGlow = new THREE.Mesh(
    new THREE.PlaneGeometry(1.1, 2.3),
    new THREE.MeshBasicMaterial({ color: 0xf59e0b, transparent: true, opacity: 0.25 })
  );
  hallGlow.rotation.y = -Math.PI / 2;
  hallGlow.position.set(3.48, 0.6, -1.5);
  scene.add(hallGlow);

  // ================= MOBILIARIO DE LA SALA =================
  // Mueble de Televisión (Credenza)
  const tvStand = new THREE.Mesh(new THREE.BoxGeometry(1.8, 0.45, 0.5), woodMat);
  tvStand.position.set(-0.6, -0.37, -2.1);
  tvStand.receiveShadow = true;
  tvStand.castShadow = true;
  scene.add(tvStand);

  // Televisor
  const tvFrame = new THREE.Mesh(
    new THREE.BoxGeometry(1.4, 0.85, 0.06),
    new THREE.MeshStandardMaterial({ color: 0x050505, roughness: 0.3 })
  );
  tvFrame.position.set(-0.6, 0.35, -2.05);
  tvFrame.castShadow = true;
  scene.add(tvFrame);

  // Pantalla encendida emisiva
  const tvScreenGeo = new THREE.PlaneGeometry(1.32, 0.78);
  const tvScreenMat = new THREE.MeshStandardMaterial({
    color: 0xe0f2fe,
    emissive: 0x7dd3fc,
    emissiveIntensity: tvIntensity.value * 2.0
  });
  tvScreenMesh = new THREE.Mesh(tvScreenGeo, tvScreenMat);
  tvScreenMesh.position.set(-0.6, 0.35, -2.01);
  scene.add(tvScreenMesh);

  // Sofá frente al televisor
  const sofaBase = new THREE.Mesh(new THREE.BoxGeometry(2.0, 0.35, 0.85), sofaMat);
  sofaBase.position.set(0.4, -0.42, 0.1);
  sofaBase.receiveShadow = true;
  sofaBase.castShadow = true;
  scene.add(sofaBase);

  const sofaBack = new THREE.Mesh(new THREE.BoxGeometry(2.0, 0.55, 0.25), sofaMat);
  sofaBack.position.set(0.4, -0.15, 0.5);
  sofaBack.castShadow = true;
  scene.add(sofaBack);

  // Sujeto / Silueta de personaje (Busto estilizado)
  const charGroup = new THREE.Group();
  charGroup.position.set(-0.1, -0.15, -0.6);

  const charMat = new THREE.MeshStandardMaterial({
    color: 0x94a3b8,
    roughness: 0.45,
    metalness: 0.1
  });

  const charTorso = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.26, 0.55, 24), charMat);
  charTorso.position.y = 0.28;
  charTorso.castShadow = true;
  charTorso.receiveShadow = true;
  charGroup.add(charTorso);

  const charHead = new THREE.Mesh(new THREE.SphereGeometry(0.16, 24, 24), charMat);
  charHead.position.set(0, 0.7, 0);
  charHead.scale.set(0.85, 1.1, 0.9);
  charHead.castShadow = true;
  charHead.receiveShadow = true;
  charGroup.add(charHead);

  scene.add(charGroup);

  // ================= LUCES DE LA ESCENA =================

  // 1. LUZ NATURAL (LUNA FRÍA EXTERIOR ~7500K)
  moonLight = new THREE.DirectionalLight(0x7dd3fc, moonIntensity.value);
  moonLight.position.set(-4.5, 2.5, 0.2);
  moonLight.target = charGroup;
  moonLight.castShadow = true;
  moonLight.shadow.mapSize.width = 1024;
  moonLight.shadow.mapSize.height = 1024;
  moonLight.shadow.bias = -0.0008;
  scene.add(moonLight);

  moonFill = new THREE.PointLight(0x38bdf8, moonIntensity.value * 0.35, 9.0);
  moonFill.position.set(-3.2, 1.2, -0.2);
  scene.add(moonFill);

  // 2. LUZ PRÁCTICA DEL TELEVISOR (RECT LIGHT / SPOT CIAN-BLANCO)
  tvLight = new THREE.SpotLight(0xbae6fd, tvIntensity.value, 6.0, Math.PI / 2.6, 0.6, 1.2);
  tvLight.position.set(-0.6, 0.35, -1.9);
  tvLight.target.position.set(0.2, 0.0, 0.3);
  tvLight.castShadow = true;
  tvLight.shadow.bias = -0.001;
  scene.add(tvLight);
  scene.add(tvLight.target);

  // 3. LUZ CÁLIDA DE PASILLO (TUNGSTENO ~2700K)
  hallLight = new THREE.PointLight(0xf59e0b, hallIntensity.value, 6.5, 1.5);
  hallLight.position.set(3.2, 0.8, -1.4);
  hallLight.castShadow = true;
  hallLight.shadow.bias = -0.001;
  scene.add(hallLight);

  // 4. LUZ DRAMÁTICA (RIM / RECORTE DE SILUETA)
  rimLight = new THREE.DirectionalLight(0xe0f2fe, rimIntensity.value);
  rimLight.position.set(1.5, 1.8, -1.8);
  rimLight.target = charGroup;
  rimLight.castShadow = false;
  scene.add(rimLight);

  // Luz ambiente muy tenue
  const ambient = new THREE.AmbientLight(0x06080e, 0.15);
  scene.add(ambient);

  updateLights();

  // ================= CONTROL DE CÁMARA =================
  const domEl = renderer.domElement;

  const onMouseDown = (e) => {
    isDragging = true;
    previousMousePosition = { x: e.clientX, y: e.clientY };
  };

  const onMouseMove = (e) => {
    if (!isDragging) return;
    const deltaX = e.clientX - previousMousePosition.x;
    const deltaY = e.clientY - previousMousePosition.y;

    cameraAngle.theta -= deltaX * 0.006;
    cameraAngle.phi += deltaY * 0.004;

    cameraAngle.theta = Math.max(-0.6, Math.min(0.7, cameraAngle.theta));
    cameraAngle.phi = Math.max(0.08, Math.min(0.55, cameraAngle.phi));

    updateCameraPos();
    previousMousePosition = { x: e.clientX, y: e.clientY };
  };

  const onMouseUp = () => {
    isDragging = false;
  };

  domEl.addEventListener('mousedown', onMouseDown);
  window.addEventListener('mousemove', onMouseMove);
  window.addEventListener('mouseup', onMouseUp);

  domEl.addEventListener('touchstart', (e) => {
    if (e.touches.length === 1) {
      isDragging = true;
      previousMousePosition = { x: e.touches[0].clientX, y: e.touches[0].clientY };
    }
  });
  window.addEventListener('touchmove', (e) => {
    if (!isDragging || e.touches.length !== 1) return;
    const deltaX = e.touches[0].clientX - previousMousePosition.x;
    const deltaY = e.touches[0].clientY - previousMousePosition.y;

    cameraAngle.theta -= deltaX * 0.006;
    cameraAngle.phi += deltaY * 0.004;
    cameraAngle.theta = Math.max(-0.6, Math.min(0.7, cameraAngle.theta));
    cameraAngle.phi = Math.max(0.08, Math.min(0.55, cameraAngle.phi));

    updateCameraPos();
    previousMousePosition = { x: e.touches[0].clientX, y: e.touches[0].clientY };
  });
  window.addEventListener('touchend', onMouseUp);

  let frameCount = 0;
  const animate = () => {
    animId = requestAnimationFrame(animate);
    frameCount++;

    // Efecto sutil de titileo en el televisor
    if (tvEnabled.value && tvLight && tvScreenMesh) {
      const flicker = 1.0 + Math.sin(frameCount * 0.15) * 0.06 + Math.cos(frameCount * 0.35) * 0.03;
      tvLight.intensity = tvIntensity.value * flicker;
      tvScreenMesh.material.emissiveIntensity = tvIntensity.value * 2.0 * flicker;
    }

    renderer.render(scene, camera);
  };
  animate();
};

const updateCameraPos = () => {
  if (!camera) return;
  const radius = 4.6;
  const x = radius * Math.sin(cameraAngle.theta) * Math.cos(cameraAngle.phi);
  const y = 0.5 + radius * Math.sin(cameraAngle.phi);
  const z = radius * Math.cos(cameraAngle.theta) * Math.cos(cameraAngle.phi);

  camera.position.set(x, y, z);
  camera.lookAt(0, 0.35, -0.4);
};

const updateLights = () => {
  if (moonLight && moonFill) {
    moonLight.visible = moonEnabled.value;
    moonFill.visible = moonEnabled.value;
    moonLight.intensity = moonIntensity.value;
    moonFill.intensity = moonIntensity.value * 0.35;
  }

  if (shaftMesh) {
    shaftMesh.visible = moonEnabled.value;
    shaftMesh.material.opacity = moonEnabled.value ? moonIntensity.value * 0.03 : 0.0;
  }

  if (tvLight && tvScreenMesh) {
    tvLight.visible = tvEnabled.value;
    tvLight.intensity = tvIntensity.value;
    tvScreenMesh.material.emissiveIntensity = tvEnabled.value ? tvIntensity.value * 2.0 : 0.0;
  }

  if (hallLight) {
    hallLight.visible = hallEnabled.value;
    hallLight.intensity = hallIntensity.value;
  }

  if (rimLight) {
    rimLight.visible = rimEnabled.value;
    rimLight.intensity = rimIntensity.value;
  }
};

onMounted(() => {
  initThree();
});

onBeforeUnmount(() => {
  if (animId) cancelAnimationFrame(animId);
  if (renderer && renderer.domElement) {
    renderer.dispose();
  }
});
</script>

<style scoped>
.technical-figure {
  margin: 20px 0;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  background: #ffffff;
  overflow: hidden;
}

.figure-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 14px;
  background: #f9fafb;
  border-bottom: 1px solid #e5e7eb;
}

.header-left {
  display: flex;
  align-items: baseline;
  gap: 10px;
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

.viewport-hint {
  font-size: 10.5px;
  color: #9ca3af;
  font-family: monospace;
}

.presets-bar {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 14px;
  background: #f3f4f6;
  border-bottom: 1px solid #e5e7eb;
  flex-wrap: wrap;
}

.preset-title {
  font-size: 11px;
  font-weight: 600;
  color: #4b5563;
}

.preset-buttons {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.preset-btn {
  padding: 3px 10px;
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
  background: #f9fafb;
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
  height: 300px;
  cursor: grab;
}

.canvas-wrapper:active {
  cursor: grabbing;
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

.toggle-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.toggle-row input[type="checkbox"] {
  accent-color: #111827;
  width: 15px;
  height: 15px;
  cursor: pointer;
}

.toggle-row input[type="range"] {
  flex: 1;
  accent-color: #111827;
  cursor: pointer;
}

input[type="range"] {
  width: 100%;
  accent-color: #111827;
  cursor: pointer;
}

.hints {
  display: flex;
  justify-content: space-between;
  font-size: 9.5px;
  color: #6b7280;
}

.methodology-note {
  background: #f9fafb;
  border-top: 1px solid #e5e7eb;
  padding: 10px 14px;
  font-size: 11.5px;
  color: #4b5563;
  line-height: 1.45;
}

.methodology-note strong {
  color: #111827;
}

@media (max-width: 768px) {
  .controls-grid {
    grid-template-columns: 1fr;
  }
  .presets-bar {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
