<template>
  <div class="technical-figure">
    <div class="figure-header">
      <div class="header-left">
        <span class="label">SIMULADOR 3D INTERACTIVO</span>
        <span class="desc">Metodología Chris Brejon — Iluminación de Interiores en 3 Capas</span>
      </div>
      <span class="viewport-hint">Arrastra para rotar la vista</span>
    </div>

    <!-- PRESETS PEDAGÓGICOS -->
    <div class="presets-bar">
      <span class="preset-title">Presets rápidos:</span>
      <div class="preset-buttons">
        <button
          :class="['preset-btn', { active: currentPreset === 'full' }]"
          @click="applyPreset('full')"
        >
          Setup Completo Brejon
        </button>
        <button
          :class="['preset-btn', { active: currentPreset === 'window-only' }]"
          @click="applyPreset('window-only')"
        >
          Solo Ventana Fría
        </button>
        <button
          :class="['preset-btn', { active: currentPreset === 'no-dramatic' }]"
          @click="applyPreset('no-dramatic')"
        >
          Sin Luz Dramática (Ver el problema)
        </button>
        <button
          :class="['preset-btn', { active: currentPreset === 'dramatic-only' }]"
          @click="applyPreset('dramatic-only')"
        >
          Solo Luz Dramática
        </button>
      </div>
    </div>
    
    <!-- VIEWPORT 3D -->
    <div class="canvas-wrapper" ref="canvasContainer"></div>

    <!-- CONTROLES PARAMÉTRICOS POR CAPAS -->
    <div class="controls-grid">
      
      <!-- CAPA 1: NATURAL LIGHT (VENTANA EXTERIOR) -->
      <div class="control-card">
        <div class="control-label">
          <span>1. Natural Light (Ventana Exterior):</span>
          <code>{{ naturalEnabled ? naturalIntensity.toFixed(1) + ' lux' : 'Apagada' }}</code>
        </div>
        <div class="toggle-row">
          <input type="checkbox" v-model="naturalEnabled" @change="onManualChange" />
          <input type="range" min="0" max="4" step="0.1" v-model.number="naturalIntensity" :disabled="!naturalEnabled" @input="onManualChange" />
        </div>
        <div class="hints"><span>Luz fría exterior (~6.500K) que entra por el vano</span></div>
      </div>

      <!-- CAPA 2: PRACTICAL LIGHT (LÁMPARA DE MESA) -->
      <div class="control-card">
        <div class="control-label">
          <span>2. Practical Light (Lámpara visible):</span>
          <code>{{ practicalEnabled ? practicalIntensity.toFixed(1) + ' cd' : 'Apagada' }}</code>
        </div>
        <div class="toggle-row">
          <input type="checkbox" v-model="practicalEnabled" @change="onManualChange" />
          <input type="range" min="0" max="3" step="0.1" v-model.number="practicalIntensity" :disabled="!practicalEnabled" @input="onManualChange" />
        </div>
        <div class="hints"><span>Fuente visible cálida (~2.700K) en el set dressing</span></div>
      </div>

      <!-- CAPA 3: DRAMATIC LIGHT (LUZ DE ESTUDIO MOTIVADA) -->
      <div class="control-card">
        <div class="control-label">
          <span>3. Dramatic Light (Luz de Estudio):</span>
          <code>{{ dramaticEnabled ? dramaticIntensity.toFixed(1) + ' cd' : 'Apagada' }}</code>
        </div>
        <div class="toggle-row">
          <input type="checkbox" v-model="dramaticEnabled" @change="onManualChange" />
          <input type="range" min="0" max="4" step="0.1" v-model.number="dramaticIntensity" :disabled="!dramaticEnabled" @input="onManualChange" />
        </div>
        <div class="hints"><span>Foco invisible fuera de cuadro que esculpe el busto</span></div>
      </div>

      <!-- PARÁMETRO FÍSICO: SOURCE RADIUS -->
      <div class="control-card">
        <div class="control-label">
          <span>4. Source Radius (Radio de la Fuente):</span>
          <code>{{ sourceRadius.toFixed(1) }} cm</code>
        </div>
        <input type="range" min="0.1" max="2.0" step="0.1" v-model.number="sourceRadius" @input="updateLights" />
        <div class="hints"><span>0.1 (Punto nítido irreal)</span><span>2.0 (Reflejo suave de bombilla real)</span></div>
      </div>

    </div>

    <!-- EXPLICACIÓN CLARA DEL EJEMPLO -->
    <div class="methodology-note">
      <strong>Clave del método Brejon:</strong> Si pruebas el botón <em>"Sin Luz Dramática"</em>, notarás que la lámpara sobre la mesa solo ilumina la parte inferior y deja la cara del busto empastada en sombras. Si le subiéramos tanta potencia a la lámpara para iluminar la cara, quemaríamos la mesa en blanco puro. La solución profesional es dejar la lámpara con potencia suave (como excusa visual) y sumar la <em>Luz Dramática</em> invisible para esculpir los rasgos.
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';

