<template>
  <div class="technical-figure">
    <div class="figure-header">
      <span class="label">SIMULADOR INTERACTIVO</span>
      <span class="desc">Iluminación de Interiores — Metodología Chris Brejon (Capas y Contraste Térmico)</span>
    </div>
    
    <!-- VIEWPORT 3D: HABITACIÓN INTERIOR -->
    <div class="canvas-wrapper" ref="canvasContainer"></div>

    <!-- CONTROLES PARAMÉTRICOS POR CAPAS DE BREJON -->
    <div class="controls-grid">
      
      <!-- CAPA 1: NATURAL LIGHT (VENTANA EXTERIOR) -->
      <div class="control-card">
        <div class="control-label">
          <span>1. Natural Light (Ventana Exterior):</span>
          <code>{{ naturalEnabled ? naturalIntensity.toFixed(1) + ' lux' : 'Apagada' }}</code>
        </div>
        <div class="toggle-row">
          <input type="checkbox" v-model="naturalEnabled" @change="updateLights" />
          <input type="range" min="0" max="4" step="0.1" v-model.number="naturalIntensity" :disabled="!naturalEnabled" @input="updateLights" />
        </div>
        <div class="hints"><span>Luz fría de cielo (~6500K) ingresando por el vano</span></div>
      </div>

      <!-- CAPA 2: PRACTICAL LIGHT (LÁMPARA DE ESCRITORIO) -->
      <div class="control-card">
        <div class="control-label">
          <span>2. Practical Light (Lámpara de Set):</span>
          <code>{{ practicalEnabled ? practicalIntensity.toFixed(1) + ' cd' : 'Apagada' }}</code>
        </div>
        <div class="toggle-row">
          <input type="checkbox" v-model="practicalEnabled" @change="updateLights" />
          <input type="range" min="0" max="3" step="0.1" v-model.number="practicalIntensity" :disabled="!practicalEnabled" @input="updateLights" />
        </div>
        <div class="hints"><span>Fuente visible cálida (~2800K) en el set dressing</span></div>
      </div>

      <!-- CAPA 3: DRAMATIC LIGHT (LUZ DE ESTUDIO MOTIVADA) -->
      <div class="control-card">
        <div class="control-label">
          <span>3. Dramatic Light (Luz de Estudio):</span>
          <code>{{ dramaticEnabled ? dramaticIntensity.toFixed(1) + ' cd' : 'Apagada' }}</code>
        </div>
        <div class="toggle-row">
          <input type="checkbox" v-model="dramaticEnabled" @change="updateLights" />
          <input type="range" min="0" max="4" step="0.1" v-model.number="dramaticIntensity" :disabled="!dramaticEnabled" @input="updateLights" />
        </div>
        <div class="hints"><span>Foco fuera de cuadro que esculpe el sujeto motivado por la lámpara</span></div>
      </div>

      <!-- PARÁMETRO FÍSICO: SOURCE RADIUS (ESPECULARIDAD REAL) -->
      <div class="control-card">
        <div class="control-label">
          <span>4. Source Radius (Radio de la Fuente):</span>
          <code>{{ sourceRadius.toFixed(1) }} cm</code>
        </div>
        <input type="range" min="0.1" max="2.0" step="0.1" v-model.number="sourceRadius" @input="updateLights" />
        <div class="hints"><span>0.1 (Punto nítido)</span><span>2.0 (Reflejo suave de bombilla física)</span></div>
      </div>

    </div>

    <!-- NOTA METODOLÓGICA DE BREJON -->
    <div class="methodology-note">
      <strong>Flujo de Trabajo Brejon:</strong> Observa cómo la <em>Practical Light</em> establece la excusa visual en la mesa, pero es la <em>Dramatic Light</em> la que realmente modela el volumen del busto sin quemar la lámpara.
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
const dramaticIntensity = ref(2.5);

const sourceRadius = ref(0.8);

let scene, camera, renderer, animId;
let windowLight, windowFill, practicalLight, dramaticLight, lampBulbMesh, bustMesh;

