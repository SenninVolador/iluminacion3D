<template>
  <div class="technical-figure">
    <div class="figure-header">
      <span class="label">SIMULADOR INTERACTIVO</span>
      <span class="desc">Movilidad Técnica en Unreal Engine (Static vs. Stationary vs. Movable)</span>
    </div>
    
    <div class="canvas-wrapper" ref="canvasContainer"></div>

    <div class="controls-panel">
      <div class="mobility-selector">
        <button 
          v-for="mode in modes" 
          :key="mode.id" 
          :class="['mode-btn', { active: selectedMode === mode.id }]"
          @click="selectMode(mode.id)"
        >
          <span class="mode-title">{{ mode.name }}</span>
          <span class="mode-cost">{{ mode.cost }}</span>
        </button>
      </div>

      <div class="mode-explanation">
        <p><strong>Descripción:</strong> {{ currentModeData.description }}</p>
        <p><strong>Comportamiento:</strong> {{ currentModeData.behavior }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';

const canvasContainer = ref(null);
const selectedMode = ref('stationary');

const modes = [
  { 
    id: 'static', 
    name: 'Static (Estática)', 
    cost: '0.0 ms (Coste Cero)',
    description: 'Iluminación y sombras precalculadas y horneadas en mapas de textura (Lightmaps).',
    behavior: 'Si el objeto se mueve, su sombra se queda pegada en el suelo como una pintura.'
  },
  { 
    id: 'stationary', 
    name: 'Stationary (Estacionaria)', 
    cost: '0.8 ms (Híbrida)',
    description: 'Luz directa dinámica sobre personajes móviles + rebotes indirectos horneados.',
    behavior: 'La sombra se mueve en tiempo real con el objeto. Máximo 4 luces solapadas.'
  },
  { 
    id: 'movable', 
    name: 'Movable (Dinámica)', 
    cost: '2.5 ms (Tiempo Real)',
    description: 'Calculada 100% fotograma a fotograma en la GPU (Lumen / Virtual Shadow Maps).',
    behavior: 'Tanto la luz como el objeto pueden moverse libremente con sombras dinámicas continuas.'
  }
];

const currentModeData = computed(() => {
  return modes.find(m => m.id === selectedMode.value) || modes[0];
});

let scene, camera, renderer, movingCube, movingLight, animId;
let bakedShadowPlane;

const selectMode = (modeId) => {
  selectedMode.value = modeId;
};

const initThree = async () => {
  if (typeof window === 'undefined') return;
  const THREE = await import('three');

  const container = canvasContainer.value;
  if (!container) return;

  const width = container.clientWidth || 600;
  const height = 240;

  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x111217);

  camera = new THREE.PerspectiveCamera(40, width / height, 0.1, 100);
  camera.position.set(0, 2.0, 4.5);
  camera.lookAt(0, 0.2, 0);

  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(width, height);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  container.innerHTML = '';
  container.appendChild(renderer.domElement);

  // Suelo
  const floorGeo = new THREE.PlaneGeometry(8, 8);
  const floorMat = new THREE.MeshStandardMaterial({ color: 0x3f3f46, roughness: 0.8 });
  const floor = new THREE.Mesh(floorGeo, floorMat);
  floor.rotation.x = -Math.PI / 2;
  floor.receiveShadow = true;
  scene.add(floor);

  // Sombra horneada falsa (para modo static)
  const bakedGeo = new THREE.CircleGeometry(0.5, 32);
  const bakedMat = new THREE.MeshBasicMaterial({ color: 0x111111, transparent: true, opacity: 0.7 });
  bakedShadowPlane = new THREE.Mesh(bakedGeo, bakedMat);
  bakedShadowPlane.rotation.x = -Math.PI / 2;
  bakedShadowPlane.position.set(0, 0.01, 0);
  scene.add(bakedShadowPlane);

  // Cubo en movimiento
  const cubeGeo = new THREE.BoxGeometry(0.7, 0.7, 0.7);
  const cubeMat = new THREE.MeshStandardMaterial({ color: 0xe4e4e7, roughness: 0.3, metalness: 0.1 });
  movingCube = new THREE.Mesh(cubeGeo, cubeMat);
  movingCube.position.set(0, 0.35, 0);
  movingCube.castShadow = true;
  scene.add(movingCube);

  // Luz móvil
  movingLight = new THREE.DirectionalLight(0xfff3d6, 2.5);
  movingLight.position.set(2, 3, 2);
  movingLight.castShadow = true;
  movingLight.shadow.mapSize.width = 1024;
  movingLight.shadow.mapSize.height = 1024;
  scene.add(movingLight);

  const ambient = new THREE.AmbientLight(0x1e293b, 0.4);
  scene.add(ambient);

  let t = 0;
  const animate = () => {
    animId = requestAnimationFrame(animate);
    t += 0.02;

    // El cubo oscila de izquierda a derecha
    const posX = Math.sin(t) * 1.5;
    movingCube.position.x = posX;

    if (selectedMode.value === 'static') {
      // En modo static, la sombra real dinámica está desactivada y se ve la horneada en el centro fijo
      movingLight.castShadow = false;
      movingCube.castShadow = false;
      bakedShadowPlane.visible = true;
    } else if (selectedMode.value === 'stationary') {
      // En modo stationary, el objeto móvil proyecta sombra dinámica
      movingLight.castShadow = true;
      movingCube.castShadow = true;
      bakedShadowPlane.visible = false;
    } else if (selectedMode.value === 'movable') {
      // En modo movable, la luz también se mueve
      movingLight.castShadow = true;
      movingCube.castShadow = true;
      bakedShadowPlane.visible = false;
      movingLight.position.x = 2 + Math.cos(t) * 1.0;
    }

    renderer.render(scene, camera);
  };
  animate();
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

.mobility-selector {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 8px;
  margin-bottom: 12px;
}

.mode-btn {
  background: #ffffff;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  padding: 8px 10px;
  text-align: left;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  gap: 2px;
  transition: all 0.15s;
}

.mode-btn.active {
  border-color: #111827;
  background: #111827;
}

.mode-btn.active .mode-title {
  color: #ffffff;
}

.mode-btn.active .mode-cost {
  color: #93c5fd;
}

.mode-title {
  font-size: 11.5px;
  font-weight: 700;
  color: #111827;
}

.mode-cost {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  color: #4b5563;
}

.mode-explanation {
  font-size: 11.5px;
  color: #374151;
  line-height: 1.45;
  background: #ffffff;
  padding: 10px 12px;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
}

.mode-explanation p {
  margin: 2px 0;
}

@media (max-width: 768px) {
  .mobility-selector {
    grid-template-columns: 1fr;
  }
}
</style>