const canvasContainer = ref(null);

const naturalEnabled = ref(true);
const naturalIntensity = ref(2.2);

const practicalEnabled = ref(true);
const practicalIntensity = ref(1.4);

const dramaticEnabled = ref(true);
const dramaticIntensity = ref(2.4);

const sourceRadius = ref(0.8);
const currentPreset = ref('full');

let scene, camera, renderer, animId;
let windowLight, windowFill, practicalLight, dramaticLight, lampBulbMesh, bustGroup, bustMaterial, shaftMesh;
let isDragging = false;
let previousMousePosition = { x: 0, y: 0 };
let cameraAngle = { theta: 0.1, phi: 0.28 }; // Rotación esférica suave

const applyPreset = (presetKey) => {
  currentPreset.value = presetKey;
  if (presetKey === 'full') {
    naturalEnabled.value = true;
    naturalIntensity.value = 2.2;
    practicalEnabled.value = true;
    practicalIntensity.value = 1.4;
    dramaticEnabled.value = true;
    dramaticIntensity.value = 2.4;
  } else if (presetKey === 'window-only') {
    naturalEnabled.value = true;
    naturalIntensity.value = 2.8;
    practicalEnabled.value = false;
    practicalIntensity.value = 0.0;
    dramaticEnabled.value = false;
    dramaticIntensity.value = 0.0;
  } else if (presetKey === 'no-dramatic') {
    naturalEnabled.value = true;
    naturalIntensity.value = 1.8;
    practicalEnabled.value = true;
    practicalIntensity.value = 2.0;
    dramaticEnabled.value = false;
    dramaticIntensity.value = 0.0;
  } else if (presetKey === 'dramatic-only') {
    naturalEnabled.value = false;
    naturalIntensity.value = 0.0;
    practicalEnabled.value = false;
    practicalIntensity.value = 0.0;
    dramaticEnabled.value = true;
    dramaticIntensity.value = 3.0;
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
  scene.background = new THREE.Color(0x0c0e14);

  camera = new THREE.PerspectiveCamera(36, width / height, 0.1, 100);
  updateCameraPos();

  renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
  renderer.setSize(width, height);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;
  container.innerHTML = '';
  container.appendChild(renderer.domElement);

  // ================= MATERIALES DE LA HABITACIÓN =================
  const wallMat = new THREE.MeshStandardMaterial({ color: 0x27272a, roughness: 0.85 });
  const floorMat = new THREE.MeshStandardMaterial({ color: 0x18181b, roughness: 0.5, metalness: 0.05 });
  const frameMat = new THREE.MeshStandardMaterial({ color: 0x09090b, roughness: 0.4 });
  const glassMat = new THREE.MeshBasicMaterial({ color: 0x60a5fa, transparent: true, opacity: 0.15 });

  // 1. Suelo
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

  // Cuadro decorativo en la pared
  const artFrame = new THREE.Mesh(new THREE.BoxGeometry(1.6, 1.0, 0.04), frameMat);
  artFrame.position.set(-0.2, 1.6, -2.47);
  artFrame.receiveShadow = true;
  scene.add(artFrame);

  const artCanvas = new THREE.Mesh(
    new THREE.PlaneGeometry(1.5, 0.9),
    new THREE.MeshStandardMaterial({ color: 0x3b4252, roughness: 0.7 })
  );
  artCanvas.position.set(-0.2, 1.6, -2.44);
  scene.add(artCanvas);

  // 3. Pared Izquierda con Hueco de Ventana Atelier
  const leftWallUpper = new THREE.Mesh(new THREE.BoxGeometry(0.2, 1.4, 7), wallMat);
  leftWallUpper.position.set(-3.6, 2.1, 0);
  scene.add(leftWallUpper);

  const leftWallLower = new THREE.Mesh(new THREE.BoxGeometry(0.2, 0.8, 7), wallMat);
  leftWallLower.position.set(-3.6, -0.2, 0);
  leftWallLower.receiveShadow = true;
  scene.add(leftWallLower);

  // Rejilla de Ventana (Estilo Taller / Atelier - 6 paneles)
  const windowGroup = new THREE.Group();
  windowGroup.position.set(-3.5, 0.9, -0.4);

  // Marco exterior
  const outerFrame = new THREE.Mesh(new THREE.BoxGeometry(0.08, 1.4, 1.8), frameMat);
  windowGroup.add(outerFrame);

  // Parteluz horizontal
  const dividerH = new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.05, 1.76), frameMat);
  windowGroup.add(dividerH);

  // Parteluces verticales (2 divisiones = 3 columnas)
  const dividerV1 = new THREE.Mesh(new THREE.BoxGeometry(0.1, 1.36, 0.05), frameMat);
  dividerV1.position.z = -0.55;
  windowGroup.add(dividerV1);

  const dividerV2 = new THREE.Mesh(new THREE.BoxGeometry(0.1, 1.36, 0.05), frameMat);
  dividerV2.position.z = 0.55;
  windowGroup.add(dividerV2);

  // Vidrio azulado translúcido
  const windowGlass = new THREE.Mesh(new THREE.PlaneGeometry(1.76, 1.36), glassMat);
  windowGlass.rotation.y = Math.PI / 2;
  windowGroup.add(windowGlass);

  scene.add(windowGroup);

  // Haz de luz volumétrico suave desde la ventana
  const shaftGeo = new THREE.CylinderGeometry(0.6, 2.4, 5.0, 16, 1, true);
  const shaftMat = new THREE.MeshBasicMaterial({
    color: 0x93c5fd,
    transparent: true,
    opacity: 0.07,
    blending: THREE.AdditiveBlending,
    side: THREE.DoubleSide,
    depthWrite: false
  });
  shaftMesh = new THREE.Mesh(shaftGeo, shaftMat);
  shaftMesh.rotation.z = Math.PI / 3.2;
  shaftMesh.rotation.y = -Math.PI / 7;
  shaftMesh.position.set(-1.8, 0.6, -0.4);
  scene.add(shaftMesh);

  // ================= MOBILIARIO Y OBJETO HERO =================
  // Escritorio de Madera Oscura
  const deskMat = new THREE.MeshStandardMaterial({ color: 0x1e222d, roughness: 0.45 });
  const deskTop = new THREE.Mesh(new THREE.BoxGeometry(2.3, 0.08, 1.3), deskMat);
  deskTop.position.set(0.1, 0.0, -0.4);
  deskTop.receiveShadow = true;
  deskTop.castShadow = true;
  scene.add(deskTop);

  // Patas de metal oscuro
  const legMat = new THREE.MeshStandardMaterial({ color: 0x111827, roughness: 0.3, metalness: 0.7 });
  const legCoords = [
    [-0.95, -0.3, -0.95],
    [1.15, -0.3, -0.95],
    [-0.95, -0.3, 0.15],
    [1.15, -0.3, 0.15]
  ];
  legCoords.forEach(([x, y, z]) => {
    const leg = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.025, 0.6, 16), legMat);
    leg.position.set(x, y, z);
    leg.castShadow = true;
    scene.add(leg);
  });

  // Libreta de apuntes sobre la mesa
  const bookCover = new THREE.Mesh(
    new THREE.BoxGeometry(0.35, 0.03, 0.45),
    new THREE.MeshStandardMaterial({ color: 0x475569, roughness: 0.8 })
  );
  bookCover.position.set(0.15, 0.05, -0.2);
  bookCover.rotation.y = 0.2;
  bookCover.receiveShadow = true;
  scene.add(bookCover);

  // ================= ESCULTURA HERO: BUSTO CLÁSICO ESTILIZADO =================
  bustGroup = new THREE.Group();
  bustGroup.position.set(-0.25, 0.04, -0.4);

  bustMaterial = new THREE.MeshStandardMaterial({
    color: 0xf1f5f9,
    roughness: 0.35,
    metalness: 0.05
  });

  // Pedestal de mármol/piedra
  const plinth = new THREE.Mesh(new THREE.BoxGeometry(0.32, 0.12, 0.32), deskMat);
  plinth.position.y = 0.06;
  plinth.castShadow = true;
  plinth.receiveShadow = true;
  bustGroup.add(plinth);

  // Pecho / Torso
  const chest = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.24, 0.42, 24), bustMaterial);
  chest.position.y = 0.32;
  chest.castShadow = true;
  chest.receiveShadow = true;
  bustGroup.add(chest);

  // Cuello
  const neck = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.09, 0.15, 16), bustMaterial);
  neck.position.y = 0.58;
  neck.castShadow = true;
  neck.receiveShadow = true;
  bustGroup.add(neck);

  // Cabeza con forma de busto escultórico
  const head = new THREE.Mesh(new THREE.SphereGeometry(0.17, 24, 24), bustMaterial);
  head.position.set(0, 0.76, 0);
  head.scale.set(0.85, 1.15, 0.95);
  head.castShadow = true;
  head.receiveShadow = true;
  bustGroup.add(head);

  // Nariz / Perfil facial (para proyectar sombras clave en la mejilla)
  const nose = new THREE.Mesh(new THREE.ConeGeometry(0.04, 0.1, 12), bustMaterial);
  nose.rotation.x = Math.PI / 2;
  nose.position.set(0.0, 0.75, 0.16);
  nose.castShadow = true;
  bustGroup.add(nose);

  scene.add(bustGroup);

  // ================= LÁMPARA DE ESCRITORIO (PRACTICAL LIGHT) =================
  const lampGroup = new THREE.Group();
  lampGroup.position.set(0.72, 0.04, -0.45);

  const brassMat = new THREE.MeshStandardMaterial({ color: 0xd4af37, roughness: 0.3, metalness: 0.85 });
  const lampBase = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.14, 0.03, 24), brassMat);
  lampBase.castShadow = true;
  lampGroup.add(lampBase);

  // Brazo curvado
  const stem1 = new THREE.Mesh(new THREE.CylinderGeometry(0.018, 0.018, 0.42, 16), brassMat);
  stem1.position.set(0, 0.22, 0);
  lampGroup.add(stem1);

  const arm = new THREE.Mesh(new THREE.CylinderGeometry(0.015, 0.015, 0.28, 16), brassMat);
  arm.position.set(-0.1, 0.44, 0);
  arm.rotation.z = Math.PI / 4;
  lampGroup.add(arm);

  // Pantalla de la lámpara apuntando hacia la mesa y el busto
  const shadeMat = new THREE.MeshStandardMaterial({ color: 0x15803d, roughness: 0.3, metalness: 0.2, side: THREE.DoubleSide });
  const shade = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.07, 0.18, 24, 1, true), shadeMat);
  shade.position.set(-0.2, 0.48, 0);
  shade.rotation.z = -Math.PI / 3;
  shade.castShadow = true;
  lampGroup.add(shade);

  // Ampolleta visible emisiva
  const bulbMat = new THREE.MeshStandardMaterial({
    color: 0xffedd5,
    emissive: 0xfb923c,
    emissiveIntensity: practicalIntensity.value * 2.5
  });
  lampBulbMesh = new THREE.Mesh(new THREE.SphereGeometry(0.045, 16, 16), bulbMat);
  lampBulbMesh.position.set(-0.2, 0.46, 0);
  lampGroup.add(lampBulbMesh);

  scene.add(lampGroup);

  // ================= LUCES DE LA ESCENA (3 CAPAS DE BREJON) =================

  // 1. NATURAL LIGHT: Sol / Cielo frío exterior (~6500K)
  windowLight = new THREE.DirectionalLight(0x93c5fd, naturalIntensity.value);
  windowLight.position.set(-4.5, 2.8, -0.4);
  windowLight.target = bustGroup;
  windowLight.castShadow = true;
  windowLight.shadow.mapSize.width = 1024;
  windowLight.shadow.mapSize.height = 1024;
  windowLight.shadow.bias = -0.0008;
  scene.add(windowLight);

  windowFill = new THREE.PointLight(0xbfdbfe, naturalIntensity.value * 0.4, 8.0);
  windowFill.position.set(-3.2, 1.2, -0.4);
  scene.add(windowFill);

  // 2. PRACTICAL LIGHT: Lámpara de mesa (~2700K cálida)
  practicalLight = new THREE.PointLight(0xfb923c, practicalIntensity.value, 3.2, 2.0);
  practicalLight.position.set(0.52, 0.5, -0.45);
  practicalLight.castShadow = true;
  practicalLight.shadow.bias = -0.001;
  scene.add(practicalLight);

  // 3. DRAMATIC LIGHT: Luz de estudio invisible motivada por la lámpara
  dramaticLight = new THREE.DirectionalLight(0xfed7aa, dramaticIntensity.value);
  dramaticLight.position.set(1.8, 1.3, 0.7);
  dramaticLight.target = bustGroup;
  dramaticLight.castShadow = true;
  dramaticLight.shadow.mapSize.width = 1024;
  dramaticLight.shadow.mapSize.height = 1024;
  dramaticLight.shadow.bias = -0.0008;
  scene.add(dramaticLight);

  // Luz ambiental mínima para que las sombras no sean negro total
  const ambient = new THREE.AmbientLight(0x0f172a, 0.18);
  scene.add(ambient);

  updateLights();

  // ================= INTERACCIÓN CON RATÓN / TOUCH =================
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

    // Limitar ángulos para no atravesar el suelo ni girar detrás del muro
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

  // Soporte táctil en dispositivos móviles
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

  const animate = () => {
    animId = requestAnimationFrame(animate);
    renderer.render(scene, camera);
  };
  animate();
};