const initThree = async () => {
  if (typeof window === 'undefined') return;
  const THREE = await import('three');

  const container = canvasContainer.value;
  if (!container) return;

  const width = container.clientWidth || 600;
  const height = 270;

  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x0a0c10);

  camera = new THREE.PerspectiveCamera(38, width / height, 0.1, 100);
  camera.position.set(0, 1.4, 4.4);
  camera.lookAt(0, 0.5, 0);

  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(width, height);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  container.innerHTML = '';
  container.appendChild(renderer.domElement);

  // ================= GEOMETRÍA DE HABITACIÓN =================
  const wallMat = new THREE.MeshStandardMaterial({ color: 0x3f3f46, roughness: 0.85 });
  const floorMat = new THREE.MeshStandardMaterial({ color: 0x27272a, roughness: 0.7 });

  // Suelo
  const floorGeo = new THREE.PlaneGeometry(8, 6);
  const floor = new THREE.Mesh(floorGeo, floorMat);
  floor.rotation.x = -Math.PI / 2;
  floor.position.y = -0.6;
  floor.receiveShadow = true;
  scene.add(floor);

  // Pared de fondo
  const backWallGeo = new THREE.PlaneGeometry(8, 4);
  const backWall = new THREE.Mesh(backWallGeo, wallMat);
  backWall.position.set(0, 1.4, -2.5);
  backWall.receiveShadow = true;
  scene.add(backWall);

  // Pared izquierda con hueco de ventana
  const leftWallUpper = new THREE.Mesh(new THREE.BoxGeometry(0.2, 1.5, 6), wallMat);
  leftWallUpper.position.set(-3.5, 2.0, 0);
  scene.add(leftWallUpper);

  const leftWallLower = new THREE.Mesh(new THREE.BoxGeometry(0.2, 0.8, 6), wallMat);
  leftWallLower.position.set(-3.5, -0.2, 0);
  leftWallLower.receiveShadow = true;
  scene.add(leftWallLower);

  // Marco de ventana
  const windowFrameMat = new THREE.MeshStandardMaterial({ color: 0x18181b, roughness: 0.5 });
  const frameH = new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.08, 2.0), windowFrameMat);
  frameH.position.set(-3.4, 0.9, -0.5);
  scene.add(frameH);

  // ================= MOBILIARIO Y OBJETO DE PRUEBA =================
  // Mesa / Escritorio
  const deskMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.6 });
  const deskTop = new THREE.Mesh(new THREE.BoxGeometry(2.0, 0.1, 1.2), deskMat);
  deskTop.position.set(0.1, 0.0, -0.4);
  deskTop.receiveShadow = true;
  deskTop.castShadow = true;
  scene.add(deskTop);

  const deskLeg1 = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 0.6), deskMat);
  deskLeg1.position.set(-0.8, -0.3, -0.8);
  scene.add(deskLeg1);
  const deskLeg2 = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 0.6), deskMat);
  deskLeg2.position.set(1.0, -0.3, -0.8);
  scene.add(deskLeg2);

  // Sujeto: Busto / Estatua sobre la mesa
  const bustGeo = new THREE.CylinderGeometry(0.18, 0.28, 0.65, 32);
  const bustMat = new THREE.MeshStandardMaterial({ color: 0xe2e8f0, roughness: 0.35, metalness: 0.1 });
  bustMesh = new THREE.Mesh(bustGeo, bustMat);
  bustMesh.position.set(-0.2, 0.38, -0.4);
  bustMesh.castShadow = true;
  bustMesh.receiveShadow = true;
  scene.add(bustMesh);

  // Cabeza de la estatua
  const headGeo = new THREE.SphereGeometry(0.2, 24, 24);
  const head = new THREE.Mesh(headGeo, bustMat);
  head.position.set(-0.2, 0.8, -0.4);
  head.castShadow = true;
  scene.add(head);

  // ================= LÁMPARA DE MESA (PRACTICAL) =================
  const lampBaseMat = new THREE.MeshStandardMaterial({ color: 0x71717a, roughness: 0.3, metalness: 0.8 });
  const lampBase = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.14, 0.04, 24), lampBaseMat);
  lampBase.position.set(0.65, 0.07, -0.5);
  scene.add(lampBase);

  const lampPole = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.02, 0.45, 16), lampBaseMat);
  lampPole.position.set(0.65, 0.3, -0.5);
  scene.add(lampPole);

  const shadeMat = new THREE.MeshStandardMaterial({ color: 0x27272a, roughness: 0.5, side: THREE.DoubleSide });
  const lampShade = new THREE.Mesh(new THREE.ConeGeometry(0.18, 0.2, 24, 1, true), shadeMat);
  lampShade.position.set(0.65, 0.52, -0.5);
  scene.add(lampShade);

  // Ampolleta visible emisiva
  const bulbMat = new THREE.MeshStandardMaterial({
    color: 0xffedd5,
    emissive: 0xfb923c,
    emissiveIntensity: practicalIntensity.value * 2.5
  });
  lampBulbMesh = new THREE.Mesh(new THREE.SphereGeometry(0.06, 16, 16), bulbMat);
  lampBulbMesh.position.set(0.65, 0.46, -0.5);
  scene.add(lampBulbMesh);

  // ================= LUCES DE LA ESCENA =================

  // 1. LUZ NATURAL (VENTANA EXTERIOR A 6500K - AZUL/BLANCO FRÍO)
  windowLight = new THREE.DirectionalLight(0x93c5fd, naturalIntensity.value);
  windowLight.position.set(-4.0, 2.5, -0.5);
  windowLight.target = bustMesh;
  windowLight.castShadow = true;
  windowLight.shadow.mapSize.width = 1024;
  windowLight.shadow.mapSize.height = 1024;
  windowLight.shadow.bias = -0.001;
  scene.add(windowLight);

  windowFill = new THREE.PointLight(0xbfdbfe, naturalIntensity.value * 0.4, 7.0);
  windowFill.position.set(-3.2, 1.2, -0.5);
  scene.add(windowFill);

  // 2. LUZ PRÁCTICA (AMPOLLETA CÁLIDA A 2800K)
  practicalLight = new THREE.PointLight(0xfb923c, practicalIntensity.value, 2.8, 1.8);
  practicalLight.position.set(0.65, 0.44, -0.5);
  practicalLight.castShadow = true;
  practicalLight.shadow.bias = -0.002;
  scene.add(practicalLight);

  // 3. LUZ DRAMÁTICA (STUDIO LIGHT MOTIVADA POR LA LÁMPARA)
  dramaticLight = new THREE.DirectionalLight(0xfed7aa, dramaticIntensity.value);
  dramaticLight.position.set(1.5, 1.2, 0.6);
  dramaticLight.target = bustMesh;
  dramaticLight.castShadow = true;
  scene.add(dramaticLight);

  // Luz ambiente base muy tenue
  const ambient = new THREE.AmbientLight(0x111827, 0.2);
  scene.add(ambient);

  updateLights();

  const animate = () => {
    animId = requestAnimationFrame(animate);
    renderer.render(scene, camera);
  };
  animate();
};

const updateLights = () => {
  if (windowLight && windowFill) {
    windowLight.visible = naturalEnabled.value;
    windowFill.visible = naturalEnabled.value;
    windowLight.intensity = naturalIntensity.value;
    windowFill.intensity = naturalIntensity.value * 0.4;
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

  if (bustMesh && bustMesh.material) {
    // Simular Source Radius suavizando la rugosidad especular aparente
    bustMesh.material.roughness = 0.25 + (sourceRadius.value * 0.2);
    bustMesh.material.needsUpdate = true;
  }
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
  height: 270px;
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
  font-size: 9px;
  color: #6b7280;
}

.methodology-note {
  background: #f9fafb;
  border-top: 1px solid #e5e7eb;
  padding: 10px 14px;
  font-size: 11px;
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
}
</style>
