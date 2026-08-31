<template>
  <div class="technical-figure">
    <div class="figure-header">
      <span class="label">SIMULADOR INTERACTIVO</span>
      <span class="desc">Mapa de Normales (Normal Map) vs. Superficie Plana</span>
    </div>
    
    <div class="canvas-wrapper" ref="canvasContainer"></div>

    <div class="controls-panel">
      <div class="toggle-box">
        <label class="toggle-label">
          <input type="checkbox" v-model="normalMapEnabled" @change="toggleNormalMap" />
          <span>Activar Mapa de Normales (Normal Map)</span>
        </label>
        <div class="explanation">
          <span v-if="normalMapEnabled">
             <strong>Normal Map Activado:</strong> Los vectores de luz rebotan en micro-valles simulados, generando sombras y volumen 3D <em>sin añadir un solo polígono</em>.
          </span>
          <span v-else>
             <strong>Superficie Plana:</strong> La luz rebota en un plano uniforme. El modelo se percibe plano y sin relieve.
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';

const canvasContainer = ref(null);
const normalMapEnabled = ref(true);

let scene, camera, renderer, planeMesh, dirLight, animId, proceduralNormalMap;

// Generar una textura de normales procedural rápida (ladrillo / relieve)
function createProceduralNormalTexture(THREE) {
  const size = 256;
  const canvas = document.createElement('canvas');
  canvas.width = size;
  canvas.height = size;
  const ctx = canvas.getContext('2d');

  // Fondo azul tangente neutro (128, 128, 255)
  ctx.fillStyle = 'rgb(128, 128, 255)';
  ctx.fillRect(0, 0, size, size);

  // Dibujar biseles de relieve simulados
  for (let y = 0; y < size; y += 32) {
    for (let x = 0; x < size; x += 64) {
      const offsetX = (y / 32) % 2 === 0 ? 0 : 32;
      const bx = (x + offsetX) % size;

      // Cara izquierda (resalta rojo)
      ctx.fillStyle = 'rgb(220, 128, 220)';
      ctx.fillRect(bx, y, 6, 28);

      // Cara superior (resalta verde)
      ctx.fillStyle = 'rgb(128, 220, 220)';
      ctx.fillRect(bx, y, 60, 6);

      // Cara derecha / sombra
      ctx.fillStyle = 'rgb(50, 128, 220)';
      ctx.fillRect(bx + 56, y, 6, 28);
    }
  }

  const texture = new THREE.CanvasTexture(canvas);
  texture.wrapS = THREE.RepeatWrapping;
  texture.wrapT = THREE.RepeatWrapping;
  texture.repeat.set(2, 2);
  return texture;
}

const initThree = async () => {
  if (typeof window === 'undefined') return;
  const THREE = await import('three');

  const container = canvasContainer.value;
  if (!container) return;

  const width = container.clientWidth || 600;
  const height = 240;

  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x18181b);

  camera = new THREE.PerspectiveCamera(40, width / height, 0.1, 100);
  camera.position.set(0, 0, 3.2);

  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(width, height);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  container.innerHTML = '';
  container.appendChild(renderer.domElement);

  proceduralNormalMap = createProceduralNormalTexture(THREE);

  const geo = new THREE.SphereGeometry(1, 48, 48);
  const mat = new THREE.MeshStandardMaterial({
    color: 0x94a3b8,
    roughness: 0.35,
    metalness: 0.15,
    normalMap: normalMapEnabled.value ? proceduralNormalMap : null
  });
  planeMesh = new THREE.Mesh(geo, mat);
  scene.add(planeMesh);

  // Luz móvil rotatoria para ver el relieve dinámico
  dirLight = new THREE.DirectionalLight(0xfff8ee, 3.0);
  dirLight.position.set(2, 1.5, 2);
  scene.add(dirLight);

  const fill = new THREE.AmbientLight(0x27272a, 0.4);
  scene.add(fill);

  let angle = 0;
  const animate = () => {
    animId = requestAnimationFrame(animate);
    angle += 0.015;
    dirLight.position.x = Math.cos(angle) * 2.5;
    dirLight.position.y = Math.sin(angle) * 1.5;
    planeMesh.rotation.y += 0.003;
    renderer.render(scene, camera);
  };
  animate();
};

const toggleNormalMap = () => {
  if (planeMesh && planeMesh.material) {
    planeMesh.material.normalMap = normalMapEnabled.value ? proceduralNormalMap : null;
    planeMesh.material.needsUpdate = true;
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

.toggle-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  font-weight: 600;
  color: #111827;
  cursor: pointer;
  margin-bottom: 6px;
}

.toggle-label input {
  accent-color: #111827;
  width: 16px;
  height: 16px;
}

.explanation {
  font-size: 11.5px;
  color: #4b5563;
  line-height: 1.4;
}
</style>