const updateCameraPos = () => {
  if (!camera) return;
  const radius = 4.4;
  const x = radius * Math.sin(cameraAngle.theta) * Math.cos(cameraAngle.phi);
  const y = 0.5 + radius * Math.sin(cameraAngle.phi);
  const z = radius * Math.cos(cameraAngle.theta) * Math.cos(cameraAngle.phi);

  camera.position.set(x, y, z);
  camera.lookAt(0, 0.45, -0.3);
};

const updateLights = () => {
  if (windowLight && windowFill) {
    windowLight.visible = naturalEnabled.value;
    windowFill.visible = naturalEnabled.value;
    windowLight.intensity = naturalIntensity.value;
    windowFill.intensity = naturalIntensity.value * 0.4;
  }

  if (shaftMesh) {
    shaftMesh.visible = naturalEnabled.value;
    shaftMesh.material.opacity = naturalEnabled.value ? naturalIntensity.value * 0.035 : 0.0;
  }

  if (practicalLight && lampBulbMesh) {
    practicalLight.visible = practicalEnabled.value;
    practicalLight.intensity = practicalIntensity.value;
    lampBulbMesh.material.emissiveIntensity = practicalEnabled.value ? practicalIntensity.value * 2.5 : 0.0;
  }

  if (dramaticLight) {
    dramaticLight.visible = dramaticEnabled.value;
    dramaticLight.intensity = dramaticIntensity.value;
  }

  if (bustMaterial) {
    // Simular el efecto visual de Source Radius
    bustMaterial.roughness = 0.22 + (sourceRadius.value * 0.22);
    bustMaterial.needsUpdate = true;
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
