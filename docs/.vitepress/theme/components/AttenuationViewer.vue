<template>
  <div class="technical-figure">
    <div class="figure-header">
      <span class="label">SIMULADOR INTERACTIVO</span>
      <span class="desc">Radio de Atenuación y Decaimiento Físico (1/d²)</span>
    </div>
    
    <div class="canvas-wrapper" ref="canvasContainer"></div>

    <div class="controls-panel">
      <div class="control-group-full">
        <div class="control-label">
          <span>Radio de Atenuación (Attenuation Radius):</span>
          <code>{{ radiusValue }} cm ({{ radiusFeedback }})</code>
        </div>
        <input type="range" min="100" max="600" step="10" v-model.number="radiusValue" @input="updateRadius" />
        <div class="hints">
          <span>100 cm (Luz muy concentrada / ajustada)</span>
          <span>600 cm (Sobredimensionada / Atraviesa paredes)</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';

const canvasContainer = ref(null);
const radiusValue = ref(300);

let scene, camera, renderer, pointLight, helperMesh, animId;

const radiusFeedback = computed(() => {
  const r = radiusValue.value;
  if (r < 180) return 'Alcance corto · Optimizado';
  if (r < 380) return 'Alcance medio estándar';
  return '⚠️ Riesgo de sobrecoste en GPU (Overdraw)';
});

const initThree = async () => {
  if (typeof window === 'undefined') return;
  const THREE = await import('three');

  const container = canvasContainer.value;
  if (!container) return;

  const width = container.clientWidth || 600;
  const height = 240;

  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x111217);

  camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 100);
  camera.position.set(0, 1.2, 4.5);
  camera.lookAt(0, 0, 0);

  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(width, height);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  container.innerHTML = '';
  container.appendChild(renderer.domElement);

  // Suelo y pared para ver el radio
  const floorGeo = new THREE.PlaneGeometry(8, 8);
  const wallMat = new THREE.MeshStandardMaterial({ color: 0x52525b, roughness: 0.8 });
  const floor = new THREE.Mesh(floorGeo, wallMat);
  floor.rotation.x = -Math.PI / 2;
  floor.position.y = -0.8;
  scene.add(floor);

  const wallGeo = new THREE.PlaneGeometry(8, 4);
  const wall = new THREE.Mesh(wallGeo, wallMat);
  wall.position.z = -2;
  wall.position.y = 1.2;
  scene.add(wall);

  // Objetos de prueba
  const sphereGeo = new THREE.SphereGeometry(0.5, 32, 32);
  const sphereMat = new THREE.MeshStandardMaterial({ color: 0xe4e4e7, roughness: 0.3, metalness: 0.2 });
  const sphere = new THREE.Mesh(sphereGeo, sphereMat);
  sphere.position.set(-1, -0.3, -0.5);
  scene.add(sphere);

  const cubeGeo = new THREE.BoxGeometry(0.7, 0.7, 0.7);
  const cube = new THREE.Mesh(cubeGeo, sphereMat);
  cube.position.set(1.2, -0.45, -0.8);
  cube.rotation.y = 0.5;
  scene.add(cube);

  // Luz puntual (Point Light)
  pointLight = new THREE.PointLight(0xffedd5, 12, radiusValue.value / 100, 2);
  pointLight.position.set(0, 0.4, 0);
  scene.add(pointLight);

  // Esfera pequeña visible que representa la bombilla
  const bulbGeo = new THREE.SphereGeometry(0.08, 16, 16);
  const bulbMat = new THREE.MeshBasicMaterial({ color: 0xffedd5 });
  const bulb = new THREE.Mesh(bulbGeo, bulbMat);
  bulb.position.copy(pointLight.position);
  scene.add(bulb);

  // Guía visual del radio
  const wireGeo = new THREE.SphereGeometry(1, 16, 16);
  const wireMat = new THREE.MeshBasicMaterial({ color: 0x38bdf8, wireframe: true, transparent: true, opacity: 0.15 });
  helperMesh = new THREE.Mesh(wireGeo, wireMat);
  helperMesh.position.copy(pointLight.position);
  scene.add(helperMesh);

  updateRadius();

  const animate = () => {
    animId = requestAnimationFrame(animate);
    renderer.render(scene, camera);
  };
  animate();
};

const updateRadius = () => {
  const r = radiusValue.value / 100;
  if (pointLight) {
    pointLight.distance = r;
  }
  if (helperMesh) {
    helperMesh.scale.set(r, r, r);
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
  height: 240px;
}

.controls-panel {
  padding: 12px 16px;
  background: #f9fafb;
  border-top: 1px solid #e5e7eb;
}

.control-group-full {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.control-label {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  font-weight: 600;
  color: #111827;
}

.control-label code {
  color: #111827;
  font-size: 11px;
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
</style>
