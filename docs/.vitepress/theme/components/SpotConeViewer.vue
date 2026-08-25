<template>
  <div class="technical-figure">
    <div class="figure-header">
      <span class="label">SIMULADOR INTERACTIVO</span>
      <span class="desc">Conos de una Spot Light (Inner vs. Outer Cone Angle)</span>
    </div>
    
    <div class="canvas-wrapper" ref="canvasContainer"></div>

    <div class="controls-panel">
      <div class="control-group">
        <div class="control-label">
          <span>Inner Cone Angle (Ángulo Interno):</span>
          <code>{{ innerAngle }}° (100% de luz)</code>
        </div>
        <input type="range" min="5" max="60" step="1" v-model.number="innerAngle" @input="validateAndSetSpot" />
        <div class="hints"><span>Haz central concentrado</span></div>
      </div>

      <div class="control-group">
        <div class="control-label">
          <span>Outer Cone Angle (Ángulo Externo):</span>
          <code>{{ outerAngle }}° (Borde difuso)</code>
        </div>
        <input type="range" min="10" max="75" step="1" v-model.number="outerAngle" @input="validateAndSetSpot" />
        <div class="hints"><span>Penumbra suave de caída</span></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';

const canvasContainer = ref(null);
const innerAngle = ref(20);
const outerAngle = ref(45);

let scene, camera, renderer, spotLight, animId, targetObj;

const validateAndSetSpot = () => {
  if (innerAngle.value >= outerAngle.value) {
    innerAngle.value = outerAngle.value - 2;
  }
  updateSpot();
};

const initThree = async () => {
  if (typeof window === 'undefined') return;
  const THREE = await import('three');

  const container = canvasContainer.value;
  if (!container) return;

  const width = container.clientWidth || 600;
  const height = 250;

  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x111217);

  camera = new THREE.PerspectiveCamera(40, width / height, 0.1, 100);
  camera.position.set(0, 1.8, 4.2);
  camera.lookAt(0, 0.4, 0);

  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(width, height);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  container.innerHTML = '';
  container.appendChild(renderer.domElement);

  // Suelo y pared
  const floorGeo = new THREE.PlaneGeometry(8, 8);
  const wallMat = new THREE.MeshStandardMaterial({ color: 0x52525b, roughness: 0.8 });
  const floor = new THREE.Mesh(floorGeo, wallMat);
  floor.rotation.x = -Math.PI / 2;
  floor.position.y = -0.5;
  scene.add(floor);

  const wallGeo = new THREE.PlaneGeometry(8, 5);
  const wall = new THREE.Mesh(wallGeo, wallMat);
  wall.position.z = -1.8;
  wall.position.y = 1.5;
  scene.add(wall);

  // Spot Light
  targetObj = new THREE.Object3D();
  targetObj.position.set(0, 0.8, -1.8);
  scene.add(targetObj);

  spotLight = new THREE.SpotLight(0xfffaed, 25);
  spotLight.position.set(0, 2.5, 1.2);
  spotLight.target = targetObj;
  spotLight.distance = 8;
  scene.add(spotLight);

  const ambient = new THREE.AmbientLight(0x1e293b, 0.2);
  scene.add(ambient);

  updateSpot();

  const animate = () => {
    animId = requestAnimationFrame(animate);
    renderer.render(scene, camera);
  };
  animate();
};

const updateSpot = () => {
  if (spotLight) {
    const outerRad = (outerAngle.value * Math.PI) / 180;
    spotLight.angle = outerRad;
    // Penumbra en Three.js va de 0 (borde duro) a 1 (máxima suavidad)
    const penumbraRatio = Math.max(0, Math.min(1, (outerAngle.value - innerAngle.value) / outerAngle.value));
    spotLight.penumbra = penumbraRatio;
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
  margin: 16px 0;
  overflow: hidden;
  background: #ffffff;
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
  height: 250px;
}

.controls-panel {
  padding: 12px 16px;
  background: #f9fafb;
  border-top: 1px solid #e5e7eb;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.control-group {
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
  font-size: 9.5px;
  color: #6b7280;
}

@media (max-width: 768px) {
  .controls-panel {
    grid-template-columns: 1fr;
  }
}
</style>
